import random


async def generate_invite_code():
    lowercase_chars = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    symbols = '!@#$%^&*?'
    numbers = '123456789'

    chars = lowercase_chars + uppercase_chars + symbols + numbers

    invite_code = str()

    for i in range(20):
        invite_code += random.choice(chars)

    return invite_code
