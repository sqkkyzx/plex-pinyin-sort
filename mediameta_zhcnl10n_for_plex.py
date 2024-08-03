import argparse
import logging
import os
import time
from itertools import chain

import yaml
import requests
import pypinyin
import plexapi.media
from plexapi.myplex import PlexServer

logging.basicConfig(level=logging.INFO)

plexapi_reload_options = {
    'checkFiles': False,
    'includeAllConcerts': False,
    'includeBandwidths': False,
    'includeChapters': False,
    'includeChildren': False,
    'includeConcerts': False,
    'includeExternalMedia': False,
    'includeExtras': False,
    'includeFields': False,
    'includeGeolocation': False,
    'includeLoudnessRamps': False,
    'includeMarkers': False,
    'includeOnDeck': False,
    'includePopularLeaves': False,
    'includePreferences': False,
    'includeRelated': False,
    'includeRelatedCount': False,
    'includeReviews': False,
    'includeStations': False
}


def loadtags(source):
    if source.startswith('http://') or source.startswith('https://'):
        # 如果是 URL，使用 requests 获取内容
        response = requests.get(source)
        response.raise_for_status()  # 确保请求成功
        return yaml.safe_load(response.text)
    else:
        # 如果是本地文件路径，读取文件
        if not os.path.isfile(source):
            raise FileNotFoundError(f"File not found: {source}")
        with open(source, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)


def loadconfig():
    def load_allow_libs(yaml_file_path):
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                _allow_libs = {}
                for key, value in data['allowLibs'].items():
                    _allow_libs[key] = [k for k, v in value.items() if v is True]
                _allow_libs = {k: v for k, v in _allow_libs.items() if v}
        except Exception as e:
            logging.error(f'指定的配置文件不存在或解析错误，将使用默认的配置。')
            logging.debug(e)
            _allow_libs = {'movie': ['movie', 'collection'], 'show': ['show'], 'artist': ['artist', 'album']}
        return _allow_libs

    def load_allow_tags(yaml_file_path):
        all_allow_tags = {'Genre': 'genres', 'Style': 'styles', 'Mood': 'moods', 'Country': 'countries',
                          'Director': 'directors'}
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                _allow_tags = {
                    k: all_allow_tags.get(k) for k, v in data['allowTags'].items() if v and all_allow_tags.get(k)
                }
        except Exception as e:
            logging.error(f'指定的配置文件不存在或解析错误，将使用默认的配置。')
            logging.debug(e)
            _allow_tags = {'Genre': 'genres', 'Style': 'styles', 'Mood': 'moods'}
        return _allow_tags

    def load_form_file(yaml_file_path):
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

                class _cfg:
                    configfile = yaml_file_path
                    baseurl = data['auth']['baseurl']
                    token = data['auth']['token']
                    daysago = data['daysAgo']
                    sorttitle = data['sortTitle']
                    transtags = data['transTags']
                    tagsfile = data['tagsFile']

                return _cfg
        except Exception as e:
            logging.debug(e)
            return False

    def load_from_args():
        parser = argparse.ArgumentParser(description="一个接受基本 URL 作为参数的脚本。")
        parser.add_argument('--configfile', default="config.yaml", type=str, required=False, help="配置文件路径")
        parser.add_argument('--baseurl', default="", type=str, required=False,
                            help="Plex 地址，例如 http://127.0.0.1:32400")
        parser.add_argument('--token', default="", type=str, required=False, help="Plex Token")
        parser.add_argument('--daysago', default=0, type=int, required=False, help="仅搜索多少天前的媒体，0为不限制")
        parser.add_argument('--sorttitle', default=True, type=bool, required=False, help="开启标题排序")
        parser.add_argument('--transtags', default=True, type=bool, required=False, help="开启标签翻译")
        parser.add_argument('--tagsfile', default="tags.yaml", type=str, required=False, help="配置文件路径")
        args = parser.parse_args()

        class _cfg:
            configfile = args.configfile
            baseurl = args.baseurl
            token = args.token
            daysago = args.daysago
            sorttitle = args.sorttitle
            transtags = args.transtags
            tagsfile = args.tagsfile

        return _cfg

    args_cfg = load_from_args()
    file_cfg = load_form_file(args_cfg.configfile)
    _allow_libs_ = load_allow_libs(args_cfg.configfile)
    _allow_tags_ = load_allow_tags(args_cfg.configfile)

    if file_cfg:
        return file_cfg, _allow_libs_, _allow_tags_
    else:
        if not args_cfg.baseurl or not args_cfg.token:
            raise "未提供参数或配置文件。"
        return args_cfg, _allow_libs_, _allow_tags_


def has_chinese(string):
    """判断是否有中文"""
    return any('\u4e00' <= char <= '\u9fff' for char in string)


def convert_sort_to_pinyin(text):
    """将字符串转换为拼音首字母形式。"""
    pinyin_list = pypinyin.pinyin(text, style=pypinyin.FIRST_LETTER)
    pinyin_str = ''.join([item[0].upper() for item in pinyin_list])
    return pinyin_str.translate(str.maketrans("：（），", ":(),"))


def convert_tags_to_zhcn(tags: list[str], transdict: dict):
    return list(set(transdict.get(tag, tag) for tag in tags))


def list_media(pms_client, allow_libs, days):
    filters = {"addedAt>>": F"{days}d"} if days != 0 else None

    op_medias = []

    for library in pms_client.library.sections():
        allowed_libtypes = allow_libs.get(library.type, [])
        for libtype in allowed_libtypes:
            _list = library.search(libtype=libtype, filters=filters)
            op_medias.extend(_list)

    return op_medias


def search_media(pms_client, title):
    op_medias = pms_client.library.search(title=title)
    return op_medias


def op_sort(media):
    if has_chinese(media.titleSort):
        new_sort_title = convert_sort_to_pinyin(media.title)
        # media.editSortTitle(convert_sort_to_pinyin(media.title))
        media.editField('titleSort', convert_sort_to_pinyin(media.title), locked=True)
        logging.info(f"Set <{media.title}> SortTitle to [{new_sort_title}]")


def op_tag(media: plexapi.media, transdict: dict, trans_tagset: set, allow_libs, allow_tags, baseurl, token):
    _allow_types = [item for item in chain.from_iterable(allow_libs.values()) if item != 'collection']
    if media.type in _allow_types:

        metadata = requests.get(
            url=f'{baseurl}{media.key}', headers={'X-Plex-Token': token, 'Accept': 'application/json'}
        ).json().get("MediaContainer", {}).get("Metadata", [{}])[0]

        for tag_name, tag_name_s in allow_tags.items():
            tags = [tag.get('tag') for tag in metadata.get(tag_name, [])]
            if tags and any(tag in trans_tagset for tag in tags):
                new_tags = convert_tags_to_zhcn(tags, transdict)
                media.editTags(tag_name_s, tags, False, True).reload(**plexapi_reload_options)
                media.editTags(tag_name_s, new_tags, True, False).reload(**plexapi_reload_options)
                logging.info(F"Translate <{media.title}> {tag_name} {tags} to {new_tags}")


def main(
        baseurl: str, token: str, days: int,
        sortTitle: bool, transTags: bool,
        tag_source: str,
        allow_libs: dict, allow_tags: dict,
):
    client = PlexServer(baseurl, token)
    t1 = int(time.time() * 1000)

    op_medias = list_media(client, allow_libs, days)
    t2 = int(time.time() * 1000)
    logging.info(f'msg="过去 {days} 天内新增了 {len(op_medias)} 个媒体。" duration={(t2 - t1)}ms')

    if sortTitle:
        for op_media in op_medias:
            op_sort(op_media)
        t3 = int(time.time() * 1000)
        logging.info(f'msg="已设置中文排序标题。" duration={(t3 - t2)}ms')
    else:
        t3 = int(time.time() * 1000)

    if transTags:
        transdict = loadtags(tag_source)
        transtagset = set(transdict.keys())
        for op_media in op_medias:
            op_tag(op_media, transdict, transtagset, allow_libs, allow_tags, baseurl, token)
        t4 = int(time.time() * 1000)
        logging.info(f'msg="已设置中文标签。" duration={(t4 - t3)}ms')
    else:
        t4 = int(time.time() * 1000)

    logging.info(f'msg="全部任务已完成。" duration={(t4 - t1)}ms')


def removeTagLock(baseurl, token, days, allow_libs, allow_tags):
    client = PlexServer(baseurl, token)
    op_medias = list_media(client, allow_libs, days)
    for op_media in op_medias:
        _allow_types = [item for item in chain.from_iterable(allow_libs.values()) if item != 'collection']
        if op_media.type not in _allow_types:
            continue
        for tag_name, tag_name_s in allow_tags.items():
            op_media.editTags(tag_name_s, [], False, True).reload()
            logging.info(F"Unlock <{op_media.title}> {tag_name}")
    logging.info('Unlock All Tag')


if __name__ == '__main__':
    Config, AllowLibs, AllowTags = loadconfig()
    main(
        Config.baseurl, Config.token, Config.daysago, Config.sorttitle, Config.transtags, Config.tagsfile,
        AllowLibs, AllowTags
    )
