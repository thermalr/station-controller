class FifoList:
    def __init__(self):
        self.data = []
    def append(self, data):
        self.data.append(data)
    def pop(self):
        return self.data.pop(0)
        
if __name__=='__main__':  # Run a test/example when run as a script:
    a = FifoList(  )
    a.append(10)
    a.append(20)
    print(a.pop( ))
    a.append(5)
    print(a.pop())
    print(a.pop())