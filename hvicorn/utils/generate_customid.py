from string import ascii_letters, digits
from random import choice

generate_customid = lambda: "".join([choice(ascii_letters + digits) for _ in range(6)])
