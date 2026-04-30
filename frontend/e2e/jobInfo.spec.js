import { expect, test } from "@playwright/test";

test("job info page loads", async ({ page }) => {
  await page.goto("http://localhost:5173/jobs/");

  const firstJob = page.locator(`//div[@id="jobs"]//a`).first();
  const firstJobText = await firstJob.textContent();
  expect(firstJobText).not.toBeNull();
  await firstJob.click();

  await expect(page.getByRole("heading", { name: firstJobText })).toBeVisible();
});
