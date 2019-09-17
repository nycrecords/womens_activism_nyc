import unittest
from unittest.mock import patch

from app.tests.utils import BaseTestCase

SHARE_STORY_TEMPLATE = "stories/share_a_story.html"


class StoriesViewsTests(BaseTestCase):
    @patch("app.stories.views.render_template", return_value="failure")
    def test_post_bad_video(self, render_template_patch):
        with render_template_patch:
            response = self.client.post("/share", data={"video_url": "bad.com"})
            self.assertEqual(response.data, b"failure")

    @patch("app.stories.views.render_template", return_value="failure")
    def test_post_good_video(self, render_template_patch):
        with render_template_patch:
            response = self.client.post(
                "/share", data={"video_url": "http://youtube.com"}
            )
            self.assertEqual(response.data, b"failure")


if __name__ == "__main__":
    unittest.main()
