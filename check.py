from swiplserver import PrologThread

PART1_FN = "bagian1.txt"
PART2_FN = "bagian2.txt"
PART3_FN = "bagian3.txt"

PART1_WEIGHT = 20
PART2_WEIGHT = 40
PART3_WEIGHT = 40

FN_WEIGHT = [
    (PART1_FN, PART1_WEIGHT),
    (PART2_FN, PART2_WEIGHT),
    (PART3_FN, PART3_WEIGHT),
]


def check(
    st: PrologThread, at: PrologThread, ans_fn: str, sol_fn: str, verbose: bool = 0
):
    st.query(f"consult('solutions/{sol_fn}')")
    at.query(f"consult('answers/{ans_fn}')")

    total_score = 0
    list_score = []
    i = 1
    for fn, weight in FN_WEIGHT:
        if verbose:
            print("=" * 10, f"PART {i}", "=" * 10)

        score = check_helper(fn, weight, st, at, verbose)
        list_score.append(score)
        total_score += score

        if verbose:
            print(f"=== END OF PART {i}", "==" * 5, "\n")
        i += 1

    return round(total_score, 2), list_score, sol_fn


def check_helper(
    filename: str,
    weight: int,
    st: PrologThread,
    at: PrologThread,
    verbose: bool = 0,
):
    correct = 0

    f = open(f"solutions/{filename}")
    queries = [line.strip() for line in f if line.strip()]
    for query in queries:
        try:
            s = list_of_unique_dict(st.query(query))
            an = list_of_unique_dict(at.query(query))
            if verbose and s != an:
                print("QUERY:", query)
                print("The solution should be: ")
                print(s)
                print("But the answer says: ")
                print(an)
                print("=" * 28, "\n")
            else:
                correct += 1
        except Exception:
            if verbose:
                print("Error occured")
                print(query)
                try:
                    at.query(query)
                except Exception as e:
                    print(str(e))
                    print("Answer got wrong")
                try:
                    st.query(query)
                except Exception as e:
                    print(str(e))
                    print("Solution got wrong")
                print("=" * 20)

    score = (correct / len(queries)) * weight
    return score


def list_of_unique_dict(res: dict):
    if type(res) == bool:
        return []

    li = []
    for r in res:
        if r not in li:
            tmp = []
            for key, val in r.items():
                tmp.append((key, val))
            if tmp not in li:
                li.append(tmp)

    return sorted(li)
