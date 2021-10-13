def tupop(t1, t2, op):
    if op == 0:
        return tuple(int(a + b) for a, b in zip(t1, t2))
    elif op == 1:
        return tuple(int(a - b) for a, b in zip(t1, t2))
    elif op == 2:
        return tuple(int(a * b) for a, b in zip(t1, t2))
    elif op == 3:
        return tuple(int(a / b) for a, b in zip(t1, t2))
