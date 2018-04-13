# encoding=utf-8

"""
使用 jieba 分词库

pip install jieba
"""
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

import jieba
import json

with open('public/index.json', 'r') as f:
	data_dict = json.load(f)
	print("load public/index.json complete.")

for index in range(len(data_dict)):
	data = data_dict[index]
	data['title_s'] = " ".join(jieba.cut_for_search(data['title']))
	data['content_s'] = " ".join(jieba.cut_for_search(data['content']))

print("word segmentation complete.")

with open('public/index.json', 'w') as f:
	json.dump(data_dict,f, ensure_ascii=False)

print("write public/index.json complete.")
