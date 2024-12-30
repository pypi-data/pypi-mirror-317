import hashlib
import yaml
from apify import Actor
from .constants import *
from .utils import elapsed, prompt_template_yaml

# opt 종류
QUERY = 'query'
FIX = 'fix'
PROMPT = 'prompt'
KEYWORDS = 'keywords'
DESCRIPTION = 'description'
def get(_domain, _name, _opt):
    if _domain == SX_DOMAIN_NEWS:
        query_domain = f'query_{SX_DOMAIN_NEWS}'
    if _domain == SX_DOMAIN_COMPANY:
        query_domain = f'query_{SX_DOMAIN_COMPANY}'
    if _domain == SX_DOMAIN_COIN:
        query_domain = f'query_{SX_DOMAIN_COIN}'

    datadict = prompt_template_yaml(query_domain)
    for entry in datadict:
        if entry.get('name') == _name:
            if _opt == FIX:

                if _name == '삼성생명':
                    return '4ff9fde083e595ee'
                if _name == '이루':
                    return 'bc57de0abb747e24'

                return fix_query(entry[QUERY].strip())
            return entry[_opt].strip()
    return None

# 'Hello | World + 한글 - "Test"'
def fix_query(_naver_query):
    hash_bytes = hashlib.sha256(_naver_query.encode()).digest()
    out =  bytes(a ^ b ^ c ^ d for a, b, c, d in zip(hash_bytes[:8], hash_bytes[8:16], hash_bytes[16:24], hash_bytes[24:]))
    return out.hex()

async def getkv(_name, _opt):
    kv_store = await Actor.open_key_value_store(name=SX_KV_CONFIG)
    begintrx = await kv_store.get_value(f'{SX_SCRAPER}{SX_EXT_YAML}') or None
    if not begintrx:
        return get(_name, _opt)
    datadict = yaml.load(begintrx, Loader=yaml.FullLoader)
    for entry in datadict:
        if entry.get('name') == _name:
            if _opt == FIX:
                return fix_query(entry[QUERY].strip())
            return entry[_opt].strip()
    return None