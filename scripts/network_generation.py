"""
    Generate network for Gitter and GitHub platform
"""
import Config as cfg
from . import role_generation
import networkx as nx
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
import codecs
# Customize matplotlib
matplotlib.rcParams.update({# Use mathtext, not LaTeX
                            'text.usetex': False,
                            # Use the Computer modern font
                            'font.family': 'serif',
                            'font.serif': 'cmr10',
                            'mathtext.fontset': 'cm',
                            })


# "comment-to/reply-to" edge
def add_edge(dic, item):
    u, v = item
    if u == '' or v == '':
        return dic

    if u == v:
        return dic
    if item in dic.keys():
        dic[item] += 1
    elif (v, u) in dic.keys():
        dic[(v, u)] += 1
    else:
        dic[item] = 1
    return dic


# "in the same dialog/conversation" edge
def add_edge_v2(dic, node_list):
    if '' in node_list:
        return dic
    for i, u in enumerate(node_list):
        for v in node_list[i + 1:]:
            if u == v:
                continue
            if (u, v) in dic.keys():
                dic[(u, v)] += 1
            elif (v, u) in dic.keys():
                dic[(v, u)] += 1
            else:
                dic[u, v] = 1
    return dic


def draw_network_attributes(G):
    # draw
    d = dict(nx.degree(G))
    # get all degrees
    x = list(range(max(d.values()) + 1))
    # get the number of occurrences for each degree
    d_list = nx.degree_histogram(G)
    # P (the number of occurrences for each degree) =
    #           The number of nodes corresponding to each degree value/the number of total points
    y = np.array(d_list) / len(G.nodes)

    # 1. plot the degree distribution on normal axes
    plt.plot(x, y, 'o-', color='b')
    plt.xlabel('degree')
    plt.ylabel('degree_prob')
    plt.show()
    # plt.savefig(prefix + '.png')

    # 2. plot it on the logarithmic axis, and exclude the point 0 value coordinates
    new_x = []
    new_y = []
    # 删除0值
    for i in range(len(x)):
        if y[i] != 0:
            new_x.append(x)
            new_y.append(y)

    # draw
    plt.plot(new_x, new_y, 'o-', color='g')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('degree')
    plt.ylabel('degree_prob')
    plt.grid()
    plt.show()
    # plt.savefig(prefix + '_log.png')

    print("  # of nodes:", len(G.nodes()), "# of edges:", len(G.edges()))
    print("  avg. degree is：", sum(d.values()) / len(G.nodes))
    # print("diameter：", nx.diameter(G))
    # print("degree centrality:", sum(nx.degree_centrality(G).values()) / len(G.nodes))
    # print("betweenness centrality:", sum(nx.betweenness_centrality(G).values()) / len(G.nodes))
    # print("closeness centrality:", sum(nx.closeness_centrality(G).values()) / len(G.nodes))


def gitter_network(org):
    main_chatroom = cfg.org_to_chatroom[org]
    chat_msg = open('../data/{}/chat_msg/{}.txt'.format(org, main_chatroom.replace('/', '_')), encoding='utf-8').read()
    nodes = role_generation.generate_chat_role(org)
    edges_dic = {}
    G = nx.Graph()
    G.add_nodes_from(nodes)

    dialogs = chat_msg.split(cfg.dialog_separator)
    for dialog in dialogs:
        utterances = dialog.split('\n')
        ask_id = ''
        node_list = set()
        for sentence in utterances:
            match = cfg.regex.search(sentence)
            if match is None:
                continue
            username = match.group(3)
            if username not in nodes:
                continue
            if sentence.startswith('1'):
                # 对话 initiator
                ask_id = username
                node_list.add(username)
                continue
            if username == ask_id:
                continue
            node_list.add(username)
            edges_dic = add_edge(edges_dic, (ask_id, username))
    G.add_weighted_edges_from([u, v, weight] for (u, v), weight in edges_dic.items())
    draw_network_attributes(G)
    os.makedirs('../data/{}/networks'.format(org), exist_ok=True)
    nx.write_gml(G, "../data/{}/networks/chat.gml".format(org))
    return G


def github_network(org):
    main_repo = cfg.org_to_repo[org]
    nodes = role_generation.generate_github_devs(org)['all_members']
    edges_dic = {}
    issues = list(json.load(open('../data/{}/issues/{}.json'.format(org, main_repo.replace('/', '-')))))
    prs = list(json.load(open('../data/{}/prs/{}.json'.format(org, main_repo.replace('/', '-')))))
    commits = list(json.load(open('../data/{}/commits/{}.json'.format(org, main_repo.replace('/', '-')))))
    G = nx.Graph()
    G.add_nodes_from(nodes)

    for issue in issues:
        if 'commenters' in issue.keys():
            for commenters in issue['commenters']:
                edges_dic = add_edge(edges_dic, (issue['user'], commenters))
    for pr in prs:
        if 'issue_commenters' in pr.keys():
            for i_c in pr['issue_commenters']:
                edges_dic = add_edge(edges_dic, (pr['user'], i_c))
        if 'pr_commenters' in pr.keys():
            for p_c in pr['pr_commenters']:
                edges_dic = add_edge(edges_dic, (pr['user'], p_c))
        if 'reviewers' in pr.keys():
            for r in pr['reviewers']:
                edges_dic = add_edge(edges_dic, (pr['user'], r))

    G.add_weighted_edges_from([u, v, weight] for (u, v), weight in edges_dic.items())

    # draw_network_attributes(G, 'networks/degree_distribution/code_' + project)
    nx.write_gml(G, "../data/{}/networks/code.gml".format(org))
    print('   ', org, 'nodes: {}, edges: {}'.format(len(nodes), len(edges_dic)))
    return G


def cal_slc(org):
    G = nx.read_gml("../data/{}/networks/code.gml".format(org))

    N = {}
    Q = {}
    CL = {}
    for node in G.nodes:
        node_nei = list(G.neighbors(node))
        for n_i in node_nei:
            node_nei = node_nei + list(G.neighbors(n_i))
        node_nei = list(set(node_nei))
        N[node] = len(node_nei) - 1

    for node in G.nodes:
        node_nei = list(G.neighbors(node))
        t = 0
        for n_i in node_nei:
            t = t + N[n_i]
        Q[node] = t

    for node in G.nodes:
        node_nei = list(G.neighbors(node))
        t = 0
        for n_i in node_nei:
            t = t + Q[n_i]
        CL[node] = t

    with open('../data/{}/role/code_slc.json'.format(org), 'w', encoding='utf-8') as f:
        json.dump(CL, f, indent=2)
    return CL


def generate_node_edge_txt(org, community):
    """ Generate the node.txt required by Gephi to distinguish CPC-nodes from other nodes in the network """

    G = nx.read_gml("../data/{}/networks/{}.gml".format(org, community))
    cpcs = [dev[:-1] for dev in open(cfg.devs_path.format(org)).readlines()]

    with codecs.open('../data/{}/networks/node_{}.txt'.format(org, community), 'w', 'gbk') as f:
        f.write('ID label Class\r\n')
        for node in G.nodes:
            if node in cpcs:
                cls = 1
            else:
                cls = 2
            f.write(node + ' ' + node + ' ' + str(cls) + '\r\n')

    with codecs.open('../data/{}/networks/edge_{}.txt'.format(org, community), 'w', 'gbk') as f:
        f.write('Source Target\r\n')
        for u, v in G.edges:
            f.write(u + ' ' + v + '\r\n')


if __name__ == '__main__':
    # generate_node_edge_txt('appium', 'chat')
    for org in cfg.orgs:
        print(org)
        # gitter_network(org)
        # github_network(org)
        # cal_slc(org)
        generate_node_edge_txt(org, 'chat')
        generate_node_edge_txt(org, 'code')
        # print()