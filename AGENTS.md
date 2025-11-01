# AGENTS.md

This file provides guidance to Coding Agents when working with code in this repository.

## Project Overview

**ductile-ui** is a Python library that provides declarative UI components for discord.py, inspired by React's component model. It enables building Discord bot interfaces using a state-driven, component-oriented architecture.

- **Language**: Python 3.10+
- **Core Dependencies**: discord.py >= 2.2.0, pydantic >= 2.12.3
- **Package Manager**: UV (v0.9.7)
- **Build System**: Hatchling
- **Code Quality**: Ruff (strict linting + formatting)
- **Testing**: pytest with pytest-mock and pytest-cov

## Development Commands

```bash
# First-time setup
uv sync --dev

# Linting
uv run ruff check

uv run ruff check --fix

# Formatting
uv run ruff format --check

# Testing
uv run pytest
```

Alternatively, you can use mise tasks.

```bash
# First-time setup
mise install && mise init

# Linting
mise run lint
# Formatting
mise run format
# Testing
mise run test
```

### State Management (src/ductile/state.py)

The `State[T]` class is the core of reactive UI updates, inspired by React hooks:

```python
class State[T]:
    def get_state(self) -> T
    def set_state(self, value: T | Callable[[T], T]) -> None  # Auto-triggers view.sync()
    def revert_state(self) -> None
```

**Key behavior**: `set_state()` automatically calls `View.sync()` to re-render the UI. This is the mechanism that enables reactive updates.

### View Pattern (src/ductile/view.py)

Views define declarative UIs through the `render()` method:

```python
class MyView(View):
    def __init__(self):
        super().__init__()
        self.state = State(initial_value, self)

    def render(self) -> ViewObject:
        # Return ViewObject with content, embeds, files, components
        return ViewObject(
            content="...",
            embeds=[...],
            components=[Button(...), Select(...)]
        )
```

`ViewObject` is a Pydantic model with fields: `content`, `embeds`, `files`, `components`. When state changes, `render()` is called again to produce new UI.

### Controllers (src/ductile/controller/)

Controllers manage view lifecycle and Discord API interaction:

- `MessageableController`: Send views to channels/DMs via `.send()`
- `InteractionController`: Respond to interactions via `.respond()` or `.edit_original()`
- Both support `await controller.wait()` to get final state values

### UI Components (src/ductile/ui/)

Wrappers around discord.py UI components with enhanced callbacks:

- `Button(label, style, on_click)`: Custom buttons
- `LinkButton(label, url, style)`: URL buttons
- `Modal(title, components, on_submit)`: Modal dialogs with `TextInput`
- `Select`, `UserSelect`, `RoleSelect`, `ChannelSelect`, `MentionableSelect`: Selection components

**Callback patterns**:

- Async functions: Must call `await interaction.response.defer()` manually
- Sync functions: Library automatically defers the interaction

## Code Quality Standards

### Linter / Formatter

We are using Ruff with strict settings. All code must pass both linting and formatting checks before merging.

### Testing Patterns

See `tests/test_state.py` for examples:

```python
@pytest.fixture
def mock_view():
    view = MagicMock(spec=View)
    view.sync = MagicMock()
    return view

def test_state_operations(mock_view):
    state = State(0, mock_view)
    state.set_state(lambda x: x + 1)
    assert state.get_state() == 1
    assert mock_view.sync.called
```

Use pytest fixtures for View/State setup and pytest-mock for tracking behavior.

## Type System

The library is fully typed with:

- Generic types: `State[T]`, `InteractionCallback[T]`
- Pydantic models: `ViewObject` for runtime validation
- TypedDict: `ButtonStyle`, `SelectStyle` for component styling
- `typing-extensions` for Python 3.10 compatibility (e.g., `Self`)

When adding new features, maintain type hints throughout.

## Compatibility Requirements

- **discord.py >= 2.2.0**: Required. No backwards compatibility with 2.1.x or 1.x
- **Python 3.10+**: Uses modern type hints (`|` syntax, `Self`, generics)
- **Pydantic v2**: Uses v2 API (BaseModel, field validators)

## CI/CD Pipeline

Using GitHub Actions. See `.github/workflows/` for details.

## Examples

See `examples/` directory for reference implementations:

- `basic.py`: Simple counter with increment/decrement
- `confirm.py`: Confirmation dialogs
- `pagination.py`: Pagination patterns
- `select_page.py`: Select component usage

These examples demonstrate common patterns and best practices for using the library.
