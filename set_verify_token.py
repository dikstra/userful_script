import time
import base64
import hmac
import hashlib
import random
import string

def generate_token(key,expire=3600):
    ts_str=str(time.time() + expire)
    ts_byte=ts_str.encode("utf-8")
    sha_tshestr=hmac.new(key.encode("utf-8"),ts_byte.encode("utf-8"),digestmod=hashlib.sha1).hexdigest()
    token = ts_str + ':' + sha_tshestr
    b64_token=base64.urlsafe_b64encode(token)
    #return b64_token.decode("utf-8")
    return b64_token

def verify_token(key,token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        #token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), digestmod=hashlib.sha1)
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        return False
    return True

def get_key():
    salt = "!@#$%^&*()><?+-/_"
    a = string.ascii_letters + string.digits + salt
    key = random.sample(a, 8)
    keys = "".join(key)
    print keys

if __name__ == '__main__':
    key=str(get_key())
    #key = "abcd"
    token=generate_token(key)
    #generate_token()
    values=verify_token(key,token)
