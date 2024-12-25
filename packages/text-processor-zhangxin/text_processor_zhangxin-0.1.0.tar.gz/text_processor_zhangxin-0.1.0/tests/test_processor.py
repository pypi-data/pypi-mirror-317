# tests/test_processor.py

import unittest
from text_processor_zhangxin.processor import AdvancedTextProcessor

class TestAdvancedTextProcessor(unittest.TestCase):

    def setUp(self):
        self.text = "Hello, world! This is a test. A palindrome? Yes, a palindrome!"
        self.processor = AdvancedTextProcessor(self.text)
        self.stopwords = ["is", "a", "the", "this", "of", "and"]

    def test_get_char_frequency(self):
        expected_freq = {'H': 1, 'e': 1, 'l': 3, 'o': 2, ',': 1, ' ': 7, 'w': 1, 'r': 1, 'd': 1, '!': 1, 'T': 1, 'h': 1, 'i': 2, 's': 2, 'a': 3, 't': 3, '.': 2, '?': 1, 'Y': 1}
        self.assertEqual(self.processor.get_char_frequency(), expected_freq)

    def test_clean_text(self):
        expected_cleaned = "Hello world This is a test A palindrome Yes a palindrome"
        self.assertEqual(self.processor.clean_text(), expected_cleaned)

    def test_extract_words(self):
        expected_words = ['hello', 'world', 'this', 'is', 'a', 'test', 'a', 'palindrome', 'yes', 'a', 'palindrome']
        self.assertEqual(self.processor.extract_words(), expected_words)

    def test_word_frequency(self):
        expected_word_freq = {'hello': 1, 'world': 1, 'this': 1, 'is': 1, 'a': 3, 'test': 1, 'palindrome': 2, 'yes': 1}
        self.assertEqual(self.processor.word_frequency(), expected_word_freq)

    def test_remove_stopwords(self):
        text_without_stopwords = "hello world test palindrome palindrome"
        self.assertEqual(self.processor.remove_stopwords(self.stopwords), text_without_stopwords)

    def test_count_sentences(self):
        self.assertEqual(self.processor.count_sentences(), 3)

    def test_replace_substring(self):
        self.assertEqual(self.processor.replace_substring("world", "universe"), "Hello, universe! This is a test. A palindrome? Yes, a palindrome!")

    def test_get_unique_words(self):
        expected_unique_words = {'hello', 'world', 'this', 'is', 'a', 'test', 'palindrome', 'yes'}
        self.assertEqual(self.processor.get_unique_words(), expected_unique_words)

    def test_to_title_case(self):
        expected_title_case = "Hello, World! This Is A Test. A Palindrome? Yes, A Palindrome!"
        self.assertEqual(self.processor.to_title_case(), expected_title_case)

    def test_find_longest_word(self):
        self.assertEqual(self.processor.find_longest_word(), "palindrome")

    def test_is_palindrome(self):
        palindrome_text = "A man, a plan, a canal, Panama"
        processor = AdvancedTextProcessor(palindrome_text)
        self.assertTrue(processor.is_palindrome())

        non_palindrome_text = "Hello World"
        processor = AdvancedTextProcessor(non_palindrome_text)
        self.assertFalse(processor.is_palindrome())

    def test_reverse_text(self):
        self.assertEqual(self.processor.reverse_text(), "!emordnilap a ,?emordnilap a .tset a si sihT !dlrow ,olleH")

if __name__ == "__main__":
    unittest.main()
