import os
import re
import json


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
    '时间': 'time',
    '地址': 'address',
}

address_data = {'YueHan': '0xFe38e3418AC699602178a0F7b281cE6DD5C5bb17',
                '@Niels': '0x19582b8EcAcebB0DC2b91B3Df0C0CCd5f779D0A0',
                'Hugo': '0x30f5354490fA2650a34e084452C71cC2EfFCc5A3',
                'xiashuang': '0x312b33BEec823869C068aD211beD894BE42FF158',
                '菠菜菠菜': '0x2d058BD1039562a6B91AEC84646d154C6013b7A7',
                'shuang': '0x12189A3B33CDa988ef10375ce835AB582d3248c3',
                'Vincent': '0xA6822638554A87E7FE6E64Dd5e52ae3cD4018014',
                'Aviv': '0x23FED883D76fC168754e4E300242d9D8c2Bb599F',
                'memeswap': '0xFdB66e0294Eb698b500c5FE4eB81dF5B3fB39c3b',
                '@JZ': '0x5737C4BB90F38548beE5B749225F329AD3Ff2253',
                'SCaesar': '0x8859DF12f4994b5E5E1DC7Ed9dF7e4cA47652662',
                'wenchuan': '0x2653645F230471555abAB040E0A1bc535F646aad',
                'shisi.eth': '0xD59d0eB6CB13664d9A68df6F46BA75430d400f55',
                '@linus': '0x5179C0A4C9207EeddB45412959aFe4B5400275af',
                'Nicole': '0x3DEF0898d1Ff2eF41eeC5F596391175E34C65A5a',
                '@猫老大': '0x6da3BCF0F43051eF03266f17bcf8e9Ac38F94BF7',
                'Feynman': '0x0B8D92C26F0fE2a9C39EdE47193a4a75f8C19E03',
                'Abby': '0x6CE117d8C4f940B9E212c291AF12b82F383a949F',
                'wes': '0x4a2e38f642357691C392E968d7F6171D911De73C',
                'Liz': '0xc3325c4A38ce389b785Fd431b11fd86e5512A6a1',
                'huaxia': '0x549Afb2F9Cdb90fdef7861b65c2Bcf80AaBbF765',
                '大葱 Fred': '0xD7243a8d5B0c02086624Bc0C525Aa192B4864dE1',
                'Tommy': '0x74eb5B7E5300C1962E2710D0D3Ee070215E56Ffb',
                'cpr': '0x1D7B70369B3F82B4719B526EF66f9e174c384e5e',
                'Herson': '0x93725B56949e8f34feAF8E1A303ABCc69B329950',
                'will': '0x23D75D919106665C99d2ffa93b3AA7545B96Fe21',
                'Frank': '0x77D8b4357EbCC9eb09826Cd0bbA2de92231bc00A',
                'zeagle': '0x778881534C9F85E4580A1F7A7926cb35a71F4e18',
                'createpjf': '0x31709B5E376Cfd5A174E10c49A4D38cF6E1bCf53',
                'TonyTX': '0x12Ad2F0314FBB77b3050776a81CC15a9F452512d',
                'Chasey': '0xc87301293712db364DcE491E822175F188054bf6',
                'Pitofui': '0xf30a5A4748009AfDc52F53b713173B19dfE275D2'}

addresses = address_data.keys()


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
                        one_post_str_list.append(
                            f'【地址】{address_data[i.split("】")[-1].replace("：",":").replace(":", "").strip()]}')
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


for address in get_all_presenters():
    if address not in list(addresses):
        print(address)

print('----')
for address in list(addresses):
    if address not in get_all_presenters():
        print(address)
