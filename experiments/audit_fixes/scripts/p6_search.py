import json
ids = ['2013_30', '1977_99', '2013_35', '2013_57', '1980_217', '2013_101', '1980_133', '2013_121', '1978_33', '2008_516', '1981_187', '2002_171', '1980_222', '2013_95', '1977_145', '2017_14', '1981_55', '2001_414', '1980_105']
with open('/repo/artifacts/week12_prediction_cross_reference.json') as f: d = json.load(f)
def search(obj, path=''):
  if isinstance(obj, dict):
    for k, v in obj.items():
      if any(i in k for i in ids): print(f'{path}.{k}')
      search(v, path+'.'+k if path else k)
  elif isinstance(obj, list):
    for idx, item in enumerate(obj):
      if isinstance(item, str) and any(i in item for i in ids): print(f'{path}[{idx}] = {item}')
      search(item, f'{path}[{idx}]')
  elif isinstance(obj, str) and any(i in obj for i in ids): print(f'{path} = {obj}')
search(d)
