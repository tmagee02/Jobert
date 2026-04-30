import { expect, test } from "@playwright/test";

test("jobs page loads", async ({ page }) => {
  await page.goto("http://localhost:5173/jobs/");
  await expect(
    page.getByRole("heading", { name: "Discover new job openings." })
  ).toBeVisible();
});
