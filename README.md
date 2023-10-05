# PLEX 中文本地化
plex 的中文电影默认排序是按照笔画数排的，对检索中文电影十分不友好，运行此脚本后可对指定电影库进行拼音排序，并可使用拼音首字母检索电影。关于多线程，测试了数量为 170 的电影库，单线程用时 3.4943103790283203 秒，4线程用时 1.3947198390960693 秒，该结果仅供参考。

- 实现除照片外，所有类型媒体库按标题拼音首字母排序。
- 实现除照片外，所有类型媒体库类别标签更改中文。
- 实现保存配置文件简化下次运行流程。
- 支持多线程运行，一定程度上提高了大容量媒体库的修改速度。



# 第三方模块依赖

    pip install pypinyin

# 一般运行
直接执行即可，通过命令行交互进行选择：

    已成功连接到服务器DATACENTER
    0> 测试库1
    1> 测试库2
    2> 电影
    3> 剧集
    4> 纪录片
    5> 其他影片
    请选择库：0
    
    1> 电影
    2> 节目
    8> 艺术家
    9> 专辑
    10> 单曲
    请选择要操作的类型：1
    共计170个媒体
    
    请输入运行的线程数（输入整数数字，默认为2）：2
    运行完毕，用时 0.5379037857055664 秒


# 非交互式运行（以便于无人值守使用）
使用带参数的命令，参数顺序不可自由调整：

    python plex_localization_zhcn.py http://192.168.3.2:32400 cRBnx9eQDgGy9zs4G-7F 0 1 2

其中 `http://192.168.3.2:32400` 为连接地址，格式需要正确，结尾不可带斜杠， `cRBnx9eQDgGy9zs4G-7F` 为 TOKEN ，后面的三个数字分别为 `库` `操作类型` `线程数`。可以先使用交互式操作了解每个参数的含义。
    
# Python 版本
- 仅在 3.11 版本完成测试
- 推测 3.9 版本可以支持，但未经测试。

# Todo

- [x] 移除 plexapi 库依赖
- [x] 更改排序为拼音后，锁定字段，避免刷新元数据时被更改
- [x] 支持存储配置文件以简化下次登录流程
- [x] 剧集类型库，解决部分标签无法翻译的问题
- [x] 增加音乐库艺术家类型支持
- [x] 增加音乐库专辑类型支持
- [x] 增加音乐库 风格(style)标签 支持
- [x] 增加多线程支持
- [x] 增加命令行参数支持，以便于无人值守运行

# 如何查看 PLEX TOKEN

- PLEX 服务器部署在 Windows 系统时，可通过注册表 `计算机\HKEY_CURRENT_USER\Software\Plex, Inc.\Plex Media Server` 中的 `PlexOnlineToken` 项来查看 TOKEN 值
