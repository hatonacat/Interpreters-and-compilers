class A:
    def __init__(self):
        self.a = 2
        self.b = 3

    def add_one(self, x):
        return x+1
    
    def add_two(self, x):
        return x+2


if __name__ == "__main__":
    my_instance = A()
    user_input = input("> ")
    result = getattr(my_instance, user_input)
    print(result)
    print(result(1))