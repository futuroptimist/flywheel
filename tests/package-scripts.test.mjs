import { readFileSync } from 'node:fs';

/**
 * Ensure required npm scripts exist so CI workflows stay green.
 */
test('package.json defines test:ci script', () => {
  const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url)));
  expect(pkg.scripts['test:ci']).toBeDefined();
});
