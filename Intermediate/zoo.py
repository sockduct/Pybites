#! /usr/bin/env python3.13
'''
Finish the Animal class below adding one or more class variables and a
classmethod so that the following code:
dog = Animal('dog')
cat = Animal('cat')
fish = Animal('fish')
lion = Animal('lion')
mouse = Animal('mouse')
print(Animal.zoo())

...produces the following output:
10001. Dog
10002. Cat
10003. Fish
10004. Lion
10005. Mouse

Few things to note here:
* The sequencing starts at 10000
* Each animal gets title cased
* An individual animal should print the sequence+name string

Best to implement the __str__ method on the class.

Making another animal at this point, the following should work:
horse = Animal('horse')
assert str(horse) == "10006. Horse"

This is what the pytest code tests when you submit your code.

Have fun and code more Python! Join our growing developer Circle community to
learn together with other passionate Pythonistas...
'''


from __future__ import annotations


class Animal:
    sequence = 10_000
    members: dict[str, int] = {}

    def __init__(self, name: str) -> None:
        self.name = name
        Animal.sequence += 1
        Animal.members[name] = Animal.sequence

    def __str__(self) -> str:
        return f'{Animal.members[self.name]}. {self.name.title()}'

    @classmethod
    def zoo(cls: type[Animal]) -> str:
        return '\n'.join(
            f'{sequence}. {animal.title()}' for animal, sequence in Animal.members.items()
        )


if __name__ == '__main__':
    dog = Animal('dog')
    cat = Animal('cat')
    fish = Animal('fish')
    lion = Animal('lion')
    mouse = Animal('mouse')
    print(Animal.zoo())

    horse = Animal('horse')
    assert str(horse) == "10006. Horse"
