import { describe, it, expect, vi } from 'vitest';
import { fetchRepoStat, updateBasicsTable, loadRepos } from './gen-repo-feature-summary';
import fs from 'node:fs';
import path from 'node:path';

class FakeOctokit {
  request = vi
    .fn()
    .mockImplementation((url: string) => {
      if (url.startsWith('GET /repos/')) {
        return Promise.resolve({ data: { stargazers_count: 5 } });
      }
      return Promise.resolve({ data: { total_count: 3 } });
    });
}

describe('fetchRepoStat', () => {
  it('retrieves stars and open issues', async () => {
    const stat = await fetchRepoStat(new FakeOctokit() as any, 'owner/repo');
    expect(stat).toEqual({ stars: 5, openIssues: 3 });
  });
});

describe('updateBasicsTable', () => {
  it('inserts stars and issues columns', () => {
    const md = [
      '',
      '## Basics',
      '| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |',
      '| - | - | - | - | - |',
      '| [owner/repo](url) | main | `abc1234` | ok | 2025-08-04 |',
      '',
    ].join('\n');
    const result = updateBasicsTable(md, {
      'owner/repo': { stars: 1, openIssues: 2 },
    });
    expect(result).toContain('Stars');
    expect(result).toContain('Open Issues');
    expect(result).toContain('| [owner/repo](url) | main | `abc1234` | ok | 1 | 2 | 2025-08-04 |');
  });
});

describe('loadRepos', () => {
  it('reads list and strips branches', () => {
    const tmp = path.join(process.cwd(), 'tmp_repos.txt');
    fs.writeFileSync(tmp, 'owner1/repo1\nowner2/repo2@branch\n');
    expect(loadRepos(tmp)).toEqual(['owner1/repo1', 'owner2/repo2']);
    fs.unlinkSync(tmp);
  });
});

describe('updateBasicsTable defaults', () => {
  it('fills zero when stats missing', () => {
    const md = [
      '',
      '## Basics',
      '| Repo | Branch | Commit | Trunk | Last-Updated (UTC) |',
      '| - | - | - | - | - |',
      '| [x/y](url) | main | `zzz` | ok | 2025-01-01 |',
      '',
    ].join('\n');
    const result = updateBasicsTable(md, {});
    expect(result).toContain('| [x/y](url) | main | `zzz` | ok | 0 | 0 | 2025-01-01 |');
  });
});

describe('updateBasicsTable without section', () => {
  it('returns original text', () => {
    expect(updateBasicsTable('no basics here', {})).toBe('no basics here');
  });
});
