from unittest.mock import call, MagicMock, patch
from unittest import TestCase

from tests.test_utils.requests_utils import mock_api_call
from vistafetch import VistaFetchClient
from vistafetch.model import Fund, SearchResult, Stock


@patch("vistafetch.client.api_session")
class TestVistaFetchClient(TestCase):
    def test_client(self, session_mock: MagicMock):
        VistaFetchClient()

        self.assertIn(
            call.headers.update({"Application": "application/json; charset=utf-8"}),
            session_mock.mock_calls,
        )

    def test_client_additional_headers(self, session_mock: MagicMock):
        header = {
            "Application": "application/json; charset=utf-8",
            "another-header": "another-value",
        }

        VistaFetchClient(client_headers=header)

        self.assertIn(call.headers.update(header), session_mock.mock_calls)

    def test_search_asset(self, session_mock: MagicMock):
        session_mock.get.side_effect = mock_api_call

        result = VistaFetchClient().search_asset(search_term="some_term")

        self.assertTrue(isinstance(result, SearchResult))
        self.assertEqual(2, len(result.assets))
        self.assertTrue(isinstance(result.get(), Fund))
        self.assertTrue(isinstance(result.get(1), Stock))
