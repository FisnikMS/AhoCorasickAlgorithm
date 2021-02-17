import BinarySearchTree, LinkedList;


class PatternMatchingMachine:

    def __init__(self, keywords):
        assert type(keywords) == list, "keywords must be a list"

        self.keywords = keywords
        self.goto_list = []
        self.failure_list = []
        self.output_list = []
        self.next_move_hash_map = {}

    def init_non_deterministic_pattern_matching_machine(self):
        # clear lists
        self.goto_list = []
        self.failure_list = []
        self.output_list = []

        self.__init_goto_list()
        self.failure_list = [0] * len(self.goto_list)
        self.__init_failure_list()

    def init_deterministic_pattern_matching_machine(self):
        # clear lists
        self.next_move_hash_map = {}
        self.init_non_deterministic_pattern_matching_machine()

        self.__init_next_move_hash_map()

    def non_deterministic_pattern_matching(self, text_string):
        assert type(text_string) == str, "text_string must be a string"
        assert len(self.keywords) > 0 \
               and len(self.goto_list) > 0 \
               and len(self.failure_list) > 0 \
               and len(self.output_list) > 0, "make sure to initilize the non deterministic pattern matching machine before calling this method"

        # print("Execute non deterministic pattern matching machine, with keywords {} \n".format(self.keywords))
        state = 0
        for i in range(len(text_string)):
            while state != 0 and self.goto_list[state].findval(text_string[i]) == - 1:
                state = self.failure_list[state]

            state_tmp = self.goto_list[state].findval(text_string[i])
            state = state_tmp[1] if state_tmp != -1 else 0

            if self.output_list[state] is not None:
                self.output_list[state].print(i)

    def deterministic_pattern_matching(self, text_string):
        assert type(text_string) == str, "text_string must be a string"
        assert len(self.keywords) > 0 \
               and len(self.goto_list) > 0 \
               and len(self.failure_list) > 0 \
               and len(self.output_list) > 0 \
               and len(
            self.next_move_hash_map) > 0, "make sure to initilize the deterministic pattern matching machine before calling this method"
        # print("Execute deterministic pattern matching machine, with keywords {} \n".format(self.keywords))
        state = 0
        for i in range(len(text_string)):

            state = self.next_move_hash_map.get((state, text_string[i]), 0)

            if self.output_list[state] is not None:
                self.output_list[state].print(i)

    ###############################################  NAIVE APPROACH  ###############################################

    def naive_approach(self, text_string):
        assert type(text_string) == str, "text_string must be string"
        # print("Execute naive algorithm, with keywords {} \n".format(self.keywords))
        for key in self.keywords:
            matching = 0
            for i in range(len(text_string)):
                if text_string[i] == key[matching]:
                    matching += 1

                    if matching == len(key):
                        print("Keyword {} was found at Position {}".format(key, i - len(key)))
                        matching = 0
                else:
                    matching = 0

    ###############################################  PRIVATE METHODES  ###############################################

    def __init_failure_list(self):

        queue = []
        # initialize state zero
        transitions = self.goto_list[0].getChilds()
        for (alphabet, s) in transitions:
            queue.append(s)
            self.failure_list[s] = 0
        # breath search first through all states
        while len(queue) > 0:
            r = queue.pop(0)
            transitions = self.goto_list[r].getChilds()
            # calculate  failure function for all valid transitions that are reachable from state r
            if transitions != None:
                for (alphabet, s) in transitions:

                    queue.append(s)
                    state = self.failure_list[r]
                    # determine the longest proper suffix of the string that is represented by r
                    while state != 0 and self.goto_list[state].findval(alphabet) == -1:
                        state = self.failure_list[state]

                    failure_tuple = self.goto_list[state].findval(alphabet)
                    # if a transition exists from f(r) with input a, then update the failure function. Otherwise fill the index with a zero
                    self.failure_list[s] = failure_tuple[1] if failure_tuple != -1 else 0

                    # merge the output sets
                    if self.output_list[self.failure_list[s]] is not None and self.output_list[
                        s] is not None:
                        self.output_list[s].insert(self.output_list[self.failure_list[s]])

    def __init_goto_list(self):
        newstate = 0
        def enter(word):
            assert type(word) == str, "word must be a string"
            nonlocal newstate
            state = 0
            j = 0

            # check if a prefix of word exists
            tmp = self.goto_list[state].findval(word[j])
            while j < len(word) and self.goto_list[state].findval(word[j]) != - 1:
                state = self.goto_list[state].findval(word[j])[1]
                j = j + 1
            # create states for all alphabets, that are not presented in the automata
            if j < len(word):
                for p in range(j, len(word)):
                    newstate += 1
                    self.goto_list[state].insert(word[p], newstate)
                    self.goto_list.append(BinarySearchTree.Node(word[p]))
                    self.output_list.append(None)
                    state = newstate
            # initialize output function for the inserted word
            self.output_list[state] = LinkedList.LinkedList(word)


        self.goto_list.append(BinarySearchTree.Node(chr(0)))
        self.output_list.append(None)
        for i in range(len(self.keywords)):
            enter(self.keywords[i])

    def __init_next_move_hash_map(self):

        queue = []
        transitions = self.goto_list[0].getChilds()
        for (alphabet, s) in transitions:
            self.next_move_hash_map[(0, alphabet)] = s
            queue.append(s)

        while len(queue) > 0:
            r = queue.pop(0)
            # add all valid transitions from the goto function of state r into the next move function
            transitions = self.goto_list[r].getChilds()

            if transitions != None:
                for (alphabet, s) in transitions:
                    self.next_move_hash_map[(r, alphabet)] = s
                    queue.append(s)

            # add all valid transitions from the failure function of r into the next move function
            transitions_from_failure_function = self.goto_list[self.failure_list[r]].getChilds()
            if transitions_from_failure_function != None:
                for (alphabet, s) in transitions_from_failure_function:
                    # avoid overwriting valid transitions
                    if self.next_move_hash_map.get((r, alphabet)) == None:
                        self.next_move_hash_map[(r, alphabet)] = s
