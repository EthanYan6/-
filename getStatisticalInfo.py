import json
import urllib.request
import datetime

from config import YUQUE_TOKEN, DIDA_COOKIE, LOGIN, X_DEVICE


def get_yuque_data(token):
    """
    获取语雀的相关统计信息
    """
    url_user = "https://www.yuque.com/api/v2/user"
    url_repos = "https://www.yuque.com/api/v2/users/{}/repos".format(LOGIN)
    url_docs = "https://www.yuque.com/api/v2/repos/%s/docs"
    ua_header = {
        "User-Agent": "xiaoyan_test_api",
        "X-Auth-Token": token,
    }
    # 获取用户信息
    request_user = urllib.request.Request(url_user, headers=ua_header)
    response = urllib.request.urlopen(request_user)
    user_info_dict = json.loads(response.read())
    user_info_dict_detail = user_info_dict.get('data')
    created_at = user_info_dict_detail.get('created_at')
    format = '%Y-%m-%dT%H:%M:%S.%fZ'
    utc_time = datetime.datetime.strptime(created_at, format)
    local_time = utc_time + datetime.timedelta(hours=8)
    days = (datetime.datetime.now() - local_time).days

    # 获取仓库相关信息
    request_repos = urllib.request.Request(url_repos, headers=ua_header)
    response_repos = urllib.request.urlopen(request_repos)
    repos_info_dict = json.loads(response_repos.read())

    total_docs = 0
    total_word_count = 0
    total_likes_count = 0
    total_comments_count = 0
    total_read_count = 0
    for item in repos_info_dict.get('data'):
        total_docs += item['items_count']
        # 获取指定仓库的相关信息
        repo_id = item['id']
        url_docs_str = url_docs % repo_id
        request_docs = urllib.request.Request(url_docs_str, headers=ua_header)
        response_docs = urllib.request.urlopen(request_docs)
        docs_info_dict = json.loads(response_docs.read())
        for doc_info in docs_info_dict.get('data'):
            total_word_count += doc_info['word_count']
            total_likes_count += doc_info['likes_count']
            total_comments_count += doc_info['comments_count']
            total_read_count += doc_info['read_count']

    print('语雀统计信息：')
    print('======================================')
    print('使用天数：       %s' % days)
    print('关注：           %s' % user_info_dict_detail.get('following_count'))
    print('粉丝：           %s' % user_info_dict_detail.get('followers_count'))
    print('仓库数量：       %s' % user_info_dict_detail.get('books_count'))
    print('已公开仓库数量： %s' % user_info_dict_detail.get('public_books_count'))
    print('文档数量：       %s' % total_docs)
    print('总字数：         %s' % total_word_count)
    print('点赞：           %s' % total_likes_count)
    print('评论：           %s' % total_comments_count)
    print('阅读量：         %s' % total_read_count)
    print('=======power by 小闫同学===============')
    print('')
    print('')

def get_dida_data(cookie):
    """
    获取嘀嗒清单的相关统计信息
    """
    url = "https://api.dida365.com/api/v3/user/ranking"
    ua_header = {
        "User-Agent": "xiaoyan_test_api",
        "cookie": cookie,
        "x-device": X_DEVICE,
    }
    request = urllib.request.Request(url, headers=ua_header)
    response = urllib.request.urlopen(request)
    info_dict = json.loads(response.read())
    print('嘀嗒清单统计信息：')
    print('======================================')
    print('您的勤奋超过了 {}% 的用户'.format(info_dict.get('ranking')))
    print('使用天数：   {}'.format(info_dict.get('dayCount')))
    print('等级：       {}'.format(info_dict.get('level')))
    print('成就值：     {}'.format(info_dict.get('score')))
    print('清单数量：   {}'.format(info_dict.get('projectCount')))
    print('任务总数：   {}'.format(info_dict.get('taskCount')))
    print('已完成：     {}'.format(info_dict.get('completedCount')))
    print('=======power by 小闫同学===============')


# 执行
get_yuque_data(YUQUE_TOKEN)
get_dida_data(DIDA_COOKIE)
