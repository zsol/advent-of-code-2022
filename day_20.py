import sys
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Node:
    value: int
    next: "Node"
    prev: "Node"
    head: ClassVar["Node"]

    def append(self, value: int) -> None:
        tail = self.head.prev
        tail.next = Node(value, next=self.head, prev=tail)
        self.head.prev = tail.next

    def unlink(self, forward: bool = True) -> "Node":
        next = self.next
        prev = self.prev
        if next is prev:
            raise ValueError("Can't unlink from singleton list")
        if self is self.head:
            type(self).head = next if forward else prev
        next.prev = prev
        prev.next = next
        return self

    def insert_before(self, new_node: "Node") -> None:
        new_node.next = self
        new_node.prev = self.prev
        if self is self.head:
            type(self).head = new_node
        self.prev.next = new_node
        self.prev = new_node

    def shift(self, by: int, length: int) -> None:
        by = by % length if by >= 0 else -(abs(by) % length)
        if by == 0:
            return
        target = self
        forward = by > 0
        if forward:
            while by >= 0:
                target = target.next
                by -= 1
        else:
            while by < 0:
                target = target.prev
                by += 1
        node = self.unlink(forward)
        target.insert_before(node)

    def __str__(self) -> str:
        ret = "["
        cur = self.head
        ret += str(cur.value)
        cur = cur.next
        while cur is not self.head:
            ret += f", {cur.value}"
            cur = cur.next
        ret += "]"
        return ret


def main() -> None:
    numbers: list[Node] = []
    ll: Node | None = None
    second = sys.argv[1] == "2"
    multiplier = 811589153 if second else 1
    while line := sys.stdin.readline().rstrip():
        value = int(line) * multiplier
        if not ll:
            ll = Node(value, None, None)  # type: ignore
            ll.next = ll
            ll.prev = ll
            Node.head = ll
        else:
            ll.append(value)
        numbers.append(Node.head.prev)

    for _ in range(10 if second else 1):
        for node in numbers:
            node.shift(node.value, len(numbers) - 1)

    reordered_numbers: list[int] = []
    for start_node in numbers:
        if start_node.value == 0:
            break

    reordered_numbers.append(start_node.value)
    start_node = start_node.next
    while start_node.value != 0:
        reordered_numbers.append(start_node.value)
        start_node = start_node.next
    score = 0
    for ind in [1000, 2000, 3000]:
        score += (foo := reordered_numbers[ind % len(reordered_numbers)])
    print(score)


if __name__ == "__main__":
    main()
