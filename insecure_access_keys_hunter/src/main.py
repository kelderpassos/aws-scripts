from iam.IamManager import IamManager
from utils.utils import (
    access_key_scan,
    generate_report,
    get_age,
    get_delete_reply,
    print_separator,
)

replies = access_key_scan()
iam = IamManager(profile=replies.profile)


def get_old_keys():
    print_separator()
    print("Listando usuários e chaves de acesso...")
    users = iam.list_users()
    access_keys = iam.list_access_keys(users)

    old_keys = []

    for key in access_keys:
        for key_metadata in key:
            if "CreateDate" in key_metadata:
                age = get_age(key_metadata)

                if age > replies.age:
                    old_keys.append(
                        {
                            "username": key_metadata.get("UserName", "Unknown"),
                            "key_age": age,
                            "key_id": key_metadata.get("AccessKeyId", "Unknown"),
                            "status": key_metadata.get("Status", "Unknown"),
                        }
                    )

    if len(old_keys) == 0:
        print(f"Não há chaves mais velhas que {replies.age}")
    else:
        print(f"{len(old_keys)} chaves mais velhas que {replies.age} encontradas")

    return old_keys


def delete_old_keys(old_keys) -> None:
    for old_key in old_keys:
        iam.delete_access_keys(old_key)


if __name__ == "__main__":
    old_keys = get_old_keys()
    generate_report(old_keys, filename=f"report-{replies.profile}.csv")
    delete_reply = get_delete_reply()

    if delete_reply:
        delete_old_keys(old_keys)
    print("Script finalizado")
