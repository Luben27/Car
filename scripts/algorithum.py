class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next

class struc:
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c
class BaseStackQueue:
    def push(self, data):
        raise NotImplemented
    def pop(self):
        raise NotImplemented
    def peek(self):
        raise NotImplemented
    def is_empty(self):
        raise NotImplemented
    def is_full(self):
        raise NotImplemented
    def display(self):
        raise NotImplemented
class ArrayStack(BaseStackQueue):
   def __init__(self, max_length=640*480):
     self.items = []
     self.top = -1  
     self.max_length = max_length

   def push(self, data):
     if not  self.is_full():  
         self.top += 1
         self.items.append(data)

   def pop(self):
     if not self.is_empty(): 
         data = self.items[self.top]
         del self.items[self.top]
         self.top -= 1
         return data
     else :
         return 0

   def peek(self):
     if not self.is_empty():
        return self.items[self.top] 
     else :
         return 0
   def is_empty(self):
        if self.top == -1:
            return 1
        else :
            return 0
   def top_return(self):
       return self.top
   def is_full(self):
        if (self.top == self.max_length):
            return 1
        else :
            return 0

   def display(self):
     for index in range(self.top):
       print(self.items[index])

class BaseQueue:
    def enqueue(self, data):
        raise NotImplemented
    def dequeue(self):
        raise NotImplemented
    def peek(self):
        raise NotImplemented
    def is_empty(self):
        raise NotImplemented
    def is_full(self):
        raise NotImplemented
    def display(self):
        raise NotImplemented

class ArrayQueue(BaseQueue):
   def __init__(self, max_length=640*480):
     self.front = -1
     self.rear = -1
     self.items = []
     self.max_length = max_length

   def enqueue(self, data):
     if not self.is_full():
         self.rear+=1
         self.items.append(data)
   def dequeue(self):
     if not self.is_empty():
         deq=self.items[0]
         del self.items[0]
         self.rear-=1
         return deq
     else :
         return 0
   def peek(self):
     if self.is_empty():
         return self.items[0]

   def is_empty(self):
     return self.front == self.rear

   def is_full(self):
     return self.rear == self.max_length-1

   def display(self):
     current = Node(None, self.front)
     while current.next:
       current = current.next
       print(current)
