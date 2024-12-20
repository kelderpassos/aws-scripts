from iam.IamManager import IamManager
from utils.utils import get_age


NINETY = 90
iam = IamManager()

def select_old_keys(access_keys):
    ages = []

    for key in access_keys:
        for key_metadata in key:
            print(key_metadata, 'key')
            age = get_age(key_metadata)

            # TODO: completar o objeto com as infos sobre as chaves antigas
            if age > NINETY:
                ages.append({
                    'User': key_metadata['UserName'],
                    # 'Key_age'
                })
    
    return ages

# TODO: considerar mudar o nome da função visto que talvez ela não seja uma Lambda
def handler():
    users = iam.list_users()
    access_keys = iam.list_access_keys(users)
    old_key = select_old_keys(access_keys)

    print(old_key, "OLD KEY")

# TODO: agregar pandas para geração de relatório

if __name__ == "__main__":
    handler()
