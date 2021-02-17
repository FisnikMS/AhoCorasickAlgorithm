class Node:

    def __init__(self, alphabet, state=None):

        self.left = None
        self.right = None
        self.alphabet = alphabet
        self.state = state


    def insert(self, alphabet, state):
        #assert alphabet.isalpha(),  "alphabet should be a character"
        assert type(state) == int,  "state should be an integer"

        if alphabet < self.alphabet:
                if self.left is None:
                    self.left = Node(alphabet, state)
                else:
                    self.left.insert(alphabet, state)
        elif alphabet > self.alphabet:
                if self.right is None:
                    self.right = Node(alphabet, state)
                else:
                    self.right.insert(alphabet, state)
        else:
                self.alphabet = alphabet
                self.state = state


    def findval(self, searchVal):
        if searchVal == self.alphabet:
            return -1 if self.state is None else (self.alphabet, self.state)
        elif searchVal < self.alphabet:
            if self.left is None:
                return -1
            return self.left.findval(searchVal)
        elif searchVal > self.alphabet:
            if self.right is None:
                return -1
            return self.right.findval(searchVal)
        else:
            return self.alphabet, self.state

    def getChilds(self):
        left_tree = []
        right_tree = []

        if self.left is not None:
            left_tree = self.left.searchRecursive()
        if self.right is not None:
            right_tree = self.right.searchRecursive()

        return left_tree + right_tree

    def searchRecursive(self):
        nodes = [(self.alphabet, self.state)]
        if self.left is not None:
            nodes = nodes + self.left.searchRecursive()
        if self.right is not None:
            nodes = nodes + self.right.searchRecursive()

        return nodes
