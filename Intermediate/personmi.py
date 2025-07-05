#! /usr/bin/env python3.13
'''
Implement the following class structure: print(Child.__mro__):
(<class '__main__.Child'>,
 <class '__main__.Father'>,
 <class '__main__.Mother'>,
 <class '__main__.Person'>,
 <class 'object'>)

Each class has the following string representation:
person = Person()
dad = Father()
mom = Mother()
child = Child()

print(person)
print(dad)
print(mom)
print(child)

Output:
I am a person
I am a person and cool daddy
I am a person and awesome mom
I am the coolest kid

You should use inheritance here, so the I am a person substring should only
occur in the Person base class.


Layout:

    Person
    //  \\
   //    \\
Father  Mother
   \\    //
    \\  //
    Child
'''


from pprint import pformat


class Person:
    def __repr__(self) -> str:
        return f'Person({id(self)})'

    def __str__(self) -> str:
        return 'I am a person'


class Father(Person):
    def __repr__(self) -> str:
        return f'Father({id(self)})'

    def __str__(self) -> str:
        return f'{super().__str__()} and cool daddy'


class Mother(Person):
    def __repr__(self) -> str:
        return f'Mother({id(self)})'

    def __str__(self) -> str:
        return f'{super().__str__()} and awesome mom'


class Child(Father, Mother):
    def __repr__(self) -> str:
        return f'Child({id(self)})'

    def __str__(self) -> str:
        return 'I am the coolest kid'


if __name__ == '__main__':
    person = Person()
    father = Father()
    mother = Mother()
    child = Child()

    print(f'Child.__mro__:\n{pformat(Child.__mro__)}')
    for obj in person, father, mother, child:
        print(f'{obj.__class__}:  {obj}')
