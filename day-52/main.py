#!/usr/bin/env python3


class Node:
    def __init__(self, key, value, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        output = ""
        if self.prev is not None:
            output += "> "
        output += f"({self.key},{self.value})"
        if self.next is not None:
            output += " -"
            output += str(self.next)
        return output

    def __repr__(self):
        return str(self)


class LRU:
    def __init__(self, n):
        self.size = 0
        self.maxsize = n
        self.kv = dict()  # key -> node
        self.first = None  # node
        self.last = None  # node

    def __str__(self):
        return f"LRU[{self.size}/{self.maxsize}, {self.last}]"

    def __repr__(self):
        return str(self)

    def get(self, key):
        # key does not exist
        if key not in self.kv:
            return None

        # key exists: find value and set node as the first element
        # extract node
        node = self.kv[key]

        # update the double-ended queue
        if (node.prev is not None) and (node.next is not None):
            # node is not an end of the deque
            node.prev.next = node.next
        if node.next is not None:
            # node is not the first element
            node.next.prev = node.prev

        if (self.last == node) and (node.next is not None):
            self.last = node.next

        if self.first != node:
            oldfirst = self.first
            oldfirst.next = node
            node.prev = oldfirst
            node.next = None
            self.first = node

        # return value
        return node.value

    def set(self, key, value):
        # delete one element if max size was already reached
        if self.size == self.maxsize:
            last = self.last
            del self.kv[last.key]
            last.next.prev = None
            self.last = last.next
            self.size -= 1

            # edge case: self.maxsize == 1 means self.last = self.first
            if self.first == last:
                self.first = None

        # insert new element
        oldfirst = self.first
        node = Node(key, value, prev=oldfirst)
        self.first = node
        if oldfirst is not None:
            oldfirst.next = node
        else:
            self.last = node
        self.kv[key] = node
        self.size += 1
        assert self.size <= self.maxsize


def main():
    # cache = LRU(1)
    # cache = LRU(2)
    # cache = LRU(3)
    # cache = LRU(4)
    cache = LRU(5)

    print("##### Empty cache #####")
    print(cache)
    print(cache.get("a"))
    print(cache)
    print()

    print("##### Add a = 1 #####")
    cache.set("a", 1)
    print(cache)
    print(cache.get("a"))
    print(cache)
    print()

    print("##### Add b = 2 #####")
    cache.set("b", 2)
    print(cache)
    print(cache.get("b"))
    print(cache)
    print(cache.get("a"))
    print(cache)
    print(cache.get("b"))
    print(cache)
    print()

    print("##### Add c = 3 #####")
    cache.set("c", 3)
    print(cache)
    print(cache.get("c"))
    print(cache)
    print(cache.get("a"))
    print(cache)
    print(cache.get("b"))
    print(cache)
    print(cache.get("c"))
    print(cache)
    print()

    print("##### Add d = 4 #####")
    cache.set("d", 4)
    print(cache)
    print(cache.get("d"))
    print(cache)
    print(cache.get("a"))
    print(cache)
    print(cache.get("b"))
    print(cache)
    print(cache.get("c"))
    print(cache)
    print(cache.get("d"))
    print(cache)
    print()


if __name__ == "__main__":
    main()
