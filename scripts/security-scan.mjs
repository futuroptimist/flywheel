import fs from 'fs/promises';

function headers(token) {
  const h = { 'User-Agent': 'flywheel-security-scan', Accept: 'application/vnd.github+json' };
  if (token) h.Authorization = `token ${token}`;
  return { headers: h };
}

export async function scanRepo(repo, branch = 'main', token = null, fetchImpl = fetch) {
  const opts = headers(token);
  const depUrl = `https://api.github.com/repos/${repo}/contents/.github/dependabot.yml?ref=${branch}`;
  const depResp = await fetchImpl(depUrl, opts).catch(() => ({ ok: false }));
  const dependabot = depResp.ok;

  const secUrl = `https://api.github.com/repos/${repo}/secret-scanning/alerts?per_page=1`;
  const secResp = await fetchImpl(secUrl, opts).catch(() => ({ status: 404 }));
  const secret = secResp.status === 200;

  const readmeUrl = `https://api.github.com/repos/${repo}/readme?ref=${branch}`;
  const readmeResp = await fetchImpl(readmeUrl, opts).catch(() => ({ ok: false }));
  let readme = '';
  if (readmeResp.ok) {
    const json = await readmeResp.json();
    const enc = json.encoding || 'base64';
    readme = Buffer.from(json.content || '', enc).toString();
  }
  const codeql = /codeql/i.test(readme);
  const snyk = /snyk/i.test(readme);

  return { repo, dependabot, secret, codeql, snyk };
}

function mark(flag) {
  return flag ? '✅' : '❌';
}

export function renderTable(results) {
  const header = '| Repo | Dependabot | Secret-Scanning | CodeQL | Snyk (badge) |';
  const sep = '| ---- | ---------- | --------------- | ------ | ------------ |';
  const rows = results.map((r, idx) => {
    const link = `[${r.repo}](https://github.com/${r.repo})`;
    const repoLink = idx === 0 ? `**${link}**` : link;
    return `| ${repoLink} | ${mark(r.dependabot)} | ${mark(r.secret)} | ${mark(r.codeql)} | ${mark(r.snyk)} |`;
  });
  return [header, sep, ...rows].join('\n');
}

export async function updateDoc(path, table) {
  const text = await fs.readFile(path, 'utf8');
  const lines = text.split('\n');
  const secHeader = '## Security & Dependency Health';
  const covIndex = lines.findIndex((l) => l.startsWith('## Coverage & Installer'));
  if (covIndex === -1) throw new Error('Coverage section not found');
  const nextSection = lines.findIndex((l, i) => i > covIndex && l.startsWith('## '));
  const insertAt = nextSection === -1 ? lines.length : nextSection;
  const secIndex = lines.findIndex((l) => l.startsWith(secHeader));
  if (secIndex !== -1) {
    const end = lines.findIndex((l, i) => i > secIndex && l.startsWith('## '));
    const sliceEnd = end === -1 ? lines.length : end;
    lines.splice(secIndex, sliceEnd - secIndex, secHeader, table, '');
  } else {
    lines.splice(insertAt, 0, '', secHeader, table, '');
  }
  await fs.writeFile(path, lines.join('\n'));
}

export async function run(args = process.argv.slice(2)) {
  const reposFrom = args[args.indexOf('--repos-from') + 1];
  const out = args[args.indexOf('--out') + 1];
  const tokenIdx = args.indexOf('--token');
  const token = tokenIdx !== -1 ? args[tokenIdx + 1] : process.env.GITHUB_TOKEN;
  const list = (await fs.readFile(reposFrom, 'utf8')).split(/\r?\n/).filter(Boolean);
  const results = [];
  for (const entry of list) {
    const [repo, branch = 'main'] = entry.split('@');
    results.push(await scanRepo(repo, branch, token));
  }
  const table = renderTable(results);
  await updateDoc(out, table);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  run();
}

