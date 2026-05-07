import os
import unicodedata

# 读取词表
with open('ci_biao.txt', 'r', encoding='utf-8') as f:
    word_list = set(line.strip() for line in f if line.strip())

# 获取目录中的所有文件
files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'ci_biao.txt']


def is_punctuation(ch):
    return unicodedata.category(ch).startswith('P')


def segment_text(text, word_list):
    words = []
    i = 0
    while i < len(text):
        if is_punctuation(text[i]):
            i += 1
            continue
        matched = False
        for j in range(len(text) - i, 0, -1):
            candidate = text[i:i+j]
            if candidate in word_list:
                words.append(candidate)
                i += j
                matched = True
                break
        if not matched:
            if text[i].isascii() and text[i].isalpha():
                start = i
                while i < len(text) and text[i].isascii() and text[i].isalpha():
                    i += 1
                words.append(text[start:i])
            else:
                words.append(text[i])
                i += 1
    return words

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = ''.join(content.split())
    words = segment_text(content, word_list)
    unique_words = []
    seen = set()
    for word in words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    word_count = len(unique_words)
    print(f"文档: {file}")
    print(f"词数: {word_count}")
    print(f"包含的词: {unique_words}")
    print()