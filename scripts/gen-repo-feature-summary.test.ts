import { describe, it, expect, vi } from 'vitest';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const get = vi.fn();
vi.mock('octokit', () => ({
  Octokit: class {
    rest = { repos: { get } };
  },
}));
const { generate } = await import('./gen-repo-feature-summary');

describe('gen-repo-feature-summary', () => {
  it('adds Stars and Open Issues columns', async () => {
    get.mockResolvedValue({ data: { stargazers_count: 7, open_issues_count: 2 } });
    const dir = mkdtempSync(join(tmpdir(), 'repo-summary-'));
    const file = join(dir, 'repo-feature-summary.md');
    const content = `## Basics\n| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |\n| ---- | ------ | ------ | ----- | ----------------- |\n| [foo/bar](https://github.com/foo/bar) | main | n/a | n/a | n/a |\n`;
    writeFileSync(file, content);

    await generate({ docPath: file });
    const out = readFileSync(file, 'utf8');
    expect(out).toContain('| Repo | Branch | Commit | Trunk | Stars | Open Issues | Last-Updated (UTC) |');
    expect(out).toContain('| [foo/bar](https://github.com/foo/bar) | main | n/a | n/a | 7 | 2 | n/a |');
  });

  it('dry run handles up-to-date files', async () => {
    get.mockResolvedValue({ data: { stargazers_count: 1, open_issues_count: 1 } });
    const dir = mkdtempSync(join(tmpdir(), 'repo-summary-'));
    const file = join(dir, 'repo-feature-summary.md');
    const content = `## Basics\n| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |\n| ---- | ------ | ------ | ----- | ----------------- |\n| [foo/bar](https://github.com/foo/bar) | main | n/a | n/a | n/a |\n`;
    writeFileSync(file, content);
    await generate({ docPath: file });
    await generate({ docPath: file, dryRun: true });
    const out = readFileSync(file, 'utf8');
    expect(out).toContain('1 | 1');
  });

  it('falls back to n/a when fetch fails or slug missing', async () => {
    get.mockRejectedValue(new Error('oops'));
    const dir = mkdtempSync(join(tmpdir(), 'repo-summary-'));
    const file = join(dir, 'repo-feature-summary.md');
    const content = `## Basics\n| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |\n| ---- | ------ | ------ | ----- | ----------------- |\n| [foo/bar](https://github.com/foo/bar) | main | n/a | n/a | n/a |\n| plain-text | main | n/a | n/a | n/a |\n`;
    writeFileSync(file, content);
    await generate({ docPath: file });
    const out = readFileSync(file, 'utf8');
    expect(out).toContain('| [foo/bar](https://github.com/foo/bar) | main | n/a | n/a | n/a | n/a | n/a |');
    expect(out).toContain('| plain-text | main | n/a | n/a | n/a | n/a | n/a |');
  });

  it('executes via CLI', async () => {
    get.mockResolvedValue({ data: { stargazers_count: 0, open_issues_count: 0 } });
    const original = process.argv[1];
    const script = './gen-repo-feature-summary.ts?cli';
    process.argv[1] = join(process.cwd(), 'scripts', 'gen-repo-feature-summary.ts');
    process.argv.push('--dry-run');
    await import(script);
    process.argv.pop();
    process.argv[1] = original;
  });
});
