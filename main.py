from sponge import Sponge

def text2int(text):
    return int.from_bytes(text.encode('utf-8'), 'little')

M = '''
Lorem ipsum dolor sit amet,
consectetur adipiscing elit.
Ut malesuada nisl id nibh commodo,
sed pharetra sem tempus.
In ut ligula non purus sollicitudin porttitor.
Etiam facilisis semper magna eu blandit. Quisque. 
'''

# swap left and right parts of the S
def exampleF(value, bitcap):
    bitcap = int(bitcap / 2)
    leftS = value >> bitcap
    rightS = value & ((1 << bitcap) - 1)
    return (rightS << bitcap) | leftS

# instead of exampleF 3 arg can be any other mixing function
sponge = Sponge(16, 64, lambda x: exampleF(x, 80))

# hash quality depend on exampleF implementation
print(sponge.operate(text2int(M), 16))