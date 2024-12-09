from collections.abc import Generator

import pytest
from pytest_mock import MockFixture, MockType

from ductile import State
from ductile.view import View


@pytest.fixture
def view() -> View:
    return View()


@pytest.fixture
def view_spy(mocker: MockFixture, view: View) -> Generator[MockType, None, None]:
    spy = mocker.spy(view, "sync")

    yield spy
    spy.reset_mock()


@pytest.fixture
def state(view: View) -> Generator[State[int], None, None]:
    test_state = State(0, view)

    yield test_state
    test_state.set_state(0)


def test_get_state(state: State[int]) -> None:
    assert state.get_state() == 0


def test_get_state_with_call(state: State[int]) -> None:
    assert state() == 0


def test_set_state(state: State[int]) -> None:
    state.set_state(1)
    assert state.get_state() == 1


def test_set_state_bubble_sync(state: State[int], view_spy: MockType) -> None:
    state.set_state(1)
    view_spy.assert_called_once()


def test_set_state_with_previous_value(state: State[int]) -> None:
    state.set_state(lambda x: x + 1)
    assert state.get_state() == 1


def test_revert_state(state: State[int]) -> None:
    state.set_state(1)
    assert state.get_state() == 1

    state.revert_state()
    assert state.get_state() == 0
