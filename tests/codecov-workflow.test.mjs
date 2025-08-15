import { readFileSync } from 'node:fs';
import { test, expect } from '@jest/globals';

// Ensure Codecov uploads don't break when secrets are unavailable
const workflow = readFileSync(new URL('../.github/workflows/02-tests.yml', import.meta.url), 'utf8');

test('Codecov uploads are gated on CODECOV_TOKEN', () => {
  expect(workflow).toMatch(/CODECOV_TOKEN/);
  expect(workflow).toMatch(/env\.CODECOV_TOKEN != ''/);
});

test('Codecov failures do not break CI', () => {
  expect(workflow).toMatch(/fail_ci_if_error: false/);
});
