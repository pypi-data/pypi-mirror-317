from . import ratser
from flint import fmpq_mat, fmpq
from .trick import trick, to_walnut
from .walimp import from_walnut
from sys import argv


def main_trick():
    if len(argv) != 4:
        print(f"usage: {argv[0]} input_file.mpl numeration_system output_file.txt")
        exit(1)
    mpl = argv[1]
    ns = argv[2]
    name = argv[3]
    with open(mpl) as f:
        s = from_walnut(f)
    t = s.minimize()
    print(f"Rank: {t.rank()}")
    st = trick(t)
    print(f"{len(st)} states")
    print("values:", sorted(list(set(x[1] for _, x in st.items()))))
    with open(name, "w") as f:
        to_walnut(st, ns, f)
    print("Done!")
