from treelib import Tree

# 创建树
tree = Tree()

# 创建根节点
tree.create_node("Root", "root")  # 参数：tag, identifier

# 添加子节点
tree.create_node("Child1", "child1", parent="root")  # 参数：tag, identifier, parent
tree.create_node("Child2", "child2", parent="root")
tree.create_node("Grandchild1", "grandchild1", parent="child1")

# 显示树结构
print("\n显示整棵树:")
tree.show()

# 获取节点
node = tree.get_node("child1")
print("\n获取节点信息:", node.tag, node.identifier)

# 修改节点标签
tree.get_node("child1").tag = "Updated Child1"
print("\n修改节点后的树:")
tree.show()

# 删除节点
tree.remove_node("child2")
print("\n删除节点后的树:")
tree.show()

# 其他常用方法
print("\n树的深度:", tree.depth())
print("节点总数:", len(tree))
print("所有节点:", tree.all_nodes())
print("根节点:", tree.root)
print("child1的子节点:", tree.children("child1"))
print("child1的父节点:", tree.parent("child1").tag)
print("是否为叶子节点:", tree.get_node("grandchild1").is_leaf())
