# PLEX 中文本地化
PLEX 对中文标题的媒体，默认按照笔画数排列，对检索中文电影不友好，此脚本可对指定电影库进行拼音排序，并可使用拼音首字母检索媒体，同时汉化流派、风格、情绪标签。

- 实现除照片外，所有类型媒体库按标题拼音首字母排序。
- 实现除照片外，所有类型媒体库类别标签更改中文。
- 实现保存配置文件，简化下次运行流程。
- 支持多线程运行，一定程度上提高了性能，测试媒体数量 170 的电影库，单线程用时 3.49 秒，4线程用时 1.39 秒，供参考。
- 支持使用命令行参数非交互式运行，以便于事件触发、定时触发等无人值守运行。

## 第三方模块依赖

    pip install pypinyin requests

## 交互式运行

直接执行，通过命令行交互进行选择：

    .\plex_localization_zhcn.py
    
    已成功连接到服务器DATACENTER
    
    请输入运行的线程数（输入整数数字，默认为2）：4
    
    1> 电影 <movie>
    2> 剧集 <show>
    3> 纪录片 <show>
    7> 音乐 <artist>
    4> 其他影片 <movie>
    请选择库：1
    
    <movie> 类型共计170个媒体
    ...
    
    <movie> 类型共计48个合集
    ...
    
    运行完毕，用时 0.45556211471557617 秒



## 非交互式运行（便于无人值守使用）
使用带参数的命令，参数顺序和数量不可自由调整：

    python plex_localization_zhcn.py http://192.168.3.2:32400 cRBnx9eQDgGy9zs4G-7F 1 4

其中 `http://192.168.3.2:32400` 为连接地址，格式需要正确，结尾不可带斜杠， `cRBnx9eQDgGy9zs4G-7F` 为 TOKEN ，后面的两个数字分别为 `库ID` 和 `线程数`。
可以先使用交互式操作了解一下每个参数的含义以及对应库的ID。

特殊用例，将选择的库ID 设置为 `999` ，则将遍历除了照片库以外的所有库：

    python plex_localization_zhcn.py http://192.168.3.2:32400 cRBnx9eQDgGy9zs4G-7F 999 4

    已成功连接到服务器DATACENTER

    <movie> 类型共计170个媒体
    
    <movie> 类型共计48个合集
    
    <show> 类型共计2个媒体
    
    <artist> 类型共计1个媒体
    
    <album> 类型共计1个媒体
    
    <track> 类型共计39个媒体
    
    <movie> 类型共计1个媒体
    
    运行完毕，用时 0.7199623584747314 秒
  

## Python 版本
- 仅在 3.11 版本完成测试
- 推测 >= 3.9 版本可以支持，但未经测试。

## Todo

- [x] 移除 plexapi 库依赖
- [x] 更改排序为拼音后，锁定字段，避免刷新元数据时被更改
- [x] 支持存储配置文件以简化下次登录流程
- [x] 剧集类型库，解决部分标签无法翻译的问题
- [x] 增加音乐库艺术家类型支持
- [x] 增加音乐库专辑类型支持
- [x] 增加音乐库 风格(style)标签 支持
- [x] 增加多线程支持
- [x] 增加命令行参数支持，以便于无人值守运行
- [x] 增加所有库遍历运行
      
## 如何查看 PLEX TOKEN

- PLEX 服务器部署在 Windows 系统时，可通过注册表 `计算机\HKEY_CURRENT_USER\Software\Plex, Inc.\Plex Media Server` 中的 `PlexOnlineToken` 项来查看 TOKEN 值

## 感谢

- 该脚本参考了 [timmy0209](https://github.com/timmy0209) 的脚本 [plex-chinese-genre](https://github.com/timmy0209/plex-chinese-genre) 及 [plex-pinyin-sort](https://github.com/timmy0209/plex-pinyin-sort) 的思路，于此基础上整理重构而来。
- 2023.10.05 参考了[x1ao4](https://github.com/x1ao4) 提供的合集相关代码。
