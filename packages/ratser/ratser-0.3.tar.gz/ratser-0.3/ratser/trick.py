from .intmap import mapper


def trick(s):
    m = mapper()
    st = dict()
    todo = [s.l]
    while todo:
        cur = todo.pop()
        q = m[tuple(cur)]
        if q not in st:
            img = dict()
            for a in s.m.keys():
                nxt = cur * s.m[a]
                qq = m[tuple(nxt)]
                img[a] = qq
                if qq not in st:
                    todo.append(nxt)
            st[q] = (img, (cur * s.r)[0, 0])
    return st


def arity(v):
    if isinstance(v, str):
        return 1
    return len(v)


def pretty(v):
    if isinstance(v, str):
        return v
    return " ".join(v)


def to_walnut(st, ns, f):
    n = len(st)
    k = arity(list(st[0][0].keys())[0])
    f.write(" ".join([ns] * k) + "\n")
    for s in range(n):
        (m, o) = st[s]
        f.write(f"\n{s} {o}\n")
        for v in sorted(m.keys()):
            f.write(f"{pretty(v)} -> {m[v]}\n")
