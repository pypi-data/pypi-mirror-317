import json
from pathlib import Path
from mimetypes import MimeTypes

mimetypes = MimeTypes()

custom_types = {
    "application/vnd.wap.xhtml+xml": ".xhtml",
    "application/x-json": ".json",
    "application/json-amazonui-streaming": ".json",
}

for k, v in custom_types.items():
    mimetypes.add_type(k, v)

# https://github.com/patrickmccallum/mimetype-io/blob/master/src/mimeData.json
with open(Path(__file__).resolve().parent / 'res' / 'mimeData.json', 'rb') as f:
    data_list = json.load(f)
for data in data_list:
    if data['fileTypes']:
        mimetypes.add_type(data['name'], data['fileTypes'][0])
        for name in data['links']['deprecates']:
            mimetypes.add_type(name, data['fileTypes'][0])
