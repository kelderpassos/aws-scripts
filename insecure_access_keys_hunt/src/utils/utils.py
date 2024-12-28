import configparser
import csv
import datetime
import logging
import os
from typing import Dict, Union


def get_age(key_metadata):
    age = datetime.datetime.now(datetime.timezone.utc) - key_metadata["CreateDate"]
    return age.days


def generate_report(keys, filename) -> None:
    try:
        current_directory = os.getcwd()
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["UserName", "AccessKeyId", "CreateDate", "AgeDays"])

            for key in keys:
                writer.writerow(
                    [key["username"], key["key_id"], key["status"], key["key_age"]]
                )
        print(f"Relatório {filename} gerado com sucesso no caminho {current_directory}")
    except PermissionError as e:
        logging.error(f"Erro de permissão ao escrever o arquivo {filename}: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao gerar o relatório: {e}")


def input_values(delete = 2) -> Dict[str, Union[str, int | bool]]:
    try:
        path = os.path.expanduser("~/.aws/credentials")

        config = configparser.ConfigParser()
        config.read(path)
        profiles = config.sections()
        if not profiles:
            logging.error(
                "Nenhuma credencial foi encontrada. Verifique o caminho ~/.aws/credentials"
            )
            exit(1)

        print("Perfis encontrados. Escolha um pelo número:")
        for index, profile in enumerate(profiles):
            print(f"{index + 1} {profile}")

        profile_chosen = int(input()) - 1
        if not (0 <= profile_chosen < len(profiles)):
            logging.error("Índice inválido")
            exit(1)

        age_limit = int(input("Defina o limite de idade das chaves em dias: "))

        # TODO terminar esta parte
        print("Gostaria de apagar as chaves encontradas? Esta ação não pode ser desfeita")
        print("1 - sim")
        print("2 - não")
        to_delete = int(input())

        if delete == to_delete:
            return {"age": age_limit, "profile": profiles[profile_chosen], "to_delete": to_delete}
            
        return {"age": age_limit, "profile": profiles[profile_chosen]}
    except ValueError as e:
        logging.error(f"Erro de entrada do usuário: {e}")
        exit(1)
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        exit(1)
