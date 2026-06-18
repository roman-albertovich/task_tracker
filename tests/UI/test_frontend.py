import pytest
from playwright.sync_api import Page, expect

def test_add_new_task_via_ui(page: Page):
    """"UI-test for adding new task"""

    #1. Open page our app
    page.goto("http://localhost:8000/")

    #2. Fill page locator ID
    page.fill("#taskName", "Test from Playwright")
    page.fill("#taskDesc", "Chek rendering DOM-tree")
    page.fill("#taskAuthor", "Autotest UI")

    #3. Click to add
    page.click("#btnSubmit")

    #4. Check result (expect из playwright умеет автоматически ждать появления элемента)
    # Find a h3-title with text our task
    task_title_locator = page.locator(".task-item h3:has-text('Test from Playwright')").first

    # Убеждаемся, что элемент стал видимым на странице
    expect(task_title_locator).to_be_visible(timeout=5000)

    # Проверяем, что статус задачи по умоланию отображается как NEW
    status_locator = page.locator(".task-item:has-text('Test from Playwright') .task-status").first
    expect(status_locator).to_have_text("NEW")
