import pytest

@pytest.fixture(scope="session")
def record_video_dir(tmp_path_factory):
    # Directory where Playwright will save videos
    return tmp_path_factory.mktemp("videos")

@pytest.fixture(scope="session")
def browser_context_args(record_video_dir):
    # Pass video directory into Playwright browser context
    return {"record_video_dir": str(record_video_dir)}
