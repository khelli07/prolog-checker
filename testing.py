from swiplserver import PrologMQI

from check import *

with PrologMQI() as mqi:
    with mqi.create_thread() as pt:
        pt.query("consult('solutions/praprak_sc.pl')")
        result = pt.query("swap([0,1,2],3,1,X)")
        result = list_of_unique_dict(result)
        print(result)
