import jellyfish
from pprint import pprint

def levenshtein_distance(a, b):
    return jellyfish.levenshtein_distance(a, b)

def jaro_distance(a, b):
    return jellyfish.jaro_distance(a, b)

def checkForBeerMaster(beer, mastersDict):
    pprint('beer to check is ' + beer)
    lev_dict = {}
    jaro_dict = {}
    for k,v in mastersDict.items():
        # pprint(v)
        # pprint(jaro_distance(v, beer))
        # pprint(levenshtein_distance(v, beer))
        # pprint(jellyfish.jaro_winkler_similarity(v, beer))
        #
        # lev_dict[k] = levenshtein_distance(v, beer)
        # lev_bestMatchKey = min(lev_dict, key=lev_dict.get)
        #
        #
        # jaro_dict[k] = jaro_distance(v, beer)
        # # jaro_bestMatchKey = max(jaro_dict, key=jaro_dict.get)


        if v in beer:
            return k

    return None



# for k,v in masterbeernames.items():
#     pprint(v)
#     pprint(similar(v, 'Bud Light Pale Lager Draft - St. Louis, MO'))
#     masterbeernames[k] = similar(v, 'Bud Light Pale Lager Draft - St. Louis, MO')
# pprint(max(masterbeernames, key=masterbeernames.get))
#pprint(max([1,2,3,4]))

# pprint(similar('Dogfish Head SeaQuench Ale', 'Bud Light Pale Lager Draft - St. Louis, MO'))
#
# pprint(similar('Miller Light', 'Bud Light Pale Lager Draft - St. Louis, MO'))
# pprint(similar('Coors Light', 'Bud Light Pale Lager Draft - St. Louis, MO'))
# pprint(similar('Bud Light', 'Bud Light Pale Lager Draft - St. Louis, MO'))

if __name__ == "__main__":
    masterbeernames={113:'Dogfish Head SeaQuench Ale', 124:'Miller Light', 125:'Coors Light', 116:'Bud Light'}
    pprint(checkForBeerMaster('Bud Light Pale Lager Draft - St. Louis, MO', masterbeernames))
