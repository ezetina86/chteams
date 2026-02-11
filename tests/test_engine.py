from unittest.mock import MagicMock, patch
from chteams.engine import ActivityEngine


def test_engine_stops_on_is_running_false():
    mock_controller = MagicMock()
    # Set interval to 1 so it runs quickly
    engine = ActivityEngine(controller=mock_controller, interval=1)

    # We want to run the loop at least once and then stop
    # We'll use a side_effect to stop the engine after the first interaction
    def stop_engine(*args, **kwargs):
        engine.is_running = False

    mock_controller.focus_teams_and_interact.side_effect = stop_engine

    with patch("time.sleep", return_value=None), \
         patch("chteams.engine.Live"), \
         patch("chteams.engine.keyboard.Listener"):
        engine.run()

    assert mock_controller.start_caffeinate.called
    assert mock_controller.focus_teams_and_interact.called
    assert mock_controller.stop_caffeinate.called
