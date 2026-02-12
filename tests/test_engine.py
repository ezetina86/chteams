from unittest.mock import MagicMock, patch
from chteams.engine import ActivityEngine


def test_engine_initialization():
    """Tests that the engine initializes correctly."""
    mock_controller = MagicMock()
    engine = ActivityEngine(controller=mock_controller, interval=100, debug=True)
    assert engine.interval == 100
    assert engine.debug is True
    assert engine.paused is False


@patch("chteams.engine.InputHandler")
def test_handle_input_pauses_engine(mock_input_handler_class):
    """Tests that a pause request from the input handler toggles the paused state."""
    mock_controller = MagicMock()
    
    # Instantiate a real engine, but its InputHandler will be a mock
    engine = ActivityEngine(controller=mock_controller)
    
    # Ensure is_set returns False by default so it doesn't toggle immediately
    engine.input_handler.pause_requested.is_set.return_value = False
    
    # Verify starting state
    assert engine.paused is False
    
    # Simulate the input handler thread setting the pause event
    engine.input_handler.pause_requested.is_set.return_value = True
    
    # Call the input handler
    engine._handle_input()
    
    # Verify the engine is paused and the event was cleared
    assert engine.paused is True
    engine.input_handler.pause_requested.clear.assert_called_once()
    
    # Set it back to False for the next call
    engine.input_handler.pause_requested.is_set.return_value = False
    engine._handle_input()
    assert engine.paused is True  # Should stay True because is_set was False


@patch("chteams.engine.ActivityEngine._handle_input")
@patch("chteams.engine.InputHandler")
def test_run_loop_calls_handle_input(mock_input_handler_class, mock_handle_input):
    """Tests that the run loop correctly calls the input handler."""
    mock_controller = MagicMock()
    mock_input_handler_class.return_value = MagicMock()
    
    engine = ActivityEngine(controller=mock_controller, interval=1, debug=True)

    def stop_engine(*args, **kwargs):
        engine.is_running = False
        
    mock_controller.focus_teams_and_interact.side_effect = stop_engine

    with patch("time.sleep", return_value=None):
        engine.run()

    # The loop should run once, calling _handle_input at least once.
    assert mock_handle_input.call_count >= 1


@patch("chteams.engine.InputHandler")
def test_engine_shuts_down_after_max_failures(mock_input_handler_class):
    """Tests that the engine stops after 3 consecutive interaction failures."""
    mock_controller = MagicMock()
    mock_handler = MagicMock()
    # IMPORTANT: Ensure is_set() returns False so it doesn't enter PAUSED state
    mock_handler.pause_requested.is_set.return_value = False
    mock_input_handler_class.return_value = mock_handler
    
    engine = ActivityEngine(controller=mock_controller, interval=1)
    
    # Always fail
    mock_controller.focus_teams_and_interact.side_effect = RuntimeError("Persistent failure")

    with patch("time.sleep", return_value=None), \
         patch("chteams.engine.Live"):
        engine.run()

    # Should have attempted 3 times (max_failures) and then stopped
    assert mock_controller.focus_teams_and_interact.call_count == 3
    assert not engine.is_running
    assert mock_controller.notify.call_count == 4  # 3 failures + 1 shutdown notification
