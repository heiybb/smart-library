"""
Return 16 length encrypt password
Used to stored in the local database
"""
import hmac


def encrypt(password):
    """
    :param password: password income
    :return: encrypted password
    """
    encrypt_key = '399259500'.encode(encoding="utf-8")
    password = password.encode(encoding="utf-8")

    hmd5 = hmac.new(password, encrypt_key).hexdigest().encode(encoding="utf-8")

    rule = list(hmac.new("csit2019australia".encode(encoding="utf-8"), hmd5).hexdigest())
    source = list(hmac.new("rmit1995melbourne".encode(encoding="utf-8"), hmd5).hexdigest())

    for i in range(0, 32):
        if not source[i].isdigit():
            if rule[i] in "csit.rmit.edu.au":
                source[i] = source[i].upper()
    code = "".join(source[1:16])
    if not source[0].isdigit():
        code = source[0] + code
    else:
        code = "K" + code
    return code
