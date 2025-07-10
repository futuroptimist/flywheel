import { test, expect } from '@playwright/test';

// Utility to collect failed JS requests during navigation
async function getFailedJsRequests(page, gotoUrl) {
  const failed = [];
  page.on('requestfailed', (request) => {
    const url = request.url();
    if (url.endsWith('.js')) {
      failed.push(url);
    }
  });
  await page.goto(gotoUrl);
  return failed;
}

test('model dropdown and canvas are visible', async ({ page }) => {
  await page.goto('/');

  // Verify dropdown visibility
  const dropdown = page.locator('#model-select');
  await expect(dropdown).toBeVisible();

  // Verify canvas visibility - use viewer canvas to avoid ambiguity
  await expect(page.locator('#viewer canvas')).toBeVisible();
});

test('no failed JS resource requests', async ({ page }) => {
  const failedJs = await getFailedJsRequests(page, '/');
  expect(failedJs, `Failed JS resources: ${failedJs.join(', ')}`).toEqual([]);
});
