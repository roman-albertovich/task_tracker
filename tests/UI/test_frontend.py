from playwright.sync_api import Page, expect

def create_new_task_via_ui(page: Page):
    # 1. Open page our app
    page.goto("http://127.0.0.1:8000/")

    # 2. Fill page locator ID
    page.fill("#taskName", "Test from Playwright")
    page.fill("#taskDesc", "Chek rendering DOM-tree")
    page.fill("#taskAuthor", "Autotest UI")

    # 3. Click to add
    with page.expect_response("**/tasks") as response_info:
        page.click("#btnSubmit")

    response = response_info.value
    assert response.status == 201

    response_data = response.json()
    task_id = response_data["id"]

    # 4. Check result (expect из playwright умеет автоматически ждать появления элемента)
    task_card = page.locator(f'.task-item[data-id="{task_id}"]').first

    # Убеждаемся, что элемент стал видимым на странице
    expect(task_card).to_be_visible(timeout=5000)

    # Проверяем, что статус задачи по умоланию отображается как NEW
    expect(task_card.locator(".task-status")).to_have_text("NEW")
    return task_id

def test_add_new_task_via_ui(page: Page):
    """"UI-test for adding new task"""
    create_new_task_via_ui(page)

def test_delete_task_via_ui(page: Page):
    """"UI-test for deleting task"""
    task_id = create_new_task_via_ui(page)

    task_card = page.locator(f'.task-item[data-id="{task_id}"]').first

    task_card.locator(".btn-delete").click()

    confirm_btn = page.locator("#confirmDeleteBtn")
    expect(confirm_btn).to_be_visible(timeout=5000)

    with page.expect_response(lambda res: res.request.method == "DELETE" and "/tasks" in res.url) as response_info:
        confirm_btn.click()
    response = response_info.value
    assert response.status == 204, f"Ожидался статус 204, но бэкенд вернул {response.status}"
    expect(task_card).not_to_be_visible(timeout=5000)
