import csv, time, json
import numpy as np
from pytrends.request import TrendReq

def getnum(v):
    if isinstance(v, str):
        return float(v.replace(',', ''))
    return float(v)

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

bystate = {}
with open("results.csv", 'rU') as fp:
    reader = csv.reader(fp)
    header = reader.next()
    for row in reader:
        bystate[row[0]] = getnum(row[header.index('Trump (R)')]) / getnum(row[header.index("Total '16 Votes")])

def login(username, password):
    return TrendReq(username, password, custom_useragent=None)

def get_correl(pytrends, word):
    data = pytrends.geomap(dict(q=word, geo='US'))
    with open("data/" + word + ".json", 'w') as outfp:
        json.dump(data, outfp)

    trendvalues = []
    resultvalues = []
    for row in data['table']['rows']:
        state = None
        value = None
        for col in row['c']:
            if isinstance(col['v'], unicode) and col['v'][0:3] == 'US-':
                state = col['v'][3:]
            if isinstance(col['v'], float):
                value = col['v']

        trendvalues.append(value)
        resultvalues.append(bystate[states[state]])

    corr = np.corrcoef(trendvalues, resultvalues)[0, 1]

    with open('correls.csv', 'a') as outfp:
        writer = csv.writer(outfp)
        writer.writerow([word, corr])

    return corr
