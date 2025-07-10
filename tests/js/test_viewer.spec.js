import { test, expect } from '@playwright/test';

test('canvas renders', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await page.waitForSelector('canvas');
  await expect(page.locator('canvas')).toBeVisible();
});
