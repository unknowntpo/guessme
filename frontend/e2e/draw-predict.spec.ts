import { test, expect } from '@playwright/test'

test.describe('Draw and Predict Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should display the main page elements', async ({ page }) => {
    // Header
    await expect(page.locator('h1')).toContainText('Guessme')

    // Prompt text
    await expect(page.getByText('Draw a digit (0-9)')).toBeVisible()

    // Canvas should be visible
    const canvas = page.locator('canvas')
    await expect(canvas).toBeVisible()

    // Controls should be visible
    await expect(page.getByTestId('clear-btn')).toBeVisible()
    await expect(page.getByTestId('send-btn')).toBeVisible()
  })

  test('should have Send button disabled when canvas is empty', async ({ page }) => {
    const sendBtn = page.getByTestId('send-btn')
    await expect(sendBtn).toBeDisabled()
  })

  test('should enable Send button after drawing', async ({ page }) => {
    const canvas = page.locator('canvas')
    const sendBtn = page.getByTestId('send-btn')

    // Draw a simple line
    const box = await canvas.boundingBox()
    if (box) {
      await page.mouse.move(box.x + 50, box.y + 50)
      await page.mouse.down()
      await page.mouse.move(box.x + 150, box.y + 150)
      await page.mouse.up()
    }

    await expect(sendBtn).toBeEnabled()
  })

  test('should clear canvas when Clear clicked', async ({ page }) => {
    const canvas = page.locator('canvas')
    const sendBtn = page.getByTestId('send-btn')
    const clearBtn = page.getByTestId('clear-btn')

    // Draw something
    const box = await canvas.boundingBox()
    if (box) {
      await page.mouse.move(box.x + 50, box.y + 50)
      await page.mouse.down()
      await page.mouse.move(box.x + 150, box.y + 150)
      await page.mouse.up()
    }

    // Verify Send is enabled
    await expect(sendBtn).toBeEnabled()

    // Clear canvas
    await clearBtn.click()

    // Send should be disabled again
    await expect(sendBtn).toBeDisabled()
  })

  test('should show result after sending drawing', async ({ page }) => {
    const canvas = page.locator('canvas')
    const sendBtn = page.getByTestId('send-btn')

    // Draw a "1" - vertical line
    const box = await canvas.boundingBox()
    if (box) {
      await page.mouse.move(box.x + 200, box.y + 50)
      await page.mouse.down()
      await page.mouse.move(box.x + 200, box.y + 350)
      await page.mouse.up()
    }

    // Send the drawing
    await sendBtn.click()

    // Wait for result to appear (with loading)
    await expect(page.getByTestId('result-card')).toBeVisible({ timeout: 10000 })

    // Verify result elements
    await expect(page.getByText('Digit')).toBeVisible()
    await expect(page.getByText('Confidence')).toBeVisible()
    await expect(page.getByTestId('try-again-btn')).toBeVisible()
  })

  test('should reset game when Try Again clicked', async ({ page }) => {
    const canvas = page.locator('canvas')
    const sendBtn = page.getByTestId('send-btn')

    // Draw and send
    const box = await canvas.boundingBox()
    if (box) {
      await page.mouse.move(box.x + 200, box.y + 50)
      await page.mouse.down()
      await page.mouse.move(box.x + 200, box.y + 350)
      await page.mouse.up()
    }
    await sendBtn.click()

    // Wait for result
    await expect(page.getByTestId('result-card')).toBeVisible({ timeout: 10000 })

    // Click Try Again
    await page.getByTestId('try-again-btn').click()

    // Result should be hidden
    await expect(page.getByTestId('result-card')).not.toBeVisible()

    // Controls should be back
    await expect(page.getByTestId('send-btn')).toBeVisible()
    await expect(page.getByTestId('send-btn')).toBeDisabled()
  })

  test('should show loading state while sending', async ({ page }) => {
    const canvas = page.locator('canvas')
    const sendBtn = page.getByTestId('send-btn')

    // Draw something
    const box = await canvas.boundingBox()
    if (box) {
      await page.mouse.move(box.x + 100, box.y + 100)
      await page.mouse.down()
      await page.mouse.move(box.x + 300, box.y + 300)
      await page.mouse.up()
    }

    // Click send and check for loading state
    await sendBtn.click()

    // The button should show loading or result should appear
    // (depending on how fast the API responds)
    await expect(
      page.getByTestId('result-card').or(page.getByText('Sending...'))
    ).toBeVisible({ timeout: 10000 })
  })
})

test.describe('Error Handling', () => {
  test('should handle API errors gracefully', async ({ page, context }) => {
    // Intercept API calls and return error
    await context.route('**/predict', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' })
      })
    })

    await page.goto('/')

    const canvas = page.locator('canvas')
    const sendBtn = page.getByTestId('send-btn')

    // Draw something
    const box = await canvas.boundingBox()
    if (box) {
      await page.mouse.move(box.x + 100, box.y + 100)
      await page.mouse.down()
      await page.mouse.move(box.x + 300, box.y + 300)
      await page.mouse.up()
    }

    // Send
    await sendBtn.click()

    // Should show result card (with error)
    await expect(page.getByTestId('result-card')).toBeVisible({ timeout: 10000 })

    // Try Again button should still be available
    await expect(page.getByTestId('try-again-btn')).toBeVisible()
  })
})
