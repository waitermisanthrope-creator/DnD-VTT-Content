"""Validate all race lore, preserved game data and optional live public delivery."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

import jsonschema

ROOT=Path(__file__).resolve().parents[1]
CATALOG='catalog/v3/index.json'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public',action='store_true')
    args=parser.parse_args()
    source=json.loads((ROOT/'sources/race-descriptions-1.0.0.json').read_text())
    def old(path):
        return subprocess.check_output(['git','show',source['baseline']+':'+path],cwd=ROOT)
    data=json.loads((ROOT/CATALOG).read_bytes())
    before={m['id']:m for m in json.loads(old(CATALOG))['packages']}
    byid={m['id']:m for m in data['packages']}
    assert len(byid)==len(data['packages'])==304 and set(byid)==set(before), 'Catalog IDs changed'
    changed=set(source['updatedPackages'])|{'dnd.collections.races'}
    assert len(changed)==43 and len(source['records'])==42
    assert {pid for pid in byid if byid[pid]!=before[pid]}==changed, 'Unrelated catalog changes'
    assert not subprocess.check_output(['git','diff',source['baseline'],'--name-only','--diff-filter=MD','--','packages/'],cwd=ROOT).strip(), 'Old immutable payload altered'
    schema=json.loads((ROOT/'schemas/catalog-entry-v1.schema.json').read_text())
    race_ids=set()
    for pid,m in byid.items():
        assert set(m['dependencies'])<=set(byid), 'Unresolved dependency'
        if m['type']!='race' and pid!='dnd.collections.races':continue
        jsonschema.validate(m,schema,format_checker=jsonschema.FormatChecker())
        path='packages/'+m['url'].rsplit('/',1)[-1]
        raw=(ROOT/path).read_bytes()
        assert (len(raw),hashlib.sha256(raw).hexdigest())==(m['bytes'],m['sha256']),pid
        d=json.loads(raw)
        assert all(d[k]==m[k] for k in ('id','type','version','schemaVersion'))
        if m['type']=='collection':
            jsonschema.validate(d,json.loads((ROOT/'schemas/mod-collection-v1.schema.json').read_text()))
            assert d['members']==m['dependencies'] and len(d['members'])==m['packageCount']==47
            assert m['version']=='1.0.2'
            prev=json.loads(old('packages/'+before[pid]['url'].rsplit('/',1)[-1]))
            assert d['members']==prev['members'], 'Collection composition changed'
            continue
        r,=d['races'];rid=r['id'];assert rid not in race_ids;race_ids.add(rid)
        assert len(r['desc'])>350 and 'Возраст и жизнь:' in r['desc'] and not r['desc'].startswith('Дополнение:'),pid
        assert any('Возраст и жизнь:' in s for s in r['seed']['raceFeatureDescriptions']),pid
        assert 'старые' in r['desc'] or rid=='warforged',pid
        if pid not in changed:
            assert m==before[pid] and raw==old(path),'Aquatic package changed'
            continue
        assert rid in source['records']
        expected=source['records'][rid]
        for s in expected['lore']+[expected['age']]:
            assert s in r['desc'] and s in r['seed']['raceFeatureDescriptions'],'Lore lost: '+rid
        previous=json.loads(old('packages/'+before[pid]['url'].rsplit('/',1)[-1]))
        prior=previous['races'][0]
        # Normalize only the intended prose/version fields; all remaining data must match exactly.
        normalized=json.loads(json.dumps(d))
        normalized['version']=previous['version']
        normalized['races'][0]['desc']=prior['desc']
        if 'raceFeatureDescriptions' in prior['seed']:
            normalized['races'][0]['seed']['raceFeatureDescriptions']=prior['seed']['raceFeatureDescriptions']
        else:
            normalized['races'][0]['seed'].pop('raceFeatureDescriptions',None)
        assert normalized==previous,'Game data changed: '+pid
        assert m['version']=='1.0.1' and m['publishedAt']==before[pid]['publishedAt'] and m['updatedAt']>=m['publishedAt']
        assert m['url']!=before[pid]['url']
    assert len(race_ids)==47
    assert set(byid['dnd.collections.races']['dependencies'])=={m['id'] for m in byid.values() if m['type']=='race'}
    if args.public:
        url='https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/'+CATALOG
        public=json.load(urllib.request.urlopen(url,timeout=45));live={m['id']:m for m in public['packages']}
        assert all(live[pid]==byid[pid] for pid in changed),'Live catalog mismatch'
        def download(pid):
            m=live[pid];raw=urllib.request.urlopen(m['url'],timeout=45).read()
            assert (len(raw),hashlib.sha256(raw).hexdigest())==(m['bytes'],m['sha256']),pid
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(download,sorted(changed)))
        print('RACE_DESCRIPTIONS_PUBLIC_PASS: live catalog and43 real downloads match sizes/SHA-256')
    print('RACE_DESCRIPTIONS_CONTENT_PASS: all47 races have lore and age; 42 prose-only updates; game data and old payloads preserved')


if __name__=='__main__':main()
