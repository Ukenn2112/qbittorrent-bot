## qBittorrent Telegram 管理机器人

一个非常简单的Telegram机器人，使用 [qBittorrent WebUI中的API (v4.1+)](https://github.com/qbittorrent/qBittorrent/wiki/Web-API-Documentation) 和 [python-qBittorrent](https://github.com/v1k45/python-qBittorrent) .

### 功能

仅实现了qBittorrent Web API的一小部分功能：

- 根据下载状态查看种子列表
- 通过磁力链接/种子文件添加种子
- 管理种子（暂停/恢复，设置强制启动，增加优先级，强制重新检查，删除）
- 启用/禁用/更改替代速度限制
- 查看您的qBittorrent设置
- 将您的种子列表导出为json文件

有关命令列表，请使用 `/help`

### 安装

1. [启用qBittorrent的Web UI](https://github.com/lgallard/qBittorrent-Controller/wiki/How-to-enable-the-qBittorrent-Web-UI)
2. 将 `config.example.toml` 重命名为 `config.toml`
3. 按以下方式编辑 `config.toml` :
  - `[telegram]` 部分：将您的API令牌放置在 `token` 并将您的用户ID放置在 `admins` 中
  - `[qbitttorrent]` 根据您的qBittorrent WebUI设置填写三个值
4. 通过 `pip install -r requirements.txt` 安装所需依赖
5. 通过 `python main.py` 来开始运行

### 权限

默认情况下，任何人都可以使用只读命令 (查看种子列表，过滤种子，查看设置) 但是在 `permissions.json` 文件中有几个值 (如果未启动机器人，则为 `default_permissions.json`) 可以切换设置谁可以使用该机器人：

- `free_read`: 当为 `true` 时, 任何人都可以使用只读命令 (查看种子列表，种子信息和当前设置)
- `free_write`: 当为 `true` 时, 任何人都可以通过磁力链接和文件添加种子。仅在 `free_read` 为 `true` 时有效
- `free_edit`: 当为 `true` 时, 任何人都可以管理torrent和设置qbittorrent。仅在 `free_read` 为 `true` 时有效
- `admins_only`: 当为 `true` 时，除了被列为 `admins` 的用户之外，其他任何人都不能使用该机器人。该设置优先于 `free_*` 设置。

您可以使用 `/permissions` 和 `/pset` 命令在聊天窗口中查看和更改当前权限配置

### 通过测试...

我使这个机器人能够管理我在Raspbian运行的Raspberry上下载的内容 (使用qBittorrent的 [headless version](https://github.com/qbittorrent/qBittorrent/wiki/Setting-up-qBittorrent-on-Ubuntu-server-as-daemon-with-Web-interface-(15.04-and-newer))), 这是我在其中测试过的唯一环境。还有我正在使用的systemd文件， `qbtbot.service` (假设您要在python3虚拟环境中运行该机器人)

### BotFather 命令建议

通过 [@BotFather](https://t.me/botfather) 使用下面的命令来设置你的机器人的命令建议。

```
quick - get an overview of what we're downloading
active - list active torrents
tostart - show torrents that are not active or completed
help - see the help message
completed - list completed torrents
all - list all torrents
downloading - list downloading torrents
paused - list paused torrents
inactive - list inactive torrents
set - change a setting
filter - filter torrents by name
log - get the log file
settings - get the settings list
altdown - set the alternative download speed (in kb/s)
altup - set the alternative upload speed (in kb/s)
json - export the list of torrents
permissions - get the current permissions configuration
pset - change the value of a permission setting
pauseall - pause all torrents
resumeall - resume all torrents
config - get the qbittorrent's section of the config file
rmkb - remove the keyboard
```
