import { test, expect } from '@playwright/test';

test('rotate, zoom and reset', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await page.waitForFunction(() => window.viewerControls !== undefined);
  const bbox = await page.locator('#viewer canvas').boundingBox();
  if (!bbox) throw new Error('no bbox');

  await page.mouse.move(bbox.x + bbox.width / 2, bbox.y + bbox.height / 2);
  await page.mouse.down();
  await page.mouse.move(bbox.x + bbox.width / 2 + 50, bbox.y + bbox.height / 2);
  await page.mouse.up();

  // zoom
  await page.mouse.wheel(0, -200);

  // check that camera moved
  const angle = await page.evaluate(() => window.viewerControls.getAzimuthalAngle());
  expect(Math.abs(angle)).toBeGreaterThan(0);

  // reset via double-click
  await page.dblclick('#viewer canvas');
  const resetAngle = await page.evaluate(() => window.viewerControls.getAzimuthalAngle());
  expect(Math.abs(resetAngle)).toBeLessThan(0.01);
});
