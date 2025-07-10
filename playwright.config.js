import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/playwright',
  webServer: {
    command: 'python web/app.py',
    port: 5000,
    timeout: 20000,
    reuseExistingServer: true,
  },
  use: {
    browserName: 'chromium',
    headless: true,
  },
});
