from playwright.sync_api import Page, expect
import allure
import pytest

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
@allure.story("Filter tasks")
class TestTaskFilters:

    @allure.story("Create new task")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_new_task_via_ui(page: Page):
        """"UI-test for adding new task"""
        create_new_task_via_ui(page)

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
            with page.expect_response(
                    lambda res: res.request.method == "DELETE" and "/tasks" in res.url) as response_info:
                confirm_btn.click()
            response = response_info.value
            assert response.status == 204, f"Ожидался статус 204, но бэкенд вернул {response.status}"

        with allure.step("Check a visible the deleted task"):
            expect(task_card).not_to_be_visible(timeout=5000)

    @allure.title("Filter tasks by status: {status}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("status", ["NEW", "IN_PROGRESS", "DONE"])
    def test_filter_by_status(self, page: Page, status: str):
        page.goto("http://127.0.0.1:8000/")

        with allure.step(f"Выбор статуса '{status}' в выпадающем списке"):
            page.select_option("#filterStatus", value=status)

        with allure.step("Проверка, что все отображаемые карточки имеют выбранный статус"):
            # Ждем завершения сетевого запроса фильтрации
            page.wait_for_load_state("networkidle")

            statuses = page.locator(".task-item .task-status").all_text_contents()
            for item_status in statuses:
                assert item_status == status, f"Ожидался статус {status}, но найден {item_status}"

    @allure.title("Filter tasks by name")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_by_name(self, page: Page):
        page.goto("http://127.0.0.1:8000/")
        search_query = "Test from Playwright"

        with allure.step(f"Ввод '{search_query}' в поле поиска по названию"):
            page.fill("#filterName", search_query)

        with allure.step("Проверка соответствия названий найденных карточек"):
            page.wait_for_load_state("networkidle")
            titles = page.locator(".task-item .task-title").all_text_contents()
            for title in titles:
                assert search_query.lower() in title.lower()

    @allure.title("Filter tasks by author")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_author(self, page: Page):
        page.goto("http://127.0.0.1:8000/")
        author_query = "Autotest UI"

        with allure.step(f"Ввод '{author_query}' в поле поиска по автору"):
            page.fill("#filterAuthor", author_query)

        with allure.step("Проверка авторов на найденных карточках"):
            page.wait_for_load_state("networkidle")
            authors = page.locator(".task-item .task-author").all_text_contents()
            for author in authors:
                assert author_query.lower() in author.lower()