import re
import json

pattern = r'\W+'

# 读取json中的数据
info = []
words = []
with open("data/TOEFL_2.json", 'r') as f:
    for line in f.readlines():
        temp_info = eval(line)
        if temp_info["content"]["word"]["wordHead"]:
            words.append(temp_info["content"]["word"]["wordHead"])
            info.append(temp_info)
f.close()

# print(words[1])

word_in_text = []
with open("./test.txt") as f:
    for line in f.readlines():
        for word in re.split(pattern, line):
            word_in_text.append(word.lower())

all_info = []
for temp in info:
    if temp["content"]["word"]["wordHead"] in word_in_text:
        # anki背面
        word = "\'"+temp["content"]["word"]["wordHead"]+"\' " 
        anki_info = {"trans": [], "example": []}

        # 翻译
        if temp["content"]["word"]["content"]["trans"]:
            temp_trans_info = temp["content"]["word"]["content"]["trans"]
            for item in temp_trans_info:
                temp_str = f"{item['pos']}.{item['tranCn']}"  # "词性.中文翻译"
                anki_info["trans"].append(temp_str)

        # 例句
        if "sentence" in temp["content"]["word"]["content"].keys():
            temp_exm_info = temp["content"]["word"]["content"]["sentence"]
            for item in temp_exm_info["sentences"]:
                anki_info["example"].append([item["sContent"], item["sCn"]])

        trans_str = ""
        for item in anki_info["trans"]:
            trans_str += item + "  "

        exm_str = ""
        for _, item in enumerate(anki_info["example"]):
            str_sen = f"{_ + 1}. {item[0]}"
            str_tran = f"{item[1]}"
            exm_str += str_sen + " -- " + str_tran + f"\n"
        split = f"___________________________________________________________"
        all_info.append([split,"\n", word,"\n", trans_str,"\n", exm_str])
        # example_sen.append([anki_info["example"][0], anki_info["example"][1]])
with open('result.txt', 'w') as f:
    for info in all_info:
        for i in info:
            f.writelines(i)
        