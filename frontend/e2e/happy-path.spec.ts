import { expect, test } from "@playwright/test";

test("upload → brief → mock plan → mock job → result", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /continue in local demo/i }).click();
  await page.getByLabel("Start with a project name").fill("Playwright living room");
  await page.getByRole("button", { name: /create project/i }).click();
  await expect(page.getByRole("heading", { name: "Playwright living room" })).toBeVisible();

  await page.getByLabel("Room name").fill("South-facing lounge");
  await page.getByRole("button", { name: "Add room" }).click();
  await expect(page.getByLabel("Active room")).toContainText("South-facing lounge");

  const png = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=", "base64");
  await page.locator('input[type="file"]').setInputFiles({ name: "room.png", mimeType: "image/png", buffer: png });
  await expect(page.getByRole("status")).toContainText("safely uploaded");

  await page.getByLabel("Style direction").fill("Soft contemporary");
  await page.getByRole("button", { name: /next: room details/i }).click();
  await page.getByRole("button", { name: /create design plan/i }).click();
  await expect(page.getByRole("heading", { name: "Soft contemporary" })).toBeVisible();
  await page.getByRole("button", { name: /queue visual preview/i }).click();
  await expect(page.getByText("Preview queued.")).toBeVisible();
  await expect(page.getByText("Preview ready")).toBeVisible({ timeout: 45_000 });
  await expect(page.getByRole("heading", { name: "Design options" })).toBeVisible();
  await expect(page.getByText("Generated with mock providers")).toBeVisible();
});
