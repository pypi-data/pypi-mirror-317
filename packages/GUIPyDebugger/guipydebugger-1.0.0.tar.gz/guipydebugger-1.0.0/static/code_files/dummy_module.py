class SomeClass:
    '''
        Trying to see if cleandoc will work?
        Is it working?
        How about now?
    '''
    class_var = "can you read me?"
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def exp_x(self, x) -> int:
        return x * x
    
    def exp_y(self, y) -> int:
        return y * y
    
someClass = SomeClass(10, 20)