import sys
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def extract_data_from_file(file_path, hashtags):
    data = defaultdict(int)
    with open(file_path, 'r') as f:
        content = json.load(f)
        for hashtag in hashtags:
            if hashtag in content:
                for country, count in content[hashtag].items():
                    data[hashtag] += count
    return data

def scan_data_files(data_folder, hashtags):
    all_data = defaultdict(lambda: defaultdict(int))
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.lang'):
            file_path = os.path.join(data_folder, file_name)
            # Extract the day of the year from the file name
            month_day = file_name.split('-')[1:3]
            month = int(month_day[0])
            day = int(month_day[1].split('.')[0])
            day_of_year = (month - 1) * 31 + day  # Use 31 days per month to avoid issues with different month lengths
            daily_data = extract_data_from_file(file_path, hashtags)
            for hashtag, count in daily_data.items():
                all_data[hashtag][day_of_year] += count
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
    
    # Save the plot as a PNG file named based on the hashtags used
    filename = "_".join(hashtags) + ".png"
    plt.savefig(filename)
    print(f"Plot saved as {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python alternative_reduce.py <hashtag1> <hashtag2> ...")
        sys.exit(1)

    hashtags = sys.argv[1:]
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # Define the path to the outputs folder relative to the script directory
    data_folder = os.path.join(script_dir, '..', 'outputs')
    
    data = scan_data_files(data_folder, hashtags)
    
    # Print the number of uses per day for error checking purposes
    for hashtag in hashtags:
        print(f"Usage of {hashtag} per day:")
        for day in range(1, 367):
            print(f"Day {day}: {data[hashtag].get(day, 0)}")
    
    plot_data(data, hashtags)
