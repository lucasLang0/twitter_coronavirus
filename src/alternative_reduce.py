#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags',nargs='+',required=True)
#parser.add_argument('--output_path',required=True)
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
from datetime import datetime
import matplotlib.dates as mdates

# map
total = defaultdict(lambda: Counter())
pattern = r'geoTwitter([0-9][0-9]-[0-9][0-9]-[0-9][0-9])\.zip\.lang'
for output in sorted(os.listdir("./outputs")):
    date_file = os.path.join('./outputs', output)
    
    # Print file being processed for debugging
    print(f"Processing file: {output}")
    
    with open(date_file) as f:
        date_data = json.load(f)
    
    match = re.search(pattern, output)
    if match:
        date = match.group(1)
        print(f"Extracted date: {date}")
        
        # Debug which hashtags are found
        found_tags = []
        for hashtag in args.hashtags:
            if hashtag in date_data:
                count = sum(date_data[hashtag].values())
                found_tags.append(f"{hashtag}({count})")
            else:
                count = 0
            total[hashtag][date] += count
        
        if found_tags:
            print(f"Found hashtags: {', '.join(found_tags)}")
        else:
            print(f"No requested hashtags found in this file")

# visualize

# print the count values
hashtag_string = ''
for hashtag in args.hashtags:
    hashtag_string += hashtag
    hashtag_string += '_'
    items = sorted(total[hashtag].items(), key=lambda item: datetime.strptime(item[0], "%y-%m-%d"))
    for k,v in items:
        print(k,':',v)
    tweets = [i[1] for i in items]
    date = [datetime.strptime(i[0], "%y-%m-%d") for i in items]
    plt.plot(date, tweets, label = hashtag)
#date = [datetime.strptime(i[0], "%y-%m-%d") for i in total[args.hashtags[0]]]
plt.xlabel("Date")
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
#plt.xticks([x for x in date if x.day == 1], rotation=45)
plt.xticks(rotation = 45)
plt.ylabel("Number of Tweets")
plt.tight_layout(pad = 1.15)
plt.legend()
plt.savefig(f"daily_{hashtag_string}tweets_plot.png")
