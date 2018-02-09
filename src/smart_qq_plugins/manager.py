# coding: utf-8
import re
from smart_qq_bot.handler import (
    list_handlers,
    list_active_handlers,
    activate,
    inactivate,
)
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message, on_bot_inited, on_private_message

cmd_hello = re.compile(r"hello")
cmd_list_plugin = re.compile(r"技能表")
cmd_inactivate = re.compile(r"禁用技能\{(.*?)\}")
cmd_activate = re.compile(r"开启技能\{(.*?)\}")


def do_activate(text):
    result = re.findall(cmd_activate, text)
    if result:
        activate(result[0])
        return "技能 [%s] 已启用" % result[0]


def do_inactivate(text):
    re.findall(cmd_inactivate, text)
    result = re.findall(cmd_inactivate, text)
    if result:
        inactivate(result[0])
        return "技能 [%s] 已禁用" % result[0]


def do_hello(text):
    if re.match(cmd_hello, text):
        return "小波今天也元气地为大家服务哦！"


def do_list_plugin(text):
    if re.match(cmd_list_plugin, text):
        text = "技能一览(%s): %s\n激活技能(%s): %s" % (
            len(list_handlers()),
            ", ".join(list(list_handlers())),
            len(list_active_handlers()),
            ", ".join(list(list_active_handlers()))
        )
        return text

@on_bot_inited("PluginManager")
def manager_init(bot):
    logger.info("Plugin Manager is available now:)")


@on_all_message(name="唤醒")
def hello_bot(msg, bot):
    result = do_hello(msg.content)
    if result is not None:
        return bot.reply_msg(msg, result)


@on_private_message(name="管家")
def manage_tool(msg, bot):
    private_handlers = (
        do_inactivate, do_activate, do_list_plugin
    )
    for handler in private_handlers:
        result = handler(msg.content)
        if result is not None:
            return bot.reply_msg(msg, result)
