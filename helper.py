def get_node_using_name(node_lst, name: str):
    for node in node_lst:
        if node.name == name:
            return node