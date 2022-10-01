from dict_to_str import dict2str
from read_url import url
import os


def post(subname, s):
    os.system("http POST "+url()+subname + " " + s)


def put(subname, s):
    os.system("http PUT "+url()+subname + " " + s)


def delete(subname, s):
    os.system("http DELETE "+url()+subname + " " + s)
