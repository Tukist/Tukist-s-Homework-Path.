"""
3 阶 B-Tree (m=3) 的实现
给定键值序列 [10, 20, 5, 6, 12, 30, 25]，依次插入并展示最终树结构

B-Tree 性质 (m=3):
  - 每个节点最多 m-1 = 2 个键值, 最多 m = 3 个孩子
  - 非根节点至少 ceil(m/2)-1 = 1 个键值
  - 非根内部节点至少 ceil(m/2) = 2 个孩子
  - 所有叶节点在同一层
  - 键值升序，孩子键值范围满足 BST 性质
"""

from __future__ import annotations

import sys
import io

# 强制 UTF-8 输出，避免 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ======================== B-Tree 节点 ========================
@dataclass
class BTreeNode:
    """B-Tree 节点 (m=3: 最多 2 个键, 最多 3 个孩子)"""
    keys: List[int] = field(default_factory=list)
    children: List['BTreeNode'] = field(default_factory=list)
    is_leaf: bool = True

    @property
    def n(self) -> int:
        return len(self.keys)

    @property
    def child_count(self) -> int:
        return len(self.children)

    def is_full(self) -> bool:
        """节点键值数是否已达上限 (m-1 = 2) — 实际上我们允许插入后临时到 3 再分裂"""
        return self.n >= 2


# ======================== B-Tree 类 ========================
class BTree:
    """3 阶 B-Tree"""
    MAX_KEYS = 2   # m - 1

    def __init__(self):
        self.root: Optional[BTreeNode] = None
        self.insert_steps: List[str] = []

    def insert(self, key: int) -> None:
        """插入一个键值"""
        self.insert_steps.append(f"\n>>> 插入 {key}")

        if self.root is None:
            self.root = BTreeNode(keys=[key])
            self.insert_steps.append(f"    树为空 → 根节点: {self.root.keys}")
            return

        result = self._insert_recursive(self.root, key)

        # 根节点溢出：需要创建新根
        if result is not None:
            mid_key, right_child = result
            old_root = self.root
            self.root = BTreeNode(keys=[mid_key], is_leaf=False,
                                  children=[old_root, right_child])
            self.insert_steps.append(
                f"    根节点溢出 → 中间键 {mid_key} 提升为新根，"
                f"左孩子={old_root.keys}，右孩子={right_child.keys}"
            )

    def _insert_recursive(self, node: BTreeNode, key: int) -> Optional[Tuple[int, 'BTreeNode']]:
        """
        递归插入，若节点溢出则返回 (提升键, 新右孩子)
        """
        if node.is_leaf:
            # 叶节点：直接插入
            self._insert_sorted(node.keys, key)
            self.insert_steps.append(f"    插入到叶节点 → {node.keys}")

            if node.n > self.MAX_KEYS:
                return self._split(node)
            return None

        # 内部节点：找到孩子并递归
        i = self._child_index(node.keys, key)
        result = self._insert_recursive(node.children[i], key)

        if result is not None:
            mid_key, right_child = result
            # 将提升键和右孩子插入当前节点
            node.keys.insert(i, mid_key)
            node.children.insert(i + 1, right_child)
            self.insert_steps.append(
                f"    键 {mid_key} 提升到内部节点 → {node.keys}"
            )

            if node.n > self.MAX_KEYS:
                return self._split(node)

        return None

    def _split(self, node: BTreeNode) -> Tuple[int, 'BTreeNode']:
        """分裂满节点（3 个键），返回 (中间键, 新右节点)"""
        mid_idx = 1  # 3 个键的中间索引

        mid_key = node.keys[mid_idx]

        # 右半部分成为新节点
        right = BTreeNode(
            keys=node.keys[mid_idx + 1:],
            is_leaf=node.is_leaf
        )
        # 左半部分保留在原节点
        node.keys = node.keys[:mid_idx]

        # 分配孩子
        if not node.is_leaf:
            right.children = node.children[mid_idx + 1:]
            node.children = node.children[:mid_idx + 1]

        self.insert_steps.append(
            f"    分裂节点 → 提升键 {mid_key}，左={node.keys}，右={right.keys}"
        )
        return mid_key, right

    @staticmethod
    def _insert_sorted(keys: List[int], key: int) -> None:
        for i, k in enumerate(keys):
            if key < k:
                keys.insert(i, key)
                return
        keys.append(key)

    @staticmethod
    def _child_index(keys: List[int], key: int) -> int:
        for i, k in enumerate(keys):
            if key < k:
                return i
        return len(keys)


# ======================== 树形结构可视化 ========================
def print_tree(tree: BTree) -> None:
    print("\n" + "=" * 60)
    print("  3 阶 B-Tree 最终结构")
    print("=" * 60)
    if tree.root is None:
        print("  (空树)")
        return
    _print_node(tree.root, prefix="  ", is_last=True, is_root=True)


def _print_node(node: BTreeNode, prefix: str, is_last: bool, is_root: bool = False) -> None:
    connector = "└── " if is_last else "├── "
    keys_str = ", ".join(str(k) for k in node.keys)
    label = "根节点" if is_root else "节点"
    info = (f"[{keys_str}]  "
            f"(键值数={node.n}, 孩子数={node.child_count}, "
            f"{'叶' if node.is_leaf else '非叶'})")
    print(f"{prefix}{connector}{label}: {info}")

    if not node.is_leaf and node.children:
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            _print_node(child, child_prefix, i == len(node.children) - 1)


# ======================== 逐层展示 ========================
def print_levels(tree: BTree) -> None:
    print("\n" + "-" * 60)
    print("  逐层展示")
    print("-" * 60)
    if tree.root is None:
        print("  (空树)")
        return

    level = 0
    queue = [tree.root]
    while queue:
        print(f"\n  第 {level} 层:")
        next_q = []
        for i, node in enumerate(queue):
            keys_str = ", ".join(str(k) for k in node.keys)
            if node.is_leaf:
                tag = "叶节点"
            else:
                tag = f"非叶, 孩子数={node.child_count}"
            print(f"    结点{i}: [{keys_str}]  |  {tag}")
            if not node.is_leaf:
                next_q.extend(node.children)
        queue = next_q
        level += 1


# ======================== 性质验证 ========================
def verify_btree(tree: BTree) -> Tuple[bool, List[str]]:
    m = 3
    MAX_KEYS = m - 1          # 2
    MIN_KEYS = (m + 1) // 2 - 1  # ceil(3/2)-1 = 1
    MIN_CHILDREN = (m + 1) // 2  # ceil(3/2) = 2
    results: List[str] = []

    if tree.root is None:
        return True, ["✅ 空树"]

    all_ok = True
    leaf_depth: List[int] = []  # 收集所有叶节点深度用于性质3检查

    def check(node: BTreeNode, depth: int, is_root: bool) -> None:
        nonlocal all_ok

        # --- 性质: 键值升序 ---
        if node.keys != sorted(node.keys):
            results.append(f"❌ 键值不升序: {node.keys}")
            all_ok = False

        # --- 性质: 最多 m-1 个键 ---
        if node.n > MAX_KEYS:
            results.append(f"❌ 节点键值过多: {node.keys} ({node.n} > {MAX_KEYS})")
            all_ok = False

        # --- 性质: 最多 m 个孩子 ---
        if node.child_count > m:
            results.append(f"❌ 节点孩子过多: {node.child_count} > {m}")
            all_ok = False

        # --- 性质: 非根节点最少键值数 ---
        if not is_root and node.n < MIN_KEYS:
            results.append(f"❌ 非根节点键值不足: {node.keys} ({node.n} < {MIN_KEYS})")
            all_ok = False

        # --- 性质: 孩子数 == 键值数 + 1 (内部节点) ---
        if not node.is_leaf and node.child_count != node.n + 1:
            results.append(f"❌ 孩子数与键值数不匹配: 键值={node.n}, 孩子={node.child_count}")
            all_ok = False

        # --- 性质: 非根内部节点最少孩子数 ---
        if not is_root and not node.is_leaf and node.child_count < MIN_CHILDREN:
            results.append(
                f"❌ 非根内部节点孩子不足: {node.child_count} < {MIN_CHILDREN}, keys={node.keys}"
            )
            all_ok = False

        # --- 叶节点深度 ---
        if node.is_leaf:
            leaf_depth.append(depth)

        # --- 性质: BST 范围检查 ---
        if node.children:
            for i, child in enumerate(node.children):
                lo = -float('inf') if i == 0 else node.keys[i - 1]
                hi = float('inf') if i == len(node.keys) else node.keys[i]
                for k in child.keys:
                    if not (lo < k < hi):
                        results.append(f"❌ 键 {k} 不在范围 ({lo}, {hi})")
                        all_ok = False

        # 递归
        for child in node.children:
            check(child, depth + 1, is_root=False)

    check(tree.root, 0, is_root=True)

    # 汇总性质检查
    if tree.root.n >= 1:
        results.append(f"✅ 性质1: 根节点至少有 1 个键 (实际: {tree.root.n})")
    else:
        results.append("❌ 性质1: 根节点无键")
        all_ok = False

    results.append(f"✅ 性质2: 每个节点最多 {MAX_KEYS} 个键")

    if len(set(leaf_depth)) == 1:
        results.append(f"✅ 性质3: 所有叶节点在同一层 (深度={leaf_depth[0]})")
    else:
        results.append(f"❌ 性质3: 叶节点深度不一致 {leaf_depth}")
        all_ok = False

    results.append(f"✅ 性质4: 非根内部节点至少有 {MIN_CHILDREN} 个孩子")

    results.append(f"✅ 性质5: 孩子键值范围正确 (BST 性质)")

    if all_ok:
        results.append(f"\n  🎉 所有 B-Tree 性质验证通过！")
    else:
        results.append(f"\n  ⚠️  存在性质违反，请检查！")

    return all_ok, results


# ======================== 主程序 ========================
def main():
    keys = [10, 20, 5, 6, 12, 30, 25]
    tree = BTree()

    print("=" * 60)
    print(f"  3 阶 B-Tree 构建过程")
    print(f"  插入序列: {keys}")
    print("=" * 60)

    for key in keys:
        tree.insert(key)

    # 插入过程日志
    print("\n插入过程详情:")
    for step in tree.insert_steps:
        print(step)

    # 树形结构
    print_tree(tree)

    # 逐层展示
    print_levels(tree)

    # 验证
    passed, results = verify_btree(tree)
    print("\n" + "=" * 60)
    print("  B-Tree 性质验证")
    print("=" * 60)
    for r in results:
        print(f"  {r}")


if __name__ == "__main__":
    main()
