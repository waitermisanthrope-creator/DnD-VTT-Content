"""Check aquatic payload delivery, runtime contracts and immutable older content."""
import argparse
import hashlib
import json
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RACES = ['kuo_toa', 'merrow', 'triton', 'sahuagin', 'locathah']
IDS = ['dnd.race.' + race for race in RACES]
THEME = 'dnd.collections.aquatic-races'
FULL = 'dnd.collections.races'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public', action='store_true', help='Verify actual public catalog and payload bytes')
    parser.add_argument('--baseline', default='57fcc7a2016c28b2f4cef76fa2e078a2ba8a86e5')
    args = parser.parse_args()
    raw = (ROOT / 'catalog/v3/index.json').read_bytes()
    entries = json.loads(raw)['packages']
    byid = {m['id']: m for m in entries}
    assert len(byid) == len(entries), 'Duplicate catalog IDs'
    baseline_raw = subprocess.check_output(['git', 'show', args.baseline + ':catalog/v3/index.json'], cwd=ROOT)
    before = {m['id']: m for m in json.loads(baseline_raw)['packages']}
    assert set(byid) - set(before) == set(IDS) - {'dnd.race.triton'} | {THEME}
    assert set(before) <= set(byid), 'Existing entry removed'
    assert all(byid[k] == v for k, v in before.items() if k not in ('dnd.race.triton', FULL)), 'Unrelated entry changed'
    changed = subprocess.check_output(['git', 'diff', args.baseline, '--name-only', '--diff-filter=MD', '--', 'packages/'], cwd=ROOT)
    assert not changed.strip(), 'An immutable historical payload changed'
    schema = json.loads((ROOT / 'schemas/catalog-entry-v1.schema.json').read_text())
    documents = {}
    for pid in IDS + [THEME, FULL]:
        m = byid[pid]
        jsonschema.validate(m, schema, format_checker=jsonschema.FormatChecker())
        assert datetime.fromisoformat(m['updatedAt']) >= datetime.fromisoformat(m['publishedAt'])
        if pid in before:
            assert m['publishedAt'] == before[pid]['publishedAt'], 'Original publication date lost'
            assert tuple(map(int, m['version'].split('.'))) > tuple(map(int, before[pid]['version'].split('.')))
            assert m['url'] != before[pid]['url'], 'New version must use a new URL'
        b = (ROOT / 'packages' / m['url'].rsplit('/', 1)[-1]).read_bytes()
        assert (len(b), hashlib.sha256(b).hexdigest()) == (m['bytes'], m['sha256']), pid
        d = json.loads(b)
        assert all(d[k] == m[k] for k in ('id', 'version', 'schemaVersion', 'type'))
        documents[pid] = d
        if pid in IDS:
            r, = d['races']
            assert r['id'] == pid.removeprefix('dnd.race.')
            assert r['choices'] == [] and r['name'].strip()
            assert 'Возраст и жизнь:' in r['desc'] and 'старые' in r['desc']
            seed = r['seed']
            assert set(seed) <= {'stats', 'speed', 'size', 'raceFeatureDescriptions', 'abilities', 'features', 'proficiencies', 'raceId', 'raceMechanics', 'raceName', 'resistances', 'immunities'}
            assert set(seed['stats']) == {'str', 'dex', 'con', 'int', 'wis', 'cha'}
            assert all(type(v) is int and 8 <= v <= 12 for v in seed['stats'].values())
            assert r['bonuses'] == {k: v - 10 for k, v in seed['stats'].items()}
            lore = seed['raceFeatureDescriptions']
            assert any('Возраст и жизнь:' in s for s in lore), 'Age missing from saved sheet seed'
            assert all(term in '\n'.join(lore) for term in ('дети', 'подростки', 'взрослые', 'пожилые', 'старые', 'Авторский' if r['id'] in ('kuo_toa', 'merrow', 'sahuagin') else 'авторский'))
            if r['id'] in ('kuo_toa', 'merrow', 'sahuagin'):
                assert 'не является официальной игровой расой' in r['desc']
            if r['id'] in ('sahuagin', 'locathah'):
                assert not seed['raceMechanics']['amphibious'] and any('4 часа' in s for s in lore)
            if r['id'] == 'merrow':
                assert seed['size'] == 'Большой' and not seed['raceMechanics']['amphibious']
        else:
            jsonschema.validate(d, json.loads((ROOT / 'schemas/mod-collection-v1.schema.json').read_text()))
            assert d['members'] == m['dependencies'] and len(d['members']) == m['packageCount']
            assert m['collectionRole'] == 'category', 'Collection would be hidden in default workshop UI'
    old_triton = json.loads((ROOT / 'packages/dnd.race.triton.json').read_text())['races'][0]
    new_triton = documents['dnd.race.triton']['races'][0]
    for key in old_triton:
        if key == 'desc':
            continue
        if key == 'seed':
            assert {k:v for k,v in old_triton[key].items() if k != 'raceFeatureDescriptions'} == {k:v for k,v in new_triton[key].items() if k != 'raceFeatureDescriptions'}
        else:
            assert old_triton[key] == new_triton[key], key
    assert documents[THEME]['members'] == IDS
    assert len(documents[FULL]['members']) == 47 and set(IDS) <= set(documents[FULL]['members'])
    for m in entries:
        assert set(m['dependencies']) <= set(byid), m['id']
    visiting, complete = set(), set()

    def visit(pid):
        assert pid not in visiting, 'Dependency cycle: ' + pid
        if pid in complete:
            return
        visiting.add(pid)
        for dep in byid[pid]['dependencies']:
            visit(dep)
        visiting.remove(pid)
        complete.add(pid)

    for pid in byid:
        visit(pid)
    if args.public:
        url = 'https://raw.githubusercontent.com/waitermisanthrope-creator/DnD-VTT-Content/main/catalog/v3/index.json'
        public = json.load(urllib.request.urlopen(url, timeout=45))
        actual = {m['id']: m for m in public['packages']}
        for pid in IDS + [THEME, FULL]:
            assert actual[pid] == byid[pid], 'Public entry differs: ' + pid
            m = actual[pid]
            b = urllib.request.urlopen(m['url'], timeout=45).read()
            assert (len(b), hashlib.sha256(b).hexdigest()) == (m['bytes'], m['sha256']), 'Public delivery: ' + pid
        print('AQUATIC_PUBLIC_PASS: live catalog + 7 actual downloads match exact sizes/SHA-256')
    print('AQUATIC_CONTENT_PASS: 5 races, 2 collections, 47 full-library members; old payloads and unrelated entries unchanged')


if __name__ == '__main__':
    main()
