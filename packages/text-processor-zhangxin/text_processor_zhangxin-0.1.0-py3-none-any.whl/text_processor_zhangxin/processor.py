# text_processor_zhangxin/processor.py

import re
from collections import Counter

class AdvancedTextProcessor:
    def __init__(self, text):
        self.text = text

    # 清理文本，去除多余的空格和换行符
    def clean_text(self):
        return re.sub(r'\s+', ' ', self.text).strip()

    # 统计文本中的单词频率
    def word_frequency(self):
        words = self.extract_words()
        return dict(Counter(words))

    # 从文本中提取所有单词
    def extract_words(self):
        return re.findall(r'\b\w+\b', self.text.lower())

    # 去除停用词
    def remove_stopwords(self, stopwords):
        words = self.extract_words()
        filtered_words = [word for word in words if word not in stopwords]
        return ' '.join(filtered_words)

    # 统计句子的数量
    def count_sentences(self):
        sentences = re.split(r'[.!?]', self.text)
        return len([s for s in sentences if s.strip()])

    # 替换文本中的子串
    def replace_substring(self, old, new):
        return self.text.replace(old, new)

    # 提取唯一的单词
    def get_unique_words(self):
        words = self.extract_words()
        return set(words)

    # 将文本转换为标题格式
    def to_title_case(self):
        return self.text.title()

    # 检查文本是否为回文
    def is_palindrome(self):
        cleaned_text = re.sub(r'[^A-Za-z0-9]', '', self.text.lower())
        return cleaned_text == cleaned_text[::-1]

    # 反转文本
    def reverse_text(self):
        return self.text[::-1]

    # 获取文本中的最长单词
    def find_longest_word(self):
        words = self.extract_words()
        return max(words, key=len)
