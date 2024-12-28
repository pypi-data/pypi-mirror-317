from typing import Iterable
import json

__version__ = "0.6.1"

class Node:
    def __init__(self, char: str, is_end: bool = False) -> None:
        self.char = char
        self.children = {}  # Use a dictionary for faster lookups
        self.is_end = is_end

class TRIE:
    def __init__(self, iterable: Iterable[str] = None, case_insensitive: bool = False) -> None:
        self.root = Node("")
        self.case_insensitive = case_insensitive
        if iterable is not None:
            self.extend(iterable)

    def _normalize(self, word: str) -> str:
        return word.lower() if self.case_insensitive else word

    def add(self, word: str) -> None:
        word = self._normalize(word)
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Node(char)
            node = node.children[char]
        node.is_end = True

    def extend(self, words: Iterable[str]) -> None:
        for word in words:
            self.add(word)

    def match(self, word: str) -> bool:
        word = self._normalize(word)
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def find(self, word: str) -> int:
        word = self._normalize(word)
        if not self.match(word):
            return -1
        index = 0
        stack = [(self.root, 0)]
        while stack:
            current_node, depth = stack.pop()
            if depth == len(word):
                return index
            for child_char, child_node in sorted(current_node.children.items()):
                if depth < len(word) and child_char == word[depth]:
                    stack.append((child_node, depth + 1))
                    break
                index += 1 + len(child_node.children)
        return index

    def prefix_match(self, prefix: str) -> Iterable[str]:
        prefix = self._normalize(prefix)
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        def dfs(node, path):
            if node.is_end:
                yield ''.join(path)
            for char, child_node in node.children.items():
                yield from dfs(child_node, path + [char])

        return dfs(node, list(prefix))

    def delete(self, word: str) -> bool:
        word = self._normalize(word)
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0

            char = word[depth]
            if char not in node.children:
                return False

            child_node = node.children[char]
            should_delete = _delete(child_node, word, depth + 1)

            if should_delete:
                del node.children[char]
                return not node.is_end and len(node.children) == 0

            return False

        return _delete(self.root, word, 0)

    def export(self, filepath: str) -> None:
        def serialize(node):
            return {
                "char": node.char,
                "is_end": node.is_end,
                "children": {char: serialize(child) for char, child in node.children.items()}
            }

        with open(filepath, "w") as f:
            json.dump(serialize(self.root), f)

    @staticmethod
    def import_trie(filepath: str, case_insensitive: bool = False) -> 'TRIE':
        def deserialize(data):
            node = Node(data["char"], data["is_end"])
            node.children = {char: deserialize(child) for char, child in data["children"].items()}
            return node

        with open(filepath, "r") as f:
            data = json.load(f)
            trie = TRIE(case_insensitive=case_insensitive)
            trie.root = deserialize(data)
            return trie

    def __iter__(self):
        def dfs(node, path):
            if node.is_end:
                yield ''.join(path)
            for char, child_node in node.children.items():
                yield from dfs(child_node, path + [char])

        yield from dfs(self.root, [])

    def __contains__(self, word: str) -> bool:
        return self.match(word)

if __name__ == '__main__':
    trie = TRIE(['hello', 'world', '!', ',', 'hen', 'hell'], case_insensitive=True)
    trie.add('Help')
    trie.extend(['HeLLo', 'WoRlD'])
    for word in trie:
        print(word)
    print('hello' in trie)  # True
    print('unknown' not in trie)  # True
    print(trie.find('hell'))  # Index of 'hell'
    print(list(trie.prefix_match('he')))  # ['hello', 'hen', 'hell', 'help']
    trie.delete('hell')
    print(list(trie))  # ['hello', 'world', '!', ',', 'hen', 'help']
    trie.export("trie.json")
    imported_trie = TRIE.import_trie("trie.json", case_insensitive=True)
    print(list(imported_trie))
