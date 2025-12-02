import pytest
import json
import allure


@pytest.fixture
def check_status_code():
    def _check(response, expected_status=200):
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}"
        )

        if response.text:
            allure.attach(
                f"Status code: {response.status_code}\n\nResponse body:\n{response.text}",
                name="Response",
                attachment_type=allure.attachment_type.TEXT
            )

        try:
            json_data = response.json()
            allure.attach(
                json.dumps(json_data, indent=2, ensure_ascii=False),
                name="Response JSON",
                attachment_type=allure.attachment_type.JSON
            )
        except Exception:
            pass

    return _check