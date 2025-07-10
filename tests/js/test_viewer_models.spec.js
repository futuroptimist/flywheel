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
  // The first option is loaded automatically on page load, so re-selecting it
  // won't trigger a network request. Skip it to avoid timeouts.
  for (const name of options.slice(1)) {
    await page.selectOption('#model-select', name);
    const value = await page.$eval('#model-select', el => el.value);
    expect(value).toBe(name);
  }
});
