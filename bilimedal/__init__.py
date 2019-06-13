#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : medal.py
# @Author: Uebb
from nonebot import on_command,CommandSession
import json
import requests



@on_command('medal', aliases=('勋章', '查勋章'))
async def medal(session):
    uid = session.get('medal', prompt='忘记输UID了？')
    print(session.state,'@on_command')
    # 获取勋章的详情
    uid_report = await get_medal_of_user(uid)
    # 向用户发送勋章详情
    await session.send(uid_report)

@medal.args_parser
async def medal_parser(session):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    #print(stripped_arg,'@medal')

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:

            session.state['medal'] = stripped_arg
            #print(session.state)
        return

    if not stripped_arg:

        session.pause('查询的UID不能为空，请重新输入')

async def get_medal_of_user(uid):
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
            result = result + str(medal_list[a]['medal_name']) + ' ' + str(medal_list[a]['level']) + ':' + str(medal_list[a]['intimacy']) + '/' + str(medal_list[a]['next_intimacy']) + ' ' + '投喂:' + str(medal_list[a]['today_intimacy']) +'\n'

        return 'UID:[' +str(uid) +']的查询如下:' +'\n'+ result
    except :
        return '请检查UID是否正确'
