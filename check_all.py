import os

from swiplserver import PrologMQI

from check import check

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
                    _, _, sol_fn = max(
                        check(st, at, ans_fn, "praprak_cc.pl", verbose=0),
                        check(st, at, ans_fn, "praprak_sc.pl", verbose=0),
                        key=lambda x: x[0],
                    )

                    total_score, list_score, sol_fn = check(
                        st, at, ans_fn, sol_fn, verbose=1
                    )

                    res.append((ans_fn, total_score, list_score))
                    print(f"Total score: {total_score} ({list_score})")
                    cont = input("Continue?(Y/N) ")
                    if cont.lower() != "y":
                        break

os.system("clear")
# Summary
print("=" * 10, "Summary", "=" * 10)
for r in res:
    fn, total_score, list_score = r
    print(fn, end=", ")
    print(f"Total score: {total_score} ({list_score})")
