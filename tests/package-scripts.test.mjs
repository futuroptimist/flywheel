import { readFileSync } from 'node:fs';

/**
 * Ensure required npm scripts exist so CI workflows stay green.
 */
test('package.json defines test:ci script', () => {
  const pkg = JSON.parse(
    readFileSync(new URL('../package.json', import.meta.url))
  );
  expect(pkg.scripts['test:ci']).toBeDefined();
});

test('playwright:install installs browser and deps', () => {
  const pkg = JSON.parse(
    readFileSync(new URL('../package.json', import.meta.url))
  );
  expect(pkg.scripts['playwright:install']).toBe(
    'playwright install-deps chromium && playwright install chromium'
  );
});

test('lint script runs eslint on repository sources', () => {
  const pkg = JSON.parse(
    readFileSync(new URL('../package.json', import.meta.url))
  );
  expect(pkg.scripts.lint).toMatch(/eslint/);
  expect(pkg.scripts.lint).toMatch(/scripts/);
});

test('format:check script uses prettier', () => {
  const pkg = JSON.parse(
    readFileSync(new URL('../package.json', import.meta.url))
  );
  expect(pkg.scripts['format:check']).toMatch(/prettier/);
});
