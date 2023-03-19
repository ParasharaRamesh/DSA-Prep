import string

def caesarCipherEncryptor(message, shift):
    lower = list(string.ascii_lowercase)
    n = len(lower)
    encrypted = ""
    for char in message:
        index = lower.index(char)
        # we only need to go by remainder amount
        _, remainder = divmod(shift, n)
        toGo = n-1-index
        if remainder <= toGo:
            encrypted += lower[index + remainder]
        else:
            diff = remainder - toGo
            #i.e. from the beginning
            encrypted += lower[diff-1]

    return encrypted


if __name__ == '__main__':
    print(caesarCipherEncryptor("abc", 2))