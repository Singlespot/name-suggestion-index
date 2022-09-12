import json
import sys

custom_brands = json.load(open('custom_data/custom_brands.json'))
custom_wikidata = json.load(open('custom_data/custom_wikidata.json'))
nsi_wikidata = json.load(open('dist/wikidata.min.json'))

for path, brand in custom_brands.items():
    nsi_path, nsi_name = path.split('|')
    nsi_file = 'data/brands/' + nsi_path + '.json'
    try:
        nsi_brands = json.load(open(nsi_file))
    except:
        print('ERROR: Reading file ' + nsi_file)
        raise
    nsi_brands_index = {brand['displayName']: i for i, brand in enumerate(nsi_brands['items'])}
    spt_brand_wikidata = brand.get('tags', {}).get('brand:wikidata')
    if not spt_brand_wikidata:
        print('ERROR: No brand:wikidata found for ' + path, file=sys.stderr)
        continue
    if not nsi_wikidata['wikidata'].get(spt_brand_wikidata):
        if nsi_brands_index.get(nsi_name):
            print('WARNING: Removing duplicate brand ' + nsi_name + ' from ' + nsi_file)
            del nsi_brands['items'][nsi_brands_index[nsi_name]]

        print('INFO: Adding ' + nsi_name + ' to ' + nsi_file)
        nsi_brands['items'].append(
            {
                "displayName": nsi_name,
                "locationSet": {"include": ["fr"]},
                "tags": brand["tags"]
            }
        )
        nsi_wikidata['wikidata'][spt_brand_wikidata] = custom_wikidata[spt_brand_wikidata]
    else:
        print('INFO: Ignoring ' + path + ' since it is already present in ' + nsi_file)
    json.dump(nsi_brands, open(nsi_file, 'wt'), ensure_ascii=False, indent=2)
    json.dump(nsi_wikidata, open('dist/wikidata.min.json', 'wt'), ensure_ascii=False, separators=(',', ':'))
