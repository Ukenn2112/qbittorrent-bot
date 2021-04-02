from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

SORTING_KEYS = ('name', 'size', 'progress', 'eta')

MAIN_MENU = ReplyKeyboardMarkup([['torrents'], ['speed cap'], ['pause all', 'resume all']], resize_keyboard=True)

LISTS_MENU = ReplyKeyboardMarkup(
    [
        ['all', 'completed'],
        ['downloading', 'paused'],
        ['active', 'inactive'],
        ['back']
    ],
    resize_keyboard=True
)

QUICK_MENU_BUTTON = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('🐇', callback_data='quick:altoff'),
        InlineKeyboardButton('🐌', callback_data='quick:alton'),
        InlineKeyboardButton('10 🐌', callback_data='altdown:10'),  # change alternative download speed
        InlineKeyboardButton('50 🐌', callback_data='altdown:50'),  # change alternative download speed
        InlineKeyboardButton('100 🐌', callback_data='altdown:100'),  # change alternative download speed
        InlineKeyboardButton('200 🐌', callback_data='altdown:200'),  # change alternative download speed
    ],
    [
        InlineKeyboardButton('✅🕑', callback_data='quick:schedon'),
        InlineKeyboardButton('❌🕑', callback_data='quick:schedoff'),
        InlineKeyboardButton('🔄 %', callback_data='quick:refresh:percentage'),
        InlineKeyboardButton('🔄 kb/s', callback_data='quick:refresh:dlspeed'),
    ]
])

SPEEDCAP_MENU = InlineKeyboardMarkup([[InlineKeyboardButton('toggle', callback_data='togglespeedcap')]])

REFRESH_ACTIVE = InlineKeyboardMarkup([[InlineKeyboardButton('refresh', callback_data='refreshactive')]])

REMOVE = ReplyKeyboardRemove()


def sort_markup(qbfilter, exclude_key='', row_width=2):
    markup = []
    sorting_keys_new = [e for e in SORTING_KEYS if e != exclude_key]
    for i in range(0, len(sorting_keys_new), row_width):
        row_keys = sorting_keys_new[i:i + row_width]
        row = [InlineKeyboardButton(row_key, callback_data='sort:{}:{}'.format(qbfilter, row_key)) for row_key in row_keys]
        markup.append(row)

    return InlineKeyboardMarkup(markup)


def actions_markup(torrent_hash):
    markup = [
        [
            InlineKeyboardButton('继续', callback_data='resume:{}'.format(torrent_hash)),
            InlineKeyboardButton('暂停', callback_data='pause:{}'.format(torrent_hash)),
            InlineKeyboardButton('刷新本页', callback_data='refresh:{}'.format(torrent_hash)),
        ],
        [
            InlineKeyboardButton('强制继续', callback_data='forcestart:{}'.format(torrent_hash)),
            InlineKeyboardButton('取消强制继续', callback_data='unforcestart:{}'.format(torrent_hash)),
            InlineKeyboardButton('查看trackers', callback_data='trackers:{}'.format(torrent_hash))
        ],
        [
            InlineKeyboardButton('提升优先级', callback_data='priorityup:{}'.format(torrent_hash)),
            InlineKeyboardButton('最大优先级', callback_data='maxpriority:{}'.format(torrent_hash))
        ],
        [
            InlineKeyboardButton('删除', callback_data='deletewithfiles:{}'.format(torrent_hash)),
            InlineKeyboardButton('强制重新效验', callback_data='recheck:{}'.format(torrent_hash)),
            InlineKeyboardButton('返回', callback_data='reduce:{}'.format(torrent_hash)),
        ]
    ]

    return InlineKeyboardMarkup(markup)


def confirm_delete(torrent_hash):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('不, 返回', callback_data='manage:{}'.format(torrent_hash)),
        InlineKeyboardButton('是, 删除', callback_data='confirmdeletewithfiles:{}'.format(torrent_hash))
    ]])


def short_markup(torrent_hash, force_resume_button=True, max_priority_button=True):
    markup = [[
        InlineKeyboardButton('暂停', callback_data='pause:{}'.format(torrent_hash)),
        InlineKeyboardButton('管理', callback_data='manage:{}'.format(torrent_hash)),
    ]]

    if max_priority_button:
        markup[0].insert(0, InlineKeyboardButton('最大优先级', callback_data='maxpriority:{}'.format(torrent_hash)))

    if force_resume_button:
        markup[0].insert(0, InlineKeyboardButton('强制继续', callback_data='forceresume:{}'.format(torrent_hash)))

    return InlineKeyboardMarkup(markup)


def alternative_download_limits(values: [list, tuple]):
    markup = [[]]
    for kbs in values:
        markup[0].append(InlineKeyboardButton('{} kbs'.format(kbs), callback_data='altdown:{}'.format(kbs)))

    return InlineKeyboardMarkup(markup)
