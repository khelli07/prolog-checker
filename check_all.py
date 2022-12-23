import os

from swiplserver import PrologMQI

from check import check

# 13521041 - 13521066
tmp = sorted(os.listdir("answers"))
ans_filenames = [fl for fl in tmp if fl.startswith("PP") and fl.endswith(".pl")][
    29 : 29 + 26
]

res = []
with PrologMQI() as mqi1:
    with PrologMQI() as mqi2:
        with mqi1.create_thread() as st:
            with mqi2.create_thread() as at:
                for ans_fn in ans_filenames:
                    f = open(f"answers/{ans_fn}")
                    if "elonMusk" and "vanRossum" in f.read():
                        checker = "praprak_cc.pl"
                    else:
                        checker = "praprak_sc.pl"

                    total_score, list_score, sol_fn = check(
                        st, at, ans_fn, checker, verbose=1
                    )

                    print(f"Checking {ans_fn}")
                    if "dynamic" in f.read():
                        print("Did bonus, please check.")
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
