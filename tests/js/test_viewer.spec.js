import { test, expect } from '@playwright/test';

test('canvas renders', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('canvas');
  await expect(page.locator('canvas')).toBeVisible();
});
