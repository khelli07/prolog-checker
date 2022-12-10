import os

from swiplserver import PrologMQI

from check import check

f = open("solutions/queries.txt")
queries = [line.strip() for line in f if line.strip()]
ans_filenames = [
    fl for fl in os.listdir("answers") if fl.startswith("PP") and fl.endswith(".pl")
]

res = []
with PrologMQI() as mqi1:
    with PrologMQI() as mqi2:
        with mqi1.create_thread() as st:
            with mqi2.create_thread() as at:
                for ans_fn in ans_filenames:
                    print(f"Checking {ans_fn}..")
                    correct, _ = max(
                        check(queries, st, at, ans_fn, "praprak_cc.pl"),
                        check(queries, st, at, ans_fn, "praprak_sc.pl"),
                        key=lambda x: x[0],
                    )

                    res.append((ans_fn, correct))

os.system("clear")
# Summary
print("=" * 10, "Summary", "=" * 10)
for r in res:
    fn, correct = r
    print(fn, end=", ")
    print(f"Total score: {correct/len(queries) * 100} ({correct}/{len(queries)})")
