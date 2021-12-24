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
        
    @staticmethod
    def isleaf(node:BinaryNode):
        return isinstance(node.L,Cap) and isinstance(node.R,Cap)


    def draw(self,key_only = True):
        layer : List[BinaryNode] = [self.root]
        seen = []
        while layer:
            print([n if n=="*" else (n.info[0] if key_only else n.info) for n in layer if n not in {None}])
            new_layer = []
            for n in layer:
                if n=="*":
                    continue
                if not isinstance(n.L,Cap):
                    new_layer.append(n.L)
                else:
                    new_layer.append("*")
                if not isinstance(n.R,Cap):
                    new_layer.append(n.R)
                else:
                    new_layer.append("*")
                if n in seen:
                    input(f"the node {n.info} is already drawn, we have a loop")
            seen.extend(layer)
            layer = new_layer
        print("\n")



class ParentedBinaryNode(BinaryNode):
    def __init__(self, info, *args) -> None:
        super().__init__(info, *(args[:2]))
        self.parent:ParentedBinaryNode = args[2] if len(args)>2 else Cap()
    def setparent(self,parent):
        if isinstance(self,Cap):
            return
        else:
            self.parent = parent
    def setl(self,node):
        self.L = node
        if not isinstance(node,Cap):
            node.setparent(self)
    def setr(self,node):
        self.R = node
        if not isinstance(node,Cap):
            node.setparent(self)

    
    def rotateL(self):
        if isinstance(self.R,Cap):
            return
        else:
            child:ParentedBinaryNode = self.R
            self.R = child.L
            ParentedBinaryNode.setparent(self.R, self)
            child.L = self
            ParentedBinaryNode.setparent(child,self.parent)
            ParentedBinaryNode.setparent(self,child)
            parent = child.parent
            if isinstance(parent,Cap):
                return
            if parent.L == self:
                parent.setl(child)
            if parent.R == self:
                parent.setr(child)
    
    def rotateR(self):
        if isinstance(self.L,Cap):
            return
        else:
            child:ParentedBinaryNode = self.L
            self.L = child.R
            ParentedBinaryNode.setparent(self.L, self)
            child.R = self
            ParentedBinaryNode.setparent(child,self.parent)
            ParentedBinaryNode.setparent(self,child)
            parent = child.parent
            if isinstance(parent,Cap):
                return
            if parent.R == self:
                parent.setr(child)
            if parent.L == self:
                parent.setl(child)


class ParentTree(Tree):
    def __init__(self) -> None:
        self.nodetype = ParentedBinaryNode
        self.root = ParentedBinaryNode(None)
        self.root.parent = Cap()
    
    def replace(self,new_node:ParentedBinaryNode,old_node:ParentedBinaryNode):
        new_node.setl(old_node.L)
        new_node.setr(old_node.R)
        new_node.setparent(old_node.parent)
        if isinstance(new_node.parent ,Cap):
            self.root = new_node
            return
        if old_node == old_node.parent.L:
            old_node.parent.L = new_node
        elif old_node == old_node.parent.R:
            old_node.parent.R = new_node
    def replace_subtree(self,new_node:ParentedBinaryNode,old_node:ParentedBinaryNode):
        new_node.setparent(old_node.parent)
        if isinstance(new_node.parent ,Cap):
            self.root = new_node
            return
        if old_node == old_node.parent.L:
            old_node.parent.L = new_node
        elif old_node == old_node.parent.R:
            old_node.parent.R = new_node
            

    def rotateL(self,node):
        try:
            assert isinstance(node,self.nodetype)
        except AssertionError:
            raise TypeError(f"node is not of the tree node type: {type(node)} != {self.nodetype}")

        node.rotateL()
        if isinstance(node.parent.parent,Cap):
            self.root = node.parent
        
    def rotateR(self,node):
        try:
            assert isinstance(node,self.nodetype)
        except AssertionError:
            raise TypeError(f"node is not of the tree node type: {type(node)} != {self.nodetype}")
        node.rotateR()
        if isinstance(node.parent.parent,Cap):
            self.root = node.parent


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


class BST(ParentTree):
    def __init__(self,insert:List) -> None:
        self.nodetype = ParentedBinaryNode
        self.root = ParentedBinaryNode(insert[0])

        self.root.parent = Cap()
        for val in insert[1:]:
            self.insert(val)
    @staticmethod
    def max(node:ParentedBinaryNode):
        curr = node
        while not isinstance(curr.R,Cap):
            curr =curr.R 
        return curr
    @staticmethod 
    def min(node:ParentedBinaryNode):
        curr =node
        while not isinstance(curr.L,Cap):
            curr = curr.L
        return curr

    def find(self,key):
        curr = self.root
        while not isinstance(curr,Cap):
            if curr.info[0] > key:
                curr = curr.L
            elif curr.info[0]<key: 
                curr = curr.R
            else:
                return curr
        return curr
    def succ(self,node:ParentedBinaryNode):
        if not isinstance(node.R,Cap):
            return self.min(node.R)
        else:
            curr = node
            parent = curr.parent
            while not isinstance(parent,Cap) and parent.R == curr:
                curr = parent
                parent = parent.parent
            return parent
    def pred(self,node:ParentedBinaryNode):
        if not isinstance(node.L,Cap):
            return self.min(node.L)
        else:
            curr = node
            parent = curr.parent
            while not isinstance(parent,Cap) and parent.L == curr:
                curr = parent
                parent = parent.parent
            return parent

    def insert(self,token):
        """
        Returns the inserted node
        """
        key,_ = token
        curr = self.root
        parent = curr.parent
        while not isinstance(curr,Cap):
            parent = curr
            if curr.info[0] > key:
                curr = curr.L
            else: 
                curr = curr.R
        node = self.nodetype(token)
        node.parent = parent
        if isinstance(parent,Cap):
            self.root = node
        elif key < parent.info[0]:
            parent.setl(node)
        else:
            parent.setr(node)
        return node
    def delete(self,key):
        node = self.find(key)
        try:
            assert not isinstance(node,Cap)
        except AssertionError:
            raise ValueError(f"Trying to delete nonexistant node with key {key}")
        
        l,r = isinstance(node.L,Cap), isinstance(node.R,Cap) 
        if self.isleaf(node):
            self.replace_subtree(Cap(),node)
        elif l and not r:
            self.replace_subtree(node.R,node)
        elif r and not l:
            self.replace_subtree(node.L,node)
        else:
            succ = self.succ(node)
            if succ.parent != node:
                self.replace_subtree(succ.R,succ)
                succ.setr(node.R)
            self.replace_subtree(node,succ)
            succ.setl(node.L)


if __name__ == '__main__':
    tree = BST([(0,0)])
    tree.draw()
    tree.insert((1,1))
    tree.draw()
    tree.insert((2,2))
    tree.draw()
    tree.insert((4,4))
    tree.insert((3,3))
    tree.insert((5,5))
    tree.draw()
    tree.delete(2)
    tree.draw()



    exit()
    tree = BalParTree(ParentedBinaryNode,[1,2,3,4,5,6,7])
    tree.draw()
    tree.rotateL(tree.root)
    tree.draw()
    tree.rotateR(tree.root)
    tree.draw()

    

    print('pre',[node.info for node in tree.traverse_pre()])
    print('post',[node.info for node in tree.traverse_post()])
    print('in',[node.info for node in tree.traverse_in()])