import re
from botok.textunits.sylcomponents import SylComponents


def get_syls(word):
    """Return syllable of a word

    Args:
        word (str): word

    Returns:
        list: syllable of the words
    """
    chunks = re.split('་', word)
    syls= []
    for chunk in chunks:
        if chunk:
            syls.append(chunk)
    return syls

def is_consonant(char):
    """Check if the character is tibetan consonant or not

    Args:
        char (str): a tibetan character

    Returns:
        boolean: true if char is tibetan consonant else false
    """
    if re.search('[\u0F40-\u0F67]', char):
        return True
    else:
        return False

def is_vowel(char):
    """Check if the character is tibetan vowel or not

    Args:
        char (str): a character

    Returns:
        Boolean: True if char is vowel else false
    """
    if char in ['ི', 'ུ', 'ེ', 'ོ']:
        return True
    else:
        return False

def get_sngon_jug(syl_part):
    """Returns if sngon jug exist else empty string

    Args:
        syl_part (str): syllable component

    Returns:
        str: one the sngon jug if one exist in syl component else empty string 
    """
    if syl_part[0] in ['ག', 'ད', 'བ', 'མ', 'འ'] and is_consonant(syl_part[1]):
        return syl_part[0]
    else:
        return ''

def get_mingzhi(syl_first_half, syl_second_half, sngon_jug):
    """Return mingzhi of the syllable using syllable components

    Args:
        syl_first_half (str): first half of syl component which could consist of sngonjug and mingzhi
        syl_second_half (str): second half of syl component which could consist of vowel of mingzhi, jes jug and yang jug

    Returns:
        str: mingzhi of syllable
    """
    mingzhi = ''
    if sngon_jug:
        mingzhi += syl_first_half[1:]
    else:
        mingzhi += syl_first_half
    if syl_second_half and is_vowel(syl_second_half[0]):
        return mingzhi+syl_second_half[0]
    else:
        return mingzhi

def get_jes_jug(syl_part):
    """Return jes jug from the second half of syllable component if it exist

    Args:
        syl_part (str): second half of syllable component

    Returns:
        str: jes jug if it exist else empty string
    """
    if re.search('ག|ང|ད|ན|བ|མ|འ|ར|ལ|ས', syl_part):
        jes_jug_pat = re.search('ག|ང|ད|ན|བ|མ|འ|ར|ལ|ས', syl_part)
        return jes_jug_pat[0]
    else:
        if len(syl_part)>=2:
            return syl_part[1]
        else:
            return ''

def get_yang_jug(syl_part):
    """Return yang jug from second half of syllable component

    Args:
        syl_part (str): second half of syllable component

    Returns:
        str: yangjug if oen exist else empty string
    """
    if is_vowel(syl_part[0]):
        if len(syl_part)==3:
            return syl_part[2]
        else:
            return ""
    else:
        if len(syl_part)>0:
            return syl_part[1]
        else:
            return ""

def parse_syl(syl):
    """Parse syllable components

    Args:
        syl (str): syllable

    Returns:
        dict: consit of all the possible component of a syllable which are sngonjug, mingzhi, jesjug and yangjug
    """
    syl_parts = {}
    sngon_jug = ''
    jes_jug = ''
    mingzhi = ''
    yang_jug = ''
    sc = SylComponents()
    components = sc.get_parts(syl)
    if components:
        if len(components[0]) >= 2:
            sngon_jug = get_sngon_jug(components[0])
        mingzhi = get_mingzhi(components[0], components[1], sngon_jug)
        if components[1]:
            jes_jug = get_jes_jug(components[1])
        if len(components[1]) >= 2:
            yang_jug = get_yang_jug(components[1])
        syl_parts = {
            'sngon_jug': sngon_jug,
            'mingzhi': mingzhi,
            'jes_jug': jes_jug,
            'yang_jug': yang_jug
        }
    return syl_parts

def build_syl(syl_parts):
    sngon_jug = syl_parts.get('sngon_jug', '')
    mingzhi = syl_parts.get('mingzhi', '')
    jes_jug = syl_parts.get('jes_jug', '')
    yang_jug = syl_parts.get('yang_jug', '')
    syl = f'{sngon_jug}{mingzhi}{jes_jug}{yang_jug}་'
    return syl