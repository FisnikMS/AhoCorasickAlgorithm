class Node:

    def __init__(self, word, state=None, next_node=None):
        self.state = state
        self.word = word
        self.next_node = next_node


class LinkedList:
    def __init__(self, state, word=None):
        self.head = Node(state, word)

    def insert(self, new_node):
        current = self.head
        while current.next_node:
            current = current.next_node
        current.next_node = new_node

    def print(self, index):
        current = self.head

        while current:
            print("Keyword {} was found at Position {}".format(current.word, index - len(current.word)))
            current = current.next_node.head if current.next_node is not None else current.next_node
