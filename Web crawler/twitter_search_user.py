import datetime
import os
import random
import time
import traceback
import urllib
import pandas as pd
import requests
from dateparser.search import search_dates

# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# proxies = {'https': 'https://127.0.0.1:1080', "http": "http://127.0.0.1:1080"}
proxies = {'https': 'https://127.0.0.1:7890', "http": "http://127.0.0.1:7890"}
# proxy = '127.0.0.1:10809'
# proxies = {'http': 'socks5://127.0.0.1:10808', "https": "socks5://127.0.0.1:10808"}
# proxies = {'http':'http://'+proxy, 'https':'https://'+ proxy}


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
]


def get_spider_time():
    g_spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return g_spider_time


def get_time(a):
    a = a.replace("+0000", "")
    time_str = search_dates(a)
    times = time_str[0][-1]
    print(times, type(times))
    publish_time_end = (times + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return publish_time_end


def get_session():
    s = requests.session()
    s.keep_alive = False
    s.proxies = proxies
    s.allow_redirects = False
    s.verify = False
    return s


def get_token():
    while True:
        try:
            with open('token.txt', 'r') as f:
                tokens = f.read()
            return tokens
        except Exception as e:
            print("Error in obtaining token:", e)


def get_html(url):
    s = get_session()
    # print("Tokens obtained for the first time：",tokens)
    while True:
        try:
            tokens = get_token()
            headers = {
                'Referer': 'https://twitter.com/algore',
                'Origin': 'https://twitter.com',
                'User-Agent': random.choice(user_agents),
                'x-guest-token': tokens,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
            }
            print("Start request url", url)
            """{'errors': [{'code': 200, 'message': 'Forbidden.'}]},Rate limit exceeded"""
            """{'errors': [{'code': 34, 'message': 'Sorry, that page does not exist.'}]}"""

            r = s.get(url, headers=headers, proxies=proxies, timeout=20, verify=False)
            res = str(r.json())
            if "Rate limit exceeded" in res or 'Forbidden' in res or "Sorry, that page does not exist" in res:
                s = get_session()
                continue
            else:
                return r
        except Exception as e:
            s = get_session()
            print(e)
            tokens = get_token()


def get_twitter_info(tim, threeDayAgosss, j,df,index,file):
    print("!!!!!!!!!!!!!!!!!!!!!!!!", tim, threeDayAgosss)
    cursors = ''
    num = 0
    while num < 50:
        num += 1
        try:
            url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=(from%3A{})%20until%3A{}%20since%3A{}%20-filter%3Areplies&count=20&query_source=typed_query{}&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel'.format(
                j, tim, threeDayAgosss, cursors)
            res = get_html(url)
            res_dict = res.json()
            if res_dict['globalObjects']['tweets']:
                print("aaaa")
                get_twitter_article(res_dict['globalObjects'], j,df,index,file)
                try:
                    if res_dict['timeline']['instructions'][0]['addEntries']['entries'][-1]:
                        page_next = res_dict['timeline']['instructions'][0]['addEntries']['entries'][-1]
                        print(page_next)
                        cursor = page_next['content']['operation']['cursor']['value']
                        print(cursor)
                        cursor = urllib.parse.quote(cursor)
                        cursors = "&cursor={}".format(cursor)
                except Exception as e:
                    print("Error in obtaining parameters of the next page", e)
                    break
            else:
                break
        except Exception as e:
            print("Error on the next page.:", e)
            break


def save_csv(conlist,keyword):
    print("Save：", conlist)
    pf = pd.DataFrame(conlist)
    print("@@@@@@@@@@@@","{}.csv".format(keyword))
    pf.to_csv("{}.csv".format(keyword), header=False, index=False, mode='a', encoding='utf-8')


def get_twitter_article(data, keyword,df,index,file):
    try:
        if data:
            for key, i in data['tweets'].items():
                print('------------------------------')
                info = {}
                forward_info = {}
                try:
                    m_parent_id = i['retweeted_status_id_str']
                    info['m_parent_id'] = m_parent_id
                    forward_info['r_parent_id'] = m_parent_id
                except:
                    info['m_parent_id'] = ''
                    forward_info['r_parent_id'] = ''

                # Forwarded tweets.
                if info['m_parent_id']:
                    # the url of the forwarded tweets.
                    # m_parent_url = '{}/status/'.format(user_url) + info['m_parent_id']
                    # info['m_parent_url'] = m_parent_url
                    # print("the url of the forwarded tweets，",m_parent_url)
                    # the content of forwarded tweet.
                    m_parent_content = i['full_text']
                    info['m_parent_content'] = m_parent_content
                    # print("the content of forwarded tweet,",m_parent_content)
                    r_is_trans = 1
                    info['r_is_trans'] = r_is_trans
                    print(r_is_trans)
                    info['m_content'] = ''
                else:
                    # r_is_trans = 0
                    info['r_is_trans'] = 0
                    m_content = i['full_text']
                    info['m_content'] = m_content
                    # print("Text content:",m_content)
                try:
                    quoted_status_id_str = i['quoted_status_id_str']
                    info['quoted_status_id_str'] = quoted_status_id_str
                except:
                    info['quoted_status_id_str'] = ''
                try:
                    if info['quoted_status_id_str'] and info['m_parent_id'] == '':
                        r_is_comment_replay = 1
                        info['r_is_comment_replay'] = r_is_comment_replay
                        # print(r_is_comment_replay)
                        m_parent_id = i['quoted_status_id_str']
                        info['m_parent_id'] = m_parent_id
                        m_parent_content = data['tweets'][m_parent_id]['full_text']
                        info['m_parent_content'] = m_parent_content
                        r_is_trans = 0
                        info['r_is_trans'] = 0
                        m_content = ''
                        info['m_content'] = m_content
                    else:
                        r_is_comment_replay = 0
                        info['r_is_comment_replay'] = r_is_comment_replay
                except:
                    pass
                m_content_id = i['conversation_id_str']
                info['m_mid'] = m_content_id
                info['m_content_id'] = m_content_id
                try:
                    m_images_lis = i['extended_entities']['media']
                    img_list = []
                    for j in m_images_lis:
                        img_list.append(j['media_url'])
                    info['m_images'] = img_list
                except:
                    info['m_images'] = ''
                # tweet video address.
                try:
                    m_videos = i['entities']['media'][0]['expanded_url']
                    if "video" in m_videos:
                        info['m_videos'] = m_videos
                    else:
                        info['m_videos'] = ''

                except:
                    info['m_videos'] = ''
                # Number of comments.
                try:
                    r_comment_num = i['reply_count']
                    info['r_comment_num'] = r_comment_num
                    print(r_comment_num)
                except:
                    info['r_comment_num'] = ''
                # publish time
                try:
                    print(i['created_at'])
                    g_publish_time = get_time(i['created_at'])
                    info['g_publish_time'] = g_publish_time.replace("-", "/")
                    forward_info['g_publish_time'] = g_publish_time
                    print(g_publish_time)
                except:
                    info['g_publish_time'] = ''
                    forward_info['g_publish_time'] = ''
                forward_info['m_is_remove'] = 1
                # favourite count
                try:
                    r_like_num = i['favorite_count']
                    info['r_like_num'] = r_like_num
                    print(r_like_num)
                except:
                    info['r_praised_num'] = ''
                # retweet count
                try:
                    r_trans_num = i['retweet_count']
                    print(r_trans_num)
                    info['r_trans_num'] = r_trans_num
                except:
                    info['r_trans_num'] = ''
                # Is the tweet valid?
                # user id
                try:
                    user_id_str = i['user_id_str']
                    info['u_id'] = user_id_str
                except:
                    info['u_id'] = ''
                if info['m_content']:
                    df['url'][index] = m_content
                    print("&&&&&&&&&","https://twitter.com/{}/status/{}".format(keyword,m_content_id))
                    ppp = pd.DataFrame(df)
                    ppp.to_csv("D:\players\ings\\"+"{}".format(file))
                    save_csv([{'g_publish_time': info['g_publish_time'],'m_content': info['m_content']}],keyword)


    except Exception as e:
        traceback.print_exc()
        print(e)


def time_end_start(i, start_time):
    aaa = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    threeDayAgo = (aaa + datetime.timedelta(days=i))
    threeDayAgosss = (threeDayAgo - datetime.timedelta(days=1))
    return threeDayAgo, threeDayAgosss


def run():
    file_dir = "D:\players\ing"    # By modifying this path, the web crawler can read CSV files and crawl tweets corresponding to users id and dates.
    for root, dirs, files in os.walk(file_dir):
        # print("The number of files to be processed is:" + str(len(files)))
        for file in files:
            print("zzz",file)
            lis = [file[:-4]]
            df = pd.read_csv("D:\players\ing\\"+"{}".format(file))
            hh = df.shape
            print(hh)
            df['url'] = ['' for i in range(0,hh[0])]
            for index, i in enumerate(df['Date']):
                # df['url'] = ['http://www.baidu.com'] + ['' for j in range(1, 640)]
                i = i.replace("/","-")
                start_time = i
                # end time
                end_time = i
                d1 = datetime.datetime.strptime(start_time, '%Y-%m-%d')
                d2 = datetime.datetime.strptime(end_time, '%Y-%m-%d')
                delta = d2 - d1
                ccc = delta.days
                print(ccc)
                for i in range(0, int(ccc) + 1):
                    tim, threeDayAgosss = time_end_start(i, start_time)
                    tim = str(tim).replace("00:00:00", "").replace(" ", "")
                    threeDayAgosss = str(threeDayAgosss).replace("00:00:00", "").replace(" ", "")
                    print(tim)
                    if tim:
                        get_token()
                        for j in lis:
                            get_twitter_info(tim, threeDayAgosss, j,df,index,file)
                    else:
                        time.sleep(60)


if __name__ == '__main__':
    run()
