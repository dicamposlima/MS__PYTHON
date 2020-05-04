"""
Initial file
"""
v = 123.45434546324
r = f'{v:_^40.2f}'
print(r)

lista = [1, 2, 3, 4]
print(list(map(str, lista)))

print()
import hashlib


print('diêgo'.encode('latin1'))

with open('teste.txt', 'a') as file:
    file.write(f'hello\n')
with open('teste.txt') as file:
    f = file.readlines()
    print(lambda: v for v in f)

class T():
    def __init__(self, valor):
        self.valor = valor
    def __repr__(self):
        return 'class T'
    def __len__(self):
        return 10
    def __str__(self):
        return 'str str'

tc = T(10)
print(repr(tc))
print(tc.__dict__)


class Node:
    def __init__(self):
        pass
    @staticmethod
    def get_transaction_value():
        return 'sdsadasdsadsad'

print(Node.get_transaction_value())