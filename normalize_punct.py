import re


from pathlib import Path
from botok import BoString
from botok.vars import CharMarkers
from syls import parse_syl

def is_punt(string):
    normal_punt = CharMarkers(5)
    special_punt = CharMarkers(6)
    bo_string = BoString(string)
    for _, char_marker_value in bo_string.base_structure.items():
        char_maker = CharMarkers(char_marker_value)
        if char_maker == normal_punt or char_maker == special_punt:
            return True
    return False

def get_syls(text):
    chunks = re.split('(་)',text)
    syls = []
    cur_syl = ''
    for chunk in chunks:
        if re.search('་',chunk):
            cur_syl += chunk
            syls.append(cur_syl)
            cur_syl = ''
        else:
            cur_syl += chunk
    if cur_syl:
        syls.append(cur_syl)
    return syls


def get_chunks(text):
    chunks = []
    parts = re.split("([\u0F0D-\u0F14])", text)
    cur_chunk = ""
    for part in parts:
        if re.search("([\u0F0D-\u0F14])", part):
            cur_chunk += part
            chunks.append(cur_chunk)
            cur_chunk = ""
        else:
            cur_chunk += part
    
    if cur_chunk:
        chunks.append(cur_chunk)
    return chunks

def shad_after_ng_normalization(chunk):
    syls = get_syls(chunk)
    last_syl = syls[-1]
    syl_parts = parse_syl(last_syl)
    if syl_parts['yang_jug']:
        return chunk
    if syl_parts['jes_jug'] == "ང":
        if "ང་" in last_syl:
            return chunk
        else:
            nor_last_syl = last_syl.replace("ང", "ང་")
            chunk = chunk.replace(last_syl, nor_last_syl)
            return chunk
    return chunk




def normalize_punct(text):
    normalized_text = ""
    chunks = get_chunks(text)
    for chunk in chunks:
        normalized_text += shad_after_ng_normalization(chunk)
