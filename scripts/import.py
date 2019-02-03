"""
Import the DATASETS_NB most popular datasets from data.gouv.fr into lektor
"""
import json
import requests

DATASETS_NB = 5
DATASETS_URL = 'https://data.gouv.fr/api/1/datasets?page_size=%s' % DATASETS_NB
LEKTOR_URL = 'http://localhost:5000/admin/api'


def make_resources(resources):
    output = []
    for r in resources:
        output.append('#### resource ####')
        res_markup = ['%s: %s' % (k, v) for k, v in r.items()]
        output.append('\n---\n'.join(res_markup))
    return '\n'.join(output)


def create_dataset(data):
    r = requests.post('/'.join((LEKTOR_URL, 'newrecord')), json={
        'id': data['id'],
        'model': 'dataset',
        'path': '/datasets/%s' % data['id']
    })
    print('create', r.status_code)
    return r.json()


def update_dataset(path, data):
    r = requests.put('/'.join((LEKTOR_URL, 'rawrecord')), json={
        'path': path,
        'data': data,
    })
    print('update', r.status_code)
    return r.json()


r = requests.get(DATASETS_URL)

for d in r.json()['data']:
    data = {
        'id': d['slug'],
        'title': d['title'],
        'description': d['description'],
        'resources': [
            {
                'url': d['resources'][0]['url'],
                'description': d['resources'][0]['title'],
            }
        ],
    }
    data['resources'] = make_resources(data['resources'])
    dataset = create_dataset(data)
    if dataset['exists']:
        res = update_dataset(dataset['path'], data)
        print('Updated dataset %s' % data['id'])
    else:
        print('Created dataset %s' % data['id'])
