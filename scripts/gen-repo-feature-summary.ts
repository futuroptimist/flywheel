#!/usr/bin/env node
import { Octokit } from 'octokit';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export interface RepoStat {
  stars: number;
  openIssues: number;
}

export async function fetchRepoStat(octokit: Octokit, repo: string): Promise<RepoStat> {
  const [owner, name] = repo.split('/');
  const { data: repoData } = await octokit.request('GET /repos/{owner}/{repo}', {
    owner,
    repo: name,
  });
  const { data: issueData } = await octokit.request('GET /search/issues', {
    q: `repo:${owner}/${name} type:issue state:open`,
    per_page: 1,
  });
  return { stars: repoData.stargazers_count, openIssues: issueData.total_count };
}

export function loadRepos(listPath: string): string[] {
  return fs
    .readFileSync(listPath, 'utf8')
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => l.split('@')[0]);
}

export function updateBasicsTable(md: string, stats: Record<string, RepoStat>): string {
  const lines = md.split('\n');
  const basicsHeader = lines.findIndex((l) => l.trim() === '## Basics');
  if (basicsHeader === -1) return md;
  let tableStart = basicsHeader + 1;
  /* c8 ignore next */
  while (tableStart < lines.length && !lines[tableStart].startsWith('|')) tableStart++;
  let tableEnd = tableStart;
  while (tableEnd < lines.length && lines[tableEnd].startsWith('|')) tableEnd++;
  const rows = lines.slice(tableStart + 2, tableEnd).map((line) => line.split('|').slice(1, -1).map((c) => c.trim()));
  const newRows = rows.map((cols) => {
    const repoLink = cols[0];
  /* c8 ignore next */
  const repoName = repoLink.replace(/\*\*/g, '').match(/\[(.*?)\]/)?.[1] ?? '';
    const stat = stats[repoName] ?? { stars: 0, openIssues: 0 };
    const updated = [cols[0], cols[1], cols[2], cols[3], String(stat.stars), String(stat.openIssues), cols[4]];
    return `| ${updated.join(' | ')} |`;
  });
  const header = '| Repo | Branch | Commit | Trunk | Stars | Open Issues | Last-Updated (UTC) |';
  const sep = '| ---- | ------ | ------ | ----- | ----- | ----------- | ----------------- |';
  const newTable = [header, sep, ...newRows];
  return [...lines.slice(0, tableStart), ...newTable, ...lines.slice(tableEnd)].join('\n');
}
/* c8 ignore start */
async function main() {
  const token = process.env.GITHUB_TOKEN;
  const dryRun = process.argv.includes('--dry-run');
  const repoListPath = path.resolve('docs/repo_list.txt');
  const mdPath = path.resolve('docs/repo-feature-summary.md');
  const repos = loadRepos(repoListPath);
  const octokit = new Octokit({ auth: token });
  const stats: Record<string, RepoStat> = {};
  for (const repo of repos) {
    stats[repo] = await fetchRepoStat(octokit, repo);
  }
  const original = fs.readFileSync(mdPath, 'utf8');
  const updated = updateBasicsTable(original, stats);
  if (dryRun) {
    if (updated !== original) {
      console.error('docs/repo-feature-summary.md is not up to date');
      process.exit(1);
    }
    return;
  }
  fs.writeFileSync(mdPath, updated);
}

if (fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
/* c8 ignore end */
