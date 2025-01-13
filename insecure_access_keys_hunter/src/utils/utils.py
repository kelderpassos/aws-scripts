import configparser
import csv
import datetime
import logging
import os
from dataclasses import dataclass


@dataclass
class InputValues:
    age: int
    profile: str | None


def print_separator():
    print("---------------------------")


def get_age(key_metadata):
    age = datetime.datetime.now(datetime.timezone.utc) - key_metadata["CreateDate"]
    return age.days


def access_key_scan() -> InputValues:
    path = os.path.expanduser("~/.aws/credentials")

    config = configparser.ConfigParser()
    config.read(path)
    profiles = config.sections()

    if not profiles:
        raise RuntimeError(
            "Nenhuma credencial foi encontrada. Verifique o caminho ~/.aws/credentials"
        )

    print("Perfis encontrados. Escolha um pelo número:")
    for index, profile in enumerate(profiles):
        print(f"{index + 1} - {profile}")

    try:
        profile_chosen = int(input()) - 1
        if not (0 <= profile_chosen < len(profiles)):
            raise ValueError("Índice inválido")

        age_limit = int(input("Defina o limite de idade das chaves em dias: "))
        return InputValues(age=age_limit, profile=profiles[profile_chosen])
    except ValueError as e:
        logging.error(f"Erro de entrada do usuário: {e}")
        raise


def generate_report(keys, filename) -> None:
    current_directory = os.getcwd()
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["UserName", "AccessKeyId", "Status", "AgeDays"])

            for key in keys:
                writer.writerow(
                    [key["username"], key["key_id"], key["status"], key["key_age"]]
                )
        print_separator()
        print(f"Relatório {filename} gerado com sucesso no caminho {current_directory}")
    except PermissionError as e:
        logging.error(f"Erro de permissão ao escrever o arquivo {filename}: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao gerar o relatório: {e}")


def get_delete_reply() -> bool:
    print_separator()
    print("Deseja apagar as chaves encontradas? (1 - Sim, 2 - Não)")

    try:
        return int(input().strip()) == 1
    except ValueError:
        logging.error("Escolha 1 ou 2 para responder")
        return False
