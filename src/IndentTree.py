class IndentTreeNode:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
        self.children = []

    def generate_tree_from_list(self, value_list):
        level_value_nums = self._get_value_nums_at_start_level(value_list)
        self.children = [IndentTreeNode(self, value_list[i]) for i in level_value_nums]
        for i, child in enumerate(self.children):
            sub_start = level_value_nums[i] + 1
            if len(level_value_nums) > i+1:
                sub_end = level_value_nums[i+1]
            else:
                sub_end = len(value_list)
            child.generate_tree_from_list(value_list[sub_start:sub_end])

    def _get_value_nums_at_start_level(self, values):
        numbers = []
        if len(values) > 0:
            start_indent = values[0].indent
            for i, value in enumerate(values):
                    if value.indent == start_indent:
                        numbers.append(i)
        return numbers

    def __str__(self):
        spacing = ""
        return "\n".join(self.pprint(spacing))

    def walk(self):
        yield self
        for child in self.children:
            for n in child.walk():
                yield n

    def pprint(self, spacing):
        output = []
        n = 100
        if self.value is not None:
            for line in str(self.value).split("\n"):
                chunks = [spacing + line[i:i+n].strip() for i in range(0, len(line), n)]
                output.extend(chunks)
        for child in self.children:
            output.extend(child.pprint(spacing + "    "))
        return output
