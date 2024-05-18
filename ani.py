# 获取ani网盘所有直链

#增量更新，前3个文件夹都是实时更新的，后面的文件夹目录结构不会变
# import cloudscraper
import requests
import urllib.parse
import os
# # 创建一个Cloudscraper实例，设置延迟和模拟的浏览器环境
# scraper = cloudscraper.create_scraper(delay=5, browser={
#     'browser': 'chrome',
#     'platform': 'windows',
#     'mobile': False,
# })

base_url = "https://aniopen.an-i.workers.dev/"

#获取一级目录
def get_folder(base_url):
    try:
        res = requests.post(base_url, json={"password":"null"}).json()
        folder_names = [i["name"] for i in res['files'] if 'folder' in i['mimeType']]
        return folder_names
    # video_name = [i["name"] for i in res['files'] if 'video' in i['mimeType']]
    # print(folder_names)
    except Exception as e:
        print(e)

def strm(anime):
    try:
        res = requests.post(base_url + anime, json={"password":"null"}).json()
        video_names = [i["name"] for i in res['files'] if 'video' in i['mimeType']]
        strm_urls = [base_url + urllib.parse.quote(anime + video_name) + '?d=true' for video_name in video_names]
        # 文件路径
        file_paths = [anime + video_name + ".strm" for video_name in  video_names]
        # 确保文件夹存在
        for file_path, strm_url in zip(file_paths,strm_urls):
            # 创建并写入
            if os.path.exists(file_path):
                continue
            os.makedirs(os.path.dirname(file_path), exist_ok=True) 
            with open(file_path, 'w') as file:
                file.write(strm_url)
                print(f'{file_path}写入成功！')
        # video_name = [i["name"] for i in res['files'] if 'video' in i['mimeType']]
        # print(folder_names)
    except Exception as e: 
        print(e)
        

# 获取二级番剧目录名称
# 前3个文件夹都是实时更新的，后面的文件夹目录结构不会变,这里只获取完结番剧
date_folders = get_folder(base_url)
date_urls = [base_url + i + "/" for i in date_folders]
ani_folders = [get_folder(i) for i in date_urls]
anime_list = [f'{date}/{anime}/' for date, sublist in zip(date_folders, ani_folders) for anime in sublist]
for anime in anime_list:
    strm(anime)
# print(anime_list)
# print(list(all_folders))
