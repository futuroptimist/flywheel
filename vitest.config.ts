import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['scripts/**/*.test.ts'],
    coverage: {
      reporter: ['text', 'lcov'],
      lines: 90,
      branches: 90,
      include: ['scripts/gen-repo-feature-summary.ts', 'scripts/gen-repo-feature-summary.ts*'],
    },
  },
});
