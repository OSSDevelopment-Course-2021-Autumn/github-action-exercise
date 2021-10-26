#coding: utf-8

from flask import Flask, request
from markupsafe import escape
from flask import render_template, jsonify
from flask_cors import CORS
import pymongo
import random as rd
from collections import Counter


app = Flask(__name__)
app.debug = True
#为了解决vue与jinja2的语法冲突，这里把jinja2的标志进行修改
#不过以后用jinja2的话，编码可能需要注意到这里的修改！
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
CORS(app)

vector_feature_list = ["feature", "fix", "refactor", "test", "doc", 
    "deprecate", "build", "deploy", "license", "other"] #跟data_prepare.py一致

def upper_comp(comp_name):
    if len(comp_name) <= 3:
        return comp_name.upper() #全部大写
    return comp_name.title() # 每个单词首字母大写

@app.route('/development_test')
def dev_test():
    return render_template("test.html")

# company dashboard 主页创建时会对这个url进行请求，返回主页所需要的数据
# 公司类型和数量、项目类型和数量、task类型和数量
# 前端会绘制饼图
@app.route('/home')
def home():
    global vector_feature_list
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client['company_dashboard']
    collection1 = db['company_type']
    company_type = collection1.find() #返回的是一个生成器，需要遍历取到结果
    comp2type = {}
    for i in company_type:
        if i['type'] not in comp2type:
            comp2type[i['type']] = 0
        comp2type[i['type']] += 1

    collection2 = db['repository_type']
    repository_type = collection2.find() #返回的是一个生成器，需要遍历取到结果

    repo2type = {}
    for i in repository_type:
        if i['type'] not in repo2type:
            repo2type[i['type']] = 0
        repo2type[i['type']] += 1

    collection3 = db['task_amount']
    task2amount = {}
    for task in vector_feature_list:
        res = collection3.count_documents({'task': task})
        task2amount[task] = res
    #print(comp2type)
    #print(repo2type)
    #print(task2amount)

    # repo2type 的种类太多，导致饼状图过于臃肿，所以这里合并数量少的那些repository类型
    a = list(repo2type.values())
    a.sort()
    a.reverse()
    other = 0
    newrepo2type = {}
    for k, v in repo2type.items():
        if v <= a[10]:
            other += v
        else:
            newrepo2type[k] = v
    newrepo2type['other'] = other
    repo2type = newrepo2type

    response = {
        'ct2amount': comp2type, #叫comptype2amount更贴切
        'rt2amount': repo2type, #叫repotype2amount更贴切
        'task2amount': task2amount
    }
    return jsonify(response) #把信息交给前端处理。前端监听对应的端口，接受json返回值进行渲染页面

@app.route('/comp_list') # 返回给首页的公司选择组件
def comp_list():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client['company_dashboard']
    collection = db['company_type']
    res = collection.find()
    comp_list = [x['company'] for x in res]
    icomp_list = ["red hat", "rackspace", "nec", 
        "hpe", "mirantis", "ibm", "intel", "hp", 
        "huawei", "canonical"] # important comp list

    # 把所有的公司都变成首字母大写；如果长度<=3，那么全部大写字母
    comp_list = [upper_comp(c) for c in comp_list]
    icomp_list = [upper_comp(c) for c in icomp_list]

    response = {
        'comp_list': comp_list,
        'icomp_list': icomp_list
    }
    return jsonify(response)

# 要求输入格式是yyyy-mm
# 输出的月份一定得两位
def next_month(month):
    y = int(month[:4])
    m = int(month[5:])
    m += 1
    if m == 12:
        y += 1
        m = 1
    if m < 10:
        return str(y) + '-0' + str(m)
    else:
        return str(y) + '-' + str(m)

@app.route('/company/<comp_name>', methods=['POST'])
def company_info(comp_name):
    #贡献最多的项目：贡献最多的task数量那个项目，不少于最多项目的80%task数量的其他项目
    #贡献最多的task：同理
    if request.method == 'POST':
        compared_company = request.form['compared_company'].strip().split('  ')
        compared_company = [x.lower() for x in compared_company if x]

    comp_name = comp_name.lower()

    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client['company_dashboard']

    # 公司目标获取
    collection = db['company_type']
    res = collection.find_one({'company': comp_name})
    comp_type = ""
    if res: # 如果是None代表不存在人工分出的公司类型
        comp_type = res['type']

    Grepo2type = {} # G是global的意思，但是其实并不global，历史遗留问题
    collection = db['repository_type']
    res = collection.find()
    for i in res:
        Grepo2type[i['repository']] = i['type']
    # 得到不同rt对应的task数量有多少
    # 按照task数量来缩减rt到other类型，而不是通过repo数量缩减
    collection = db['task_amount']
    res = collection.find()
    rt2tcnt = {}
    total = 0
    for i in res:
        total += 1
        if i['repository'] not in Grepo2type:
            continue
        rt = Grepo2type[i['repository']]
        if rt not in rt2tcnt:
            rt2tcnt[rt] = 0
        rt2tcnt[rt] += i['amount']
    # print("######### TOTAL of collection task_amount: %d"%(total)) # 输出为224170，应该没问题
    # print(rt2tcnt)
    # 合并数量过少的repo type
    # TODO: 可以用先验知识取代这部分代码
    a = list(rt2tcnt.values())
    a.sort()
    a.reverse()
    # print(a.most_common(10))
    limit = a[10]
    # print(a)
    # print("limit is %d"%(limit))
    for r, t in Grepo2type.items():
        # Grepotype中有且仅有一个类型不在rt2tcnt中，如下行，猜测是因为数据库task_amount中没有
        # Bridges for integration sardonic not in rt2tcnt
        if t not in rt2tcnt:
            continue
        if rt2tcnt[t] <= limit:
            Grepo2type[r] = 'other'

    # 公司偏好的项目和任务；和偏好具体的饼图数据
    collection = db['task_amount']
    res = collection.find({"company": comp_name})
    rt2amount = {}
    repo2amount = {}
    task2amount = {}
    for i in res:
        r = i['repository']
        t = i['task']
        if r not in repo2amount:
            repo2amount[r] = 0
        if t not in task2amount:
            task2amount[t] = 0
        repo2amount[r] += i['amount']
        task2amount[t] += i['amount']
        if i['repository'] not in Grepo2type: # 没有分类的项目数据不算入饼图
            continue
        rt = Grepo2type[i['repository']]
        if rt not in rt2amount:
            rt2amount[rt] = 0
        rt2amount[rt] += i['amount']

    #print(comp_name)
    #print(len(repo2amount))
    #print(len(task2amount))
    rmost = max([x for x in repo2amount.values()])
    tmost = max([x for x in task2amount.values()])
    rret = []
    for r, a in repo2amount.items():
        if a >= 0.8 * rmost:
            rret.append({'repository': r, 'amount': a})
    tret = []
    for t, a in task2amount.items():
        if a >= 0.8 * tmost:
            tret.append({'task': r, 'amount': a})

    collection = db['month_comp']
    # 需要得到每个月贡献强度和贡献广度的公司集合
    comp_list = compared_company
    if comp_name not in compared_company:
        comp_list.append(comp_name) # 需要展示贡献强度和广度的公司不只有勾选上的公司，也有dashboard页面的主体公司
    # 先确定贡献强度和广度图需要展示的最小的月份和最大的月份
    max_month_list = []
    min_month_list = []
    for c in comp_list:
        temp = collection.find_one({"company": c}, sort = [("month", -1)])
        max_month_list.append(temp['month'])
        temp = collection.find_one({"company": c}, sort = [("month", 1)])
        min_month_list.append(temp['month'])
    max_month = max(max_month_list) # 所有需要提供贡献强度和和广度的公司，所应该呈现的最大的月份
    min_month = min(min_month_list) # 所有需要提供贡献强度和和广度的公司，所应该呈现的最小的月份

    month_list = []
    month = min_month
    while month <= max_month:
        month_list.append(month)
        month = next_month(month)
    month_state = {c:[] for c in comp_list} # 里面格式为{company: [month1:{xxx}, month2: {xxx}]}
    for month in month_list:
        for c in comp_list:
            res = collection.find_one({"company": c, "month": month})
            if not res: # 未找到这个月公司的贡献情况
                month_state[c].append({
                    "extent_rel_r": 0.0, 
                    "extent_rel_rt": 0.0, 
                    "intensity_rel_cmt": 0.0, 
                    "intensity_rel_dev": 0.0
                })
            else:
                month_state[c].append({
                    "extent_rel_r": res['extent_rel_r'],
                    "extent_rel_rt": res['extent_rel_rt'],
                    "intensity_rel_cmt": res['intensity_rel_cmt'],
                    "intensity_rel_dev": res['intensity_rel_dev']
                })

    # 得到每个月的统计数据。这里只使用了commit为例
    collection = db['month_comp']
    stat_max_month = collection.find_one({"company": comp_name}, sort = [("month", -1)]) # 对于dashboard主体company而言的最大月份，与贡献强度和广度所需不同
    stat_max_month = stat_max_month['month']
    stat_min_month = collection.find_one({"company": comp_name}, sort = [("month", 1)]) # 对于dashboard主体company而言的最小月份，与贡献强度和广度所需不同
    stat_min_month = stat_min_month['month']
    commit_state = []
    month_list_main = []
    month = stat_min_month
    while month <= stat_max_month:
        month_list_main.append(month)
        month = next_month(month)
    collection = db['month_comp_repo']
    for month in month_list_main:
        # Rtotal是指对全部的repository做贡献的数据在数据库中的名称
        res = collection.find_one({"company": comp_name, "month": month, "repository": "Rtotal"})
        if not res:
            continue
        commit_state.append(res['commit_amount'])

    # 以网络形式展示公司合作关系
    nodes = []
    edges = []
    cid = 1
    comp2cid = {comp_name: 0} # 记录在网络中的节点id
    # 得到合作关系密切的公司
    collection = db['company_coop_text']
    coop_text = collection.find_one({"company": comp_name})['coop_text'].strip(';')
    coop_dict = {}
    for item in coop_text.split(";"):
        temp = item.split('###')
        coop_dict[temp[0]] = temp[1] # {comp => coop_intensity}
        if temp[0] not in comp2cid:
            comp2cid[temp[0]] = cid
            cid += 1
    collection = db['company_coop_intensity']
    maxi_node_value = -1
    for comp, intensity in coop_dict.items():
        res = collection.find_one({"company1": comp_name, "company2": comp})
        s0 = "协作强度: " + str(res['coop_intensity'])
        #s0 = ""
        s1 = "协作项目: " + ", ".join(res['repository'].split(';'))
        s1 = ""
        nodes.append({# 事实上，vis里面的id，label等属性并不带有引号，不知道后面会不会出现偏差 => 不会，js的object key加不加都一样
            'id': comp2cid[comp],
            'label': comp,
            'value': res['coop_intensity']**0.5 #节点大小
        })
        edges.append({
            'from': comp2cid[comp_name],
            'to': comp2cid[comp],
            'label': s0 + s1,
            'width': max((res['coop_intensity']//10)**0.5, 1) #线的宽度。贡献最多的mirantis最高合作强度是3400，做个变换让线不太粗
        })
        maxi_node_value = max(maxi_node_value, res['coop_intensity'] ** 0.5 * 1.5)
    nodes.append({
        'id': 0,
        'label': comp_name,
        'value': maxi_node_value
    })
    response = {
        'goal': comp_type, #商业目标
        'comp_type': comp_type,
        'repo_pref': rret,
        'task_pref': tret, 
        'repo2amount': rt2amount,
        'task2amount': task2amount,
        'month_list': month_list,
        'month_state': month_state,
        'month_list_main': month_list_main,
        'commit_state': commit_state,
        'nodes': nodes,
        'edges': edges,
        'test': "You receive response!"
    }
    return jsonify(response)

@app.route('/vue_test')
def vue_test():
    return render_template("vue-test/index.html") #not work, just raw html rather than rendered by Vue.js

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000)

