# This script contains tools to polish the output of the primal scheme.

from primaldimer_py import which_kmers_pools_interact  # type: ignore

from primalscheme3.core.classes import FKmer, PrimerPair, RKmer


def find_interactions(
    pool: list[PrimerPair], primerpair: PrimerPair, threshold: float, calc_all=True
) -> list[PrimerPair]:
    """Find all interactions between pools"""
    interacting_kmers: list[tuple[FKmer | RKmer, FKmer | RKmer]] = (
        which_kmers_pools_interact(
            [kmer for kmers in (pp.kmers() for pp in pool) for kmer in kmers],
            [*primerpair.kmers()],
            threshold,
            calc_all,
        )
    )

    # map the interacting kmers to the primer pairs
    # TODO speed up this part
    interacting_primerpairs = []
    for kmer1, kmer2 in interacting_kmers:
        if kmer1 in primerpair.kmers():
            interacting_primerpairs.extend([pp for pp in pool if kmer2 in pp.kmers()])
        elif kmer2 in primerpair.kmers():
            interacting_primerpairs.extend([pp for pp in pool if kmer1 in pp.kmers()])
    return interacting_primerpairs


if __name__ == "__main__":
    fkmer = FKmer(10, ["TGGAAATACCCACAAGTTAATGGTTTAAC"])
    rkmer = RKmer(100, ["ACACCTGTGCCTGTTAAACCAT"])

    pp = PrimerPair(fkmer, rkmer, 0)
    print(
        [kmer for kmers in (pp.kmers() for pp in [pp]) for kmer in kmers],
    )

    interaction = which_kmers_pools_interact([fkmer, rkmer], [*pp.kmers()], -26, True)
