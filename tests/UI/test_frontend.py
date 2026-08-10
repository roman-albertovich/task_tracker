from playwright.sync_api import Page, expect
import allure

@allure.step("Create new task with UI")
def create_new_task_via_ui(page: Page):
    # 1. Open page our app
    page.goto("http://127.0.0.1:8000/")

    with allure.step("Fill page locator ID"):
        page.fill("#taskName", "Test from Playwright")
        page.fill("#taskDesc", "Chek rendering DOM-tree")
        page.fill("#taskAuthor", "Autotest UI")

    with allure.step("Send page of create task"):
        with page.expect_response("**/tasks") as response_info:
            page.click("#btnSubmit")

    response = response_info.value
    assert response.status == 201

    response_data = response.json()
    task_id = response_data["id"]

    with allure.step("Check new page in DOM"):
        # (expect из playwright умеет автоматически ждать появления элемента)
        task_card = page.locator(f'.task-item[data-id="{task_id}"]').first
        # Убеждаемся, что элемент стал видимым на странице
        expect(task_card).to_be_visible(timeout=5000)

    with allure.step("Check task status NEW"):
        expect(task_card.locator(".task-status")).to_have_text("NEW")
    return task_id

@allure.feature("Tasks")
@allure.story("Create new task")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_new_task_via_ui(page: Page):
    """"UI-test for adding new task"""
    create_new_task_via_ui(page)

@allure.feature("Tasks")
@allure.story("Delete task")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_task_via_ui(page: Page):
    """"UI-test for deleting task"""
    task_id = create_new_task_via_ui(page)

    with allure.step("Click to DELETE button"):
        task_card = page.locator(f'.task-item[data-id="{task_id}"]').first
        task_card.locator(".btn-delete").click()

    with allure.step("Check a confirm form"):
        confirm_btn = page.locator("#confirmDeleteBtn")
        expect(confirm_btn).to_be_visible(timeout=5000)

    with allure.step("Deletion confirmation and waiting for DELETE-request"):
        with page.expect_response(lambda res: res.request.method == "DELETE" and "/tasks" in res.url) as response_info:
            confirm_btn.click()
        response = response_info.value
        assert response.status == 204, f"Ожидался статус 204, но бэкенд вернул {response.status}"

    with allure.step("Check a visible the deleted task"):
        expect(task_card).not_to_be_visible(timeout=5000)