from typing import List

'''
BinaryNode - Node with two children
    -> ParentedBinaryNode - BinaryNode with a parent pointer
        -> AVLNode - ParentedBinaryNode with avl invariant tracking
    -> Cap - BinaryNode that is terminating

Tree - Unsorted Binary tree with traversal and drawing
    -> ParentTree - Unsorted Binary tree with parent pointers (allows for tree rotations)
        -> BalParTree - (HEAP) balanced tree with parent pointer
        -> BST - Binary search tree without any thing fancy
            -> AVLTree - BST with AVL invariant
    -> BalTree - Constructs a balanced Tree with infoues taken in heap form
'''



class BinaryNode:
    def __init__(self,info,*args) -> None:
        try:
            assert len(args) <=2
        except AssertionError:
            raise TypeError(f"BinaryNode takes less than 2 children nodes, but {len(args)} were given")

        try:
            assert isinstance(BinaryNode,args) or len(args) ==0
        except AssertionError:
            raise TypeError(f"BinaryNode's children can only be BinaryNodes {args}")

        self.L :BinaryNode= Cap() if not args else args[0]
        self.R :BinaryNode= Cap() if len(args)<2 else args[1]
        self.info = info

    def setl(self,node):
        self.L = node
    def setr(self,node):
        self.R = node

    def traverse_pre(self):
        yield self
        if not isinstance(self.L,Cap):
            yield from self.L.traverse_pre()
        if not isinstance(self.R,Cap):
            yield from self.R.traverse_pre()
    def traverse_post(self):
        if not isinstance(self.L,Cap):
            yield from self.L.traverse_post()
        if not isinstance(self.R,Cap):
            yield from self.R.traverse_post()
        yield self
    def traverse_in(self):
        if not isinstance(self.L,Cap):
            yield from self.L.traverse_in()
        yield self
        if not isinstance(self.R,Cap):
            yield from self.R.traverse_in()

class Cap(BinaryNode):
    def __init__(self) -> None:
        pass
class Tree:
    def __init__(self) -> None:
        self.nodetype = BinaryNode
        self.root = Cap()
    
    def traverse_pre(self):
        yield from self.root.traverse_pre()
    def traverse_post(self):
        yield from self.root.traverse_post()
    def traverse_in(self):
        yield from self.root.traverse_in()
        



    def draw(self):
        layer : List[BinaryNode] = [self.root]
        while layer:
            print([n.info for n in layer if n is not None])
            new_layer = []
            for n in layer:
                if not isinstance(n.L,Cap):
                    new_layer.append(n.L)
                if not isinstance(n.R,Cap):
                    new_layer.append(n.R)
            layer = new_layer



class ParentedBinaryNode(BinaryNode):
    def __init__(self, info, *args : BinaryNode) -> None:
        super().__init__(info, *(args[:2]))
        self.parent = args[2] if len(args)>2 else Cap()
    @staticmethod
    def setparent(node,parent):
        if isinstance(node,Cap):
            return
        else:
            node : ParentedBinaryNode
            node.parent = parent
    def setl(self,node):
        self.L = node
        self.setparent(self.L, self)
    def setr(self,node):
        self.R = node
        self.setparent(self.R, self)

class ParentTree(Tree):
    def __init__(self) -> None:
        self.nodetype = ParentedBinaryNode
        self.root = ParentedBinaryNode(None)
        self.root.parent = Cap()

    def rotateL(self,node):
        try:
            assert isinstance(node,self.nodetype)
        except AssertionError:
            raise TypeError(f"node is not of the tree node type: {type(node)} != {self.nodetype}")
        
        if isinstance(node.R,Cap):
            return
        else:
            child:ParentedBinaryNode = node.R
            node.R = child.L
            ParentedBinaryNode.setparent(node.R, node)
            child.L = node
            ParentedBinaryNode.setparent(child,node.parent)
            ParentedBinaryNode.setparent(node,child)
            parent = child.parent
            if isinstance(parent,Cap):
                self.root = child
                return
            if parent.L == node:
                parent.setl(child)
            if parent.R == node:
                parent.setr(child)
        
    def rotateR(self,node):
        try:
            assert isinstance(node,self.nodetype)
        except AssertionError:
            raise TypeError(f"node is not of the tree node type: {type(node)} != {self.nodetype}")

        if isinstance(node.L,Cap):
            return
        else:
            child:ParentedBinaryNode = node.L
            node.L = child.R
            ParentedBinaryNode.setparent(node.L, node)
            child.R = node
            ParentedBinaryNode.setparent(child,node.parent)
            ParentedBinaryNode.setparent(node,child)
            parent = child.parent
            if isinstance(parent,Cap):
                self.root = child
                return
            if parent.R == node:
                parent.setr(child)
            if parent.L == node:
                parent.setl(child)



class BalTree(Tree):
    def __init__(self,node_type,nodes_info) -> None:
        assert BinaryNode in node_type.__bases__ or BinaryNode == node_type
        nodes: List[BinaryNode] = [node_type(info) for info in nodes_info]
        for ind in range(len(nodes_info)-1,0,-1):
            if ind%2==1:
                nodes[((ind+1)>>1)-1].setl(nodes[ind])
            else:
                nodes[((ind+1)>>1)-1].setr(nodes[ind])
        self.root : BinaryNode = nodes[0]
        self.nodetype = node_type

class BalParTree(ParentTree):
    def __init__(self,node_type,nodes_info) -> None:
        assert ParentedBinaryNode in node_type.__bases__ or ParentedBinaryNode == node_type
        nodes: List[ParentedBinaryNode] = [node_type(info) for info in nodes_info]
        for ind in range(len(nodes_info)-1,0,-1):
            if ind%2==1:
                nodes[((ind+1)>>1)-1].setl(nodes[ind])
            else:
                nodes[((ind+1)>>1)-1].setr(nodes[ind])
        self.root : ParentedBinaryNode = nodes[0]
        self.nodetype = node_type
 
if __name__ == '__main__':

    tree = BalParTree(ParentedBinaryNode,[1,2,3,4,5,6,7])
    tree.draw()
    tree.rotateL(tree.root)
    tree.draw()
    tree.rotateR(tree.root)
    tree.draw()
    
    print('pre',[node.info for node in tree.traverse_pre()])
    print('post',[node.info for node in tree.traverse_post()])
    print('in',[node.info for node in tree.traverse_in()])