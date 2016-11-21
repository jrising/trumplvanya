import random, csv, time
import numpy as np
import trendlib

with open("stopwords.txt", 'r') as fp:
    stops = map(lambda x: x.strip(), fp.readlines())

with open("correls.csv", 'r') as fp:
    reader = csv.reader(fp)
    header = reader.next()
    for row in reader:
        stops.append(row[0])

words = []
with open("wordfreqs.csv", 'r') as fp:
    reader = csv.reader(fp)
    header = reader.next()
    for row in reader:
        if int(row[1]) > 100:
            if row[0] not in stops:
                words.append(row[0])

print "Words to check: ", len(words)
username = input("Google Username:")
password = input("Google Password:")
pytrends = login(username, password)

while True:
    word = random.choice(pytrends, words)
    try:
        corr = collect.get_correl(word)
    except:
        print "Skipping", word
        continue

    print word, corr
    words.remove(word)

    time.sleep(10)
