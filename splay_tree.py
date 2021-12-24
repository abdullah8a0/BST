from tree_obj import BST
import tree_obj



class SplayTree(BST):
    def __init__(self, insert) -> None:
        super().__init__(insert)

    def insert(self, token):
        node = super().insert(token)
        self.splay(node)

    def zigzig(self,node:tree_obj.ParentedBinaryNode,parent:tree_obj.ParentedBinaryNode):
        assert node.parent is parent
        assert parent is not self.root
        if parent.L is node:
            assert parent.parent.L is parent
            A,B,C,D = node.L,node.R,parent.R,parent.parent.R
            # set parents
            tree_obj.ParentedBinaryNode.setparent(B,parent)
            tree_obj.ParentedBinaryNode.setparent(C,parent.parent)
            tree_obj.ParentedBinaryNode.setparent(node,parent.parent.parent)
            tree_obj.ParentedBinaryNode.setparent(parent,node)
            tree_obj.ParentedBinaryNode.setparent(parent.parent,parent)

            # set children
            parent.L = B
            parent.parent.L =C
            if node.parent is tree_obj.Cap:
                self.root = node
            if node.parent.L == parent.parent:
                node.parent.L = node
            if node.parent.R == parent.parent:
                node.parent.R = node

            node.R = parent
            parent.R = parent.parent

        else:
            assert parent.parent.R is parent
            A,B,C,D = node.R,node.L,parent.L,parent.parent.L
            # set parents
            tree_obj.ParentedBinaryNode.setparent(B,parent)
            tree_obj.ParentedBinaryNode.setparent(C,parent.parent)
            tree_obj.ParentedBinaryNode.setparent(node,parent.parent.parent)
            tree_obj.ParentedBinaryNode.setparent(parent,node)
            tree_obj.ParentedBinaryNode.setparent(parent.parent,parent)

            # set children
            parent.R = B
            parent.parent.R =C
            if node.parent is tree_obj.Cap:
                self.root = node
            if node.parent.R == parent.parent:
                node.parent.R = node
            if node.parent.L == parent.parent:
                node.parent.L = node

            node.L = parent
            parent.L = parent.parent
            pass

    def zigzag(self,node:tree_obj.ParentedBinaryNode,parent:tree_obj.ParentedBinaryNode):
        assert node.parent is parent
        pass

    def splay(self,node):
        pass

if __name__ == '__main__':
    vals = [1,2,4,3,5,6,7]
    tree = SplayTree(list(zip(vals,vals)))
    tree.draw()