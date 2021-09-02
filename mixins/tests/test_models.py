class TestVideoURLMixin:
    def test_youtube_video_url(self, video_url_instance, video_url_with_start_instance):
        """
        Test youtube_video_url returns correct embedded url
        """
        assert video_url_instance.youtube_video_url() == (
            "https://www.youtube.com/embed/q5PjWMqaujc?rel=0&autoplay=1")
        assert video_url_with_start_instance.youtube_video_url() == (
            "https://www.youtube.com/embed/q5PjWMqaujc?rel=0&autoplay=1&start=600")
