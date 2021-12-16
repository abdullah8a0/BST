from typing import List

class Node:
    def __init__(self,val,*args) -> None:
        try:
            assert len(args) <=2
        except AssertionError:
            raise TypeError(f"Node takes less than 2 children nodes, but {len(args)} were given")

        try:
            assert isinstance(Node,args) or len(args) ==0
        except AssertionError:
            raise TypeError(f"Node's children can only be Nodes {args}")

        self.L :Node= Cap() if not args else args[0]
        self.R :Node= Cap() if len(args)<2 else args[1]
        self.val = val

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

class Cap(Node):
    def __init__(self) -> None:
        pass
class Tree:
    def __init__(self) -> None:
        self.nodetype = Node
        self.root = Cap()
    
    def traverse_pre(self):
        yield from self.root.traverse_pre()
    def traverse_post(self):
        yield from self.root.traverse_post()
    def traverse_in(self):
        yield from self.root.traverse_in()
        



    def draw(self):
        layer : List[Node] = [self.root]
        while layer:
            print([n.val for n in layer if n is not None])
            new_layer = []
            for n in layer:
                if not isinstance(n.L,Cap):
                    new_layer.append(n.L)
                if not isinstance(n.R,Cap):
                    new_layer.append(n.R)
            layer = new_layer



class ParentedNode(Node):
    def __init__(self, val, *args : Node) -> None:
        super().__init__(val, *(args[:2]))
        self.parent = args[2] if len(args)>2 else Cap()
    @staticmethod
    def setparent(node,parent):
        if isinstance(node,Cap):
            return
        else:
            node : ParentedNode
            node.parent = parent
    def setl(self,node):
        self.L = node
        self.setparent(self.L, self)
    def setr(self,node):
        self.R = node
        self.setparent(self.R, self)

class ParentTree(Tree):
    def __init__(self) -> None:
        self.nodetype = ParentedNode
        self.root = ParentedNode(None)
        self.root.parent = Cap()

    def rotateL(self,node):
        try:
            assert isinstance(node,self.nodetype)
        except AssertionError:
            raise TypeError(f"node is not of the tree node type: {type(node)} != {self.nodetype}")
        
        if isinstance(node.R,Cap):
            return
        else:
            child:ParentedNode = node.R
            node.R = child.L
            ParentedNode.setparent(node.R, node)
            child.L = node
            ParentedNode.setparent(child,node.parent)
            ParentedNode.setparent(node,child)
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
            child:ParentedNode = node.L
            node.L = child.R
            ParentedNode.setparent(node.L, node)
            child.R = node
            ParentedNode.setparent(child,node.parent)
            ParentedNode.setparent(node,child)
            parent = child.parent
            if isinstance(parent,Cap):
                self.root = child
                return
            if parent.R == node:
                parent.setr(child)
            if parent.L == node:
                parent.setl(child)



class BalTree(Tree):
    def __init__(self,node_type,nodes_val) -> None:
        assert Node in node_type.__bases__ or Node == node_type
        nodes: List[Node] = [node_type(val) for val in nodes_val]
        for ind in range(len(nodes_val)-1,0,-1):
            if ind%2==1:
                nodes[((ind+1)>>1)-1].setl(nodes[ind])
            else:
                nodes[((ind+1)>>1)-1].setr(nodes[ind])
        self.root : Node = nodes[0]
        self.nodetype = node_type

class BalParTree(ParentTree):
    def __init__(self,node_type,nodes_val) -> None:
        assert ParentedNode in node_type.__bases__ or ParentedNode == node_type
        nodes: List[ParentedNode] = [node_type(val) for val in nodes_val]
        for ind in range(len(nodes_val)-1,0,-1):
            if ind%2==1:
                nodes[((ind+1)>>1)-1].setl(nodes[ind])
            else:
                nodes[((ind+1)>>1)-1].setr(nodes[ind])
        self.root : ParentedNode = nodes[0]
        self.nodetype = node_type
 
if __name__ == '__main__':

    tree = BalParTree(ParentedNode,[1,2,3,4,5,6,7])
    tree.draw()
    tree.rotateL(tree.root)
    tree.draw()
    tree.rotateR(tree.root)
    tree.draw()
    
    print('pre',[node.val for node in tree.traverse_pre()])
    print('post',[node.val for node in tree.traverse_post()])
    print('in',[node.val for node in tree.traverse_in()])