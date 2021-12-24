from tree_obj import ParentedBinaryNode,ParentTree,Cap,BST
from typing import Any, List





class AVLNode(ParentedBinaryNode):
    def __init__(self, info, *args) -> None:
        super().__init__(info, *args)
        self.reeval()
        
    def setl(self, node):
        if isinstance(node, Cap):
            if not isinstance(self.R,Cap):
                self.height = self.R.height + 1
                self.bf = self.R.height
            else:
                self.height = 0
                self.bf = 0
            self.L = node
        else:
            node : AVLNode
            if not isinstance(self.R,Cap):
                self.height = max(node.height,self.R.height) +1
                self.bf = self.R.height - node.height
            else:
                self.height = node.height +1
                self.bf = - node.height
                node.parent = self
            self.L = node
    def setr(self, node):
        if isinstance(node, Cap):
            if not isinstance(self.L,Cap):
                self.height = self.L.height + 1
                self.bf = -self.L.height
            else:
                self.height = 0
                self.bf = 0
            self.R = node
        else:
            node : AVLNode
            if not isinstance(self.L,Cap):
                self.height = max(node.height,self.L.height) +1
                self.bf = -(self.L.height - node.height)
            else:
                self.height = node.height +1
                self.bf = - node.height
                node.parent = self
            self.R = node
    def reeval(self):
        if isinstance(self.R,AVLNode) and isinstance(self.L,AVLNode):  
            self.R:AVLNode
            self.L:AVLNode               
            self.height = max(self.R.height, self.L.height)+1
            self.bf = self.R.height - self.L.height
            self.R.parent = self
            self.L.parent = self
        elif isinstance(self.R,AVLNode) and isinstance(self.L,Cap): 
            self.R:AVLNode
            self.height = self.R.height+1
            self.bf = self.R.height
            self.R.parent = self
        elif isinstance(self.R,Cap) and isinstance(self.L,AVLNode):                 
            self.L:AVLNode               
            self.height = self.L.height +1
            self.bf = -self.L.height
            self.L.parent = self
        elif isinstance(self.R,Cap) and isinstance(self.L,Cap):                 
            self.height = 1
            self.bf = 0
        else:
            raise TypeError("AVLNode's children can only be AVLNode or Cap")

       
    
class AVL(BST):
    def __init__(self, nodes_val) -> None:
        self.root : AVLNode = AVLNode(nodes_val[0])
        for val in nodes_val[1:]:
            self.insert(val)
        self.nodetype = AVLNode
    def insert(self,val):
        
        pass
    def delete(self,val):
        pass
    def rotate(self,node:AVLNode):

        node.reeval() 


if __name__ == "__main__":
    vals = [1,6,7,3,5,2,4]
    vals.reverse()
    tree = BST(list(zip(vals,vals)))
    tree.draw()