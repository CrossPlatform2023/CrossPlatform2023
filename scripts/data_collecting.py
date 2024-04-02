""" List repo forkers, commits, issues and prs """

import json
import Config as cfg
import requests
import pandas
import os
import re
import requests
from bs4 import BeautifulSoup
from RQ1 import role_generation
headers = {
    'Authorization': 'token YOUR_TOKEN'}
headers_2 = {
    'Authorization': 'token YOUR_SECOND_TOKEN'}


def list_forkers(org):
    """ list org's main repo's forkers """
    forkers = set()
    main_repo = cfg.org_to_repo[org]
    url = 'https://api.github.com/repos/{}'.format(main_repo)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        total_fork_count = res.json()['forks_count']
    else:
        print('ERROR cannot get the total forks count')
        return
    for page in range(1, total_fork_count // 100 + 2):
        url = 'https://api.github.com/repos/{}/forks?page={}&per_page=100'.format(main_repo, page)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dic_list = res.json()
            for dic in dic_list:
                if dic['owner']:
                    forkers.add(dic['owner']['login'])
                    print('forker:', dic['owner']['login'])
        if page % 100 == 0:
            with open('../data/{}/role/{}_forkers.json'.format(org, main_repo.replace('/', '_')), "w", encoding='utf-8') as f:
                json.dump(list(forkers), f, indent=2)
                print(page, 'SAVED')
    with open('../data/{}/role/{}_forkers.json'.format(org, main_repo.replace('/', '_')), "w", encoding='utf-8') as f:
        json.dump(list(forkers), f, indent=2)


def list_commits(owner_repo, project, commit_count):
    print('  listing commits for {}'.format(owner_repo))
    org = project.split('-')[0]
    result = []
    for page in range(1, commit_count // 100 + 2):
        # print('Page: ', page)
        url = 'https://api.github.com/repos/{OWNER_REPO}/commits?page={PAGE}&per_page=100'.format(
            OWNER_REPO=owner_repo, PAGE=page
        )
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dict_list = res.json()
            for i in range(len(dict_list)):
                # print(dict_list[i]['url'])
                result.append({
                    'url': dict_list[i]['url'],
                    'author': dict_list[i]['author']['login'] if dict_list[i]['author'] else None,
                    'author_email': dict_list[i]['commit']['author']['email'],
                    'committer': dict_list[i]['committer']['login'] if dict_list[i]['committer'] else None,
                    'committer_email': dict_list[i]['commit']['committer']['email'],
                    'message': dict_list[i]['commit']['message'],
                    'date': dict_list[i]['commit']['committer']['date']
                })
        if page % 100 == 0:
            with open('../data/{}/commits/{}.json'.format(org, project), "w", encoding='utf-8') as f:
                json.dump(result, f, indent=2)

    print(len(result))
    with open('../data/{}/commits/{}.json'.format(org, project), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=2)


def list_issues(owner_repo, project, issues_count):
    print('  listing issues for {}'.format(owner_repo))
    org = project.split('-')[0]
    result_issue = []
    result_pr = []
    for page in range(1, issues_count // 100 + 2):
        # print('Page: ', page)
        url = 'https://api.github.com/repos/{OWNER_REPO}/issues?state=all&per_page=100&page={PAGE}'.format(
            OWNER_REPO=owner_repo, PAGE=page
        )
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dict_list = res.json()
            for i in range(len(dict_list)):
                if 'pull_request' in dict_list[i].keys():
                    # It's a PR!
                    # print('PR', dict_list[i]['url'])
                    result_pr.append({
                        'number': dict_list[i]['number'],
                        'title': dict_list[i]['title'],
                        'user': dict_list[i]['user']['login'],
                        'comments': dict_list[i]['comments'],
                        'created_at': dict_list[i]['created_at'],
                        'updated_at': dict_list[i]['updated_at'],
                        'closed_at': dict_list[i]['closed_at']
                    })
                else:
                    # It's an issue
                    # print('Issue', dict_list[i]['url'])
                    result_issue.append({
                        'number': dict_list[i]['number'],
                        'title': dict_list[i]['title'],
                        'user': dict_list[i]['user']['login'],
                        'comments': dict_list[i]['comments'],
                        'created_at': dict_list[i]['created_at'],
                        'updated_at': dict_list[i]['updated_at'],
                        'closed_at': dict_list[i]['closed_at']
                    })
        if page % 100 == 0:
            with open('../data/{}/issues/{}.json'.format(org, project), "w", encoding='utf-8') as f:
                json.dump(result_issue, f, indent=2)
            with open('../data/{}/prs/{}.json'.format(org, project), "w", encoding='utf-8') as f:
                json.dump(result_pr, f, indent=2)

    print('   issue_len, pr_len:', len(result_issue), len(result_pr))
    with open('../data/{}/issues/{}.json'.format(org, project), "w", encoding='utf-8') as f:
        json.dump(result_issue, f, indent=2)
    with open('../data/{}/prs/{}.json'.format(org, project), "w", encoding='utf-8') as f:
        json.dump(result_pr, f, indent=2)


def add_issue_comments(start_index, owner_repo, project):
    print('  updating issue comments for {}'.format(owner_repo))
    org = project.split('-')[0]
    if not os.path.exists('../data/{}/issues/{}.json'.format(org, project)):
        print('   NO SUCH FILE')
        return
    issues = list(json.load(open('../data/{}/issues/{}.json'.format(org, project))))
    for i in range(start_index, len(issues)):
        issue = issues[i]
        if 'comment_time' in issue:
            print(i, 'Already done')
            continue
        if issue['comments'] > 0:
            comments_username_list = []
            comments_time_list = []
            url = 'https://api.github.com/repos/{OWNER_REPO}/issues/{NUMBER}/comments'.format(
                OWNER_REPO=owner_repo, NUMBER=issue['number']
            )
            # print(i, url)
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                dict_list = res.json()
                for comments in dict_list:
                    if comments['user']['type'] == 'Bot':
                        # print('Bot')
                        continue
                    comments_username_list.append(comments['user']['login'])
                    comments_time_list.append(comments['created_at'])
            if comments_username_list:
                issues[i].update({
                    'commenters': comments_username_list,
                    'comment_time': comments_time_list
                })
                # print('update', issues[i])
        if i % 100 == 0:
            with open('../data/{}/issues/{}.json'.format(org, project), "w", encoding='utf-8') as f:
                json.dump(issues, f, indent=2)
                print('   ', i, 'SAVED!')
    with open('../data/{}/issues/{}.json'.format(org, project), "w", encoding='utf-8') as f:
        json.dump(issues, f, indent=2)


def add_pr_reviews(start_index, owner_repo, project):
    print('  updating pr comments/reviews for {}'.format(owner_repo))
    org = project.split('-')[0]
    prs = list(json.load(open('../data/{}/prs/{}.json'.format(org, project))))
    # for i, pr in enumerate(prs):
    for i in range(start_index, len(prs)):
        pr = prs[i]

        # 1. update comments
        if pr['comments'] > 0:
            comments_username_list = []
            comments_time_list = []
            url = 'https://api.github.com/repos/{OWNER_REPO}/issues/{NUMBER}/comments?per_page=100'.format(
                OWNER_REPO=owner_repo, NUMBER=pr['number']
            )
            # print(i, url)
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                dict_list = res.json()
                for comments in dict_list:
                    if comments['user'] is None or comments['user']['type'] == 'Bot':
                        # print('Bot')
                        continue
                    comments_username_list.append(comments['user']['login'])
                    comments_time_list.append(comments['created_at'])
            if comments_username_list:
                prs[i].update({
                    'issue_commenters': comments_username_list,
                    'comment_time': comments_time_list
                })
                # print('update issue comments', prs[i])

        # 2. update review commenters
        review_cmts_usernames = []
        review_cmts_time = []
        url_2 = 'https://api.github.com/repos/{OWNER_REPO}/pulls/{PULL_NUMBER}/comments?per_page=100'.format(
            OWNER_REPO=owner_repo, PULL_NUMBER=pr['number']
        )
        # print(i, url_2)
        res_2 = requests.get(url_2, headers=headers)
        if res_2.status_code == 200:
            dict_list = res_2.json()
            for comments in dict_list:
                if comments['user'] is None or comments['user']['type'] == 'Bot':
                    # print('Bot')
                    continue
                review_cmts_usernames.append(comments['user']['login'])
                review_cmts_time.append(comments['created_at'])
        if review_cmts_usernames:
            prs[i].update({
                'pr_commenters': review_cmts_usernames,
                'pr_comment_time': review_cmts_time
            })
            # print('update pr comments', prs[i])

        # 3. update reviewers
        reviewers = []
        review_time = []
        url_3 = 'https://api.github.com/repos/{OWNER_REPO}/pulls/{PULL_NUMBER}/reviews?per_page=100'.format(
            OWNER_REPO=owner_repo, PULL_NUMBER=pr['number']
        )
        # print(i, url_3)
        res_3 = requests.get(url_3, headers=headers)
        if res_3.status_code == 200:
            dict_list = res_3.json()
            for review in dict_list:
                if review['user'] is None or review['user']['type'] == 'Bot':
                    # print('Bot')
                    continue
                reviewers.append(review['user']['login'])
                review_time.append(review['submitted_at'])
        if reviewers:
            prs[i].update({
                'reviewers': reviewers,
                'review_time': review_time
            })
            # print('update reviewers', prs[i])

        if i % 100 == 0:
            with open('../data/{}/prs/{}.json'.format(org, project), "w", encoding='utf-8') as f:
                json.dump(prs, f, indent=2)
            print('   ', i, 'SAVED')

    with open('../data/{}/prs/{}.json'.format(org, project), "w", encoding='utf-8') as f:
        json.dump(prs, f, indent=2)


def total_commit_count(op):
    """the total commit count of a repo, repo path = op, e.g.:'angular/angular'"""
    return re.search('\d+$', requests.get('https://api.github.com/repos/{}/commits?per_page=1'.format(op)).links['last']['url']).group()


def total_issue_count(op):
    """the total issue & pr count of a repo, repo path = op, e.g.:'angular/angular'"""
    res = requests.get('https://api.github.com/search/issues?q=repo:{}'.format(op))
    res_dict = res.json()
    return int(res_dict["total_count"])


def activity_data_collecting_routine(op):
    project = op.replace('/', '-')
    commit_count = int(total_commit_count(op))
    issue_count = total_issue_count(op)

    # list_commits(op, project, commit_count)
    # list_issues(op, project, issue_count)
    add_issue_comments(0, op, project)
    add_pr_reviews(start_index=0, owner_repo=op, project=project)
