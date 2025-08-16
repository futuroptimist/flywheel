import { readFileSync } from 'node:fs';
import { test, expect } from '@jest/globals';

const workflow = readFileSync(new URL('../.github/workflows/04-update-summary.yml', import.meta.url), 'utf8');

test('summary workflow skips run-checks hook', () => {
  expect(workflow).toMatch(/SKIP: run-checks/);
});
