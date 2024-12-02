from collections.abc import Generator

import pytest

from ductile import State
from ductile.view import View


@pytest.fixture
def state() -> Generator[State[int], None, None]:
    test_state = State(0, View())
    yield test_state
    test_state.set_state(0)


def test_get_state(state: State[int]) -> None:
    assert state.get_state() == 0


def test_get_state_with_call(state: State[int]) -> None:
    assert state() == 0


def test_set_state(state: State[int]) -> None:
    state.set_state(1)
    assert state.get_state() == 1


def test_set_state_with_previous_value(state: State[int]) -> None:
    state.set_state(lambda x: x + 1)
    assert state.get_state() == 1


def test_revert_state(state: State[int]) -> None:
    state.set_state(1)
    assert state.get_state() == 1

    state.revert_state()
    assert state.get_state() == 0
