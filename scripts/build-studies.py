"""Regenerate all static book studies from the atlas data and original study notes."""
from pathlib import Path
import re,json,html
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'index.html').read_text()
books=json.loads(re.search(r'const booksData = (\[.*?\]);',source,re.S).group(1))
notes=[x.split('|') for x in (ROOT/'data/study-notes.tsv').read_text().splitlines() if x]
assert len(books)==len(notes)==66
assert all(len(x)==6 for x in notes)
assert [x['name'] for x in books]==[x[0] for x in notes]
out=ROOT/'books';out.mkdir(exist_ok=True)
def esc(x):return html.escape(str(x),quote=True)
def filename(i,b):
 slug=re.sub(r'\s+\d+$','',b['passage']).lower().replace(' ','-')
 return f'{i+1:02}-{slug}.html'
def par(x):return '<p>'+esc(x)+'</p>'
def sect(id,title,body):return f'<section id="{id}"><h2>{title}</h2>{body}</section>'
labels=[('background','01 历史与真实处境'),('structure','02 内容结构与推进'),('purpose','03 写作目的与核心'),('passage','04 重点段落释读'),('covenant','05 圣约、基督与正典'),('application','06 难点与具体应用'),('discussion','07 讨论题与答案'),('memory','08 记忆与读经路线'),('sources','09 经文与查证')]
toc=''.join(f'<a href="#{id}">{esc(title)}</a>' for id,title in labels)
for i,(b,n) in enumerate(zip(books,notes)):
 page=filename(i,b);b['studyPath']='books/'+page
 previous=f'<a href="{filename(i-1,books[i-1])}">← {esc(books[i-1]["name"])}</a>' if i else '<a href="index.html">← 66卷目录</a>'
 following=f'<a href="{filename(i+1,books[i+1])}">{esc(books[i+1]["name"])} →</a>' if i<65 else '<a href="index.html">读完66卷 · 返回目录 →</a>'
 steps=''.join('<li>'+esc(x)+'</li>' for x in b['outline'].split('；'))
 body=sect('background','01 · 先进入真实处境',f'<p class="era">◷ {esc(b["era"])}</p>'+par(b['context']))
 body+=sect('structure','02 · 全书怎样推进？',f'<ol class="chapter-map">{steps}</ol>')
 body+=sect('purpose','03 · 写作目的与核心张力',par(b['argument']))
 body+=sect('passage','04 · 重点段落：'+esc(n[1]),par(n[2])+par(n[3]))
 body+=sect('covenant','05 · 圣约、基督与整本圣经',par(b['covenant']))
 body+=sect('application','06 · 从释读进入应用',f'<div class="caution"><h3>先辨清难点与误读</h3>{par(b["caution"])}</div><h3>具体回应</h3>'+par(b['application']))
 body+=sect('discussion','07 · 讨论题与答案',f'<h3>{esc(n[4])}</h3><div class="answer"><b>答案分析</b>{par(n[5])}</div>')
 body+=sect('memory','08 · 记忆与读经路线',f'<div class="memory">{par(b["recall"])}</div><p>本卷关键经文：{esc(b["refs"])}</p>')
 from urllib.parse import quote
 link='https://www.esv.org/'+quote(b['passage'])+'/'
 body+=sect('sources','09 · 经文与查证',f'<p><a href="{link}" target="_blank" rel="noopener noreferrer">阅读原章 · {esc(b["passage"])}</a>（ESV英文；中文请按章节对照和合本）。此页为教学释读，不是圣经或信条原文。</p><p><a href="../index.html#confessional-reading">三项联合信条与大公认信的解经边界</a> · <a href="../index.html#sources">查证资料</a></p><p>年代栏区分故事处境与写作处境；不确定处保留约数与讨论。解释应受上下文、文体与整本正典约束，不能以个人寓意代替经文论证。</p>')
 doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(b['name'])}逐卷释读：历史背景、章节结构、重点经文、圣约与基督、应用及讨论答案。"><title>{esc(b['name'])}｜逐卷精读 {i+1:02}/66｜整本圣经</title><link rel="stylesheet" href="study.css"><script src="study.js" defer></script></head><body><div class="progress" aria-hidden="true"></div><header class="toolbar"><a href="../index.html#books">← 总览</a><a href="index.html">66卷目录</a><button type="button" id="toggleToc" aria-controls="toc" aria-expanded="true">☰ 本卷目录</button></header><div class="layout"><aside id="toc"><p class="aside-title">本卷阅读目录</p><nav>{toc}</nav><div class="related"><a href="../index.html#timeline">↗ 救赎历史时间线</a><a href="../index.html#maps">↗ 地图与文化区域</a><a href="../index.html#all-kings">↗ 诸王与先知</a></div></aside><main><div class="hero"><p class="eyebrow">BOOK BY BOOK · {i+1:02} / 66 · v2.4 · 2026-10-03</p><h1>{esc(b['name'])}</h1><p class="subtitle">{esc(b['tagline'])}</p><p>先看整卷要解决什么，再进入关键段落；从历史与文体出发，在整本圣经中追踪神的应许与基督的成全。</p><div class="reading-nav">{previous}{following}</div></div>{body}<footer><div class="reading-nav">{previous}{following}</div><p>欧陆改革宗 · 救赎历史 · 圣约神学 · 圣经神学</p><a href="#">返回本卷开头 ↑</a></footer></main></div></body></html>'''
 (out/page).write_text(doc)
index_cards=''.join(f'<a class="index-card" href="{filename(i,b)}" data-book="{esc(b["name"]+" "+b["tagline"]+" "+b["era"])}"><span>{i+1:02} / 66</span><h2>{esc(b["name"])}</h2><p>{esc(b["tagline"])}</p><small>{esc(b["era"])}</small></a>' for i,b in enumerate(books))
(out/'index.html').write_text(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>66卷逐卷解读｜整本圣经</title><link rel="stylesheet" href="study.css"><script src="study.js" defer></script></head><body><header class="toolbar"><a href="../index.html#books">← 返回总览</a><a href="../index.html#timeline">时间线</a><a href="../index.html#maps">地图</a></header><main class="directory"><div class="hero"><p class="eyebrow">66 BOOKS · v2.4 · 2026-10-03</p><h1>一卷一卷，读懂整本圣经。</h1><p>66卷各有独立精读页：真实处境、内容结构、核心论证、重点段落、圣约与基督、误读与应用、讨论答案及记忆路线。按顺序阅读，也可从正在学习的书卷进入。</p><label for="directorySearch">查找书卷、主题或时代</label><input id="directorySearch" type="search" placeholder="创世记 / 大卫 / 被掳 / 囚禁…"><p id="directoryCount" role="status" aria-live="polite">66 / 66 卷</p></div><nav class="index-grid" aria-label="66卷独立精读页面">{index_cards}</nav><footer><p>旧约39卷 · 新约27卷 · 内容默认全部展开</p></footer></main></body></html>''')
# Update main-page links idempotently; keep the original anchor URLs available.
source=re.sub(r'const booksData = \[.*?\];',lambda m:'const booksData = '+json.dumps(books,ensure_ascii=False,indent=2)+';',source,count=1,flags=re.S)
source=source.replace('研读版 v2.3','研读版 v2.4')
if '进入逐卷精读专页' not in source:
 source=source.replace('<div class="book-era">◷ ${bookEscape(b.era)}</div>', '<div class="book-era">◷ ${bookEscape(b.era)}</div><p><a class="btn" href="${bookEscape(b.studyPath)}">进入逐卷精读专页 ↗</a></p>')
if '逐卷解读目录 →' not in source:
 source=source.replace('<nav class="book-index"', '<p><a class="btn" href="books/index.html">逐卷解读目录 →</a> · 66卷各有独立阅读页、重点段落及讨论答案。</p>\n      <nav class="book-index"',1)
(ROOT/'index.html').write_text(source)
print('Generated 66 individual studies, directory and main-page links.')
