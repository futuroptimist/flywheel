import { Octokit } from 'octokit';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

export interface RepoInfo {
  stars: number | 'n/a';
  openIssues: number | 'n/a';
}

const octokit = new Octokit();

async function fetchRepoInfo(owner: string, repo: string): Promise<RepoInfo> {
  try {
    const { data } = await octokit.rest.repos.get({ owner, repo });
    return { stars: data.stargazers_count, openIssues: data.open_issues_count };
  } catch {
    return { stars: 'n/a', openIssues: 'n/a' };
  }
}

function parseRepoSlug(cell: string): string | null {
  const match = cell.match(/\[([^\]]+)\]\(https:\/\/github.com\/([^\)]+)\)/);
  return match ? match[1] : null;
}

function buildRow(
  repoCell: string,
  branch: string,
  commit: string,
  trunk: string,
  info: RepoInfo,
  lastUpdated: string,
): string {
  return `| ${repoCell} | ${branch} | ${commit} | ${trunk} | ${info.stars} | ${info.openIssues} | ${lastUpdated} |`;
}

export async function generate({
  dryRun = false,
  docPath = join(dirname(fileURLToPath(import.meta.url)), '..', 'docs', 'repo-feature-summary.md'),
}: { dryRun?: boolean; docPath?: string } = {}) {
  const content = readFileSync(docPath, 'utf8');
  const basicsIndex = content.indexOf('## Basics');
  if (basicsIndex === -1) throw new Error('Basics section not found');
  const tableStart = content.indexOf('\n|', basicsIndex) + 1;
  const nextSection = content.indexOf('\n##', tableStart);
  const tableEnd = nextSection === -1 ? content.length : nextSection;
  const table = content.slice(tableStart, tableEnd).trim();
  const lines = table.split('\n');
  const header = '| Repo | Branch | Commit | Trunk | Stars | Open Issues | Last-Updated (UTC) |';
  const align = '| ---- | ------ | ------ | ----- | ----- | ----------- | ----------------- |';
  const rows = lines.slice(2).filter(Boolean);

  const newRows: string[] = [];
  for (const row of rows) {
    const cells = row.split('|').map((c) => c.trim()).filter(Boolean);
    const [repoCell, branch, commit, trunk, lastUpdated] = cells;
    const slug = parseRepoSlug(repoCell);
    let info: RepoInfo = { stars: 'n/a', openIssues: 'n/a' };
    if (slug) {
      const [owner, repo] = slug.split('/');
      info = await fetchRepoInfo(owner, repo);
    }
    newRows.push(buildRow(repoCell, branch, commit, trunk, info, lastUpdated));
  }
  const newTable = [header, align, ...newRows].join('\n');
  const newContent = content.slice(0, tableStart) + newTable + content.slice(tableEnd);

  if (dryRun) {
    if (newContent !== content) {
      console.log('repo-feature-summary.md is out of date');
    }
  } else {
    writeFileSync(docPath, newContent);
  }
}

/* c8 ignore next 6 */
if (import.meta.url === `file://${process.argv[1]}`) {
  const dryRun = process.argv.includes('--dry-run');
  generate({ dryRun }).catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
