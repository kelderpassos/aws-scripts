from secrets_manager.Secrets_Manager import SecretsManager
from constants import ORIGIN_CREDENTIALS, DESTINATION_CREDENTIALS, OLD_ACCOUNT_PREFIX, NEW_ACCOUNT_PREFIX

def execute():
    original_secrets_manager = SecretsManager(ORIGIN_CREDENTIALS)
    destination_secrets_manager = SecretsManager(DESTINATION_CREDENTIALS)

    secret_list = original_secrets_manager.list_secrets()
    
    for secret in secret_list:
        new_secret_name = secret['Name'].replace(OLD_ACCOUNT_PREFIX, NEW_ACCOUNT_PREFIX)
        if destination_secrets_manager.check_existing_secret(new_secret_name):
            print(f"Secret {new_secret_name} already exists in the destination account.")
            continue
        
        value = original_secrets_manager.get_secret_value(secret['Name'], OLD_ACCOUNT_PREFIX, NEW_ACCOUNT_PREFIX)
        destination_secrets_manager.create_secret(value)

if __name__ == '__main__':
    execute()