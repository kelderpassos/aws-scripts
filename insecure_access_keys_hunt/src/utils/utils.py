import datetime

def get_age(date):
    age = datetime.datetime.now(datetime.timezone.utc) - date['CreateDate']
    return age.days