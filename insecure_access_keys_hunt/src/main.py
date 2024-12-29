from typing import Dict, List

from iam.IamManager import IamManager
from utils.utils import generate_report, get_age, input_values

inputs = input_values()
iam = IamManager(profile=inputs.profile)

def select_old_keys(
    access_keys: List[List[Dict[str, str]]], age_limit: int
) -> List[Dict[str, str]]:
    ages = []

    for key in access_keys:
        for key_metadata in key:
            if "CreateDate" in key_metadata:
                age = get_age(key_metadata)

                if age < age_limit:  # TODO ALTERAR SINAL DE MENOR PARA SINAL DE MAIOR
                    ages.append(
                        {
                            "username": key_metadata["UserName"],
                            "key_age": age,
                            "key_id": key_metadata["AccessKeyId"],
                            "status": key_metadata["Status"],
                        }
                    )

    return ages


def get_old_keys():

    print("Listando usuários e chaves de acesso...")
    users = iam.list_users()

    access_keys = iam.list_access_keys(users)
    old_keys = select_old_keys(access_keys, inputs["age"])

    day = "dia"
    chave = "chave"
    if inputs["age"] > 1:
        day = "dias"

    print(inputs, "INPUTS")

    if len(old_keys) == 0:
        print(f"Não há chaves mais velhas que {inputs['age']} {day}")
    else:
        print(
            f"{len(old_keys)} {chave} mais velhas que {inputs['age']} {day} encontradas"
        )

    

    return old_keys


if __name__ == "__main__":
    old_keys = get_old_keys()
    generate_report(old_keys, filename=f"report-{inputs.profile}.csv")
