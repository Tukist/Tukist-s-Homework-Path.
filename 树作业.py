# #其还原为链表结构的二叉树
# class TreeNode:
#     def __init__(self,val=0):
#         self.val = val
#         self.left = None
#         self.right = None

# tree = [10,5,15,3,7,None,20]
# tree=TreeNode(10)
# tree.left=TreeNode(5)
# tree.right=TreeNode(15)
# tree.left.left=TreeNode(3)
# tree.left.right=TreeNode(7)
# tree.right.right=TreeNode(20)



#         10
#       /  \
#      5    15
#     / \     \
#    3   7     20

# class TreeNode:
#     def __init__(self, val=0):
#         self.val = val
#         self.left = None
#         self.right = None

# def build(tree_list):
#     if not tree_list or tree_list[0] is None:
#         return None
#     root = TreeNode(tree_list[0])
#     queue = [root]
#     i = 1
#     while queue and i < len(tree_list):
#         current = queue.pop(0)

#         # 处理左子节点
#         if i < len(tree_list) and tree_list[i] is not None:
#             current.left = TreeNode(tree_list[i])
#             queue.append(current.left)
#         i += 1

#         # 处理右子节点
#         if i < len(tree_list) and tree_list[i] is not None:
#             current.right = TreeNode(tree_list[i])
#             queue.append(current.right)
#         i += 1

#     return root

# # 测试
# tree = [10, 5, 15, 3, 7, None, 20]
# root = build(tree)

# # 验证构建的树结构（前序遍历）
# def preorder(root):
#     return [root.val] + preorder(root.left) + preorder(root.right) if root else []

# print(preorder(root))  # 输出: [10, 5, 3, 7, 15, 20]

# ######################################################

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None
    
    # 插入节点（构建BST用）
    def insert(self, val):
        def _insert(node, val):
            if not node:
                return TreeNode(val)
            if val < node.val:
                node.left = _insert(node.left, val)
            else:
                node.right = _insert(node.right, val)
            return node
        self.root = _insert(self.root, val)
    
    # 找中序前驱：左子树的最右节点（左子树最大值）
    def _get_predecessor(self, node):
        node = node.left
        while node.right:
            node = node.right
        return node
    
    # 找中序后继：右子树的最左节点（右子树最小值）
    def _get_successor(self, node):
        node = node.right
        while node.left:
            node = node.left
        return node
    
    # 中序前驱策略删除节点
    def delete_predecessor(self, target_val):
        def _delete(node, val):
            if not node:
                return None
            if val < node.val:
                node.left = _delete(node.left, val)
            elif val > node.val:
                node.right = _delete(node.right, val)
            else:
                # 情况1：只有一个/0个孩子，直接替换
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                # 情况2：两个孩子都有，用前驱替换
                predecessor = self._get_predecessor(node)
                node.val = predecessor.val
                node.left = _delete(node.left, predecessor.val)
            return node
        self.root = _delete(self.root, target_val)
    
    # 中序后继策略删除节点
    def delete_successor(self, target_val):
        def _delete(node, val):
            if not node:
                return None
            if val < node.val:
                node.left = _delete(node.left, val)
            elif val > node.val:
                node.right = _delete(node.right, val)
            else:
                # 情况1：只有一个/0个孩子，直接替换
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                # 情况2：两个孩子都有，用后继替换
                successor = self._get_successor(node)
                node.val = successor.val
                node.right = _delete(node.right, successor.val)
            return node
        self.root = _delete(self.root, target_val)
    
    # 中序遍历（验证BST性质，结果应为升序）
    def in_order(self):
        res = []
        def _traverse(node):
            if node:
                _traverse(node.left)
                res.append(node.val)
                _traverse(node.right)
        _traverse(self.root)
        return res
    
    # 层序遍历（打印树结构，保留None方便看结构）
    def level_order(self):
        if not self.root:
            return []
        res = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node:
                res.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                res.append(None)
        # 清除末尾多余的None
        while res and res[-1] is None:
            res.pop()
        return res

# ------------------- 题目测试 -------------------
# 题1：构建目标BST
def build_original_bst():
    bst = BST()
    seq = [50, 30, 70, 20, 40, 60, 80]
    for num in seq:
        bst.insert(num)
    return bst

print("===== 题1：初始构建完成的BST =====")
original_bst = build_original_bst()
print("层序结构：", original_bst.level_order())
print("中序遍历：", original_bst.in_order(), "\n")

# 题2 策略1：中序前驱删除根50
print("===== 策略1：中序前驱删除根50 =====")
bst1 = build_original_bst()
bst1.delete_predecessor(50)
print("层序结构：", bst1.level_order())
print("中序遍历：", bst1.in_order(), "\n")

# 题2 策略2：中序后继删除根50
print("===== 策略2：中序后继删除根50 =====")
bst2 = build_original_bst()
bst2.delete_successor(50)
print("层序结构：", bst2.level_order())
print("中序遍历：", bst2.in_order())