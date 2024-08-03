# PLEX 媒体元数据中文本地化

PLEX 对中文标题的媒体，默认按照笔画数排列，对检索中文电影不友好，此脚本可对指定电影库进行拼音排序，并可使用拼音首字母检索媒体，同时汉化流派、风格、情绪、国家、导演标签。

### 功能
- 按标题拼音首字母排序。
- 流派、风格、情绪、国家、导演标签汉化。
- 支持使用命令行参数或配置文件运行。


# 使用方法 1：配置文件

### 1. 下载文件

下载 `mediameta_zhcnl10n_for_plex.py` `config.yaml` `tags.yaml` 三个文件，放在同一个目录下

### 2. 安装依赖

    pip install pypinyin PlexAPI PyYAML

### 3. 编辑配置文件

打开 `config.yaml` 编辑配置文件，配置文件中有各项配置的详细说明。

### 4. 可选：自定义标签翻译字典

打开 `tags.yaml` 编辑标签翻译字典，请注意格式。

### 5. 运行

    python mediameta_zhcnl10n_for_plex.py

# 使用方法 2：配置参数


    python mediameta_zhcnl10n_for_plex.py baseurl="http://192.168.3.2:32400" token="cRBnx9eQDgGy9zs4G-7F"

完整的参数如下：

| 参数名        | 必填 | 默认值         | 用途                                       | 
|------------|----|-------------|------------------------------------------|
| configfile |    | config.yaml | 指定一个配置文件，在不使用默认的配置文件名或路径时有用              |
| baseurl    | ✔  |             | plex 服务器的地址                              |
| token      | ✔  |             | plex 服务器的 token                          |
| daysago    |    | 0           | 指定一个天数，比如 5 ，则脚本只会筛选 5 天内新添加的媒体。0 表示不筛选。 |
| sorttitle  |    | True        | 开启排序标题转拼音首字母功能                           |
| transtags  |    | True        | 开启标签翻译功能                                 |
| tagsfile   |    | https://mirror.ghproxy.com/raw.githubusercontent.com/sqkkyzx/plex_localization_zhcn/main/tags.yaml   | 标签翻译字典，可以是本地文件路径比如`tags.yaml`，也可以是 url   |


1. 必填指的是，没有配置文件时必填。如果配置文件存在，且格式正确，则会优先从配置文件读取配置，忽略参数配置。
2. 指定库类型和指定标签类型，只有使用配置文件时才支持更改。默认对电影、电视剧、艺术家、专辑、曲目、合集进行操作，翻译的标签默认开启流派、风格、情绪、国家。
  

# 其他说明

### Python 版本
- 仅在 3.12 版本完成测试
- 推测 >= 3.9 版本可以支持，但未经测试。
      
### 如何查看 PLEX TOKEN

- PLEX 服务器部署在 Windows 系统时，可通过注册表 `计算机\HKEY_CURRENT_USER\Software\Plex, Inc.\Plex Media Server` 中的 `PlexOnlineToken` 项来查看 TOKEN 值

### 感谢

- 该脚本参考了 [timmy0209](https://github.com/timmy0209) 的脚本 [plex-chinese-genre](https://github.com/timmy0209/plex-chinese-genre) 及 [plex-pinyin-sort](https://github.com/timmy0209/plex-pinyin-sort) 的思路，于此基础上整理重构而来。
- 2023.10.05 参考了[x1ao4](https://github.com/x1ao4) 提供的合集相关代码。
- 2024.08.03 完全重构，抛弃所有旧代码。感谢 x1ao4 贡献了国家的翻译字典。
