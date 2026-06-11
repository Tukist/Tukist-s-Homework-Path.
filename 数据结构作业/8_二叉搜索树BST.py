"""
题 1：构建 BST
从空树开始，依次插入序列 [50, 30, 70, 20, 40, 60, 80]，画出最终 BST。

题 2：删除根结点
删除根结点 50，分别用 "中序前驱" 和 "中序后继" 两种策略，画出结果。
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # ── 插入 ──────────────────────────────
    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = Node(val)
            else:
                self._insert(node.left, val)
        elif val > node.val:
            if node.right is None:
                node.right = Node(val)
            else:
                self._insert(node.right, val)

    def insert_batch(self, vals):
        for v in vals:
            self.insert(v)

    # ── 中序遍历 ──────────────────────────
    def inorder(self):
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.val)
            self._inorder(node.right, res)

    # ── 中序前驱删除 ──────────────────────
    def delete_by_predecessor(self, val):
        self.root = self._del_pred(self.root, val)

    def _del_pred(self, node, val):
        if node is None:
            return None
        if val < node.val:
            node.left = self._del_pred(node.left, val)
        elif val > node.val:
            node.right = self._del_pred(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            pred = self._max(node.left)
            node.val = pred.val
            node.left = self._del_pred(node.left, pred.val)
        return node

    def _max(self, node):
        while node.right:
            node = node.right
        return node

    # ── 中序后继删除 ──────────────────────
    def delete_by_successor(self, val):
        self.root = self._del_succ(self.root, val)

    def _del_succ(self, node, val):
        if node is None:
            return None
        if val < node.val:
            node.left = self._del_succ(node.left, val)
        elif val > node.val:
            node.right = self._del_succ(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = self._min(node.right)
            node.val = succ.val
            node.right = self._del_succ(node.right, succ.val)
        return node

    def _min(self, node):
        while node.left:
            node = node.left
        return node

    # ── 文本树图 ──────────────────────────
    def print_tree(self):
        self._print(self.root, "", True)

    def _print(self, node, prefix, is_tail):
        if node is None:
            return
        has_left = node.left is not None
        has_right = node.right is not None
        # 当前结点
        print(prefix + ("└── " if is_tail else "├── ") + str(node.val))
        # 子结点
        child_prefix = prefix + ("    " if is_tail else "│   ")
        if has_left and has_right:
            self._print(node.left, child_prefix, False)
            self._print(node.right, child_prefix, True)
        elif has_left:
            self._print(node.left, child_prefix, True)
        elif has_right:
            self._print(node.right, child_prefix, True)


# ══════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════
# ── 零依赖 SVG 图像生成 ─────────────────
def tree_to_svg(bst, title, x0, y0):
    """返回一棵树的 SVG 字符串，锚点在 (x0, y0)"""
    if bst.root is None:
        return ""

    def height(node):
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    h = height(bst.root)
    positions = {}

    def assign(node, x, y, dx):
        if node is None:
            return
        positions[id(node)] = (x, y, node.val, node)
        ndx = dx / 2
        assign(node.left, x - dx, y + 1, ndx)
        assign(node.right, x + dx, y + 1, ndx)

    initial_dx = 2 ** (h - 2) if h > 1 else 0.5
    assign(bst.root, 0, 0, initial_dx)

    r = 22       # 圆半径
    dy = 65      # 层间距
    dx = 55      # 水平间距

    lines = []
    # 边
    for nid, (x, y, val, node) in positions.items():
        px, py = x0 + x * dx, y0 + y * dy
        if node.left and id(node.left) in positions:
            cx, cy = positions[id(node.left)][:2]
            cpx, cpy = x0 + cx * dx, y0 + cy * dy
            lines.append(f'<line x1="{px}" y1="{py+r}" x2="{cpx}" y2="{cpy-r}" stroke="#999" stroke-width="2"/>')
        if node.right and id(node.right) in positions:
            cx, cy = positions[id(node.right)][:2]
            cpx, cpy = x0 + cx * dx, y0 + cy * dy
            lines.append(f'<line x1="{px}" y1="{py+r}" x2="{cpx}" y2="{cpy-r}" stroke="#999" stroke-width="2"/>')
    # 结点
    for nid, (x, y, val, node) in positions.items():
        px, py = x0 + x * dx, y0 + y * dy
        lines.append(f'<circle cx="{px}" cy="{py}" r="{r}" fill="#E8F4FD" stroke="#4A90D9" stroke-width="2.5"/>')
        lines.append(f'<text x="{px}" y="{py+5}" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">{val}</text>')

    return "\n".join(lines)


def save_svg(filename):
    seq = [50, 30, 70, 20, 40, 60, 80]
    b1 = BST(); b1.insert_batch(seq)
    b2 = BST(); b2.insert_batch(seq); b2.delete_by_predecessor(50)
    b3 = BST(); b3.insert_batch(seq); b3.delete_by_successor(50)

    w, h = 1080, 400
    col_w = w // 3
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="white"/>
  <text x="{col_w//2}" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">初始 BST</text>
  <text x="{col_w//2}" y="52" text-anchor="middle" font-size="13" fill="#666">[50, 30, 70, 20, 40, 60, 80]</text>
  {tree_to_svg(b1, "", col_w//2, 80)}
  <line x1="{col_w}" y1="20" x2="{col_w}" y2="{h-20}" stroke="#ddd" stroke-width="1"/>
  <text x="{col_w+col_w//2}" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">中序前驱删除 50</text>
  <text x="{col_w+col_w//2}" y="52" text-anchor="middle" font-size="13" fill="#666">前驱 = 40（左子树最大值）</text>
  {tree_to_svg(b2, "", col_w+col_w//2, 80)}
  <line x1="{col_w*2}" y1="20" x2="{col_w*2}" y2="{h-20}" stroke="#ddd" stroke-width="1"/>
  <text x="{col_w*2+col_w//2}" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">中序后继删除 50</text>
  <text x="{col_w*2+col_w//2}" y="52" text-anchor="middle" font-size="13" fill="#666">后继 = 60（右子树最小值）</text>
  {tree_to_svg(b3, "", col_w*2+col_w//2, 80)}
</svg>'''
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"图片已保存: {filename}")


if __name__ == "__main__":
    seq = [50, 30, 70, 20, 40, 60, 80]

    # ── 题 1：构建 BST ──────────────────────
    print("=" * 45)
    print("题 1：构建 BST（插入 " + str(seq) + "）")
    print("=" * 45)
    bst = BST()
    bst.insert_batch(seq)
    bst.print_tree()
    print("中序遍历:", bst.inorder())

    # ── 题 2：中序前驱删除 50 ──────────────
    print("\n" + "=" * 45)
    print("题 2-①：中序前驱删除根结点 50")
    print("  (前驱 = 左子树最大值 = 40)")
    print("=" * 45)
    t1 = BST()
    t1.insert_batch(seq)
    t1.delete_by_predecessor(50)
    t1.print_tree()
    print("中序遍历:", t1.inorder())

    # ── 题 2：中序后继删除 50 ──────────────
    print("\n" + "=" * 45)
    print("题 2-②：中序后继删除根结点 50")
    print("  (后继 = 右子树最小值 = 60)")
    print("=" * 45)
    t2 = BST()
    t2.insert_batch(seq)
    t2.delete_by_successor(50)
    t2.print_tree()
    print("中序遍历:", t2.inorder())

    # ── 生成 SVG 图片 ─────────────────────
    print("\n" + "=" * 45)
    save_svg("8_二叉搜索树BST.svg")
