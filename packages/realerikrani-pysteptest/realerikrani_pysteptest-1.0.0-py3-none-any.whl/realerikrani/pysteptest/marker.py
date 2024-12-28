# This code is based on the code from the pytest docs:
# https://github.com/pytest-dev/pytest/blob/24e84f08f43216f95620135305cbebe9f646e433/doc/en/example/simple.rst#incremental-testing---test-steps
# See LICENSE_OF_PYTEST file in https://github.com/realerikrani/pysteptest
# for the MIT license of pytest project.

from typing import Self

import pytest
from _pytest.config import Config
from _pytest.nodes import Item

INCREMENTAL_MARKER: str = "pysteptest"


class IncrementalTestTracker:
    def __init__(self: Self) -> None:  # noqa: D107
        self._history_of_fails: dict[str, dict[tuple[int, ...], str]] = {}

    def _has_test_failed(self, call: pytest.CallInfo) -> bool:
        """Check if the test call has failed."""
        return call.excinfo is not None

    def _get_parametrize_index(self, item: Item) -> tuple[int, ...]:
        """Retrieve the parameterization index for the test item."""
        return (
            tuple(item.callspec.indices.values()) if hasattr(item, "callspec") else ()
        )

    def _record_failed_test(
        self, item: Item, parametrize_index: tuple[int, ...]
    ) -> None:
        """Record the failed test in the history."""
        test_name = item.originalname or item.name  # type: ignore[attr-defined]
        self._history_of_fails.setdefault(str(item.cls), {}).setdefault(  # type: ignore[attr-defined]
            parametrize_index, test_name
        )

    def _get_previous_failed_test_name(
        self, cls_name: str, parametrize_index: tuple[int, ...]
    ) -> str | None:
        """Get the name of the previous failed test, if any."""
        return self._history_of_fails.get(cls_name, {}).get(parametrize_index, None)

    def handle_test_report(self, item: Item, call: pytest.CallInfo) -> None:
        """Handle the test report to record failures."""
        if INCREMENTAL_MARKER in item.keywords and self._has_test_failed(call):
            parametrize_index = self._get_parametrize_index(item)
            self._record_failed_test(item, parametrize_index)

    def handle_test_setup(self, item: Item) -> None:
        """Mark test as failed if a previous test failed."""
        if INCREMENTAL_MARKER in item.keywords:
            cls_name = str(item.cls)  # type: ignore[attr-defined]
            parametrize_index = self._get_parametrize_index(item)
            previous_test_name = self._get_previous_failed_test_name(
                cls_name, parametrize_index
            )

            if previous_test_name is not None:
                pytest.xfail(f"previous test failed ({previous_test_name})")


incremental_tracker = IncrementalTestTracker()


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "pysteptest: mark test as a pysteptest")


def pytest_runtest_makereport(item: Item, call: pytest.CallInfo) -> None:
    """Hook to record failed tests for incremental testing."""
    incremental_tracker.handle_test_report(item, call)


def pytest_runtest_setup(item: Item) -> None:
    """Hook to mark tests as expected to fail if a previous test failed."""
    incremental_tracker.handle_test_setup(item)
