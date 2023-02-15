import unittest
from unittest import mock

import src.AgileWordService as AWS

class AgileWordServiceTest(unittest.TestCase):

    def test_get_text_from_agile_service(self):
        self.assertTrue(type(AWS.getResponse()) == str)
      
    def test_parse_text_to_a_list_of_words(self):
        text = AWS.getResponse()
        
        self.assertTrue(type(AWS.parseTextToListOfWords(text)) == list)

    def test_fetch_words(self):
        listOfWords = ['FAVOR', 'RIGOR', 'SUGAR', 'POWER', 'POINT', 'PIOUS', 'GRIND', 'NASTY', 'WATER', 'AVOID',
                       'PAINT', 'ABBEY', 'SHIRE', 'CYCLE', 'SHORT', 'WHICH', 'YIELD', 'AGILE', 'BUILD', 'BRICK']
        
        self.assertEqual(listOfWords, AWS.fetchWords())
      
    @mock.patch("src.AgileWordService.getResponse")
    def test_fetch_words_throws_network_error(self, mock_getResponse):
        mock_getResponse.side_effect = RuntimeError("Network error")
        
        with self.assertRaisesRegex(RuntimeError, "Network error"):
            AWS.fetchWords()


if __name__ == 'main':
    unittest.main()
