class A:
    def greet(self) -> str: 
        return "A"
class B(A):
    def greet(self) -> str: 
        return "B"
class C(A):
    def greet(self) -> str: 
        return "C"
class D(C, B):     # multiple inheritance (the diamond)
    pass

print(D().greet())   # 'B'   ← MRO picks B (left before right)
print([c.__name__ for c in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']   ← the exact, predictable search path
