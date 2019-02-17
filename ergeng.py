# coding=utf-8
import time
from json import loads
from re import compile
from sys import argv
from urllib.request import urlopen
from urllib.request import urlretrieve

ER_GENG_URL_PREFIX = 'http://www.ergengtv.com/video/'
API_URL_FORMAT = 'https://member.ergengtv.com/api/video/vod/?id=%s'
ENCODING_UTF_8 = 'utf-8'


def get_response(url):
    return urlopen(url).read()


def get_title(html):
    return compile("title\": \"(.+?)\",").findall(html.decode(ENCODING_UTF_8))


def get_media_ids(html):
    return compile("media_id\": (.+?),").findall(html.decode(ENCODING_UTF_8))


def get_create_times(html):
    return compile("create_at\": (.+?),").findall(html.decode(ENCODING_UTF_8))


def download():
    if len(argv) < 2 or not str.startswith(argv[1], ER_GENG_URL_PREFIX):
        print('请提供下载页面URL。如：ergeng %s9979.html' % ER_GENG_URL_PREFIX)
    else:
        url = argv[1]
        try:
            url_response = get_response(url)
            create_times = get_create_times(url_response)
            create_time = time.strftime('%Y-%m-%d', time.localtime(float(create_times[0])))
            titles = get_title(url_response)
            media_ids = get_media_ids(url_response)
            file_name = '%s - 二更 %s.mp4' % (' '.join(titles), create_time)
            print('开始下载：%s' % file_name)
            api_url = API_URL_FORMAT % media_ids[0]
            api_url_response = get_response(api_url)
            decode_json = loads(api_url_response)
            download_url = decode_json["msg"]["segs"]["1080p"][0]["url"].replace('http', 'https')
            urlretrieve(download_url, file_name)
            print('*** 下载完成 ***')
        except Exception as e:
            print("下载失败：%s" % e)


if __name__ == '__main__':
    download()
