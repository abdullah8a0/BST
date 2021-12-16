class Node:
    def __init__(self,val,*args) -> None:
        assert len(args) <= 2
        self.L = None if not args else args[0]
        self.R = None if len(args)<2 else args[1]
        self.val = val

    def setl(self,node):
        self.L = node
    def setr(self,node):
        self.R = node

    def traverse_pre(self):
        yield self
        if self.L is not None:
            yield from self.L.traverse_pre()
        if self.R is not None:
            yield from self.R.traverse_pre()
    def traverse_post(self):
        if self.L is not None:
            yield from self.L.traverse_post()
        if self.R is not None:
            yield from self.R.traverse_post()
        yield self
    def traverse_in(self):
        if self.L is not None:
            yield from self.L.traverse_in()
        yield self
        if self.R is not None:
            yield from self.R.traverse_in()

class Tree:
    def __init__(self,nodes_val) -> None:
        nodes = [Node(val) for val in nodes_val]
        for ind in range(len(nodes_val)-1,0,-1):
            if ind%2==1:
                nodes[((ind+1)>>1)-1].setl(nodes[ind])
            else:
                nodes[((ind+1)>>1)-1].setr(nodes[ind])
        self.root : Node = nodes[0]
    
    def traverse_pre(self)->Node:
        yield from self.root.traverse_pre()
    def traverse_post(self)->Node:
        yield from self.root.traverse_post()
    def traverse_in(self)->Node:
        yield from self.root.traverse_in()

    def draw(self):
        layer = [self.root]
        while layer:
            print([n.val for n in layer if n is not None])
            new_layer = []
            for n in layer:
                if n.L is not None:
                    new_layer.append(n.L)
                if n.R is not None:
                    new_layer.append(n.R)
            layer = new_layer
    

if __name__ == '__main__':
    tree = Tree([1,2,3,4,5,6,7])
    tree.draw()
    
    print('pre',[node.val for node in tree.traverse_pre()])
    print('post',[node.val for node in tree.traverse_post()])
    print('in',[node.val for node in tree.traverse_in()])