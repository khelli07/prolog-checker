import json
import os
import shutil
from zipfile import ZipFile

import requests
from dotenv import load_dotenv

load_dotenv()

header = {"Authorization": os.environ["AUTH_TOKEN"]}
r = requests.get(
    "https://api-edunex.cognisia.id/course/task/answers?filter[task_id][is]=22230&page[limit]=0",
    headers=header,
    verify=False,
)

answers = json.loads(r.text)["data"]
urls = []

for ans in answers:
    url = ans["attributes"]["files"][0]["file"]
    zipfile = requests.get(url)
    filename = url[-17:].split(".")[0]

    open(f"zip/{filename}.zip", "wb").write(zipfile.content)

    try:
        with ZipFile(f"zip/{filename}.zip") as zobj:
            try:
                os.mkdir(f"zip/{filename}")
            except FileExistsError:
                pass

            zobj.extractall(path=f"zip/{filename}")
            shutil.copyfile(f"zip/{filename}/{filename}.pl", f"answers/{filename}.pl")
    except Exception:
        print(f"{filename} got error, please check manually.")
