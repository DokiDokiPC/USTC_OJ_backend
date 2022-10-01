import os

script_dir = os.path.dirname(__file__)
test_folder_dir = os.path.dirname(script_dir)
url_dir = os.path.join(test_folder_dir, 'test_url.txt')


def url():
    f = open(url_dir, mode='r')
    s = f.read()
    s=s.strip()
    return s
