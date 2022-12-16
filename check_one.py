import argparse

from swiplserver import PrologMQI

from check import check

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--answer", default="")
ans_fn = parser.parse_args().answer

if not ans_fn:
    raise Exception("File not specified")

with PrologMQI() as mqi1:
    with PrologMQI() as mqi2:
        with mqi1.create_thread() as st:
            with mqi2.create_thread() as at:
                _, _, sol_fn = max(
                    check(st, at, ans_fn, "praprak_cc.pl"),
                    check(st, at, ans_fn, "praprak_sc.pl"),
                    key=lambda x: x[0],
                )

                total_score, list_score, sol_fn = check(
                    st, at, ans_fn, sol_fn, verbose=1
                )

                print("Done checking", ans_fn, end=", ")
                print("Checked with", sol_fn)
                print("=" * 50)
                print(f"Total score: {total_score} ({list_score})")
