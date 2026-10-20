import assert from 'node:assert/strict';
import test from 'node:test';
import { digest } from '../.github/scripts/commit-identity.mjs';
import {
  classifyRoles,
  scan,
  publicReporter,
  metadataClient,
} from '../.github/scripts/commit-attribution-scanner.mjs';
import { privateCheckpoint } from '../.github/scripts/commit-attribution-checkpoint.mjs';
import {
  mkdtemp,
  mkdir,
  readFile,
  stat,
  chmod,
  writeFile,
  rm,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const raw = { name: 'Synthetic person', email: 'fixture@example.invalid' };
const entries = [
  {
    accountId: 42,
    nameSha256: digest(raw.name),
    emailSha256: digest(raw.email),
  },
];
const sha = (n) => n.toString(16).padStart(40, '0');
const commit = (n = 1) => ({
  sha: sha(n),
  author: { id: 42, type: 'User' },
  committer: { id: 42, type: 'User' },
  commit: { author: raw, committer: raw },
});

test('classifies author and committer independently', () => {
  const value = commit();
  value.author = { id: 34114096, type: 'User' };
  const result = [];
  classifyRoles(value, entries, [34114096], (code) => result.push(code));
  assert.ok(result.includes('AUTHOR_OBSOLETE_ACCOUNT'));
  assert.ok(result.includes('AUTHOR_IDENTITY_MISMATCH'));
  assert.ok(result.includes('COMMITTER_EXPECTED'));
});

const config = {
  ownerId: 42,
  extraRepositories: [],
  obsoleteAccountIds: [34114096],
  maxPages: 3,
  maxRequests: 50,
  timeoutMs: 1000,
  runTimeoutMs: 10000,
  maxSeen: 1000,
};
function fixture() {
  const f = {
    state: null,
    codes: [],
    requests: [],
    head: 1,
    base: 10,
    name: 'sample/repo',
    prs: false,
    branches: true,
    writes: 0,
  };
  f.store = {
    load: async () => structuredClone(f.state),
    save: async (state) => {
      f.writes++;
      f.state = structuredClone(state);
    },
  };
  f.get = async (path) => {
    f.requests.push(path);
    if (f.override) {
      const value = await f.override(path);
      if (value) return value;
    }
    if (path.startsWith('/user/repos?'))
      return { data: [{ id: 7, full_name: f.name, owner: { id: 42 } }] };
    if (path.includes('/branches?'))
      return {
        data: f.branches
          ? [{ name: 'main', commit: { sha: sha(f.head) } }]
          : [],
      };
    if (path.includes('/pulls?'))
      return {
        data: f.prs
          ? [
              {
                number: 1,
                head: { sha: sha(f.head) },
                base: { sha: sha(f.base) },
              },
            ]
          : [],
      };
    if (path.includes('/compare/'))
      return {
        data: { status: 'ahead', total_commits: 1, commits: [commit(f.head)] },
      };
    if (path.includes('/commits/')) return { data: commit(f.head) };
    throw new Error('private/secret fixture@example.invalid');
  };
  f.run = () =>
    scan({
      get: f.get,
      entries,
      config,
      store: f.store,
      emit: (code) => f.codes.push(code),
    });
  return f;
}

test('all role combinations preserve external people, bots, nulls and collisions', () => {
  const variants = [
    [raw, { id: 42, type: 'User' }, 'EXPECTED'],
    [
      { name: 'other', email: 'other@example.invalid' },
      { id: 77, type: 'User' },
      'UNREVIEWED',
    ],
    [
      { name: 'bot', email: 'bot@example.invalid' },
      { id: 88, type: 'Bot' },
      'BOT_UNREVIEWED',
    ],
    [raw, null, 'NULL_ATTRIBUTION'],
    [raw, { id: '42', type: 'User' }, 'INVALID_METADATA'],
    [{ name: '', email: 'bad' }, { id: 42, type: 'User' }, 'INVALID_METADATA'],
    [raw, { id: 34114096, type: 'Bot' }, 'OBSOLETE_ACCOUNT'],
  ];
  for (const author of variants)
    for (const committer of variants) {
      const value = commit();
      value.author = author[1];
      value.committer = committer[1];
      value.commit = { author: author[0], committer: committer[0] };
      const output = [];
      classifyRoles(value, entries, config.obsoleteAccountIds, (c) =>
        output.push(c)
      );
      assert.ok(output.includes(`AUTHOR_${author[2]}`));
      assert.ok(output.includes(`COMMITTER_${committer[2]}`));
    }
  const collision = {
    accountId: 77,
    nameSha256: entries[0].nameSha256,
    emailSha256: digest('other'),
  };
  for (const order of [
    [collision, ...entries],
    [...entries, collision],
  ]) {
    const output = [];
    classifyRoles(commit(), order, [], (c) => output.push(c));
    assert.deepEqual(output, ['AUTHOR_EXPECTED', 'COMMITTER_EXPECTED']);
  }
});

test('renames retain repository-ID checkpoints; overlapping PR and branch SHAs inspect once', async () => {
  const f = fixture();
  f.prs = true;
  await f.run();
  f.codes = [];
  f.head = 2;
  f.name = 'renamed/repo';
  await f.run();
  assert.equal(f.codes.filter((c) => c === 'AUTHOR_EXPECTED').length, 1);
  assert.deepEqual(f.state.repositories['7'].seen, [sha(2)]);
  f.codes = [];
  await f.run();
  assert.ok(!f.codes.includes('AUTHOR_EXPECTED'));
});

test('compare pagination checks terminal page, counts, overlaps and missing heads', async () => {
  for (const mode of ['valid', 'duplicate', 'count', 'head', 'cap']) {
    const f = fixture();
    await f.run();
    const baseline = structuredClone(f.state);
    f.head = 102;
    f.override = async (path) => {
      if (!path.includes('/compare/')) return;
      const page = Number(
        new URL(`https://fixture.invalid${path}`).searchParams.get('page')
      );
      const items =
        page === 1
          ? Array.from({ length: 100 }, (_, i) => commit(i + 2))
          : mode === 'duplicate'
            ? [commit(2)]
            : mode === 'cap'
              ? Array.from({ length: 100 }, (_, i) => commit(page * 100 + i))
              : [commit(mode === 'head' ? 103 : 102)];
      return {
        data: {
          status: 'ahead',
          total_commits: mode === 'count' ? 999 : 101,
          commits: items,
        },
        link:
          page === 1 || mode === 'cap'
            ? '<https://evil.invalid>; rel="next"'
            : '',
      };
    };
    await f.run();
    if (mode === 'valid')
      assert.equal(f.state.repositories['7'].seen.length, 101);
    else {
      assert.ok(f.codes.includes('COVERAGE_INCOMPLETE_PAGINATION'));
      assert.deepEqual(f.state, baseline);
    }
    assert.ok(!f.requests.some((path) => path.includes('evil.invalid')));
  }
});

test('inventory pagination rejects duplicate IDs and preserves prior state', async () => {
  const f = fixture();
  await f.run();
  const baseline = structuredClone(f.state);
  f.override = async (path) =>
    path.startsWith('/user/repos?')
      ? {
          data: [
            { id: 7, full_name: 'sample/repo', owner: { id: 42 } },
            { id: 7, full_name: 'sample/renamed', owner: { id: 42 } },
          ],
        }
      : undefined;
  await f.run();
  assert.ok(f.codes.includes('COVERAGE_INCOMPLETE_PAGINATION'));
  assert.ok(f.codes.includes('COVERAGE_ACCESS_GAP'));
  assert.deepEqual(f.state, baseline);
});

test('branch and PR snapshot races, base changes and force pushes never advance a checkpoint', async () => {
  for (const mode of ['branch', 'pr', 'base', 'force']) {
    const f = fixture();
    f.prs = true;
    await f.run();
    const baseline = structuredClone(f.state);
    f.head = 2;
    let reads = 0;
    if (mode === 'base') f.base = 11;
    f.override = async (path) => {
      if (mode === 'force' && path.includes('/compare/'))
        return {
          data: { status: 'diverged', total_commits: 1, commits: [commit(2)] },
        };
      if (mode === 'branch' && path.includes('/branches?') && ++reads === 2)
        return { data: [{ name: 'main', commit: { sha: sha(3) } }] };
      if (mode === 'pr' && path.includes('/pulls?') && ++reads === 2)
        return { data: [] };
    };
    await f.run();
    assert.ok(
      f.codes.includes(
        mode === 'force' ? 'COVERAGE_FORCE_PUSH' : 'COVERAGE_CHANGED_REF'
      )
    );
    assert.deepEqual(f.state, baseline);
  }
});

test('checkpoint failure, corruption, policy changes and loss never imply continuous coverage', async () => {
  for (const mode of ['load', 'save', 'corrupt', 'policy', 'loss']) {
    const f = fixture();
    await f.run();
    f.head = 2;
    f.codes = [];
    if (mode === 'load')
      f.store.load = async () => {
        throw new Error('private checkpoint');
      };
    if (mode === 'save')
      f.store.save = async () => {
        throw new Error('private checkpoint');
      };
    if (mode === 'corrupt') f.state.repositories['7'].seen = ['bad'];
    if (mode === 'policy') f.state.fingerprint = 'different';
    if (mode === 'loss') f.state = null;
    await f.run();
    assert.ok(
      f.codes.includes(
        mode === 'loss'
          ? 'COVERAGE_CHECKPOINT_MISSING'
          : 'COVERAGE_CHECKPOINT_FAILURE'
      )
    );
    if (mode === 'loss') {
      assert.ok(f.codes.includes('COVERAGE_HISTORICAL_UNSCANNED'));
      assert.deepEqual(f.state.repositories['7'].seen, []);
    }
  }
});

test('inaccessible repositories retain their checkpoint while independent repositories progress', async () => {
  const f = fixture();
  await f.run();
  f.head = 2;
  const codes = [];
  await scan({
    get: f.get,
    entries,
    config: { ...config, extraRepositories: ['extra/repo'] },
    store: { load: async () => null, save: async () => {} },
    emit: (c) => codes.push(c),
  });
  assert.ok(codes.includes('COVERAGE_UNEXPECTED_ERROR'));
  assert.ok(codes.includes('COVERAGE_NEW_REF'));
  f.override = async (path) =>
    path.startsWith('/user/repos?') ? { data: [] } : undefined;
  await f.run();
  assert.ok(f.codes.includes('COVERAGE_ACCESS_GAP'));
  assert.equal(f.state.repositories['7'].refs['branch:main'].head, sha(1));
});

test('inventory race prevents saving; deleted refs report a gap', async () => {
  const f = fixture();
  await f.run();
  f.branches = false;
  await f.run();
  assert.ok(f.codes.includes('COVERAGE_DELETED_REF'));
  let calls = 0;
  const writes = f.writes;
  f.override = async (path) =>
    path.startsWith('/user/repos?') && ++calls === 2 ? { data: [] } : undefined;
  await f.run();
  assert.ok(f.codes.includes('COVERAGE_INVENTORY_CHANGED'));
  assert.equal(f.writes, writes);
});

test('new refs after baseline inspect only the head, deduplicating against branches', async () => {
  const f = fixture();
  await f.run();
  f.prs = true;
  f.codes = [];
  await f.run();
  assert.equal(f.codes.filter((c) => c === 'AUTHOR_EXPECTED').length, 1);
  assert.ok(f.codes.includes('COVERAGE_NEW_REF'));
  assert.equal(f.requests.filter((p) => p.includes('/commits/')).length, 1);
  assert.ok(!f.requests.some((p) => p.includes('/compare/')));
});

test('malformed commits and dedup capacity exhaustion preserve the previous checkpoint', async () => {
  for (const mode of ['malformed', 'capacity']) {
    const f = fixture();
    await f.run();
    f.head = 2;
    if (mode === 'capacity') {
      f.state.repositories['7'].seen = Array.from({ length: 1000 }, (_, i) =>
        sha(i + 10)
      );
    } else {
      f.override = async (path) =>
        path.includes('/compare/')
          ? {
              data: {
                status: 'ahead',
                total_commits: 1,
                commits: [{ ...commit(2), commit: null }],
              },
            }
          : undefined;
    }
    const baseline = structuredClone(f.state);
    await f.run();
    assert.deepEqual(f.state, baseline);
    assert.ok(
      f.codes.includes(
        mode === 'capacity'
          ? 'COVERAGE_STATE_LIMIT'
          : 'COVERAGE_INVALID_METADATA'
      )
    );
  }
});

test('CLI remains warning-only with unknown or hostile arguments and no activation flag', () => {
  const result = spawnSync(
    process.execPath,
    [
      '.github/scripts/commit-attribution-cli.mjs',
      '--activate=private/secret\nfixture@example.invalid',
    ],
    { encoding: 'utf8', cwd: new URL('..', import.meta.url) }
  );
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '::warning::COVERAGE_INVALID_POLICY\n');
  assert.equal(result.stderr, '');
});

test('transport uses GET only and reports denied access, invalid bodies, timeouts and budgets privately', async () => {
  for (const mode of ['denied', 'malformed', 'timeout', 'limit']) {
    let output = '';
    const requests = [];
    const get = metadataClient(
      'synthetic',
      { ...config, maxRequests: mode === 'limit' ? 1 : 50 },
      async (url, options) => {
        requests.push([url, options]);
        if (mode === 'denied')
          return new Response('private/secret', { status: 403 });
        if (mode === 'malformed') return new Response('private/secret');
        if (mode === 'timeout')
          return new Promise((resolve, reject) => {
            const timer = setTimeout(
              () => reject(new Error('private/secret')),
              1500
            );
            options.signal.addEventListener('abort', () => {
              clearTimeout(timer);
              reject(new Error('private/secret'));
            });
          });
        return new Response('[]');
      }
    );
    await scan({
      get,
      entries,
      config,
      store: { load: async () => null, save: async () => {} },
      emit: publicReporter((line) => {
        output += line;
      }),
    });
    assert.ok(
      output.includes(
        {
          denied: 'COVERAGE_ACCESS_GAP',
          malformed: 'COVERAGE_API_ERROR',
          timeout: 'COVERAGE_TIMEOUT',
          limit: 'COVERAGE_REQUEST_LIMIT',
        }[mode]
      )
    );
    assert.ok(!/private|secret|synthetic|sample|fixture@example/.test(output));
    for (const [url, options] of requests) {
      assert.ok(url.startsWith('https://api.github.com/'));
      assert.equal(options.method, 'GET');
      assert.equal(options.redirect, 'error');
      assert.equal(options.body, undefined);
    }
  }
});

test('private checkpoint rejects unsupported hosts; POSIX atomically replaces and locks private files', async () => {
  if (process.platform === 'win32') {
    await assert.rejects(privateCheckpoint('unused'));
    return;
  }
  const directory = await mkdtemp(join(tmpdir(), 'attribution-test-'));
  const path = join(directory, 'state.json');
  try {
    await chmod(directory, 0o700);
    const store = await privateCheckpoint(path);
    try {
      assert.equal(await store.load(), null);
      await assert.rejects(privateCheckpoint(path));
      await store.save({ test: 1 });
      await store.save({ test: 2 });
      assert.deepEqual(JSON.parse(await readFile(path)), { test: 2 });
      assert.equal((await stat(path)).mode & 0o077, 0);
      await writeFile(path, 'invalid');
      await assert.rejects(store.load());
      await chmod(path, 0o644);
      await assert.rejects(store.load());
    } finally {
      await store.close();
    }
    await mkdir(join(directory, '.git'));
    await assert.rejects(privateCheckpoint(path));
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test('public reporter never serializes metadata or unknown categories', () => {
  let output = '';
  const emit = publicReporter((line) => {
    output += line;
  });
  emit('AUTHOR_EXPECTED', { repository: 'private/secret', email: raw.email });
  emit('private/secret');
  assert.equal(
    output,
    'AUTHOR_EXPECTED\n::warning::COVERAGE_UNEXPECTED_ERROR\n'
  );
});

test('first observation establishes an unscanned baseline without fetching commits', async () => {
  const requests = [];
  const get = async (path) => {
    requests.push(path);
    if (path.startsWith('/user/repos?'))
      return { data: [{ id: 7, full_name: 'sample/repo', owner: { id: 42 } }] };
    if (path.includes('/branches?'))
      return { data: [{ name: 'main', commit: { sha: sha(1) } }] };
    if (path.includes('/pulls?')) return { data: [] };
    throw new Error('unexpected private route');
  };
  let saved;
  const codes = [];
  await scan({
    get,
    entries,
    config: {
      ownerId: 42,
      extraRepositories: [],
      obsoleteAccountIds: [34114096],
      maxPages: 3,
    },
    store: {
      load: async () => null,
      save: async (state) => {
        saved = state;
      },
    },
    emit: (code) => codes.push(code),
  });
  assert.ok(codes.includes('COVERAGE_CHECKPOINT_MISSING'));
  assert.ok(codes.includes('COVERAGE_HISTORICAL_UNSCANNED'));
  assert.equal(saved.repositories['7'].refs['branch:main'].head, sha(1));
  assert.ok(
    !requests.some(
      (path) => path.includes('/commits/') || path.includes('/compare/')
    )
  );
});
