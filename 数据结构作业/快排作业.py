
# ————————————————————————随机起始点的快速排序实现————————————————————————————————————
from collections.abc import Sequence
import random


class QuickSort:
    """
    快速排序类，包含分区和排序功能。
    """

    def __init__(self, arr: Sequence[int | float]):
        """
        初始化快速排序器。

        :param arr: 待排序的数组，可以是整数或浮点数
        """
        self.arr: list[int | float] = list(arr)
        self.length: int = len(arr)

    def partition(self, left_index: int, right_index: int) -> int:
        pivot_index: int =random(left_index,right_index+1)
        pivot: int | float = self.arr[pivot_index]

        # 右指针从轴的左边开始
        right_pointer: int = right_index
        left_pointer: int = left_index

        while True:
            if left_pointer==pivot_index:
                left_pointer += 1
            if right_pointer==pivot_index:
                right_pointer -= 1
            # 左指针向右移动，直到找到大于或等于轴的值
            while left_pointer <= right_pointer and self.arr[left_pointer] < pivot:
                left_pointer += 1

            # 右指针向左移动，直到找到小于或等于轴的值
            while left_pointer <= right_pointer and self.arr[right_pointer] > pivot:
                right_pointer -= 1

            # 如果左右指针相遇或交叉，停止
            if left_pointer >= right_pointer:
                break

            # 交换左右指针指向的值
            self.arr[left_pointer], self.arr[right_pointer] = (
                self.arr[right_pointer],
                self.arr[left_pointer],
            )

        # 最后将左指针的值与轴交换
        self.arr[left_pointer], self.arr[pivot_index] = (
            self.arr[pivot_index],
            self.arr[left_pointer],
        )

        return left_pointer

    def sort(
        self, left_index: int | None = None, right_index: int | None = None
    ) -> list[int | float]:
        if left_index is None:
            left_index = 0
        if right_index is None:
            right_index = self.length - 1

        # 基准情形：如果子数组长度为0或1，不需要排序
        if right_index - left_index <= 0:
            return self.arr

        """
        长度为0： sort(0, -1)
        长度为1： sort(0, 0)
        长度为2： sort(0, 1)
        """

        # 对当前范围进行分区，获取轴的位置
        pivot_position: int = self.partition(left_index, right_index)

        # 对轴左边的子数组递归排序
        self.sort(left_index, pivot_position - 1)

        # 对轴右边的子数组递归排序
        self.sort(pivot_position + 1, right_index)

        return self.arr
test_arr3: list[int] = [64, 34, 25, 12, 22, 11, 90]
print(f"数组: {test_arr3}")
print(f"排序后参考: {sorted(test_arr3)}")


# ——————————————————————————三路快速排序实现—————————————————————————————————————————

def sanluquicksort_(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]      #python这种用list归类的小玩意写起来就是快。。。
    return sanluquicksort_(left) + middle + sanluquicksort_(right)


# 或者

from collections.abc import Sequence
import random


class QuickSort:
    """
    快速排序类，包含分区和排序功能。
    """

    def __init__(self, arr: Sequence[int | float]):
        """
        初始化快速排序器。

        :param arr: 待排序的数组，可以是整数或浮点数
        """
        self.arr: list[int | float] = list(arr)
        self.length: int = len(arr)

    def partition(self, left_index: int, right_index: int) -> (int, int): # type: ignore
        count=0
        pivot_index: int =random(left_index,right_index+1)
        pivot: int | float = self.arr[pivot_index]

        # 右指针从轴的左边开始
        right_pointer: int = right_index
        left_pointer: int = left_index

        while True:
            if left_pointer==pivot_index:
                left_pointer += 1
            if right_pointer==pivot_index:
                right_pointer -= 1
            if self.arr[left_pointer] == pivot:
                count+=1
            if self.arr[right_pointer] == pivot:
                count+=1
            # 左指针向右移动，直到找到大于或等于轴的值
            while left_pointer <= right_pointer and self.arr[left_pointer] < pivot:
                left_pointer += 1

            # 右指针向左移动，直到找到小于或等于轴的值
            while left_pointer <= right_pointer and self.arr[right_pointer] > pivot:
                right_pointer -= 1

            # 如果左右指针相遇或交叉，停止
            if left_pointer >= right_pointer:
                break

            # 交换左右指针指向的值
            self.arr[left_pointer], self.arr[right_pointer] = (
                self.arr[right_pointer],
                self.arr[left_pointer],
            )

        # 最后将左指针的值与轴交换
        self.arr[left_pointer], self.arr[pivot_index] = (
            self.arr[pivot_index],
            self.arr[left_pointer],
        )

        return (left_pointer,count)

    def sort(
        self, left_index: int | None = None, right_index: int | None = None
    ) -> list[int | float]:
        if left_index is None:
            left_index = 0
        if right_index is None:
            right_index = self.length - 1

        # 基准情形：如果子数组长度为0或1，不需要排序
        if right_index - left_index <= 0:
            return self.arr

        """
        长度为0： sort(0, -1)
        长度为1： sort(0, 0)
        长度为2： sort(0, 1)
        """
        count=0
        # 对当前范围进行分区，获取轴的位置
        pivot_position, count= self.partition(left_index, right_index)

        # 对轴左边的子数组递归排序
        self.sort(left_index, pivot_position - 1)

        # 对轴右边的子数组递归排序
        self.sort(pivot_position + 1+count, right_index)

        return self.arr
    
test_arr3: list[int] = [64, 34, 25, 12, 22, 11, 90,12,11,22,35,35,3,5,3,5,5,3,5,3,35,25,35,35,25,25,64,12]
print(f"数组: {test_arr3}")
print(f"排序后参考: {sorted(test_arr3)}")