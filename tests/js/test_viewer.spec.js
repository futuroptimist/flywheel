import { test, expect } from '@playwright/test';

test('canvas renders', async ({ page }) => {
  await page.goto('/');
  await page.waitForSelector('#viewer canvas');
  await expect(page.locator('#viewer canvas')).toBeVisible();
});
