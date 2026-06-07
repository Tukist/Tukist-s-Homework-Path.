"""
AVL 树构建与旋转实操
插入序列：[30, 20, 10, 25, 40, 35, 50]
每步输出：树形 → 平衡因子 → 失衡类型 & 旋转 → 旋转后树形
最终中序遍历验证 BST 性质
"""

from typing import Optional, List, Tuple


class AVLNode:
    """AVL 树结点"""
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1  # 叶结点高度为 1


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    # ---------- 基础工具 ----------
    @staticmethod
    def get_height(node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    @staticmethod
    def get_balance(node: Optional[AVLNode]) -> int:
        """平衡因子 = 左子树高度 - 右子树高度"""
        if not node:
            return 0
        return AVLTree.get_height(node.left) - AVLTree.get_height(node.right)

    # ---------- 旋转 ----------
    def rotate_right(self, y: AVLNode) -> AVLNode:
        """右旋（LL 型）"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        # 更新高度
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """左旋（RR 型）"""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # ---------- 插入（递归） ----------
    def _insert(self, node: Optional[AVLNode], val: int) -> Tuple[AVLNode, str]:
        """
        递归插入，返回 (新子树根, 旋转描述)
        """
        # 1. 标准 BST 插入
        if node is None:
            return AVLNode(val), ""

        rotation_info = ""

        if val < node.val:
            node.left, rotation_info = self._insert(node.left, val)
        elif val > node.val:
            node.right, rotation_info = self._insert(node.right, val)
        else:
            return node, ""  # 不允许重复

        # 2. 更新高度
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        # 3. 检查平衡因子
        balance = self.get_balance(node)

        # LL 型：左子树过高，且插入在左子树的左子树
        if balance > 1 and val < node.left.val:
            rotation_info = (
                f"[!] 失衡类型：LL 型\n"
                f"   失衡结点：{node.val}（平衡因子={balance}）\n"
                f"   旋转轴：{node.val}（右旋）"
            )
            return self.rotate_right(node), rotation_info

        # RR 型：右子树过高，且插入在右子树的右子树
        if balance < -1 and val > node.right.val:
            rotation_info = (
                f"[!] 失衡类型：RR 型\n"
                f"   失衡结点：{node.val}（平衡因子={balance}）\n"
                f"   旋转轴：{node.val}（左旋）"
            )
            return self.rotate_left(node), rotation_info

        # LR 型：左子树过高，但插入在左子树的右子树
        if balance > 1 and val > node.left.val:
            rotation_info = (
                f"[!] 失衡类型：LR 型\n"
                f"   失衡结点：{node.val}（平衡因子={balance}）\n"
                f"   旋转轴：先对 {node.left.val} 左旋，再对 {node.val} 右旋"
            )
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node), rotation_info

        # RL 型：右子树过高，但插入在右子树的左子树
        if balance < -1 and val < node.right.val:
            rotation_info = (
                f"[!] 失衡类型：RL 型\n"
                f"   失衡结点：{node.val}（平衡因子={balance}）\n"
                f"   旋转轴：先对 {node.right.val} 右旋，再对 {node.val} 左旋"
            )
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node), rotation_info

        return node, rotation_info

    def insert(self, val: int) -> str:
        """对外插入接口，返回旋转描述"""
        self.root, info = self._insert(self.root, val)
        return info

    # ---------- 遍历 ----------
    def inorder(self) -> List[int]:
        """中序遍历（验证 BST 性质）"""
        result = []
        def dfs(node):
            if node:
                dfs(node.left)
                result.append(node.val)
                dfs(node.right)
        dfs(self.root)
        return result


# ===================== 可视化 =====================

def print_tree(root: Optional[AVLNode], title: str = ""):
    """
    用缩进 + 连线风格打印 AVL 树，并在每个结点后标注平衡因子。
    示例输出：
         30(bf=0)
        /      \
     20(bf=0)  40(bf=-1)
    """
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")

    if root is None:
        print("  (空树)")
        return

    def _collect(node, depth, pos, lines, width):
        """递归收集结点信息"""
        if node is None:
            return
        bf = AVLTree.get_balance(node)
        label = f"{node.val}(bf={bf})"

        # 把 label 放到 lines[depth] 的合适位置
        while len(lines) <= depth:
            lines.append("")
        current = lines[depth]
        # 补空格到 pos
        if len(current) < pos:
            current += " " * (pos - len(current))
        current += label
        lines[depth] = current

        # 递归左右子树
        offset = max(3, len(label) + 1)
        _collect(node.left, depth + 1, pos - offset // 2, lines, width // 2)
        _collect(node.right, depth + 1, pos + offset // 2, lines, width // 2)

    lines = [""] * 8  # 最多 8 层
    _collect(root, 0, 40, lines, 80)

    for line in lines:
        if line.strip():
            print(f"  {line}")


def print_compact(root: Optional[AVLNode]):
    """
    更直观的树形打印（使用 unicode 连线字符）
    """
    if root is None:
        print("  (空树)")
        return

    def _build_lines(node) -> List[str]:
        """递归构建显示行"""
        if node is None:
            return []

        bf = AVLTree.get_balance(node)
        label = f"{node.val}(bf={bf})"

        left_lines = _build_lines(node.left)
        right_lines = _build_lines(node.right)

        # 补齐行数
        while len(left_lines) < len(right_lines):
            left_lines.append(" " * len(left_lines[0]) if left_lines else "")
        while len(right_lines) < len(left_lines):
            right_lines.append(" " * len(right_lines[0]) if right_lines else "")

        # 合并
        if not left_lines and not right_lines:
            return [label]

        # 计算宽度
        left_width = len(left_lines[0]) if left_lines else 0
        right_width = len(right_lines[0]) if right_lines else 0

        # 第 0 行：结点本身
        padding = " " * (len(label) + 2)
        left_pad = " " * (left_width // 2) if left_width else ""
        right_pad = " " * (right_width // 2) if right_width else ""

        top_line = ""
        if left_lines:
            top_line += " " * (left_width - 1) + "┌" + "─" * (len(label))
        else:
            top_line += " " * left_width

        top_line += label

        if right_lines:
            top_line += "─" * (len(label)) + "┐"
        else:
            top_line += " " * right_width

        # 缩进对齐
        mid_gap = (len(top_line) - left_width - len(label) - right_width)
        if left_lines and right_lines:
            # 有左右子树时，连线从 label 两侧出发
            pass

        result = [top_line]

        # 后续行：左右子树的行拼接
        for i in range(max(len(left_lines), len(right_lines))):
            l = left_lines[i] if i < len(left_lines) else " " * left_width
            r = right_lines[i] if i < len(right_lines) else " " * right_width
            result.append(l + padding + r)

        return result

    lines = _build_lines(root)
    for line in lines:
        print(f"  {line}")


# ===================== 主流程 =====================

def demo():
    values = [30, 20, 10, 25, 40, 35, 50]
    tree = AVLTree()

    print("╔══════════════════════════════════════════════════════╗")
    print("║     AVL 树构建与旋转实操                              ║")
    print("║     插入序列：[30, 20, 10, 25, 40, 35, 50]           ║")
    print("╚══════════════════════════════════════════════════════╝")

    for i, v in enumerate(values, 1):
        print(f"\n{'─' * 60}")
        print(f"  >>> 第 {i} 步：插入 {v}")

        # 插入前的树
        if i == 1:
            print(f"\n  插入前：空树")
        else:
            print(f"\n  插入前：")
            print_compact(tree.root)

        # 执行插入
        rotation_info = tree.insert(v)

        # 判断是否有旋转
        if rotation_info:
            print(f"\n  {rotation_info}")
            print(f"\n  旋转后：")
            print_compact(tree.root)
        else:
            print(f"\n  [OK] 插入后保持平衡，无需旋转：")
            print_compact(tree.root)

    # 最终结果
    print(f"\n{'=' * 60}")
    print(f"  最终 AVL 树")
    print(f"{'=' * 60}")
    print_compact(tree.root)

    # 中序遍历
    inorder_result = tree.inorder()
    print(f"\n{'=' * 60}")
    print(f"  中序遍历结果")
    print(f"{'=' * 60}")
    print(f"  {' → '.join(str(x) for x in inorder_result)}")

    # 验证 BST 性质
    is_sorted = inorder_result == sorted(inorder_result)
    is_complete = set(inorder_result) == set(values)
    print(f"\n  [OK] BST 性质验证：{'通过' if is_sorted else 'X 失败'}")
    print(f"     中序有序？{'是' if is_sorted else '否'}")
    print(f"     包含全部插入值？{'是' if is_complete else '否'}")

    # 平衡因子全面检查
    print(f"\n{'=' * 60}")
    print(f"  各结点平衡因子检查")
    print(f"{'=' * 60}")

    def check_all_balanced(node, depth=0):
        if node is None:
            return True
        bf = AVLTree.get_balance(node)
        indent = "  " * depth
        status = "[OK]" if abs(bf) <= 1 else "[X] 失衡!"
        print(f"  {indent}{node.val}: bf={bf} {status}")
        left_ok = check_all_balanced(node.left, depth + 1)
        right_ok = check_all_balanced(node.right, depth + 1)
        return abs(bf) <= 1 and left_ok and right_ok

    all_ok = check_all_balanced(tree.root)
    print(f"\n  全局平衡检查：{'[OK] 所有结点平衡' if all_ok else '[X] 存在失衡结点'}")


if __name__ == "__main__":
    demo()
