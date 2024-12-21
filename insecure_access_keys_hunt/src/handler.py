from iam.IamManager import IamManager
from utils.utils import get_age, generate_report, input_values
from typing import List, Dict


inputs = input_values()

def select_old_keys(
    access_keys: List[List[Dict[str, str]]], age_limit: int
) -> List[Dict[str, str]]:
    ages = []

    for key in access_keys:
        for key_metadata in key:
            if "CreateDate" in key_metadata:
                age = get_age(key_metadata)

                if age > age_limit:
                    ages.append(
                        {
                            "username": key_metadata["UserName"],
                            "key_age": age,
                            "key_id": key_metadata["AccessKeyId"],
                            "status": key_metadata["Status"],
                        }
                    )

    return ages


def main():
    iam: IamManager = IamManager(profile=inputs["profile"])

    users = iam.list_users()
    access_keys = iam.list_access_keys(users)
    old_keys = select_old_keys(access_keys, inputs["age"])
    print(old_keys, "OLD KEY")
    return old_keys


if __name__ == "__main__":
    old_keys = main()
    generate_report(old_keys, filename=f"report-{inputs['profile']}.csv")
