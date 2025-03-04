import sys
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def extract_data_from_file(file_path, hashtags):
    data = defaultdict(lambda: defaultdict(int))
    with open(file_path, 'r') as f:
        content = json.load(f)
        for hashtag in hashtags:
            if hashtag in content:
                for lang, count in content[hashtag].items():
                    data[hashtag][lang] += count
    return data

def scan_data_files(data_folder, hashtags):
    all_data = defaultdict(lambda: defaultdict(int))
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.lang'):
            file_path = os.path.join(data_folder, file_name)
            daily_data = extract_data_from_file(file_path, hashtags)
            for hashtag, counts in daily_data.items():
                for lang, count in counts.items():
                    all_data[hashtag][lang] += count
    return all_data

def plot_data(data, hashtags):
    days = list(range(1, 367))
    for hashtag in hashtags:
        counts = [data[hashtag].get(day, 0) for day in days]
        plt.plot(days, counts, label=hashtag)
    
    plt.xlabel('Day of the Year')
    plt.ylabel('Number of Tweets')
    plt.title('Daily Usage of Hashtags')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python alternative_reduce.py <hashtag1> <hashtag2> ...")
        sys.exit(1)

    hashtags = sys.argv[1:]
    data_folder = 'outputs'
    
    data = scan_data_files(data_folder, hashtags)
    plot_data(data, hashtags)
