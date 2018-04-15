---
title: Hugo 网站增加搜索功能：Lunrjs 和 Algolia
date: 2018-04-15
lastmod: 2018-04-15
draft: false
keywords: ["Hugo","Hugo 搜索","Hugo Search", "lunr", "lungs", "algolia"]
description: "本文是总结我自己在使用 Hugo 进行建站的时候给网站增加内容检索功能的结果。做这个功能的一个原因也是由于自己使用的 Even 主题没有带检索功能，所有只有自己上手撸一把。使用的检索方案包括 Lunrjs 和 Algolia，本文的处理方式可以同时支持 2 中方式，可以根据自己的情况自由选择或切换。"
categories:
 - 笔记
tags:
 - Hugo
toc: true
---

本文是总结我自己在使用 Hugo 进行建站的时候给网站增加内容检索功能的结果。做这个功能的一个原因也是由于自己使用的 Even 主题没有带检索功能，所有只有自己上手撸一把。使用的检索方案包括 Lunrjs 和 Algolia，本文的处理方式可以同时支持 2 中方式，可以根据自己的情况自由选择或切换。

<!--more-->

很多的 Hugo 主题是没有自带搜索功能的，但是们为了方便用户浏览和查找内容是需要在网站上提供搜索功能。大家可以查看 [Hugo 官方推荐的搜索方案](https://gohugo.io/tools/search/)，我在使用的时候选择的是 Lunr 和 Algolial，以下是我的方案记录。

# 生产网站 JSON 数据

由于 Lunr 和 Algolia 都同时对 JSON 数据格式的支持，所以这里我们选用网站的 JSON 数据格式。

首先需要在 `config.toml` 里面增加配置

```
[outputs]
home = [ "HTML", "RSS", "JSON"]
```

其次需要在你的主题目录里面新建 `themes/<your themme name>/layouts/index.json` 文件，输入一下内容

```
[{{ range $index, $page := .Site.Pages }}
{{- if ne $page.Type "json" -}}
{{- if and $index (gt $index 0) -}},{{- end }}
{
	"uri": "{{ $page.Permalink }}",
	"title": "{{ htmlEscape $page.Title}}",
	"tags": [{{ range $tindex, $tag := $page.Params.tags }}{{ if $tindex }}, {{ end }}"{{ $tag| htmlEscape }}"{{ end }}],
	"description": "{{ htmlEscape .Description}}",
	"content": {{$page.Plain | jsonify}}
}
{{- end -}}
{{- end -}}]
```



这个时候我们使用 `hugo` 生成网站的时候会多生成一个 `public/index.json` 的数据文件，我们的所有操作都围绕这个数据文件进行。

# 搜索框添加

> 这里的搜索框 HTML、CSS 代码添加会根据你自己的主题会有所不同

首先为了支持不同的搜索解决方案，我们需要在 `config.toml` 里面增加如下配置，这样我们在使用的时候就可以自由的开关和切换搜索功能

```
[params.Search]
    enable = true    # true or false
    type = 'algolia'  # lunr or algolia
    index = 'algolia_index'  # algolia enabled
    appID = 'algolia_application_id' # algolia enabled
    searchKey = 'algolia_search_only_key' # algolia enabled
```

然后将一下代码加入到你主题的相应位置

```
{{- if .Site.Params.Search.Enable }}
<link href="{{"lib/search/auto-complete.css" | relURL}}" rel="stylesheet">

<div class="search-wrapper">
  <div class="searchbox">
    <div id='inputfield'>
      <i class='fa fa-search icon-search'></i>
      <input id="search-by" autocomplete='off' autocorrect='off' name='address' placeholder="{{T "Search-placeholder"}}"
       spellcheck='false' type='text'>
    </div>
  </div>
</div>

{{- if (eq .Site.Params.Search.type "lunr") }}
    <script type="text/javascript">
      {{ if .Site.IsMultiLingual }}
          var baseurl = "{{.Site.BaseURL}}{{.Site.LanguagePrefix}}";
      {{ else }}
          var baseurl = "{{.Site.BaseURL}}";
      {{ end }}
    </script>
    <script type="text/javascript" src="{{"lib/search/lunr/lunr.js" | relURL}}"></script>
    <script type="text/javascript" src="{{"lib/search/lunr/auto-complete.js" | relURL}}"></script>
    <script type="text/javascript" src="{{"lib/search/lunr/search.js" | relURL}}"></script>
  {{- else }}
    <script type="text/javascript">
      var lagoliaIndex = "{{.Site.Params.Search.index}}"
      var lagoliaAppID = "{{.Site.Params.Search.appID}}"
      var lagoliaSearchKey = "{{.Site.Params.Search.searchKey}}"
    </script>
    <script src="//cdn.jsdelivr.net/autocomplete.js/0/autocomplete.jquery.min.js"></script>
    <script src="//cdn.jsdelivr.net/algoliasearch/3/algoliasearch.min.js"></script>
    <script type="text/javascript" src="{{"lib/search/algolia/search-bar.js" | relURL}}"></script>
  {{- end}}
{{- end}}
```

这里用到的一些 JS文件 和 CSS 文件请到此地址下载：https://github.com/threeq/blog.threeq.me/tree/master/themes/even/static/lib/search，放到 `static/lib/search` 目录下。

到这里我们为网站所加入的 Lunr 搜索功能就完成了，由于 Lunr 对于中文检索支持很差，我们需要手动处理一下我们的 `public/index.josn`，进行中文分词。同时这里需要使 Algolia 支持的话，也需要将我们的 JSON 数据提交到 Algolia 数据库中。

# 搜索数据预处理

这里为了同时能将 `public/index.josn` 数据进行中文分词和提交到 Algolia 中，我这里自己写了一个 Python 脚本，方便处理和后续集成自动发布。在网站根目录新建文件 `search_process.py`，输入一下内容（你也可以到 [这里下载](https://github.com/threeq/blog.threeq.me/blob/master/search_process.py)）：

```python
# encoding=utf-8

"""
Hugo 网站使用 Lunr 和 Algolia 搜索方案数据处理
数据处理需要用到 algoliasearch 和 jieba 库，先安装

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
import argparse

parser = argparse.ArgumentParser(description="site search data process.")
parser.add_argument('--managehKey', '-k', required=False, help='algolia manage key') 

args = parser.parse_args()

def sign_version(data):
	"""
	计算版本签名
	"""
	return hash(data['uri'] + '__' + data['title'] + '__' + data['content'])	

def push_data(items):
	"""
	提交数据变更
	"""
	client = algoliasearch.Client("NIACONWTKJ", args.managehKey)
	index = client.init_index('blog.threeq.me')

	res = index.add_objects(items)

	print("push count: %d. items:\n%s" % (len(res), json.dumps(res, ensure_ascii=False, indent=2)))
	
def delete_data(items):
	"""
	删除数据
	"""
	client = algoliasearch.Client("NIACONWTKJ", args.managehKey)
	index = client.init_index('blog.threeq.me')

	res = index.delete_objects(items)

	print("delete count: %d. items:\n%s" % (len(res), json.dumps(res, ensure_ascii=False, indent=2)))

def algolia_push():
	"""
	algolia 数据提交
	"""
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

	# 需要删除数据
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

######
# load public/index.json data
#####
with open('public/index.json', 'r') as f:
	data_dict = json.load(f)
	print("load public/index.json complete.")

######
# algolia search process
######
if len(args.managehKey)>0:
	algolia_push()
else:
	print("skipped algolia push.")

######    
# lunr search process
# use jieba lib
######
for index in range(len(data_dict)):
	data = data_dict[index]
	data['title_s'] = " ".join(jieba.cut_for_search(data['title']))
	data['content_s'] = " ".join(jieba.cut_for_search(data['content']))

print("word segmentation complete.")

with open('public/index.json', 'w') as f:
	json.dump(data_dict,f, ensure_ascii=False)


print("search process complete.")

```

 这是可以使用如下命令进行操作

```
$ python search_process.py -h # 查看帮助文档
$ python search_process.py -k '' # 只支持 Lunr 处理，中文分词
$ python search_process.py -k <algolia manage key> # 同时进行 Lunr 和 Algolia 处理
$ python search_process.py --managehKey <algolia manage key> # 同时进行 Lunr 和 Algolia 处理
```

最后我们还可以很方便和发布流程集成，比如下面的 `deploy.sh` 脚本

```
#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

fail() {
	echo "$1"
	exit 1
}

# Build the project.
hugo # if using a theme, replace with `hugo -t <YOURTHEME>`
echo "search key $2"
searchKey="$2"
python2 search_process.py -k "${searchKey}" || fail "site search data process fail. Error Code: [ $? ]"


# Go To Public folder
cd public
# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -ge 1  ]
    then msg="$1"
fi
    git commit -m "$msg"

 # Push source and build repos.
git push origin master

# Come Back up to the Project Root
cd ..

```

使用时如下：

```
$./deploy.sh
$./deploy.sh "this is message" <algolia manage key>
$./deploy.sh '' <algolia manage key>
```

参考：

* [hugo-lunr-zh](https://www.npmjs.com/package/hugo-lunr-zh)