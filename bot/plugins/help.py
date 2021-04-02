import logging

# noinspection PyPackageRequirements
from telegram.ext import CommandHandler, RegexHandler

from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


HELP_MESSAGE = """<b>帮助列表</b>:

<i>显示任务</i>
• /start 或 /help: 显示帮助
• /completed, /active, /paused, /downloading, /inactive, /all: 按状态显示种子列表
• /tostart: 显示未开始或未完成的种子
• /quick: 显示正在活动的种子
• /filter 或 /f <code>[关键词]</code>: 搜索种子(支持关键词匹配)
• /priorities: 按优先级显示前25个种子
• /settings 或 /s: 获取当前qBittorrent的配置参数
• /json: 得到一个包含所有种子的json文件
• /version: 显示当前qbittorrent和API版本

<i>添加任务</i>
• 上传<code>.torrent</code>后缀的文件: 按文件添加种子
• 磁力链接: 通过磁力链接添加种子

<i>设置</i>
• /altdown: 通过按钮设置备用最大下载速度
• /altdown <code>[单位 kb/s]</code>: 设置备用最大下载速度
• /altup <code>[单位 kb/s]</code>: 设置备用最大上传速度
• /pauseall: 暂停所有种子
• /resumeall: 开始所有的种子
• /set <code>[设置项目] [变更参数]</code>: 更改设置

<i>管理</i>
• /getlog 或 /log: 获取日志文件
• /permissions: 获取当前的权限配置。
• /pset <code>[key] [val]</code>: 更改密钥权限
• /config: 获取qbittorrent的配置文件部分

<i>FREE commands</i>
• /rmkb: remove the keyboard, if any"""


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_help(_, update):
    logger.info('/help from %s', update.message.from_user.first_name)

    update.message.reply_html(HELP_MESSAGE)


updater.add_handler(CommandHandler('help', on_help))
updater.add_handler(RegexHandler(r'^\/start$', on_help))
