global conf_json
conf_json = None
with open('../config/faces.json', 'r') as conf_json_f:
    conf_json = json.loads(conf_json_f.read())
    conf_json['data_path']

