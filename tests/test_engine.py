from unittest.mock import MagicMock, patch
from chteams.engine import ActivityEngine


def test_engine_stops_on_is_running_false():
    mock_controller = MagicMock()
    mock_controller.get_frontmost_app.return_value = "Terminal"
    # Set interval to 1 so it runs quickly
    engine = ActivityEngine(controller=mock_controller, interval=1)

    # We want to run the loop at least once and then stop
    # We'll use a side_effect to stop the engine after the first interaction
    def stop_engine(*args, **kwargs):
        engine.is_running = False

    mock_controller.focus_teams_and_interact.side_effect = stop_engine

    with patch("time.sleep", return_value=None), \
         patch("chteams.engine.Live"), \
         patch("chteams.engine.keyboard.GlobalHotKeys"):
        engine.run()

    assert mock_controller.start_caffeinate.called
    assert mock_controller.focus_teams_and_interact.called
    assert mock_controller.stop_caffeinate.called


def test_pause_toggle_with_focus():
    mock_controller = MagicMock()
    engine = ActivityEngine(controller=mock_controller)
    
    # Test with focus
    mock_controller.get_frontmost_app.return_value = "Terminal"
    engine._on_pause_toggle()
    assert engine.paused is True
    
    # Test without focus
    mock_controller.get_frontmost_app.return_value = "Notes"
    engine._on_pause_toggle()
    assert engine.paused is True  # Should NOT have changed back to False


def test_engine_handles_interaction_failure():
    mock_controller = MagicMock()
    engine = ActivityEngine(controller=mock_controller, interval=1)
    
    # Fail once then stop
    def fail_then_stop(*args, **kwargs):
        engine.is_running = False
        raise RuntimeError("Failed")

    mock_controller.focus_teams_and_interact.side_effect = fail_then_stop

    with patch("time.sleep", return_value=None), \
         patch("chteams.engine.Live"), \
         patch("chteams.engine.keyboard.Listener"):
        engine.run()

    assert mock_controller.notify.called
    assert engine.activity_count == 0


def test_engine_shuts_down_after_max_failures():
    mock_controller = MagicMock()
    engine = ActivityEngine(controller=mock_controller, interval=1)
    
    # Always fail
    mock_controller.focus_teams_and_interact.side_effect = RuntimeError("Persistent failure")

    with patch("time.sleep", return_value=None), \
         patch("chteams.engine.Live"), \
         patch("chteams.engine.keyboard.Listener"):
        engine.run()

    # Should have attempted 3 times (max_failures) and then stopped
    assert mock_controller.focus_teams_and_interact.call_count == 3
    assert not engine.is_running
    assert mock_controller.notify.call_count == 4  # 3 failures + 1 shutdown notification
