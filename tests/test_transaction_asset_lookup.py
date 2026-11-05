import unittest
from pathlib import Path
from unittest.mock import AsyncMock

from bs4 import BeautifulSoup
from twikit.x_client_transaction.transaction import ClientTransaction


class TransactionAssetLookupTests(unittest.IsolatedAsyncioTestCase):
    async def test_resolves_current_webpack_chunk_hash_and_indices(self):
        html = Path(__file__).parent / "fixtures/x-homepage-webpack.html"
        page = BeautifulSoup(html.read_text(), "html.parser")
        response = type("Response", (), {"text": "const a=[7], 16; const b=[23], 16; const c=[42], 16;"})()
        session = type("Session", (), {"request": AsyncMock(return_value=response)})()
        tx = ClientTransaction()

        first, rest = await tx.get_indices(page, session, {})

        self.assertEqual((first, rest), (7, [23, 42]))
        session.request.assert_awaited_once_with(
            method="GET",
            url="https://abs.twimg.com/responsive-web/client-web/ondemand.s.ab12cd34ef56a.js",
            headers={},
        )

    async def test_missing_chunk_hash_fails_closed(self):
        page = BeautifulSoup('<script>,1234:"ondemand.s"</script>', "html.parser")
        session = type("Session", (), {"request": AsyncMock()})()
        with self.assertRaisesRegex(Exception, "Couldn't get KEY_BYTE indices"):
            await ClientTransaction().get_indices(page, session, {})
        session.request.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
