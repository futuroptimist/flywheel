import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['scripts/**/*.test.ts'],
    coverage: {
      reporter: ['text', 'json'],
      lines: 90,
      branches: 90,
      include: ['scripts/gen-repo-feature-summary.ts'],
    },
  },
});
