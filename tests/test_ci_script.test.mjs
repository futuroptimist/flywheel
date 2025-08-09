import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';

async function loadPackage() {
  const pkgPath = new URL('../package.json', import.meta.url);
  const content = await readFile(pkgPath, 'utf8');
  return JSON.parse(content);
}

test('package.json includes test:ci script', async () => {
  const pkg = await loadPackage();
  expect(pkg.scripts['test:ci']).toBeDefined();
});
