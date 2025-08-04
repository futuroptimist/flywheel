import { jest } from '@jest/globals';
import fs from 'fs';
import { scanRepo, renderTable, updateMarkdown, authHeaders, main } from '../scripts/security-scan.mjs';

describe('scanRepo', () => {
  test('detects security features', async () => {
    global.fetch = jest.fn()
      // dependabot
      .mockResolvedValueOnce({ ok: true, json: async () => ({}) })
      // repo info
      .mockResolvedValueOnce({ ok: true, json: async () => ({ security_and_analysis: { secret_scanning: { status: 'enabled' } }, default_branch: 'main' }) })
      // readme
      .mockResolvedValueOnce({ ok: true, text: async () => '![CodeQL](badge) ![Snyk](badge)' });
    const result = await scanRepo('owner/repo');
    expect(result).toEqual({ repo: 'owner/repo', dependabot: true, secretScanning: true, codeql: true, snyk: true });
  });

  test('handles missing features', async () => {
    global.fetch = jest.fn()
      // dependabot 404
      .mockResolvedValueOnce({ ok: false, status: 404 })
      // repo info disabled
      .mockResolvedValueOnce({ ok: true, json: async () => ({ security_and_analysis: { secret_scanning: { status: 'disabled' } }, default_branch: 'main' }) })
      // readme empty
      .mockResolvedValueOnce({ ok: true, text: async () => '' });
    const result = await scanRepo('owner/repo');
    expect(result).toEqual({ repo: 'owner/repo', dependabot: false, secretScanning: false, codeql: false, snyk: false });
  });
});

describe('renderTable & updateMarkdown', () => {
  const sample = [
    { repo: 'futuroptimist/flywheel', dependabot: true, secretScanning: true, codeql: true, snyk: false }
  ];
  test('renders table', () => {
    const table = renderTable(sample);
    expect(table).toContain('Security & Dependency Health');
    expect(table).toContain('✅');
    expect(table).toContain('❌');
  });
  test('inserts and replaces section', () => {
    const table = renderTable(sample);
    const base = '# Title\n\n## Coverage & Installer\nfoo\n\n## Policies & Automation';
    const inserted = updateMarkdown(base, table);
    expect(inserted).toContain(table);
    const replaced = updateMarkdown(inserted, table.replace('❌', '✅'));
    expect(replaced).toContain('✅');
  });
});

test('authHeaders includes token and main writes file', async () => {
  process.env.GITHUB_TOKEN = 'testtoken';
  expect(authHeaders().Authorization).toBe('Bearer testtoken');
  delete process.env.GITHUB_TOKEN;

  const repoListPath = '../tests/tmp-repos.txt';
  const mdPath = '../tests/tmp-summary.md';
  await fs.promises.writeFile('tests/tmp-repos.txt', 'owner/repo');
  await fs.promises.writeFile('tests/tmp-summary.md', '# Title\n\n## Coverage & Installer\nfoo');
  global.fetch = jest.fn()
    .mockResolvedValueOnce({ ok: false, status: 404 })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ default_branch: 'main' }) })
    .mockResolvedValueOnce({ ok: true, text: async () => '' });
  await main({ repoListPath, markdownPath: mdPath });
  const updated = await fs.promises.readFile('tests/tmp-summary.md', 'utf8');
  expect(updated).toContain('Security & Dependency Health');
  await fs.promises.unlink('tests/tmp-repos.txt');
  await fs.promises.unlink('tests/tmp-summary.md');
});
