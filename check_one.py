import argparse
import os

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
                with open(f"answers/{ans_fn}") as f:
                    if "elonMusk" and "vanRossum" in f.read():
                        checker = "praprak_cc.pl"
                    else:
                        checker = "praprak_sc.pl"

                total_score, list_score, sol_fn = check(
                    st, at, ans_fn, checker, verbose=1
                )

                print(f"Checking {ans_fn}")
                with open(f"answers/{ans_fn}") as f:
                    if "dynamic" in f.read():
                        print("Did bonus, please check.")

                print("Done checking", ans_fn, end=", ")
                print("Checked with", sol_fn)
                print("=" * 50)
                print(f"Total score: {total_score} ({list_score})")
