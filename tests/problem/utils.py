from read_url import url
import os


def dict2str(d: dict) -> str:
    s = ""
    for k in d:
        s += " "
        s += f"{k}={d[k]}"
    return s

def get(subname):
    os.system("http GET "+url()+subname)

def post(subname, s):
    os.system("http POST "+url()+subname + " " + s)


def put(subname, s):
    os.system("http PUT "+url()+subname + " " + s)


def delete(subname, s):
    os.system("http DELETE "+url()+subname + " " + s)
