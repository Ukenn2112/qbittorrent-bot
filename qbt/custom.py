import datetime
import logging

# noinspection PyPackageRequirements
from qbittorrent import Client

from utils import u
from utils import kb
from config import config

logger = logging.getLogger(__name__)


STATES_DICT = {
    'error': '错误',
    'missingFiles': '缺失文件',
    'pausedUP': '暂停中 - 下载完成',
    'pausedDL': '暂停中 - 下载未完成',
    'queuedUP': '排队中 等待上传',
    'queuedDL': '排队中 等待下载',
    'forcedDL': '强制下载',
    'forcedUP': '强制上传',
    'uploading': '上传中',
    'stalledUP': '上传中 - 无速度',
    'checkingUP': '检查已完成的种子',
    'checkingDL': '检查还在下载的种子',
    'downloading': '下载中',
    'allocating': '预分配磁盘空间',
    'stalledDL': '下载中 - 无速度',
    'metaDL': '获取元素据',
    'checkingResumeData': '检查下载进度',
    'moving': '移动中',
    'unknown': '未知状态'
}

# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation#get-torrent-list
# https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation#get-torrent-generic-properties
NEW_ATTRS = {
    'state_pretty': lambda t: STATES_DICT.get(t['state'], t['state']),
    'size_pretty': lambda t: u.get_human_readable(t['total_size']),  # already a string apparently
    'dl_speed_pretty': lambda t: u.get_human_readable(t['dl_speed']),
    'up_speed_pretty': lambda t: u.get_human_readable(t['up_speed']),
    'dlspeed_pretty': lambda t: u.get_human_readable(t['dlspeed']),
    'upspeed_pretty': lambda t: u.get_human_readable(t['upspeed']),
    'generic_speed_pretty': lambda t: u.get_human_readable(t['generic_speed']),
    'progress_pretty': lambda t: round(t['progress'] * 100),
    'eta_pretty': lambda t: str(datetime.timedelta(seconds=t['eta'])),  # apparently it's already a string?
    'time_elapsed_pretty': lambda t: str(datetime.timedelta(seconds=t['time_elapsed'])),
    'force_start_pretty': lambda t: '是' if t['force_start'] else '否',
    'share_ratio_rounded': lambda t: round(t['share_ratio'], 5),
    'dl_limit_pretty': lambda t: '无限制' if t['dl_limit'] == -1 else u.get_human_readable(t['dl_limit'])
}

TORRENT_STRING = """• [{priority}] <code>{name}</code>
  <b>进度</b>: {progress_bar} {progress_pretty}%
  <b>状态</b>: {state_pretty}
  <b>大小</b>: {size_pretty}
  <b>当前下载/上传速度</b>: {dl_speed_pretty}/s, {up_speed_pretty}/s
  <b>速度限制</b>: {dl_limit_pretty}
  <b>种子</b> {num_leechs}, {num_seeds}
  <b>用户</b>: {peers_total} ({peers}), {seeds_total} ({seeds})
  <b>连接数</b>: {nb_connections}
  <b>分享率</b>: {share_ratio_rounded}
  <b>剩余时间</b>: {eta_pretty}
  <b>添加于</b>: {time_elapsed_pretty}
  <b>分类</b>: {category}
  <b>强制继续</b>: {force_start_pretty}
  [<a href="{info_deeplink}">任务详情</a>]"""


# noinspection PyUnresolvedReferences
class Torrent:
    def __init__(self, qbt, torrent_dict):
        self._torrent_dict = torrent_dict
        self._qbt = qbt

        self.refresh_properties(refresh_torrent_dict=False)

        self.actions_keyboard = kb.actions_markup(self.hash)

    def short_markup(self, *args, **kwargs):
        return kb.short_markup(self.hash, *args, **kwargs)
    
    def dict(self):
        return self._torrent_dict

    def refresh_properties(self, refresh_torrent_dict=True):
        if refresh_torrent_dict:
            logger.debug('refreshing torrent dict')
            self._torrent_dict = self._qbt.torrent(self.hash).dict()
        
        for key, val in self._torrent_dict.items():
            setattr(self, key, val)

    def __getitem__(self, item):
        return getattr(self, item)

    def string(self, refresh_properties=False):
        if refresh_properties:
            self.refresh_properties(refresh_torrent_dict=True)
        
        return TORRENT_STRING.format(**self._torrent_dict)

    def pause(self):
        return self._qbt.pause(self.hash)

    def resume(self):
        return self._qbt.resume(self.hash)

    def toggle_force_start(self, value=True):
        # 'force_start' method name cannot be used because it is already a property
        return self._qbt.force_start([self.hash], value=value)

    def increase_priority(self):
        return self._qbt.increase_priority([self.hash])

    def max_priority(self):
        return self._qbt.set_max_priority([self.hash])

    def recheck(self):
        return self._qbt.recheck([self.hash])

    def trackers(self):
        return self._qbt.get_torrent_trackers(self.hash)

    def delete(self, with_files=False):
        if with_files:
            return self._qbt.delete_permanently([self.hash])
        else:
            return self._qbt.delete([self.hash])


class CustomClient(Client):
    def __init__(self, url, bot_username):
        self._bot_username = bot_username
        super(CustomClient, self).__init__(url=url)
        self.online = True

    def _polish_torrent(self, torrent):
        if 'progress' in torrent:
            torrent['eta'] = 0 if torrent['progress'] == 1 else torrent['eta']  # set eta = 0 for completed torrents
            torrent['progress_bar'] = u.build_progress_bar(torrent['progress'])
        if 'hash' in torrent:
            # torrent['resume_deeplink'] = 'https://t.me/{}?start=resume{}'.format(self._bot_username, torrent['hash'])
            # torrent['pause_deeplink'] = 'https://t.me/{}?start=pause{}'.format(self._bot_username, torrent['hash'])
            torrent['manage_deeplink'] = 'https://t.me/{}?start=manage{}'.format(self._bot_username, torrent['hash'])
            torrent['info_deeplink'] = 'https://t.me/{}?start=info{}'.format(self._bot_username, torrent['hash'])

        torrent['short_name'] = torrent['name'] if len(torrent['name']) < 51 else torrent['name'][:51] + '...'

        torrent['generic_speed'] = torrent['dlspeed']
        if torrent['state'] in ('uploading', 'forcedUP'):
            torrent['generic_speed'] = torrent['upspeed']

        for k, v in NEW_ATTRS.items():
            try:
                torrent[k] = v(torrent)
            except KeyError:
                # it might be that one of the lambdas uses a key that is not available in the torrent dict,
                # eg. when we call CustomClient.torrents() with get_properties=False
                continue

        return {k: v for k, v in torrent.items()}

    @property
    def save_path(self):
        return self.preferences()['save_path']

    def _set_torrents_queueing(self, value):
        value = bool(value)

        return self.set_preferences(**{'queueing_enabled': value})

    def enable_torrents_queueing(self):
        return self._set_torrents_queueing(True)

    def disable_torrents_queueing(self):
        return self._set_torrents_queueing(False)

    @property
    def torrents_queueing(self):
        return self.preferences()['queueing_enabled']

    def torrents(self, get_properties=True, **kwargs):
        torrents = super(CustomClient, self).torrents(**kwargs) or []

        if get_properties:
            # asking for the torrents list will return a list of torrents with some details included,
            # but we can get even more details by calling get_torrent() on each torrent
            for torrent in torrents:
                details = self.get_torrent(torrent['hash'])
                if not details:
                    continue

                for k, v in details.items():
                    if k in torrent:
                        continue

                    torrent[k] = v

        return [Torrent(self, self._polish_torrent(torrent)) for torrent in torrents]

    # noinspection PyUnresolvedReferences
    def torrent(self, torrent_hash):
        torrents = self.torrents(filter='all')

        for torrent in torrents:
            if torrent.hash.lower() == torrent_hash.lower():
                return torrent

    # noinspection PyUnresolvedReferences
    def filter(self, query):
        filtered = list()

        for torrent in self.torrents(filter='all'):
            if query in torrent.name.lower():
                filtered.append(torrent)

        return filtered

    def get_schedule(self):
        p = self.preferences()

        if not p['scheduler_enabled']:
            return None

        return dict(
            from_hour='{:0>2}:{:0>2}'.format(p['schedule_from_hour'], p['schedule_from_min']),
            to_hour='{:0>2}:{:0>2}'.format(p['schedule_to_hour'], p['schedule_to_min']),
            days=str(p['scheduler_days'])
        )

    def get_alt_speed(self, human_readable=True):
        p = self.preferences()

        result = dict()

        if human_readable:
            result['status'] = 'on' if self.get_alternative_speed_status() else 'off'
            result['alt_dl_limit'] = u.get_human_readable(p['alt_dl_limit'], 0) if p['alt_dl_limit'] > -1 else 'none'
            result['alt_up_limit'] = u.get_human_readable(p['alt_up_limit'], 0) if p['alt_up_limit'] > -1 else 'none'
        else:
            result['status'] = bool(self.get_alternative_speed_status())
            result['alt_dl_limit'] = p['alt_dl_limit'] if p['alt_dl_limit'] > -1 else None
            result['alt_up_limit'] = p['alt_up_limit'] if p['alt_up_limit'] > -1 else None

        return result

    def get_speed(self):
        tinfo = self.global_transfer_info

        return (
            u.get_human_readable(tinfo['dl_info_speed']),
            u.get_human_readable(tinfo['up_info_speed'])
        )


class OfflineClient:
    """
    We use this calss when we can't connect to qbittorrent, so the bot would still run and let us
    use all the other methods that do not require to be connected to qbittoreent's webAPI
    """

    def __init__(self):
        self.online = False

    def __getattr__(self, name):
        def internal(*args, **kwargs):
            logger.debug('OfflineClient method called: %s', name)
            self._raise()

        return internal()

    def _raise(self):
        raise ConnectionError('cannot connect to qbittorrent ({})'.format(config.qbittorrent.url))
