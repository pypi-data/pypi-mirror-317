import json
import copy
from unittest import TestCase

import pytest
from lotion.base_page import BasePage
from lotion.properties.title import Title


class TestBasePage(TestCase):
    def test_ページを作成する(self):
        # When
        actual = BasePage.create(properties=[], blocks=[])

        # Then
        self.assertEqual([], actual.properties.values)

    def test_タイトルとリンクをSlack形式で出力する(self):
        # isinstanceのためにパスを揃える
        import sys

        sys.path.append("notion_api")

        # Given
        base_page = BasePage.create(
            properties=[Title.from_plain_text(name="名前", text="タイトル")],
        )
        base_page.update_id_and_url(page_id="dummy-id", url="http://example.com")

        # When
        actual = base_page.title_for_slack()

        # Then
        self.assertEqual("<http://example.com|タイトル>", actual)

    def test_webhookからのリクエストボディを処理できる(self):
        given = json.load(open("test/base_page_test/pattern1.json"))
        print(given)

        actual = BasePage.from_data(given)
        print(actual)
        self.assertEqual(given["id"], actual.id)

    @pytest.mark.current()
    def test_コピーを作成する(self):
        # Given
        base_page = BasePage.create(
            properties=[Title.from_plain_text(name="名前", text="タイトル")],
        )
        base_page.update_id_and_url(page_id="dummy-id", url="http://example.com")

        # When
        actual = base_page.copy()

        # Then
        self.assertIsNone(actual.id_)
        self.assertIsNone(actual.url_)
        self.assertEqual(base_page.properties.values, actual.properties.values)
        self.assertEqual(base_page.block_children, actual.block_children)
        self.assertNotEqual(base_page, actual)
