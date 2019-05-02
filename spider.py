import pymongo
from Crypto.Cipher import AES
from setting import *
import time,random,json,requests,base64
from get_proxy import proxy

class MusicComment(object):
    headers = HEADERS
    second_param = SECOND_PARAM
    third_param = THIRD_PARAM
    forth_param = FORTH_PARAM

    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.WangyiMusic.comment

    # 获取参数
    def get_params(self, page): # page为传入页数
        iv = IV
        first_key = self.forth_param
        second_key = 16 * 'F'
        if(page == 1): # 如果为第一页
            first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            h_encText = self.AES_encrypt(first_param, first_key, iv)
        else:
            offset = str((page-1)*20)
            first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
            h_encText = self.AES_encrypt(first_param, first_key, iv)
        h_encText = self.AES_encrypt(h_encText, second_key, iv)
        return h_encText

    # 获取 encSecKey
    def get_encSecKey(self):
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey

    # 解密过程
    def AES_encrypt(self, text, key, iv):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        encrypt_text = str(encrypt_text, encoding="utf-8") #注意一定要加上这一句，没有这一句则出现错误
        return encrypt_text

    # 获得评论json数据
    def get_json(self, url, params, encSecKey):
        data = {
             "params": params,
             "encSecKey": encSecKey
        }
        response = requests.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.content
        else:
            proxies = proxy()
            response = requests.post(url, headers=self.headers, data=data, proxies=proxies)
            return response.content


    def get_all_comments(self, url, page):
        for i in range(page):  # 逐页抓取
            params = self.get_params(i+1)
            encSecKey = self.get_encSecKey()
            json_text = self.get_json(url, params, encSecKey).decode()
            json_dict = json.loads(json_text)
            for item in json_dict['comments']:
                userid = item['user']['userId']  # 用户ID
                nickname = item['user']['nickname']  # 用户昵称
                avatar = item['user']['avatarUrl']  # 用户头像链接
                content = item['content']  # 评论内容
                likedcount = item['likedCount']  # 点赞数
                data = {
                    'userid': 'https://music.163.com/#/user/home?id='+ str(userid),
                    'nickname': nickname,
                    'avatar': avatar,
                    'content': content,
                    'likedcount': likedcount,
                }
                self.db.update({'content':data['content']}, {'$set': data}, True)
            print('第%d页抓取完毕!' % (i+1))
            time.sleep(random.choice(range(1,3)))  #爬取过快的话，设置休眠时间，跑慢点，减轻服务器负担


comment = MusicComment()
song_id = '1345848098'
url = URL.format(song_id)
comment.get_all_comments(url, page=PAGE)
