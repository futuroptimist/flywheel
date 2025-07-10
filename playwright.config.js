import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/js',
  use: {
    baseURL: 'http://localhost:42165',
  },
  webServer: {
    command: 'python webapp/app.py',
    port: 42165,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },
});
