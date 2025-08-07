import { readFile, writeFile } from 'fs/promises';

export function authHeaders() {
  const headers = { 'User-Agent': 'flywheel-security-scan', Accept: 'application/vnd.github+json' };
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  return headers;
}

async function fetchJSON(url) {
  try {
    const res = await fetch(url, { headers: authHeaders() });
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status}`);
    return res.json();
  } catch {
    return null;
  }
}

function badgeInReadme(readme, keyword) {
  const lower = readme.toLowerCase();
  return lower.includes(keyword.toLowerCase());
}

export async function scanRepo(identifier) {
  const [repo, ref] = identifier.split('@');
  const [owner, name] = repo.split('/');
  const refParam = ref ? `?ref=${ref}` : '';

  const dependabot = !!(await fetchJSON(`https://api.github.com/repos/${owner}/${name}/contents/.github/dependabot.yml${refParam}`));

  const repoData = await fetchJSON(`https://api.github.com/repos/${owner}/${name}`);
  const secretScanning = repoData?.security_and_analysis?.secret_scanning?.status === 'enabled';
  const branch = ref || repoData?.default_branch || 'main';

  let readme = '';
  try {
    const readmeRes = await fetch(`https://raw.githubusercontent.com/${owner}/${name}/${branch}/README.md`);
    readme = readmeRes.ok ? await readmeRes.text() : '';
  } catch {
    readme = '';
  }
  const codeql = badgeInReadme(readme, 'codeql');
  const snyk = badgeInReadme(readme, 'snyk');

  return { repo: `${owner}/${name}`, dependabot, secretScanning, codeql, snyk };
}

export function renderTable(results) {
  const header = [
    '## Security & Dependency Health',
    '| Repo | Dependabot | Secret-Scanning | CodeQL | Snyk (badge) |',
    '| ---- | ---------- | --------------- | ------ | ------------ |'
  ];
  const fmt = (b) => (b ? '✅' : '❌');
  const rows = results.map((r) => {
    const link = `https://github.com/${r.repo}`;
    const name = r.repo === 'futuroptimist/flywheel' ? `**[${r.repo}](${link})**` : `[${r.repo}](${link})`;
    return `| ${name} | ${fmt(r.dependabot)} | ${fmt(r.secretScanning)} | ${fmt(r.codeql)} | ${fmt(r.snyk)} |`;
  });
  return header.concat(rows).join('\n');
}

export function updateMarkdown(existing, table) {
  const lines = existing.split('\n');
  const start = lines.findIndex((l) => l.startsWith('## Security & Dependency Health'));
  if (start !== -1) {
    let end = start + 1;
    while (end < lines.length && !lines[end].startsWith('## ')) end++;
    lines.splice(start, end - start, table);
    return lines.join('\n');
  }
  const coverage = lines.findIndex((l) => l.startsWith('## Coverage & Installer'));
  if (coverage !== -1) {
    let insert = coverage + 1;
    while (insert < lines.length && !lines[insert].startsWith('## ')) insert++;
    lines.splice(insert, 0, '', table, '');
    return lines.join('\n');
  }
  return existing + '\n\n' + table;
}

export async function main(options = {}) {
  const listPath = options.repoListPath
    ? new URL(options.repoListPath, import.meta.url)
    : new URL('../docs/repo_list.txt', import.meta.url);
  const repoList = (await readFile(listPath, 'utf8')).trim().split('\n').filter(Boolean);
  const results = [];
  for (const repo of repoList) {
    try {
      results.push(await scanRepo(repo));
    } catch {
      results.push({ repo: repo.split('@')[0], dependabot: false, secretScanning: false, codeql: false, snyk: false });
    }
  }
  const table = renderTable(results);
  const mdPath = options.markdownPath
    ? new URL(options.markdownPath, import.meta.url)
    : new URL('../docs/repo-feature-summary.md', import.meta.url);
  const existing = await readFile(mdPath, 'utf8');
  const updated = updateMarkdown(existing, table);
  await writeFile(mdPath, updated);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
