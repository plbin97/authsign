import random
import string

jwtSecret = ''.join(random.choices(string.ascii_letters, k=8))
