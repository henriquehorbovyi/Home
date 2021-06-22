import os


def open_web_site(url):
    url = str(url).replace(" ", ".")
    os.popen("python3 -mwebbrowser "+url)
