import csv
import datetime
import logging
import os
import configparser

from typing import Dict, Union


def get_age(key_metadata):
    age = datetime.datetime.now(datetime.timezone.utc) - key_metadata["CreateDate"]
    return age.days


def generate_report(keys, filename) -> None:
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UserName", "AccessKeyId", "CreateDate", "AgeDays"])

        for key in keys:
            writer.writerow(
                [key["username"], key["key_id"], key["status"], key["key_age"]]
            )


def input_values() -> Dict[str, Union[str, int]] | None:
    path = os.path.expanduser("~/.aws/credentials")
    logging.info(path, "caminho")
    
    config = configparser.ConfigParser()
    config.read(path)
    profiles = config.sections()
    if not profiles:
        logging.error("Nenhuma credencial foi encontrada")
        return None

    print("Perfis disponíveis")
    for index, profile in enumerate(profiles):
        print(f"{index + 1} {profile}")

    profile_chosen = int(input("Escolha o perfil pelo número: ")) - 1
    age_limit = int(input("Defina o limite de idade das chaves: "))

    if not (0 <= profile_chosen < len(profiles)):
        raise ValueError("Índice inválido")

    mapped_inputs: dict = {"age": age_limit, "profile": profiles[profile_chosen]}
    return mapped_inputs
