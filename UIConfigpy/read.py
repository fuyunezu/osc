import json
import os


with open(os.path.dirname(os.path.realpath(__file__)).replace("\\","\\\\")+"\\Configure.json", encoding='utf-8') as f:
    t = json.load(f)
print(t[0]["n"])