import json,sys
from urllib.parse import urlparse
out=json.load(open('serps.json')) if __import__('os').path.exists('serps.json') else {}
for f in sys.argv[1:]:
    raw=json.load(open(f))
    d=json.loads(raw[0]['text']) if isinstance(raw,list) else raw
    r=d['results']; kw=r['request_metadata']['keyword']
    org=[]
    for it in r['items']:
        if it['type']!='organic' or any(x in (it.get('serp_features') or []) for x in ['mads','bads']): continue
        url=it.get('url') or it['links'][0]['url']
        org.append([len(org)+1, urlparse(url).netloc.replace('www.',''), url, it.get('title','')[:90]])
    sp=[o for o in org if 'thespearpoint' in o[1]]
    out[kw]={'features':r['summary']['SERP_features'],'top10':org[:10],'spearpoint':sp[:1],'location':'Denver, CO' if r['request_metadata'].get('location_id') else 'United States'}
    print(kw,'SP:',sp[:1]); [print('  ',o[0],o[1]) for o in org[:10]]
# re-number existing
for k,v in out.items():
    for i,o in enumerate(v['top10']): o[0]=i+1
json.dump(out,open('serps.json','w'),indent=0)
