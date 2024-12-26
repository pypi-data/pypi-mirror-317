class Node:
    def __init__(self, char: str, is_end = False) -> None:
        self.char = char
        self.nexts = []
        self.is_end = is_end
        self.connects = 0

class TRIE:
    def __init__(self) -> None:
        self.nexts = [] # collection of nodes
        self.connects = 0
    
    def add(self, _str: str) -> None:
        if self.match(_str): return
        data = self
        for i, c in enumerate(_str):
            node = next((j for j in data.nexts if j.char == c), None)
            if node is None:
                for char in _str[i:]:
                    data.connects += 1
                    node = Node(char)
                    data.nexts.append(node)
                    data = node
                data.is_end = True
                return
            data = node
        data.is_end = True
    
    def match(self, _str: str) -> bool:
        node = self
        for i in _str:
            node = next((j for j in node.nexts if j.char == i), None)
            if node is None: return False
        return node.is_end
    
    def find(self, _str: str) -> int:
        if not self.match(_str):
            return -1
        index = 0
        node = self
        for i in _str:
            for j in node.nexts:
                if j.char != i:
                    index += j.connects
                    index += 1 if j.is_end else 0
                else:
                    node = j
                    break
        return index
    
    def __iter__(self):
        def dfs(node, path):
            if node.is_end:
                yield ''.join(path)
            for next_node in node.nexts:
                yield from dfs(next_node, path + [next_node.char])

        for node in self.nexts:
            yield from dfs(node, [node.char])
        


if __name__ == '__main__':
    Strset = TRIE()
    Strset.add('hello')
    Strset.add('world')
    Strset.add('!')
    Strset.add(',')
    Strset.add('hen')
    Strset.add('hell')
    for strs in Strset: print(strs)