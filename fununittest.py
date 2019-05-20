import re


def password_check(income_password):
    if income_password:
        if re.match(r'[\w-]*$', income_password):
            return True
        else:
            return False
    else:
        return False


def email_check(email_address):
    if email_address:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address):
            return True
        else:
            return False
    else:
        return False


print(password_check(""))
print(password_check("1  "))
print(password_check("*3"))
print(password_check("-asdf"))
print(password_check("_asdf"))

print(email_check("root-ce.33@chr.moe"))
