from random import sample

def get_tmp_name(length=12):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(sample(chars, length))

first = lambda x: x[list(x.keys())[0]]