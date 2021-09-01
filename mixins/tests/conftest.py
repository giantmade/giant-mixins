import pytest

from mixins.models import VideoURLMixin


@pytest.fixture
def video_url_with_start_instance():
    return VideoURLMixin(youtube_url="https://www.youtube.com/watch?v=q5PjWMqaujc&t=600")


@pytest.fixture
def video_url_instance():
    return VideoURLMixin(youtube_url="https://www.youtube.com/watch?v=q5PjWMqaujc")