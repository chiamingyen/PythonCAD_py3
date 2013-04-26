#@+leo-ver=5-thin
#@+node:1.20130426141258.2579: * @file binarytree.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:1.20130426141258.2580: ** class BinaryTree
class BinaryTree(object):
    """
        generic tree binary structure object
    """    
    #@+others
    #@+node:1.20130426141258.2581: *3* __init__
    def __init__(self):             self.__tree=EmptyNode()
    #@+node:1.20130426141258.2582: *3* __repr__
    def __repr__(self):             return repr(self.__tree)
    #@+node:1.20130426141258.2583: *3* lookUp
    def lookUp(self, key):          return self.__tree.lookUp(key)
    #@+node:1.20130426141258.2584: *3* insert
    def insert(self, key, value):   self.__tree=self.__tree.insert(key, value)
    #@-others
#@+node:1.20130426141258.2585: ** class EmptyNode
class EmptyNode(object):
    """
        empty Node
    """
    #@+others
    #@+node:1.20130426141258.2586: *3* __repr__
    def __repr__(self):             return '*'
    #@+node:1.20130426141258.2587: *3* lookUp
    def lookUp(self, key):          return None
    #@+node:1.20130426141258.2588: *3* insert
    def insert(self, key, value):   return BinaryNode(self,key,  value, self)
    #@-others
#@+node:1.20130426141258.2589: ** class BinaryNode
class BinaryNode(object):
    """
        this class rappresent a binary node
    """
    #@+others
    #@+node:1.20130426141258.2590: *3* __init__
    def __init__(self, left,key, value, right):
        self.key,  self.data  = key, value
        self.left, self.right = left, right
    #@+node:1.20130426141258.2591: *3* lookUp
    def lookUp(self, key):
        """
            look up at the value
        """
        if self.key==key:       return self.data
        elif self.key>key:      return self.left.lookUp(key)
        else:                   return self.right.lookUp(key)
    #@+node:1.20130426141258.2592: *3* insert
    def insert(self,key,value):
        """
            insert a new value at the node
        """
        if      self.key==key:      self.data=value
        elif    self.key>key:       self.left=self.left.insert(key, value)
        elif    self.key<key:       self.right=self.right.insert(key,  value)
        return self
    #@+node:1.20130426141258.2593: *3* __repr__
    def __repr__(self): return '(%s,%s,%s,%s)'%(repr(self.left), repr(self.key),  repr(self.data), repr(self.right))
    #@-others
#@+node:1.20130426141258.2594: ** testBinaryTree
def testBinaryTree():
    x=BinaryTree()
    x.insert('root', "1")
    x.insert('layer_1', "3")
    x.insert('layer_2', "2")   
    print("-->", x.lookUp('layer_1'))
    print("-->%s"%str(x))
#@-others
if __name__=='__main__':    
    testBinaryTree()
#@-leo
