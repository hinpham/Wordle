import unittest
from unittest import mock

import src.AgileSpellChecker as ASC

class AgileSpellCheckerServiceTest(unittest.TestCase):

    def test_getResponse_valid_request_returns_a_text(self):
        self.assertTrue(ASC.getResponse("FAVOR").isalpha())

    def test_parse_converts_stringTrue_to_BooleanTrue(self):
        self.assertTrue(ASC.parse("true"))

    def test_parse_converts_stringFalse_to_BooleanFalse(self):
        self.assertFalse(ASC.parse("false"))

    @mock.patch("src.AgileSpellChecker.getResponse")
    def test_is_correct_spelling_returns_true(self, mock_getResponse):
        mock_getResponse.return_value = "true"

        self.assertTrue(ASC.isSpellingCorrect("FAVOR"))

    @mock.patch("src.AgileSpellChecker.getResponse")
    def test_is_correct_spelling_returns_false(self, mock_getResponse):
        mock_getResponse.return_value = "false"

        self.assertFalse(ASC.isSpellingCorrect("FAVOR"))

    @mock.patch("src.AgileSpellChecker.getResponse")
    def test_is_correct_spelling_receives_network_error(self, mock_getResponse):
        mock_getResponse.side_effect = RuntimeError("Network error")

        with self.assertRaisesRegex(RuntimeError, "Network error"):
            ASC.isSpellingCorrect("FAVOR")


if __name__ == 'main':
    unittest.main()
