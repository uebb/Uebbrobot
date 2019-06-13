#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : regtime.py
# @Author: Uebb
# @Date  : 2019/6/11 0011
from nonebot import on_command,CommandSession
import json
import requests
import jsonpath
import time

@on_command('regtime', aliases=('注册', '注册时间'))
async def regtime(session):
    reg = session.get('regtime', prompt='忘记输UID了？')
    print(session.state,'@on_command')
    # 获取注册时间的详情
    reg_report = await get_regtime_of_user(reg)
    # 向用户发送注册时间详情
    await session.send(reg_report)

@regtime.args_parser
async def regtime_parser(session):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    #print(stripped_arg,'@medal')

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:

            session.state['regtime'] = stripped_arg
            #print(session.state)
        return

    if not stripped_arg:

        session.pause('查询的UID不能为空，请重新输入')

async def get_regtime_of_user(reg):
    # 这里简单返回一个字符串
    # 实际应用中，返回勋章内容json并解析
    try:

        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 74.0.3729.157Safari / 537.36'
        }

        url = 'https://api.live.bilibili.com/user/v2/User/getMultiple?uids[0]=' + str(reg) + '&attributes[1]=card'
        response = requests.get(url, headers=headers)
        html_str = response.content.decode()
        jsonobj = json.loads(html_str)

        uid = jsonpath.jsonpath(jsonobj, '$..uid')[0]
        regtime = jsonpath.jsonpath(jsonobj, '$..regtime')[0]
        timeStamp = regtime  # 十位数时间戳转换工具
        timeArray = time.localtime(timeStamp)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


        result =   '\n注册时间:' +  str(formatTime)


        return 'UID:[' +str(uid) +']的查询如下:' + result
    except :
        return '请检查UID是否正确'