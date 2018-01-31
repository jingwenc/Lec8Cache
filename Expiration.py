from secrets import *
import requests
import json
from datetime import datetime

def expiration(baseurl,params):
    now = datetime.now()

    MAX_STALENESS = 30
    def is_fresh(cache_entry):
        now = datetime.now().timestamp()
        staleness = now - cache_entry['cache_timestamp']
        return staleness < MAX_STALENESS

    CACHE_FNAME = 'cache_file_name.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    except:
        CACHE_DICTION = {}


    def params_unique_combination(baseurl, params):
        alphabetized_keys = sorted(params.keys())
        res = []
        for k in alphabetized_keys:
            res.append("{}-{}".format(k, params[k]))
        return baseurl + "_".join(res)

    def make_request_using_cache(baseurl, params):
        unique_ident = params_unique_combination(baseurl,params)

        if unique_ident in CACHE_DICTION:
            if is_fresh(CACHE_DICTION[unique_ident]):
                print("Getting cached data...")
                return CACHE_DICTION[unique_ident]
        else:
            pass

        print("Making a request for new data...")
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]
    sec_since_epoch = now.timestamp()
    print(sec_since_epoch)

p={'api-key': nyt_key}
u=["https://api.nytimes.com/svc/topstories/v2/politics.json","https://api.nytimes.com/svc/topstories/v2/politics.json",
"https://api.nytimes.com/svc/topstories/v2/technology.json","https://api.nytimes.com/svc/topstories/v2/business.json",
"https://api.nytimes.com/svc/topstories/v2/theater.json"]
for i in u:
    i
    expiration(i,p)
'''
###Each section does not expire at the same time.###
'''
