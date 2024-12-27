from flint import fmpq, fmpq_mat


def cut(A, n):
    return fmpq_mat(n, n, [A[i][j, 0] for i in range(n) for j in range(n)])


def hcat(A, B):
    mA = A.ncols()
    n = A.nrows()
    assert B.nrows() == n
    mB = B.ncols()
    return A.__class__(
        n,
        mA + mB,
        [A[i, j] if j < mA else B[i, j - mA] for i in range(n) for j in range(mA + mB)],
    )


def vcat(A, B):
    m = A.ncols()
    assert B.ncols() == m
    nA = A.nrows()
    nB = B.nrows()
    return A.__class__(
        nA + nB,
        m,
        [A[i, j] if i < nA else B[i - nA, j] for i in range(nA + nB) for j in range(m)],
    )


def hcats(*xs):
    cur = xs[0]
    for nxt in xs[1:]:
        cur = hcat(cur, nxt)
    return cur


def vcats(*xs):
    cur = xs[0]
    for nxt in xs[1:]:
        cur = vcat(cur, nxt)
    return cur


def block(M):
    return vcats(*[hcats(*l) for l in M])


def zeros(m, n):
    return fmpq_mat(m, n)


def fresh(A):
    return 1 * A


def kron(A, B):
    nA = A.nrows()
    mA = A.ncols()
    nB = B.nrows()
    mB = B.ncols()
    m = mA * mB
    n = nA * nB
    return fmpq_mat(
        n,
        m,
        [A[i // nB, j // mB] * B[i % nB, j % mB] for i in range(n) for j in range(m)],
    )


def hvdot(A, B):
    return (A * B)[0, 0]


def valid(l, m, r):
    n = l.ncols()
    assert l.nrows() == 1
    assert r.ncols() == 1
    assert r.nrows() == n
    for a, ma in m.items():
        assert ma.nrows() == n
        assert ma.ncols() == n


class dep:
    def __init__(self, n):
        self.per = [None] * n
        self.alpha = fmpq_mat(n, 1)

    def step(self, s, w, v):
        for i in range(s):
            self.alpha[i, 0] = w[0, self.per[i]] / v[i][0, self.per[i]]
            w -= self.alpha[i, 0] * v[i]
        for ik, k in enumerate(w):
            if k != 0:
                self.alpha[s, 0] = 1
                self.per[s] = ik
                break
        return w


def stand(lam, mu, rho):
    # print(f">in-stand> {lam} {mu} {rho}")
    n = lam.ncols()
    rmu = {a: [] for a in mu}
    if all(x == 0 for x in lam):
        return (fmpq_mat(1, 0), dict(), fmpq_mat(0, 1))
    de = dep(n)
    lam = de.step(0, lam, None)
    r = 0
    s = 1
    v = [lam]
    while r < s:
        r += 1
        for a, M in mu.items():
            w = v[r - 1] * M
            w = de.step(s, w, v)
            rmu[a].append(fresh(de.alpha))
            if any(x != 0 for x in w):
                s += 1
                v.append(w)
    rlam = fmpq_mat(1, s, [1] + [0] * (s - 1))
    rrho = fmpq_mat(s, 1, [hvdot(v[i], rho) for i in range(s)])
    rmu = {a: cut(m, s) for (a, m) in rmu.items()}
    # print(f">out-stand> {rlam} {rmu} {rrho}")
    return (rlam, rmu, rrho)


def standmir(lam, mu, rho):
    rlam, rmu, rrho = stand(
        rho.transpose(), {a: m.transpose() for a, m in mu.items()}, lam.transpose()
    )
    return (
        rrho.transpose(),
        {a: m.transpose() for a, m in rmu.items()},
        rlam.transpose(),
    )


class ratser:
    def __init__(self, lam, mu, rho):
        self.l = lam
        self.m = mu
        self.r = rho
        valid(self.l, self.m, self.r)
        self.damin = None
        self.damize = None

    def value(self, u):
        v = self.l
        for a in u:
            v = v * self.m[a]
        return (v * self.r)[0, 0]

    def rank(self):
        s = self.minimize()
        return s.l.ncols()

    def null(self):
        return self.rank() == 0

    def triplet(self):
        return (self.l, self.m, self.r)

    def mizemini(self):
        if self.damize is None:
            s = stand(*self.triplet())
            self.damize = ratser(*standmir(*s))
        return self.damize

    def minimize(self):
        if self.damin is None:
            s = standmir(*self.triplet())
            self.damin = ratser(*stand(*s))
        return self.damin

    def poly(self, a):
        return self.m[a].minpoly()

    def __add__(self, other):
        if self.l.ncols() == 0:
            return other
        if other.l.ncols() == 0:
            return self
        (la, ma, ra) = self.triplet()
        (lb, mb, rb) = other.triplet()
        n = la.ncols()
        m = lb.ncols()
        l = block([[la, lb]])
        m = {a: block([[ma[a], zeros(n, m)], [zeros(m, n), mb[a]]]) for a in ma}
        r = block([[ra], [rb]])
        return ratser(l, m, r)

    def __rmul__(self, other):
        (l, m, r) = self.triplet()
        return ratser(other * l, m, r)

    def __mul__(self, other):
        (la, ma, ra) = self.triplet()
        (lb, mb, rb) = other.triplet()
        return ratser(kron(la, lb), {a: kron(ma[a], mb[a]) for a in ma}, kron(ra, rb))

    def __sub__(self, other):
        return self + (-1 * other)

    def __eq__(self, other):
        s = self - other
        return s.null()

    def __str__(self):
        s = ", ".join([f"{a}: {m}" for a, m in self.m.items()])
        return f"{self.l}, {'{'}{s}{'}'}, {self.r}"
