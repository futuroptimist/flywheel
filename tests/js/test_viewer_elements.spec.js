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
  let failedJs = await getFailedJsRequests(page, '/');
  // Ignore failures when loading external dependencies from unpkg since network
  // access may be restricted in CI environments.
  failedJs = failedJs.filter(url => !url.startsWith('https://unpkg.com'));
  expect(failedJs, `Failed JS resources: ${failedJs.join(', ')}`).toEqual([]);
});
