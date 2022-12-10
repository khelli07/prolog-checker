from swiplserver import PrologThread


def check(queries, st: PrologThread, at: PrologThread, ans_fn: str, sol_fn: str):
    correct = 0
    st.query(f"consult('solutions/{sol_fn}')")
    at.query(f"consult('answers/{ans_fn}')")

    for query in queries:
        try:
            s = list_of_unique_dict(st.query(query))
            an = list_of_unique_dict(at.query(query))
            if s == an:
                correct += 1
        except Exception as e:
            print(e)

    return correct, sol_fn


def recheck(queries, st: PrologThread, at: PrologThread, ans_fn: str, sol_fn: str):
    correct = 0
    st.query(f"consult('solutions/{sol_fn}')")
    at.query(f"consult('answers/{ans_fn}')")

    for query in queries:
        try:
            s = list_of_unique_dict(st.query(query))
            an = list_of_unique_dict(at.query(query))
            if s != an:
                print("QUERY:", query)
                print("The solution should be: ")
                print(s)
                print("=" * 50)
                print("But the answer says: ")
                print(an)
                print("=" * 50, "\n")
            else:
                correct += 1
        except Exception:
            print(query)
            print(st.query(query))
            print(at.query(query))

    return correct, sol_fn


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
