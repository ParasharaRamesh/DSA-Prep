class Node:
    def __init__(self, name):
        self.children = []
        self.name = name

    def addChild(self, name):
        self.children.append(Node(name))
        return self

    def depthFirstSearch(self, array):
        dfs = [self]
        while len(dfs) != 0:
            node = dfs.pop()
            array.append(node.name)
            for child in node.children[::-1]:
                dfs.append(child)
        return array