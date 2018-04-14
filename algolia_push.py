# encoding=utf-8

"""
使用 algoliasearch 客户端

pip install algoliasearch
"""
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

from algoliasearch import algoliasearch
import json

with open('public/index.json', 'r') as f:
	data_dict = json.load(f)
	print("load public/index.json complete.")

for index in range(len(data_dict)):
	data = data_dict[index]
	data['objectID'] = data['uri']

client = algoliasearch.Client("NIACONWTKJ", '2af7682a40012e3ce8cb151d6a87b524')
index = client.init_index('blog.threeq.me')

res = index.add_objects(data_dict)

print("push count: %d. items:\n%s" % (len(res), json.dumps(res, ensure_ascii=False, indent=2)))

with open('public/index.json_dump', 'w') as f:
	json.dump(data_dict,f, ensure_ascii=False)
	print("recored push data")

print("algolia push complete.")
