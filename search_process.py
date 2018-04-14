# encoding=utf-8

"""
使用 algoliasearch 客户端

pip install algoliasearch
pip install jieba
"""
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import os

from algoliasearch import algoliasearch
import jieba
import json
import getopt
import argparse

parser = argparse.ArgumentParser(description="site search data process.")
parser.add_argument('--searchKey', '-k', required=False, help='algolia manage key') 

args = parser.parse_args()

def sign_version(data):
	"""
	版本签名
	"""
	return hash(data['uri'] + '__' + data['title'] + '__' + data['content'])	

def push_data(items):
	"""
	提交数据变更
	"""
	client = algoliasearch.Client("NIACONWTKJ", args.searchKey)
	index = client.init_index('blog.threeq.me')

	res = index.add_objects(items)

	print("push count: %d. items:\n%s" % (len(res), json.dumps(res, ensure_ascii=False, indent=2)))
	
def delete_data(items):
	"""
	删除数据
	"""
	client = algoliasearch.Client("NIACONWTKJ", args.searchKey)
	index = client.init_index('blog.threeq.me')

	res = index.delete_objects(items)

	print("delete count: %d. items:\n%s" % (len(res), json.dumps(res, ensure_ascii=False, indent=2)))

def algolia_push():
	# 得到已经 push 的数据
	if os.path.isfile('public/index.push_version.json'):
		with open('public/index.push_version.json', 'r') as f:
			push_version_data = json.load(f)
			print("read version push data")
	else:
		push_version_data = dict()

	# 计算需要修改的数据
	new_items = dict()
	add_items = []
	del_items = []
	for index in range(len(data_dict)):
		data = data_dict[index]
		data['objectID'] = data['uri']
		new_items[(data['objectID'])] = True

		curr_version = sign_version(data)

		if push_version_data.has_key(data['objectID']):
			prev_version = push_version_data[data['objectID']]
		else:
			prev_version = None

		if curr_version != prev_version:
			add_items.append(data)

		push_version_data[data['objectID']] = curr_version

	for old_item in push_version_data.keys():
		if not new_items.has_key(old_item):
			del_items.append(old_item)
			del push_version_data[old_item]

	# 删除数据
	print("Delete lagolia items count： %d." % len(del_items))
	if len(del_items) > 0:
		delete_data(del_items)

	# 处理需要 push 的对象
	if len(add_items) > 0:
		push_data(add_items)
	else:
		print("Don't content Add or Modify. skipped lagolia push.")

	# 记录最新提交数据
	with open('public/index.push_version.json', 'w') as f:
		json.dump(push_version_data,f, ensure_ascii=False)
		print("write recored push data")

"""
algoliasearch 搜索处理
"""
with open('public/index.json', 'r') as f:
	data_dict = json.load(f)
	print("load public/index.json complete.")

if len(args.searchKey)>0:
	algolia_push()
else:
	print("skipped algolia push.")
"""
lunr 搜索处理
"""
for index in range(len(data_dict)):
	data = data_dict[index]
	data['title_s'] = " ".join(jieba.cut_for_search(data['title']))
	data['content_s'] = " ".join(jieba.cut_for_search(data['content']))

print("word segmentation complete.")

with open('public/index.json', 'w') as f:
	json.dump(data_dict,f, ensure_ascii=False)

print("search process complete.")
