import {
  inspectCommit,
  digest,
  repoPattern,
  shaPattern,
} from './commit-identity.mjs';

const positive = (n) => Number.isSafeInteger(n) && n > 0;
const validSha = (s) =>
  typeof s === 'string' && shaPattern.test(s) && s !== '0'.repeat(40);
const coverage = [
  'CHECKPOINT_MISSING',
  'CHECKPOINT_FAILURE',
  'HISTORICAL_UNSCANNED',
  'INVALID_METADATA',
  'INVALID_POLICY',
  'UNEXPECTED_ERROR',
  'API_ERROR',
  'ACCESS_GAP',
  'INCOMPLETE_PAGINATION',
  'INVENTORY_CHANGED',
  'CHANGED_REF',
  'FORCE_PUSH',
  'DELETED_REF',
  'NEW_REF',
  'TIMEOUT',
  'REQUEST_LIMIT',
  'STATE_LIMIT',
  'OBSERVED_RANGE_COMPLETE',
  'VISIBILITY_LIMITED',
];
const roleResults = [
  'EXPECTED',
  'IDENTITY_MISMATCH',
  'UNREVIEWED',
  'BOT_UNREVIEWED',
  'NULL_ATTRIBUTION',
  'INVALID_METADATA',
  'OBSOLETE_ACCOUNT',
];
const codes = new Set([
  ...coverage.map((code) => `COVERAGE_${code}`),
  ...['AUTHOR', 'COMMITTER'].flatMap((role) =>
    roleResults.map((code) => `${role}_${code}`)
  ),
]);
const neutral = new Set([
  'AUTHOR_EXPECTED',
  'COMMITTER_EXPECTED',
  'AUTHOR_UNREVIEWED',
  'COMMITTER_UNREVIEWED',
  'AUTHOR_BOT_UNREVIEWED',
  'COMMITTER_BOT_UNREVIEWED',
  'COVERAGE_OBSERVED_RANGE_COMPLETE',
]);

// The central scanner's public boundary intentionally accepts no repository or SHA.
export function publicReporter(write = (line) => process.stdout.write(line)) {
  return (code) => {
    const safe = codes.has(code) ? code : 'COVERAGE_UNEXPECTED_ERROR';
    write(`${neutral.has(safe) ? '' : '::warning::'}${safe}\n`);
  };
}

export function classifyRoles(commit, entries, obsolete, emit) {
  for (const role of ['author', 'committer']) {
    const prefix = role.toUpperCase();
    if (obsolete.includes(commit?.[role]?.id))
      emit(`${prefix}_OBSOLETE_ACCOUNT`);
    // Adapt each role independently to the established collision-aware classifier.
    inspectCommit(
      {
        sha: commit?.sha,
        committer: commit?.[role],
        commit: { committer: commit?.commit?.[role] },
      },
      entries,
      (code) => {
        const mapped = {
          EXPECTED_COMMITTER: 'EXPECTED',
          COMMITTER_IDENTITY_MISMATCH: 'IDENTITY_MISMATCH',
          ATTRIBUTED_COMMITTER_UNREVIEWED: 'UNREVIEWED',
          BOT_ATTRIBUTION_UNREVIEWED: 'BOT_UNREVIEWED',
          COVERAGE_NULL_ATTRIBUTION: 'NULL_ATTRIBUTION',
          COVERAGE_INVALID_METADATA: 'INVALID_METADATA',
        }[code];
        emit(`${prefix}_${mapped || 'INVALID_METADATA'}`);
      }
    );
  }
}

const failures = new WeakMap();
const fail = (code) => {
  const error = new Error();
  failures.set(error, code);
  throw error;
};
const category = (error) => failures.get(error) || 'COVERAGE_UNEXPECTED_ERROR';

// Fixed origin, GET only, no URL following and bounded memory/time/request budgets.
export function metadataClient(token, config, fetcher = fetch) {
  // Snapshot validated limits so a caller cannot mutate an active client's bounds.
  const { maxRequests, timeoutMs, runTimeoutMs } = config || {};
  const validLimits =
    positive(maxRequests) &&
    positive(timeoutMs) &&
    positive(runTimeoutMs) &&
    timeoutMs <= 2147483647 &&
    runTimeoutMs <= 2147483647;
  let requests = 0;
  const deadline = validLimits ? Date.now() + runTimeoutMs : 0;
  return async (path) => {
    if (!validLimits) fail('COVERAGE_INVALID_POLICY');
    if (++requests > maxRequests) fail('COVERAGE_REQUEST_LIMIT');
    const remaining = deadline - Date.now();
    if (remaining <= 0) fail('COVERAGE_TIMEOUT');
    if (
      typeof token !== 'string' ||
      !token ||
      typeof path !== 'string' ||
      !path.startsWith('/') ||
      path.startsWith('//')
    ) {
      fail('COVERAGE_API_ERROR');
    }
    const signal = AbortSignal.timeout(Math.min(timeoutMs, remaining));
    try {
      const response = await fetcher(`https://api.github.com${path}`, {
        method: 'GET',
        redirect: 'error',
        signal,
        headers: {
          Accept: 'application/vnd.github+json',
          Authorization: `Bearer ${token}`,
          'X-GitHub-Api-Version': '2022-11-28',
        },
      });
      if ([401, 403, 404].includes(response.status))
        fail('COVERAGE_ACCESS_GAP');
      if (!response.ok) fail('COVERAGE_API_ERROR');
      const reader = response.body.getReader();
      const chunks = [];
      let size = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        size += value.length;
        if (size > 8 * 1024 * 1024) {
          await reader.cancel();
          fail('COVERAGE_INVALID_METADATA');
        }
        chunks.push(value);
      }
      return {
        data: JSON.parse(
          new TextDecoder('utf-8', { fatal: true }).decode(
            Buffer.concat(chunks)
          )
        ),
        link: response.headers.get('link') || '',
      };
    } catch (error) {
      if (failures.has(error)) throw error;
      fail(signal.aborted ? 'COVERAGE_TIMEOUT' : 'COVERAGE_API_ERROR');
    }
  };
}

async function pages(get, path, key, maxPages, project = (data) => data) {
  const items = [];
  const seen = new Set();
  for (let page = 1; page <= maxPages; page++) {
    const { data, link = '' } = await get(
      `${path}${path.includes('?') ? '&' : '?'}per_page=100&page=${page}`
    );
    const batch = project(data);
    if (
      !Array.isArray(batch) ||
      batch.length > 100 ||
      typeof link !== 'string'
    ) {
      fail('COVERAGE_INVALID_METADATA');
    }
    for (const item of batch) {
      const id = key(item);
      if (id === undefined || seen.has(id))
        fail('COVERAGE_INCOMPLETE_PAGINATION');
      seen.add(id);
      items.push(item);
    }
    const next = /rel="next"/.test(link);
    if (next && batch.length === 0) fail('COVERAGE_INCOMPLETE_PAGINATION');
    if (!next && batch.length < 100) return items;
    // A full terminal page needs an empty sentinel page, even if Link is missing.
  }
  fail('COVERAGE_INCOMPLETE_PAGINATION');
}

async function inventory(get, config, emit) {
  let all = [];
  try {
    all = await pages(
      get,
      '/user/repos?affiliation=owner,collaborator,organization_member&sort=full_name',
      (repo) => (positive(repo?.id) ? repo.id : undefined),
      config.maxPages
    );
  } catch (error) {
    emit(category(error));
  }
  const repos = new Map();
  for (const repo of all) {
    if (!positive(repo?.owner?.id) || !repoPattern.test(repo?.full_name))
      fail('COVERAGE_INVALID_METADATA');
    if (repo.owner.id === config.ownerId) repos.set(repo.id, repo);
  }
  for (const name of config.extraRepositories) {
    try {
      const { data } = await get(`/repos/${name}`);
      if (!positive(data?.id) || !repoPattern.test(data?.full_name))
        fail('COVERAGE_INVALID_METADATA');
      repos.set(data.id, data);
    } catch (error) {
      emit(category(error));
    }
  }
  return [...repos.values()].sort((a, b) => a.id - b.id);
}

async function refs(get, name, config) {
  const root = `/repos/${name}`;
  const branches = await pages(
    get,
    `${root}/branches`,
    (b) =>
      typeof b?.name === 'string' && b.name.length > 0 && b.name.length <= 1024
        ? b.name
        : undefined,
    config.maxPages
  );
  const prs = await pages(
    get,
    `${root}/pulls?state=open&sort=created&direction=asc`,
    (pr) => (positive(pr?.number) ? pr.number : undefined),
    config.maxPages
  );
  const result = Object.create(null);
  for (const branch of branches) {
    if (!validSha(branch.commit?.sha)) fail('COVERAGE_INVALID_METADATA');
    result[`branch:${branch.name}`] = { head: branch.commit.sha };
  }
  for (const pr of prs) {
    if (!validSha(pr.head?.sha) || !validSha(pr.base?.sha))
      fail('COVERAGE_INVALID_METADATA');
    result[`pr:${pr.number}`] = { head: pr.head.sha, base: pr.base.sha };
  }
  return Object.fromEntries(
    Object.entries(result).sort(([a], [b]) => a.localeCompare(b))
  );
}

function validState(state, fingerprint, config) {
  if (
    state?.version !== 1 ||
    state.fingerprint !== fingerprint ||
    state.historical !== 'unscanned' ||
    !state.repositories ||
    Array.isArray(state.repositories) ||
    typeof state.repositories !== 'object'
  )
    return false;
  for (const [id, repo] of Object.entries(state.repositories)) {
    if (
      !positive(Number(id)) ||
      String(Number(id)) !== id ||
      !repo?.refs ||
      typeof repo.refs !== 'object' ||
      Array.isArray(repo.refs) ||
      !Array.isArray(repo.seen) ||
      repo.seen.length > config.maxSeen ||
      !repo.seen.every(validSha) ||
      new Set(repo.seen).size !== repo.seen.length
    )
      return false;
    for (const [ref, value] of Object.entries(repo.refs)) {
      if (
        !/^(branch:.{1,1024}|pr:[1-9][0-9]*)$/u.test(ref) ||
        !validSha(value?.head) ||
        (ref.startsWith('pr:')
          ? !validSha(value.base)
          : value.base !== undefined)
      )
        return false;
    }
  }
  return true;
}

export async function scan({
  get,
  entries,
  config,
  store,
  emit = publicReporter(),
}) {
  try {
    config = { maxSeen: 100000, ...config };
    if (
      !positive(config.ownerId) ||
      !Array.isArray(config.extraRepositories) ||
      !config.extraRepositories.every(
        (name) => typeof name === 'string' && repoPattern.test(name)
      ) ||
      !Array.isArray(config.obsoleteAccountIds) ||
      !config.obsoleteAccountIds.every(positive) ||
      !positive(config.maxPages) ||
      config.maxPages > 30 ||
      !positive(config.maxSeen) ||
      !Array.isArray(entries) ||
      entries.length === 0 ||
      new Set(entries.map((e) => e?.accountId)).size !== entries.length ||
      !entries.every(
        (e) =>
          positive(e?.accountId) &&
          typeof e?.nameSha256 === 'string' &&
          typeof e?.emailSha256 === 'string' &&
          /^[a-f0-9]{64}$(?![\s\S])/.test(e.nameSha256) &&
          /^[a-f0-9]{64}$(?![\s\S])/.test(e.emailSha256)
      )
    ) {
      fail('COVERAGE_INVALID_POLICY');
    }
    const fingerprint = digest(
      JSON.stringify({
        entries: entries
          .map(({ accountId, nameSha256, emailSha256 }) => ({
            accountId,
            nameSha256,
            emailSha256,
          }))
          .sort((a, b) => a.accountId - b.accountId),
        ownerId: config.ownerId,
        // Mutable lookup names do not define identity policy. Inventory resolves
        // explicit repositories to stable IDs before selecting their saved state.
        obsolete: [...new Set(config.obsoleteAccountIds)].sort((a, b) => a - b),
      })
    );
    let previous;
    try {
      previous = await store.load();
    } catch {
      fail('COVERAGE_CHECKPOINT_FAILURE');
    }
    if (previous !== null && !validState(previous, fingerprint, config))
      fail('COVERAGE_CHECKPOINT_FAILURE');
    if (previous === null) emit('COVERAGE_CHECKPOINT_MISSING');
    emit('COVERAGE_HISTORICAL_UNSCANNED');
    // The token's view cannot establish that every private repository is accessible.
    emit('COVERAGE_VISIBILITY_LIMITED');
    const state =
      previous === null
        ? { version: 1, fingerprint, historical: 'unscanned', repositories: {} }
        : structuredClone(previous);
    const repos = await inventory(get, config, emit);
    const accessible = new Set(repos.map((repo) => String(repo.id)));
    for (const id of Object.keys(state.repositories))
      if (!accessible.has(id)) emit('COVERAGE_ACCESS_GAP');
    for (const repo of repos) {
      try {
        const before = await refs(get, repo.full_name, config);
        const old = previous?.repositories[String(repo.id)];
        const seen = new Set(old?.seen || []);
        const nextRefs = { ...old?.refs };
        const inspect = (commit) => {
          if (seen.has(commit.sha)) return;
          if (seen.size >= config.maxSeen) fail('COVERAGE_STATE_LIMIT');
          let malformed = false;
          classifyRoles(commit, entries, config.obsoleteAccountIds, (code) => {
            emit(code);
            if (code.endsWith('_INVALID_METADATA')) malformed = true;
          });
          if (malformed) fail('COVERAGE_INVALID_METADATA');
          seen.add(commit.sha);
        };
        for (const [ref, current] of Object.entries(before)) {
          const prior = old?.refs[ref];
          if (!prior) {
            emit('COVERAGE_NEW_REF');
            if (old && !seen.has(current.head)) {
              const { data } = await get(
                `/repos/${repo.full_name}/commits/${current.head}`
              );
              if (data?.sha !== current.head) fail('COVERAGE_INVALID_METADATA');
              inspect(data);
            }
            nextRefs[ref] = current;
            continue;
          }
          if (prior.head === current.head && prior.base === current.base)
            continue;
          if (prior.base !== current.base) fail('COVERAGE_CHANGED_REF');
          const path = `/repos/${repo.full_name}/compare/${prior.head}...${current.head}`;
          let expected;
          const commits = await pages(
            get,
            path,
            (c) => (validSha(c?.sha) ? c.sha : undefined),
            config.maxPages,
            (data) => {
              if (data?.status !== 'ahead') fail('COVERAGE_FORCE_PUSH');
              if (
                !positive(data.total_commits) ||
                (expected !== undefined && expected !== data.total_commits)
              ) {
                fail('COVERAGE_INCOMPLETE_PAGINATION');
              }
              expected = data.total_commits;
              return data.commits;
            }
          );
          if (
            commits.length !== expected ||
            !commits.some((c) => c.sha === current.head)
          ) {
            fail('COVERAGE_INCOMPLETE_PAGINATION');
          }
          for (const commit of commits) inspect(commit);
          nextRefs[ref] = current;
        }
        for (const ref of Object.keys(nextRefs)) {
          if (!Object.hasOwn(before, ref)) {
            emit('COVERAGE_DELETED_REF');
            delete nextRefs[ref];
          }
        }
        const after = await refs(get, repo.full_name, config);
        if (JSON.stringify(before) !== JSON.stringify(after))
          fail('COVERAGE_CHANGED_REF');
        state.repositories[String(repo.id)] = {
          refs: nextRefs,
          seen: [...seen],
        };
        if (old) emit('COVERAGE_OBSERVED_RANGE_COMPLETE');
      } catch (error) {
        emit(category(error));
      }
    }
    const after = await inventory(get, config, emit);
    const signature = (list) =>
      JSON.stringify(list.map((repo) => [repo.id, repo.full_name]));
    if (signature(repos) !== signature(after))
      fail('COVERAGE_INVENTORY_CHANGED');
    try {
      await store.save(state);
    } catch {
      fail('COVERAGE_CHECKPOINT_FAILURE');
    }
  } catch (error) {
    emit(category(error));
  }
}
