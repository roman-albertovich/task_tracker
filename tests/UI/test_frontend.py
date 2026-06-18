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
    with page.expect_response("**/tasks") as response_info:
        page.click("#btnSubmit")

    response = response_info.value
    assert response.status == 201

    response_data = response.json()
    task_id = response_data["id"]

    #4. Check result (expect из playwright умеет автоматически ждать появления элемента)
    task_card= page.locator(f'.task-item[data-id="{task_id}"]').first

    # Убеждаемся, что элемент стал видимым на странице
    expect(task_card).to_be_visible(timeout=5000)

    # Проверяем, что статус задачи по умоланию отображается как NEW
    expect(task_card.locator(".task-status")).to_have_text("NEW")
