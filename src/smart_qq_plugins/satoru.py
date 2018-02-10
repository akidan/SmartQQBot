# coding: utf-8
import json
import os
import random
from random import randint
import re
import time

from smart_qq_bot.logger import logger
from smart_qq_bot.messages import PrivateMsg
from smart_qq_bot.signals import on_group_message, on_private_message

REPLY_SUFFIX = (
    '~','!','♡','❤','💙','💚','💛','💜','💕','💖','💗','💝','💞','🧡','😍','👏','👍','✌','🤘','💪','🤙🤙🤙','🖕'
)

class Satoru(object):

    def __init__(self, data_file):
        self.data = {}
        self.load(data_file)
        self.data_file = data_file
        self._learn_regex = re.compile("^#(.+?)\s*?#(.+)")
        self._remove_regx = re.compile("^遗忘 (.*)")

    def is_learn(self, key, sender_qq_id, sender_card_name):
        result = re.findall(self._learn_regex, key)
        if result:
            myList = list(result[0])
            res = list([myList[0].strip(), list([myList[1],sender_qq_id,sender_card_name,int(time.time())])])
            res_tuple = tuple(res)
            return res_tuple
        return None

    def is_remove(self, key):
        result = re.findall(self._remove_regx, key)
        if result:
            return result[0]
        return None

    def load(self, data_file):
        if os.path.isfile(data_file):
            with open(data_file, "r") as f:
                self.data = json.load(f)

    def add_rule(self, key, response, nickname):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(response)
        reply = "感谢"+nickname+"教我关于#"+key+" 的知识" + random.choice(REPLY_SUFFIX)
        return self.save(reply)

    def remove_rule(self, key):
        if key in self.data:
            del self.data[key]
            reply = "已经遗忘#"+key+" 的知识" + random.choice(REPLY_SUFFIX)
        else:
            reply = "没有找到#"+key+" 的知识" + random.choice(REPLY_SUFFIX)
        return self.save(reply)

    def match(self, key):
        if key in self.data:
            result = self.data[key]
        exist = False
        keylist = []
        for d in self.data:
            if d in key:
                exist = True
                keylist.append(d)
        if exist:
            keyword = random.choice(keylist)
            result = self.data[keyword]
            res_list = result[randint(0, len(result) - 1)]
            return res_list[0]
            # next version
            #return res_list[0]+"\n(感谢 "+res_list[2]+" 提供关于 "+reslist[0]+" 的信息)"
        return None

    def save(self, reply):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f)
        logger.info("Satoru's data file saved.")
        return reply


satoru = Satoru("./satoru.json")


@on_group_message(name="学习知识")
def send_msg(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.GroupMsg
    """
    #print (msg.src_sender_card)
    result = satoru.is_learn(msg.content, msg.src_sender_id, msg.src_sender_card)
    if result:
        key, value = result
        response = satoru.add_rule(key, value, msg.src_sender_card)
    else:
        response = satoru.match(msg.content)
    if response:
        bot.reply_msg(msg, response)


@on_private_message(name="遗忘知识")
def remove(msg, bot):
    result = satoru.is_remove(msg.content)
    if result:
        response = satoru.remove_rule(result)
        if response:
            bot.reply_msg(msg, response)
