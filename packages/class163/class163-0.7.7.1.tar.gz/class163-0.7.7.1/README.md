# Class163

#### 介绍
网易云音乐通用API库，提供了一系列用于操作网易云音乐数据的功能，包括播放列表、音乐文件、搜索等。

#### 软件架构
软件架构说明

- `__init__.py`：包的初始化文件，用于初始化包和定义包的属性。
- `playlist.py`：包含 `Playlist` 和 `playlist_from_detail` 类或函数的实现，用于处理播放列表相关的操作。
- `music.py`：包含 `Music` 和 `music_from_detail` 类或函数的实现，用于处理音乐文件相关的操作。
- `origin_file.py`：包含 `OriginFile` 类的实现，用于处理原始文件相关的操作。
- `search.py`：包含 `Search` 类的实现，用于处理搜索相关的操作。
- `common.py`：包含一些通用的函数或类，用于支持包内其他模块的功能。

#### 安装教程

1. `pip install class163`

#### 使用说明

1. 导入包：`import class163`
2. 创建 `Playlist` 对象：`playlist = class163.Playlist(playlist_id)`
3. 获取播放列表详情：`playlist_detail = playlist.get_detail()`
4. 创建 `Music` 对象：`music = class163.Music(music_id)`
5. 获取音乐文件详情：`music_detail = music.get_detail()`
6. ......

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### 许可证
本项目采用 `GNU_AGPLV3+` 许可证。
