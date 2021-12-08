import abc
from typing import Generic, TypeVar

"""
if you remove covariant=True you will get this warning
```
[Pyright reportGeneralTypeIssues] [E] Expression of type "SourceDerived" cannot be assigned to declared type "Source[Bass]"
  TypeVar "T_co@Source" is invariant
    "Derived" is incompatible with "Bass"
```

If you modify covariant to contravariant, this is what happened.
```
    def generate(self) -> T_co: <- warining
        pass

warining: [Pyright reportGeneralTypeIssues] [E] Contravariant type variable cannot be used in return type
  TypeVar "T_co@Source" is contravariant

```
"""
class Base:
    def foo(self):
        print("foo")

class Derived(Base):
    def bar(self):
        print("bar")

T_co = TypeVar('T_co', bound='Base', covariant=True)

class Source(Generic[T_co]):
    @abc.abstractmethod
    def generate(self) -> T_co:
        pass

class SourceBase(Source[Base]):
    def generate(self) -> Derived:
        return Derived() 

class SourceDerived(Source[Derived]):
    def generate(self) -> Derived:
        return Derived() 

source: Source[Base] = SourceDerived()
source.generate()

# try commenting out
#source_derived: Source[Derived] = SourceBase()
#source_derived.generate()


"""
remove contravariant=True will get warning
```
[Pyright reportGeneralTypeIssues] [E] Expression of type "SinkBase" cannot be assigned to declared type "Sink[Derived]"
  TypeVar "T_contra@Sink" is invariant
    "Base" is incompatible with "Derived"
```
"""
T_contra = TypeVar('T_contra', bound='Base', contravariant=True)
class Sink(Generic[T_contra]):
    @abc.abstractmethod
    def consume(self, value: T_contra):
        pass

class SinkBase(Sink[Base]):
    def consume(self, value: Base):
        value.foo()

class SinkDerived(Sink[Derived]):
    def consume(self, value: Derived):
        value.bar()

    def other_func(self):
        pass

base = Base()
derived = Derived()
sink_derived: Sink[Derived] = SinkBase()
# we can safely consumer
sink_derived.consume(base)
sink_derived.consume(derived)
# although you have annotated contravariant but you will get error if you call method of Sink[Derived], of course!
# sink_derived.other_func()
