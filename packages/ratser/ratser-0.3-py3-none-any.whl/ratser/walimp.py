from ratser import ratser
from flint import fmpq_mat


def from_walnut(f):
    inside = False
    acc = []
    cur = None
    data = dict()
    for l in f:
        s = l.strip()
        if inside:
            acc.append(list(map(int, s[s.rindex("[") + 1 : s.index("]")].split(","))))
            if ")" in s:
                inside = False
                data[cur] = acc
        else:
            if ":=" in s and "(" in s[s.index(":") :]:
                cur = s[: s.index(":")].strip()
                s = s[s.index("(") :]
                if ")" in s:
                    data[cur] = list(
                        map(int, s[s.rindex("[") + 1 : s.index("]")].split(","))
                    )
                else:
                    acc = [
                        list(map(int, s[s.rindex("[") + 1 : s.index("]")].split(",")))
                    ]
                    inside = True
    n = len(data["v"])
    s = fmpq_mat(1, n, data.pop("v"))
    t = fmpq_mat(n, 1, data.pop("w"))
    m = dict()
    k = 1
    for u, mu in data.items():
        assert u[:2] == "M_"
        k = (len(u.split("_")) - 1) // 2
        if k > 1:
            a = tuple(u.split("_")[-k:])
        else:
            a = u.split("_")[-1]
        m[a] = fmpq_mat(n, n, sum(mu, []))
    mz = m[tuple("0" * k)] if k > 1 else m["0"]
    for _ in range(n):
        s *= mz
    return ratser(s, m, t)
