import { readFileSync } from 'node:fs';
import { test, expect } from '@jest/globals';

const workflow = readFileSync(
  new URL('../.github/workflows/06-prompt-docs.yml', import.meta.url),
  'utf8'
);

test('pre-commit skips run-checks in prompt docs workflow', () => {
  expect(workflow).toMatch(/SKIP: run-checks/);
});
