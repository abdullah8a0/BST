from typing import List
from tree_obj import BST, Cap,ParentedBinaryNode
import tree_obj



class SplayTree(BST):
    def __init__(self, insert) -> None:
        
        self.nodetype = ParentedBinaryNode
        self.root = ParentedBinaryNode(insert[0])

        self.root.parent = Cap()
        for val in insert[1:]:
            self.insert(val)

    def insert(self, token):
        node,path = super().insert(token,return_path=True)
        self.splay(node,path)

    def delete(self, key):
        node, path = super().delete(key,return_path=True)
        self.splay(node,path)
    def find(self,key):
        node,path = super().find(key,return_path=True)
        self.splay(node,path)

    def zigzig(self,node:tree_obj.ParentedBinaryNode):
        """
        Performs the zigzig splay, the node is assumed to be in the right format
        """
        parent = node.parent
        assert parent is not self.root
        flagL = not isinstance(parent.parent.parent, Cap) and parent.parent.parent.L is parent.parent
        if parent.L is node:
            assert parent.parent.L is parent
            B,C = node.R,parent.R
            parent = node.parent
            gparent = parent.parent
            invnode = gparent.parent
            gparent.setl(C)
            parent.setr(gparent)
            parent.setl(B)
            node.setr(parent)

            node.setparent(invnode)
            if isinstance(invnode ,Cap):
                self.root = node
                return
            if flagL:
                invnode.setl(node)
            else:
                invnode.setr(node)
        else:
            assert parent.parent.R is parent
            B,C = node.L,parent.L
            parent = node.parent
            gparent = parent.parent
            invnode = gparent.parent
            gparent.setr(C)
            parent.setl(gparent)
            parent.setr(B)
            node.setl(parent)

            node.setparent(invnode)
            if isinstance(invnode ,Cap):
                self.root = node
                return
            if flagL:
                invnode.setl(node)
            else:
                invnode.setr(node)

    def zigzag(self,node:tree_obj.ParentedBinaryNode):
        """
        Performs the zigzag splay, the node is assumed to be in the right format
        """
        parent = node.parent
        assert parent is not self.root
        flagL = not isinstance(parent.parent.parent, Cap) and parent.parent.parent.L is parent.parent
        if parent.L is node:
            B,C = node.R,node.L
            gparent = parent.parent
            invnode = gparent.parent
            gparent.setr(C)
            parent.setl(B)
            node.setr(parent)
            node.setl(gparent)

            node.setparent(invnode)
            if isinstance(invnode ,Cap):
                self.root = node
                return
            if flagL:
                invnode.setl(node)
            else:
                invnode.setr(node)
        else:
            B,C = node.L,node.R
            gparent = parent.parent
            invnode = gparent.parent
            gparent.setl(C)
            parent.setr(B)
            node.setl(parent)
            node.setr(gparent)

            node.setparent(invnode)
            if isinstance(invnode ,Cap):
                self.root = node
                return
            if flagL:
                invnode.setl(node)
            else:
                invnode.setr(node)
    def splay(self,node,path:List):
        while len(path)>1:
            a = path.pop()
            b = path.pop()
            if a==b:
                self.zigzig(node)
            else:
                self.zigzag(node)
        
        if path:
            if path[0] == 'L':
                self.rotateR(node.parent)
            else:
                self.rotateL(node.parent)


if __name__ == '__main__':
    vals = [1,2,3,4,5]
    tree = SplayTree(list(zip(vals,vals)))
    tree.draw()
    tree.find(3)
    tree.draw()
    tree.find(4)
    tree.draw()
    tree.find(1)
    tree.draw()
    #node = tree.find(1)
    #tree.zigzig(node)
    #tree.draw()