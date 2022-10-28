import json
import pandas as pd
from flatten_json import flatten


with open('scival_out.json') as json_file:
    json_data = json.load(json_file)

dic_flattened = [flatten(d) for d in json_data['data']]

df = pd.DataFrame(dic_flattened)

df.to_csv("Output.csv", index=False)