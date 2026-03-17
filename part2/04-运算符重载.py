#运算符实际上是调用类的方法的魔法方法

class MySequence(object):
    def __init__(self,*args):
        self.sequence=[]
        for arg in args:
            self.sequence.append(arg)
    def __or__(self,other):
        self.sequence.append(other)
        return self
    def run(self):
        for arg in self.sequence:
            print(arg)
class Test(object):
    def __init__(self,name):
        self.name=name
    def __or__(self,other):
        return MySequence(self,other)
    def __str__(self):
        return self.name

a=Test("a")
b=Test("b")
c=Test("c")
d=a|b|c
d.run()
print(d)
print(type(d))
