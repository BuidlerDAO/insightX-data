import os
import re
import json
import pandas as pd

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))


def get_filenames(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


map_init = {
    '输出人': 'presenter',
    '主题': 'subject',
    '核心内容简介': 'core_content_summary',
    '个人思考': 'personal_thoughts',
    '相关链接': 'related_links',
    '时间': 'time'
}


def extract_data(lines):
    data = {}
    key = ""
    for line in lines:
        if "【" in line and "】" in line:
            key = line[line.index("【")+1:line.index("】")]
            key = map_init[key]
            data[key] = line.split('】')[-1].replace('：',
                                                    ':').replace(':', '').strip()
        else:
            data[key] += line
            data[key] += "\n" if line else ""
    for k, v in data.items():
        data[k] = v.strip()
    return data


use_str_list = ['输出人', '主题', '核心内容简介', '个人思考', '相关链接']
file_list = get_filenames(current_dir+'/data/origin_txt/')
not_match_list = []
data_map = {}
for filename in file_list:
    with open(f'{current_dir}/data/origin_txt/{filename}', 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        one_post_str_list = []
        for i in lines:
            if '【' in i and '】' in i:
                matches = re.findall(r'【(.*?)】', i)
                if matches[0] == '输出人':
                    if one_post_str_list != []:
                        one_post_str_list.append(
                            f'【时间】{filename.split(".")[0]}')
                        not_match_list.append(one_post_str_list)
                    one_post_str_list = []
                    one_post_str_list.append(i)
                else:
                    one_post_str_list.append(i)
            elif len(i) < 20 and ('月' in i or '2022' in i):
                pass
            else:
                one_post_str_list.append(i)

    # print(lines)
# print(not_match_list[1])
# print(extract_data(not_match_list[1]))

last_data = []
for data in not_match_list:
    last_data.append(extract_data(data))


# 保存为 JSON 文件
with open('list.json', 'w', encoding='utf-8') as f:
    json.dump(last_data, f, ensure_ascii=False, indent=4)

# 帮我找出 last_data 中所有的 presenter


def get_all_presenters():
    all_presenters = []
    for d in last_data:
        all_presenters.append(d['presenter'])
    return list(set(all_presenters))


print(get_all_presenters())
