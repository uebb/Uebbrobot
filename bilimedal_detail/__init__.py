#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : __init__.py
# @Author: Uebb
# @Date  : 2019/6/12 0012
# @Desc  :
from nonebot import on_command,CommandSession
import json
import requests
@on_command('detail', aliases=('勋章详情','查勋章'))
async def detail(session):
    uid = session.get('detail', prompt='忘记输UID了？')
    print(session.state,'@on_command')
    # 获取勋章的详情
    uid_report = await get_detail_of_user(uid)
    # 向用户发送勋章详情
    await session.send(uid_report)
@detail.args_parser
async def detail_parser(session):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    #print(stripped_arg,'@medal')
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:

            session.state['detail'] = stripped_arg
            #print(session.state)
        return
    if not stripped_arg:
        session.pause('查询的UID不能为空，请重新输入')
async def get_detail_of_user(uid):
    # 这里简单返回一个字符串
    # 实际应用中，返回勋章内容json并解析
    try:
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 74.0.3729.157Safari / 537.36'
        }
        url = 'https://api.live.bilibili.com/user/v2/User/getMultiple?uids[0]=' + str(uid) + '&attributes[1]=medal'
        response = requests.get(url, headers=headers)
        html_str = response.content.decode()

        jsonobj = json.loads(html_str)
        medal_list = jsonobj['data'][str(uid)]['medal']
        result = ''
        for a in medal_list.keys():
            #        print(a,medal_list[a])
            result = result + str(medal_list[a]['medal_name']) + ':' + '\n'+' ' + str(medal_list[a]['receive_time']) + '||'+'\n' + str(medal_list[a]['today_intimacy']) + '\n' +'\n'
        return 'UID:[' +str(uid) +']的'+'\n'+'勋章获得时间&勋章投喂：'+'\n'+result
    except :
        return '请检查UID是否正确'