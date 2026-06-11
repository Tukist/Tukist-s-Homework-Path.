# """"集合"""
# from collections.abc import Sequence
# from typing import Any

# class Set:
#     """
#     一个可查询、插入、删除的集合
#     """
#     def __init__(self, iterable: Sequence[Any]):
#         self.data = list(set(iterable))

#     def insert_last(self, element: Any) -> bool:
#         for index, item in enumerate(self.data):
#             if item == element:
#                 return False
#         self.data.append(element)
#         return self.data
#     def search(self, element: Any) -> bool:
#         for index, item in enumerate(self.data):
#             if item == element:
#                 return self.data
#         return self.data
#     def delete(self, element: Any) -> bool:
#         for index,item in enumerate(self.data):
#             if item == element:
#                 del self.data[index]
#                 return self.data
#         return self.data

# fruits = Set(['apple', 'banana', 'orange'])
# print(fruits.insert_last('grape'))  # 输出: ['apple', 'banana', 'orange', 'grape']
# print(fruits.search('apple'))     # 输出: ['apple', 'banana', 'orange', 'grape']
# print(fruits.delete('banana'))    # 输出: ['apple', 'orange', 'grape']

# 有序数组

from typing import Sequence, Any

class OrderedArrayInsert:
    """
    有序数组的插入
    """

    def __init__(self, iterable: Sequence[Any]):
        """
        :param iterable: 有序数组初始化
        """
        self.iterable = list(iterable)
        

    def insert(self, element: Any) :
        """
        插入元素
        :param element: 待插入的元素
        """
        self.len = len(self.iterable)
        # 插入逻辑（以下为常见实现，可根据需求调整）
        i = 0
        while i < self.len and self.iterable[i] < element:
            i += 1
            # print(i)
        self.iterable.append("")
        for j in range(self.len, i, -1):
            self.iterable[j] = self.iterable[j - 1]
            # print(self.iterable)
        self.iterable[i] = element
        return self.iterable

ordered_array = OrderedArrayInsert([1, 3, 5, 7])
print(ordered_array.insert(4))  # 输出: [1, 3, 4, 5, 7]
print(ordered_array.insert(0))  # 输出: [0, 1, 3, 4, 5, 7]