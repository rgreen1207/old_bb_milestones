import pytest
from unittest.mock import AsyncMock, MagicMock
from app.actions.segment_actions import SegmentActions
from app.models.segment_model import SegmentModel

@pytest.mark.asyncio
async def test_create_segment():
    # Mock the path_params argument
    path_params = {
        "client_uuid": "1234",
        "program_9char": "ABCD"
    }

    # Create a list of SegmentModel objects to test with
    segments = [
        SegmentModel(name="Segment 1"),
        SegmentModel(name="Segment 2"),
        SegmentModel(name="Segment 3")
    ]

    # Mock the HelperActions.generate_9char method
    HelperActions = MagicMock()
    HelperActions.generate_9char = AsyncMock(return_value="123456789")

    # Mock the BaseActions.create method
    BaseActions = MagicMock()
    BaseActions.create = AsyncMock(return_value=segments)

    # Create an instance of the SegmentActions class
    segment_actions = SegmentActions(BaseActions, HelperActions)

    # Call the create_segment method with the mocked arguments
    result = await segment_actions.create_segment(segments, path_params)

    # Assert that the BaseActions.create method was called with the correct arguments
    BaseActions.create.assert_called_once_with([
        SegmentModel(
            name="Segment 1",
            client_uuid="1234",
            program_9char="ABCD",
            segment_9char="123456789"
        ),
        SegmentModel(
            name="Segment 2",
            client_uuid="1234",
            program_9char="ABCD",
            segment_9char="123456789"
        ),
        SegmentModel(
            name="Segment 3",
            client_uuid="1234",
            program_9char="ABCD",
            segment_9char="123456789"
        )
    ])

    # Assert that the result is equal to the mocked segments list
    assert result == segments
