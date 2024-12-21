import datetime
import csv

from typing import Dict, Union

def get_age(key_metadata):
    age = datetime.datetime.now(datetime.timezone.utc) - key_metadata['CreateDate']
    return age.days


# : Dict[str, Union[str | datetime.datetime]]
def generate_report(keys, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        print(writer, writer)
        writer.writerow(["UserName", "AccessKeyId", "CreateDate", "AgeDays"])

        for key in keys:
            writer.writerow([key["username"], key["key_id"], key["status"], key["key_age"]])