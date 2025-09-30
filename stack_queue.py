class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, obj):
        self.items.append(obj)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, obj):
        self.items.append(obj)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def size(self):
        return len(self.items)


class PriorityQueue:
    def __init__(self):
        self.items = []

    def insert(self, value, priority):
        self.items.append((value, priority))

    def extract_max(self):
        if not self.items:
            return None
        max_idx = 0
        for i in range(1, len(self.items)):
            if self.items[i][1] > self.items[max_idx][1]:
                max_idx = i
        return self.items.pop(max_idx)

    def peek_max(self):
        if not self.items:
            return None
        max_idx = 0
        for i in range(1, len(self.items)):
            if self.items[i][1] > self.items[max_idx][1]:
                max_idx = i
        return self.items[max_idx]

    def is_empty(self):
        return len(self.items) == 0




        