import { readFile } from 'fs/promises';

async function loadPackage() {
  const pkgPath = new URL('../package.json', import.meta.url);
  const content = await readFile(pkgPath, 'utf8');
  return JSON.parse(content);
}

test('package.json includes test:ci script', async () => {
  const pkg = await loadPackage();
  expect(pkg.scripts['test:ci']).toBeDefined();
});

test('package.json provides docs-lint table check', async () => {
  const pkg = await loadPackage();
  expect(pkg.scripts['docs-lint']).toBeDefined();
  expect(pkg.scripts['docs-lint']).toContain('scripts/docs-lint.mjs');
});
