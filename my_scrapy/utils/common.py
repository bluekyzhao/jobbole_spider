from hashlib import md5


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5('https://www.baidu.com'))
