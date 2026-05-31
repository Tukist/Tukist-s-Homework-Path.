import os
import re

try:
    # 读取词表
    with open('ci_biao.txt', 'r', encoding='utf-8') as f:
        words = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
except FileNotFoundError:
    print("错误：找不到文件 ci_biao.txt")
    exit(1)
except UnicodeDecodeError:
    print("错误：ci_biao.txt 编码问题，请确保是 UTF-8 编码")
    exit(1)

# 将词表按词长分组，便于后续哈希匹配
words_by_len = {}
max_word_len = 0
for w in words:
    l = len(w)
    words_by_len.setdefault(l, set()).add(w)
    max_word_len = max(max_word_len, l)
possible_lengths = sorted(words_by_len.keys(), reverse=True)

# 倒排索引：词 -> 文档集合
inverted_index = {}

# 获取所有文档文件（除了ci_biao.txt）
docs = [f for f in os.listdir('.') if f.startswith('doc') and f.endswith('.txt')]

if not docs:
    print("错误：没有找到以 'doc' 开头的 .txt 文件")
    exit(1)

# 对于每个文档
for doc in docs:
    try:
        with open(doc, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {doc}")
        continue
    except UnicodeDecodeError:
        print(f"错误：{doc} 编码问题，请确保是 UTF-8 编码")
        continue

    # 预计算滚动哈希，避免重复切片匹配
    base = 131
    mask = (1 << 64) - 1
    n = len(content)
    h = [0] * (n + 1)
    p = [1] * (n + 1)
    for idx, ch in enumerate(content):
        h[idx + 1] = ((h[idx] * base) + ord(ch)) & mask
        p[idx + 1] = (p[idx] * base) & mask

    def substring_hash(start, end):
        return (h[end] - (h[start] * p[end - start] & mask)) & mask

    # 词表哈希按长度分组
    def word_hash(word):
        h_val = 0
        for ch in word:
            h_val = ((h_val * base) + ord(ch)) & mask
        return h_val

    hash_by_len = {
        length: {word_hash(word) for word in word_set}
        for length, word_set in words_by_len.items()
    }

    # 分词
    tokens = []
    i = 0
    while i < n:
        matched = False
        for length in possible_lengths:
            if i + length > n:
                continue
            candidate_hash = substring_hash(i, i + length)
            if candidate_hash not in hash_by_len[length]:
                continue
            candidate = content[i:i + length]
            if candidate in words_by_len[length]:
                tokens.append(candidate)
                i += length
                matched = True
                break
        if not matched:
            # 英文或数字连续字符当作一个词
            if re.match(r'[A-Za-z0-9]', content[i]):
                start = i
                while i < n and re.match(r'[A-Za-z0-9]', content[i]):
                    i += 1
                tokens.append(content[start:i])
            elif re.match(r'[\u4e00-\u9fff]', content[i]):
                tokens.append(content[i])
                i += 1
            else:
                i += 1

    # 过滤掉标点、空格、换行等，只保留词
    tokens = [token for token in tokens if re.match(r'[\u4e00-\u9fffA-Za-z0-9]+', token)]

    # 保持顺序的唯一词列表
    unique_tokens = list(dict.fromkeys(tokens))
    word_count = len(tokens)

    # 更新倒排索引
    for token in unique_tokens:
        inverted_index.setdefault(token, []).append(doc)

    print(f'{doc}: {word_count} 词')
    print(f'包含的词: {tokens}')
    print(f'唯一词（按出现顺序）: {unique_tokens}')

# 倒排索引构建完成，查询接口
print('\n倒排索引已构建完成。可以输入词来查询包含该词的文档。')
while True:
    query = input('请输入要查询的词（按回车退出）：').strip()
    if not query:
        break
    docs_with_word = inverted_index.get(query)
    if docs_with_word:
        print(f"词 '{query}' 出现在文档: {docs_with_word}")
    else:
        print(f"词 '{query}' 未出现在任何文档中。")
        