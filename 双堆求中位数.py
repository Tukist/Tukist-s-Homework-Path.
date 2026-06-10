"""
addNum：O(log n)，瓶颈在于堆的插入和弹出
findMedian：O(1)，直接读堆顶
# ===================== 时间复杂度总结 =====================
#
#  操作          | 时间复杂度 | 说明
#  --------------|-----------|-------------------------------
#  addNum(num)   | O(log n)  | 最多 5 次堆操作，每次 O(log n)
#  findMedian()  | O(1)      | 直接读堆顶，无堆结构调整
#  空间           | O(n)      | 两个堆各存约 n/2 个元素
#
#  ┌─────────────────────────────────────────────────┐
#  │              与其他方案对比                       │
#  ├──────────────┬────────────┬────────────┬─────────┤
#  │ 方案          │ addNum     │ findMedian │ 空间    │
#  ├──────────────┼────────────┼────────────┼─────────┤
#  │ 无序数组+排序 │ O(n log n) │ O(1)       │ O(n)    │
#  │ 有序数组+二分 │ O(n)       │ O(1)       │ O(n)    │
#  │ 平衡 BST     │ O(log n)   │ O(log n)   │ O(n)    │
#  │ 双堆（本方案）│ O(log n)   │ O(1)       │ O(n)    │
#  └──────────────┴────────────┴────────────┴─────────┘
#
#  结论: 双堆在「频繁查询中位数」的场景下是最优选择 ——
#  写入和查询都达到渐近最优，且实现简洁。
#  addNum 的 O(log n) 下界由比较排序的 Ω(log n) 决定，
#  双堆已经达到了理论最优平衡。
"""



def shift_up(arr, i):
    while i > 0:
        p = (i - 1) // 2
        if arr[p] >= arr[i]:
            break
        arr[p], arr[i] = arr[i], arr[p]
        i = p
def shift_down(arr, n, i):
    while 2*i + 1 < n:
        l = 2*i + 1
        r = 2*i + 2
        mx = l
        if r < n and arr[r] > arr[l]:
            mx = r
        if arr[mx] <= arr[i]:
            break
        arr[mx], arr[i] = arr[i], arr[mx]
        i = mx

"""设计一个数据结构 MedianFinder，支持两个操作：
addNum(num)：添加一个整数
findMedian()：返回当前所有数字的中位数"""

class MedianFinder:
    def __init__(self):
        self.small = []  # 大顶堆，存较小的一半
        self.large = []  # 小顶堆，存较大的一半

    def addNum(self, num: int) -> None:
        if not self.small or num <= self.small[0]:
            self.small.append(num)
            shift_up(self.small, len(self.small) - 1)
        else:
            self.large.append(num)
            shift_up(self.large, len(self.large) - 1)

        # 平衡两个堆的大小
        if len(self.small) > len(self.large) + 1:
            val = self.small[0]
            self.small[0] = self.small[-1]
            self.small.pop()
            shift_down(self.small, len(self.small), 0)
            self.large.append(val)
            shift_up(self.large, len(self.large) - 1)
        elif len(self.large) > len(self.small):
            val = self.large[0]
            self.large[0] = self.large[-1]
            self.large.pop()
            shift_down(self.large, len(self.large), 0)
            self.small.append(-val)
            shift_up(self.small, len(self.small) - 1)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(self.small[0])
        return (self.small[0] + self.large[0]) / 2.0

mf = MedianFinder()
mf.addNum(3)
print(mf.findMedian())  # 输出 3.0
mf.addNum(1)
print(mf.findMedian())  # 输出 2.0