import os

from swiplserver import PrologMQI

from check import check, recheck

f = open("solutions/queries.txt")
queries = [line.strip() for line in f if line.strip()]
ans_filenames = [
    fl for fl in os.listdir("answers") if fl.startswith("PP") and fl.endswith(".pl")
]

ans_fn = "PP01_13500000.pl"  # CHANGE THIS

with PrologMQI() as mqi1:
    with PrologMQI() as mqi2:
        with mqi1.create_thread() as st:
            with mqi2.create_thread() as at:
                correct, sol_fn = max(
                    check(queries, st, at, ans_fn, "praprak_cc.pl"),
                    check(queries, st, at, ans_fn, "praprak_sc.pl"),
                    key=lambda x: x[0],
                )

                print("Done checking", ans_fn, end=", ")
                print("Checked with", sol_fn)
                print("=" * 10, "FALSE", "=" * 10)
                recheck(queries, st, at, ans_fn, sol_fn)
                print("=" * 50)
                print(
                    f"Total score: {correct/len(queries) * 100} ({correct}/{len(queries)})"
                )
