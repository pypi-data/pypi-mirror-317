# coding = utf-8
# @Time    : 2024-12-26  14:10:57
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Key word matching utils.

import re
import os

class KeyWord:
    def __init__(self, key_words_folder):
        # get key words from file
        # get all csv files in the folder (recursively)
        self.key_word_files = []
        for root, _, files in os.walk(key_words_folder):
            for file in files:
                if file.endswith(".csv"):
                    self.key_word_files.append(os.path.join(root, file))
        self.key_words = []
        for key_word_file in self.key_word_files:
            file_id = key_word_file.split("/")[-1].split(".")[0]
            self.key_words.extend(self.load_key_words(key_word_file,file_id))
        print(f"Loaded {len(self.key_words)} key words from {len(self.key_word_files)} files.")

    def load_key_words(self, key_word_file,file_id=None):
        """Load key words from file."""
        if not file_id:
            file_id = key_word_file.split("/")[-1].split(".")[0]
        key_words = []
        with open(key_word_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                if "," not in line:
                    continue
                key_word = line.strip()
                r = key_word.split(",")
                class_name = r[0]
                key_word = r[1]
                if key_word:
                    key_words.append([class_name, key_word, file_id])
        return key_words
    
    def match(self, text: str):
        """Match key words in text."""
        matched_key_words = []
        for class_name,key_word,file_id in self.key_words:
            if "re=" in key_word:
                key_word = key_word.replace("re=", "")
                if re.search(key_word, text):
                    matched_key_words.append([class_name, key_word, file_id])
            else:
                if key_word in text:
                    matched_key_words.append([class_name, key_word, file_id])
        return matched_key_words
