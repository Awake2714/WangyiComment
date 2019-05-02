from fake_useragent import UserAgent

ua = UserAgent().random
URL = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='
PAGE = 10749
HEADERS = {
    'Host': 'music.163.com',
    'Origin': 'https://music.163.com',
    'Referer': 'https://music.163.com/song?id=1345848098',
    'User-Agent': ua,
    }

# 第二个参数
SECOND_PARAM = "010001"
# 第三个参数
THIRD_PARAM = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
FORTH_PARAM = "0CoJUm6Qyw8W8jud"
IV = "0102030405060708"
