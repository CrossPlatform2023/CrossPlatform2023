import json
import Config as cfg


def core_devs(org):
    """ return core devs list using 80% threshold"""
    author_commit_dic = {}
    main_repo = cfg.org_to_repo[org]
    commit_file_path = '../data/{}/commits/{}.json'.format(org, main_repo.replace('/', '-'))
    commits = list(json.load(open(commit_file_path)))
    code_contributors = set()
    for commit in commits:
        if commit['author'] is None:
            continue
        code_contributors.add(commit['author'])
        if commit['author'] in author_commit_dic:
            author_commit_dic[commit['author']] += 1
        else:
            author_commit_dic[commit['author']] = 1

    ans = []
    threshold = 0.8 * len(commits)
    accumulated_commits = 0
    author_commit = sorted(author_commit_dic.items(), key=lambda x: x[1], reverse=True)
    for author, commit_count in author_commit:
        if accumulated_commits > threshold:
            break
        else:
            ans.append(author)
            accumulated_commits += commit_count
    return ans, list(code_contributors)


def generate_chat_role(org, select_type='all'):
    main_repo = cfg.org_to_repo[org]
    main_chatroom = cfg.org_to_chatroom[org]

    all_chatters = set()        # all chatters except deleted account
    github_chatters = set()

    chat_msg = open('../data/{}/chat_msg/{}.txt'.format(org, main_chatroom.replace('/', '_')), encoding='utf-8').read()
    dialogs = chat_msg.split(cfg.dialog_separator)
    for dialog in dialogs:
        utterances = dialog.split('\n')
        ask_id = ''
        for sentence in utterances:
            match = cfg.regex.search(sentence)
            if match is None:
                continue
            username = match.group(3)
            if username.startswith('ghost~'):
                continue
            all_chatters.add(username)
            if not username.endswith('_twitter') and not username.endswith('_gitlab'):
                github_chatters.add(username)
    if select_type == 'all':
        return all_chatters
    elif select_type == 'github':
        return github_chatters
    else:
        return None


def generate_github_devs(org):
    """ return all GitHub participants, including committers, issue reporters, reviewers, commenters  """
    main_repo = cfg.org_to_repo[org]

    core_developers, all_coders = core_devs(org)
    issue_reporters = set()
    reviewers = set()
    commenters = set()
    issues = list(json.load(open('../data/{}/issues/{}.json'.format(org, main_repo.replace('/', '-')))))
    for issue in issues:
        issue_reporters.add(issue['user'])
        if 'commenters' in issue:
            commenters = commenters.union(issue['commenters'])
    prs = list(json.load(open('../data/{}/prs/{}.json'.format(org, main_repo.replace('/', '-')))))
    for pr in prs:
        if 'reviewers' in pr:
            reviewers = reviewers.union(pr['reviewers'])
        if 'issue_commenters' in pr:
            commenters = commenters.union(pr['issue_commenters'])
        if 'pr_commenters' in pr:
            commenters = commenters.union(pr['pr_commenters'])

    total = issue_reporters.union(set(all_coders), reviewers, commenters)
    result = {'coders': all_coders, 'issue_reporters': list(issue_reporters),
              'reviewers': list(reviewers), 'commenters': list(commenters), 'all_members': list(total)}
    # print(result)
    return result


def oss_roles(org):
    core_developers, all_coders = core_devs(org)
    main_repo = cfg.org_to_repo[org]
    github_devs_dic = generate_github_devs(org)
    all_devs = generate_chat_role(org).union(github_devs_dic['all_members'])

    forkers = list(
        json.load(open('../data/{}/role/{}_forkers.json'.format(org, main_repo.replace('/', '_')), encoding='utf-8')))
    dependence_users = list(json.load(
        open('../data/{}/role/{}_dependents.json'.format(org, main_repo.replace('/', '_')), encoding='utf-8')))

    result = {}
    for dev in all_devs:
        if dev.endswith('_gitlab') or dev.endswith('_twitter'):
            result[dev] = 'user'
        else:
            if dev in core_developers:
                result[dev] = 'core'
            elif dev in all_coders:
                result[dev] = 'peripheral'
            elif dev in github_devs_dic['issue_reporters']:
                result[dev] = 'issue'
            elif dev in github_devs_dic['reviewers']:
                result[dev] = 'reviewer'
            elif dev in github_devs_dic['commenters']:
                result[dev] = 'commenter'
            elif dev in forkers or dev in dependence_users:
                result[dev] = 'reader'
            else:
                result[dev] = 'user'

    # save CPCs
    cpcs = generate_chat_role(org).intersection(github_devs_dic['all_members'])
    with open(cfg.devs_path.format(org), 'w') as f:
        f.writelines([dev + '\n' for dev in cpcs])

    with open('../data/{}/role/oss_roles.json'.format(org), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    for org in cfg.orgs:
        oss_roles(org)
        print(org, "DONE")
        print()