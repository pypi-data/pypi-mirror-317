class ShowAccess:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.name in instance.__dict__:
            value = instance.__dict__[self.name]
            print(f"Get {self.name} = {value}")
            return value
        else:
            raise AttributeError(f"'{owner.__name__}' object has no attribute '{self.name}'")

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        print(f"Set {self.name} = {value}")

    def __delete__(self, instance):
        if self.name in instance.__dict__:
            value = instance.__dict__[self.name]
            print(f"Delete {self.name} = {value}")
            del instance.__dict__[self.name]
        else:
            raise AttributeError(f"'{type(instance).__name__}' object has no attribute '{self.name}'")

if __name__ == "__main__":
    class TestClass:
        attr = ShowAccess()

    obj = TestClass()
    obj.attr = 42
    print(obj.attr)
    del obj.attr