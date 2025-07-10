import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/js',
  webServer: {
    command: 'python webapp/app.py',
    port: 5000,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },
});
