# 使用哈希函数实现哈希表
class HashTable:
    def __init__(self, size=114514):
        self.size = size
        self.table = [None] * self.size

    def hash_function(self, key):
        # print(key,hash(key))
        return hash(key) % self.size   #这里用了一下hash函数
        

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)  # 更新现有键的值
                    return
            self.table[index].append((key, value))  # 添加新键值对

    def search(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None  # 键不存在

    def delete(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]  # 删除键值对
                    return True
        return False  # 键不存在
    
a= HashTable()
a.insert("name", "Alice")
print(a.search("name"))  # 输出: Alice
