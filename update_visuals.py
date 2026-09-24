"""Render public GitHub facts; no private metrics, credentials, or skill ratings."""
from collections import Counter
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json, urllib.request

USER = 'DKAA04'
OUT = Path(__file__).resolve().parent

def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'DKAA04-portfolio','Accept':'application/vnd.github+json'})
    return urllib.request.urlopen(request,timeout=30).read().decode()

class Contributions(HTMLParser):
    def __init__(self):
        super().__init__(); self.days={}
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='td' and 'data-date' in attrs and 'data-level' in attrs:
            self.days[attrs['data-date']]=int(attrs['data-level'])

parser=Contributions();parser.feed(fetch(f'https://github.com/users/{USER}/contributions'))
if len(parser.days)<300:
    raise RuntimeError('GitHub contribution markup changed; keep previous verified graphic.')
today=date.today().isoformat()
days=sorted((d,l) for d,l in parser.days.items() if d<=today)
colors=['#14232b','#204b42','#367c65','#56ad88','#7ee2c0']
rects=[]
for i,(day,level) in enumerate(days):
    x=26+(i//7)*13;y=57+(i%7)*13
    rects.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{colors[level]}"><title>{day}: GitHub activity level {level}/4</title></rect>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 744 191" role="img" aria-label="Public GitHub contribution levels, refreshed {today}">
<style>@keyframes scan{{from{{stroke-dashoffset:1480}}to{{stroke-dashoffset:0}}}}.trace{{animation:scan 18s linear infinite}}@media(prefers-reduced-motion:reduce){{.trace{{animation:none}}}}</style>
<rect width="744" height="191" rx="12" fill="#0b121b"/>
<text x="26" y="29" fill="#f2f6fb" font-family="monospace" font-size="14">~/ public activity</text>
<text x="718" y="29" text-anchor="end" fill="#92a7b8" font-family="monospace" font-size="11">refreshed {today}</text>
{''.join(rects)}
<path class="trace" d="M26 158 H718" fill="none" stroke="#7ee2c0" stroke-width="2" stroke-dasharray="60 1420" opacity=".65"/>
<text x="26" y="180" fill="#92a7b8" font-family="monospace" font-size="10">GitHub contribution levels · decorative scan line · no private activity inferred</text></svg>'''
(OUT/'activity.svg').write_text(svg)

repos=json.loads(fetch(f'https://api.github.com/users/{USER}/repos?per_page=100'))
langs=Counter(); counted=[]
for repo in repos:
    if repo['fork'] or repo['name']==USER or repo['archived']: continue
    langs.update(json.loads(fetch(repo['languages_url'])));counted.append(repo['name'])
total=sum(langs.values());top=langs.most_common(5)
palette=['#7ee2c0','#8ba8ff','#e6bf75','#c59ff5','#83bcd3']
bars=[];x=26
for i,(lang,n) in enumerate(top):
    w=692*n/total
    bars.append(f'<rect x="{x:.1f}" y="56" width="{w:.1f}" height="10" fill="{palette[i]}"/>');x+=w
    bars.append(f'<text x="{26+i*142}" y="93" fill="{palette[i]}" font-family="monospace" font-size="11">{escape(lang)} {100*n/total:.1f}%</text>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 744 142" role="img" aria-label="Public repository language bytes, not skill proficiency">
<rect width="744" height="142" rx="12" fill="#0b121b"/>
<text x="26" y="29" fill="#f2f6fb" font-family="monospace" font-size="14">~/ code across {len(counted)} public project repositories</text>
{''.join(bars)}
<text x="26" y="126" fill="#92a7b8" font-family="monospace" font-size="10">GitHub language bytes · top five shown · {today} · not proficiency scores</text></svg>'''
(OUT/'languages.svg').write_text(svg)
print(f'Generated visuals from {len(days)} public contribution cells and {len(counted)} public repositories.')
