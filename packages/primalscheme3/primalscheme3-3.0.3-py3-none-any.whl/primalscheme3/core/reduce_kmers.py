# This can be expanded to be mutation specific
def primer_dist(s1: str, s2: str, dist_3p=5, score_3p=10) -> int:
    """
    Returns a score of primer similarity. If the mutation is within the last `dist_3p` bases, the score is 1 * `score_3p`
    """
    score = 0
    for index, (x, y) in enumerate(zip(s1[::-1], s2[::-1])):
        if x != y:
            if index < dist_3p:
                score += score_3p
            else:
                score += 1

    return score


class CloudSequence:
    seq: str
    count: float
    thermo_result: THERMORESULT | None

    def __init__(self, seq: str, count: float):
        self.seq = seq
        self.count = count
        self.thermo_result = None

    def thermo_check(self, config: Config) -> THERMORESULT:
        """
        Checks the thermo properties of the sequence
        """
        if self.thermo_result is None:
            self.thermo_result = thermo_check(self.seq, config)
        return self.thermo_result

    def __hash__(self) -> int:
        return hash(self.seq)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, CloudSequence):
            return False
        return self.seq == value.seq


def reduce_kmers(
    seqs: list[CloudSequence], config: Config, merge_score=1
) -> set[CloudSequence]:
    """
    Reduces a set of DNA sequences by clustering them  based on their 3' end, and then minimizing the edit distance between
    all tails within the same 3' cluster. The resulting set of sequences will have at most `max_edit_dist` differences
    between any two sequences, and will all have a common 3' end of length `end_3p`.

    Args:
        seqs: A set of DNA sequences to be reduced.
        max_edit_dist: The maximum edit distance allowed between any two sequences in the same 3' cluster. Defaults to 1.
        end_3p: The length of the 3' end to use for clustering. Defaults to 6.

    Returns:
        A set of reduced DNA sequences, where each sequence has a common 3' end of length `end_3p`, and at most
        `max_edit_dist` differences between any two sequences.
    """
    ## Cluster sequences via the 3p end
    g = nx.Graph()
    # Add nodes and count
    g.add_nodes_from([(seq, {"count": seq.count}) for seq in seqs if seq.count])

    # Use a dict for memoization
    scores: dict[tuple[CloudSequence, CloudSequence], int] = {}
    for s1, s2 in itertools.combinations(seqs, 2):
        # No need to compare the same sequence
        if s1 == s2:
            continue
        pair = tuple(sorted((s1, s2), key=lambda x: x.seq))
        if pair in scores:
            continue
        scores[pair] = primer_dist(s1.seq, s2.seq)  # type: ignore

    # Add edges onto the graph
    for (s1, s2), score in scores.items():
        if score * s1.count <= merge_score:
            g.add_edge(s1, s2)
        if score * s2.count <= merge_score:
            g.add_edge(s2, s1)

    # Sets to keep track of included and accounted sequences
    included_seqs: set[CloudSequence] = set()
    accounted_seqs: set[CloudSequence] = set()

    # Get the most common sequence
    nodes = sorted(g.nodes(data=True), key=lambda x: x[1].get("count", 0), reverse=True)

    for node, _attr_dict in nodes:
        # Check if node is thermo failed
        if node.thermo_check(config) != THERMORESULT.PASS:
            continue

        # If sequence is already included or accounted for skip
        if node in accounted_seqs or node in included_seqs:
            continue

        # If the sequence is not accounted for
        included_seqs.add(node)  # Add
        # Add all the neighbors into accounted seqs
        for neighbors in g.neighbors(node):
            accounted_seqs.add(neighbors)

    print(
        "covered",
        sum([x.count for x in included_seqs] + [x.count for x in accounted_seqs]),
        "/",
        sum([x.count for x in seqs]),
    )

    return included_seqs


class Test_ReduceKmers(unittest.TestCase):
    config = Config()

    def test_reduce_kmers(self):
        """
        Tests seqs are merged if low count + low edit distance
        """
        seqs = [
            CloudSequence("CAATGGTGCGAAAGGTATAATCATTAATGT", 10),
            CloudSequence("AAATGGTGCGAAAGGTATAATCATTAATGT", 1),
        ]

        expected = [seqs[0]]
        result = reduce_kmers(
            seqs,
            self.config,
            1,
        )
        self.assertEqual(expected, list(result))

    def test_reduce_kmers_3p_mut(self):
        """
        Tests seqs are not merged if the 3' end is different
        """
        seqs = [
            CloudSequence("ATCAGAGGCTGCTCGTGTTGTA", 10),
            CloudSequence("ATCAGAGGCTGCTCGTGTTGTT", 1),
        ]
        seqs.sort(key=lambda x: x.seq)

        result = reduce_kmers(
            seqs,
            self.config,
            1,
        )
        self.assertEqual(seqs, sorted(result, key=lambda x: x.seq))

    def test_reduce_kmers_large_edit(self):
        """
        Tests sequences are not merged if the edit distance is to large. Not in 3p
        """
        seqs = [
            CloudSequence("GTAGAGAGGCTGCTCGTGTTGTA", 10),
            CloudSequence("ATCAGAGGCTGCTCGTGTTGTA", 1),
        ]
        seqs.sort(key=lambda x: x.seq)

        result = reduce_kmers(
            seqs,
            self.config,
            1,
        )
        self.assertEqual(seqs, sorted(result, key=lambda x: x.seq))
