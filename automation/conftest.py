import pytest


def pytest_configure(config):
    config._metadata = {
        "Projekt": "Testy automatyczne stron www — portfolio QA",
        "Autor": "Daniel Bryjak",
        "Framework": "Python + Pytest + Playwright",
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }
