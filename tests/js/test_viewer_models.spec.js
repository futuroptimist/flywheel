import { test, expect } from '@playwright/test';

// Helper to get available model names from the page context
async function getModelOptions(page) {
  return page.$$eval('#model-select option', opts => opts.map(o => o.value));
}

test('all generated models appear in dropdown', async ({ page }) => {
  await page.goto('/');
  const options = await getModelOptions(page);
  // We created 4 SCAD-based models plus cube.obj fixture
  expect(options).toEqual(expect.arrayContaining([
    'adapter.obj',
    'flywheel.obj',
    'shaft.obj',
    'stand.obj',
    'cube.obj',
  ]));
  // Sanity: at least 4 models
  expect(options.length).toBeGreaterThanOrEqual(4);
});

test('selecting each model triggers OBJ request', async ({ page }) => {
  await page.goto('/');
  const options = await getModelOptions(page);
  for (const name of options) {
    const [response] = await Promise.all([
      page.waitForResponse(resp => resp.url().endsWith(`/models/${name}`) && resp.ok()),
      page.selectOption('#model-select', name),
    ]);
    expect(response.ok()).toBeTruthy();
  }
}); 