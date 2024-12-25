# tests/test_app.py
import pytest

from tuitorial.app import TutorialApp
from tuitorial.highlighting import Focus


@pytest.fixture
def example_code():
    return "def test():\n    pass\n"


@pytest.fixture
def tutorial_steps():
    return [
        ("Step 1", [Focus.literal("def")]),
        ("Step 2", [Focus.literal("pass")]),
    ]


@pytest.fixture
async def app(example_code, tutorial_steps):
    app = TutorialApp(example_code, tutorial_steps)
    async with app.run_test() as pilot:
        yield app, pilot


@pytest.mark.asyncio
async def test_app_init(app):
    """Test app initialization."""
    app, pilot = await anext(app)
    assert app.current_index == 0
    assert len(app.tutorial_steps) == 2


@pytest.mark.asyncio
async def test_next_focus(app):
    """Test next focus action."""
    app, pilot = await anext(app)

    # Initial state
    assert app.current_index == 0

    # Press right arrow
    await pilot.press("right")
    assert app.current_index == 1


@pytest.mark.asyncio
async def test_previous_focus(app):
    """Test previous focus action."""
    app, pilot = await anext(app)

    # Move to last step
    app.current_index = len(app.tutorial_steps) - 1

    # Press left arrow
    await pilot.press("left")
    assert app.current_index == 0


@pytest.mark.asyncio
async def test_reset_focus(app):
    """Test reset focus action."""
    app, pilot = await anext(app)

    # Move to last step
    app.current_index = len(app.tutorial_steps) - 1

    # Press reset key
    await pilot.press("r")
    assert app.current_index == 0


@pytest.mark.asyncio
async def test_quit(app):
    """Test quit action."""
    app, pilot = await anext(app)

    # Create a task to press 'q'
    async def press_q():
        await pilot.press("q")

    # Run the press_q task and expect the app to exit
    await press_q()
    assert not app.is_running


@pytest.mark.asyncio
async def test_update_display(app):
    """Test display updates."""
    app, _ = await anext(app)
    initial_description = app.query_one("#description").render()

    # Move to next step
    app.action_next_focus()
    new_description = app.query_one("#description").render()

    assert initial_description != new_description


@pytest.mark.asyncio
async def test_current_focuses(app):
    """Test current_focuses property."""
    app, _ = await anext(app)
    assert app.current_focuses == app.tutorial_steps[0][1]


@pytest.mark.asyncio
async def test_current_description(app):
    """Test current_description property."""
    app, _ = await anext(app)
    assert app.current_description == app.tutorial_steps[0][0]
