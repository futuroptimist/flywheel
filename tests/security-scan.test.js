import fs from 'fs/promises';
import os from 'os';
import path from 'path';
import { jest } from '@jest/globals';
import { scanRepo, renderTable, updateDoc, run } from '../scripts/security-scan.mjs';

test('scanRepo detects features from API responses', async () => {
  const readme = Buffer.from('![CodeQL](a)\n![snyk](b)').toString('base64');
  const fetchMock = jest.fn()
    .mockResolvedValueOnce({ ok: true })
    .mockResolvedValueOnce({ status: 200 })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ content: readme, encoding: 'base64' }) });
  const res = await scanRepo('owner/repo', 'main', null, fetchMock);
  expect(res).toEqual({ repo: 'owner/repo', dependabot: true, secret: true, codeql: true, snyk: true });
});

test('scanRepo handles missing features', async () => {
  const fetchMock = jest.fn()
    .mockResolvedValueOnce({ ok: false })
    .mockResolvedValueOnce({ status: 404 })
    .mockResolvedValueOnce({ ok: false });
  const res = await scanRepo('owner/repo', 'main', null, fetchMock);
  expect(res).toEqual({ repo: 'owner/repo', dependabot: false, secret: false, codeql: false, snyk: false });
});

test('renderTable and updateDoc insert section', async () => {
  const table = renderTable([
    { repo: 'owner/repo', dependabot: true, secret: false, codeql: true, snyk: false }
  ]);
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'scan-'));
  const file = path.join(tmp, 'summary.md');
  await fs.writeFile(file, '# Repo Feature Summary\n\n## Coverage & Installer\n| c | d |\n\n## Policies & Automation\n');
  await updateDoc(file, table);
  const text1 = await fs.readFile(file, 'utf8');
  expect(text1).toMatch('## Security & Dependency Health');
  expect(text1).toMatch('\| Repo \| Dependabot');
  // run again to ensure replacement path
  await updateDoc(file, table);
  const text2 = await fs.readFile(file, 'utf8');
  expect(text2.match(/Security & Dependency Health/g).length).toBe(1);
});

test('run integrates scanning and updating', async () => {
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'scan-'));
  const repos = path.join(tmp, 'repos.txt');
  await fs.writeFile(repos, 'owner/repo');
  const file = path.join(tmp, 'summary.md');
  await fs.writeFile(file, '# Repo Feature Summary\n\n## Coverage & Installer\n| c | d |\n\n## Policies & Automation\n');
  const readme = Buffer.from('CodeQL badge\nSnyk badge').toString('base64');
  const mockFetch = jest.fn()
    .mockResolvedValueOnce({ ok: true })
    .mockResolvedValueOnce({ status: 200 })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ content: readme, encoding: 'base64' }) });
  const origFetch = global.fetch;
  global.fetch = mockFetch;
  await run(['--repos-from', repos, '--out', file]);
  global.fetch = origFetch;
  const text = await fs.readFile(file, 'utf8');
  expect(text).toMatch('CodeQL');
});

