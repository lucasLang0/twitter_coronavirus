# Coronavirus Twitter Analysis

This project involved analyzing geotagged tweets sent in 2020 to monitor the spread of the coronavirus on social media. The analysis used the MapReduce paradigm to handle the large-scale dataset efficiently.

## Learning Objectives

1. Work with large-scale datasets
2. Work with multilingual text
3. Use the MapReduce divide-and-conquer paradigm to create parallel code

## Background

### About the Data

Approximately 500 million tweets are sent every day. Of those tweets, about 2% are geotagged, meaning the user's device includes location information about where the tweets were sent from. The dataset contained all geotagged tweets sent in 2020, totaling about 1.1 billion tweets.

The tweets were stored in zip files, with each day having its own zip file (`geoTwitterYY-MM-DD.zip`). Inside each zip file were 24 text files, one for each hour of the day. Each text file contained a single tweet per line in JSON format.

### About MapReduce

MapReduce is a procedure for large-scale parallel processing widely used in industry. It consists of three steps: partition, map, and reduce. The partition step had already been done by splitting the tweets into one file per day. The map and reduce steps were implemented in this project.

## Tasks

### Task 1: Map

I created a Python command that counts the number of tweets sent in each language on a particular day. The Python file was called `map.py` and was located in the `src` folder. The outputs of this are in the `outputs/` folder.

### Task 2: Reduce

I wrote a Python file `./src/reduce.py` that took the outputs from the `map.py` file and reduced them together.

### Main Tasks

#### Task 0: Create the Mapper

I modified `map.py` to track the usage of hashtags on both a language and country level. The output of running `map.py` was two files: one ending in `.lang` for the language dictionary and one ending in `.country` for the country dictionary.

#### Task 1: Run the Mapper

I created a shell script called `run_maps.sh` to loop over each file in the dataset and run the `map.py` command on that file. I used the `nohup` command to ensure the program continued to run after disconnecting and the `&` operator to run all `map.py` commands in parallel.

#### Task 2: Reduce

I used the `reduce.py` file to combine all of the `.lang` files into a single file and all of the `.country` files into a different file.

#### Task 3: Visualize

I modified the `visualize.py` file to generate a bar graph of the results and store the bar graph as a PNG file. The horizontal axis of the graph was the keys of the input file, and the vertical axis was the values of the input file. The final results were sorted from low to high, including only the top 10 keys.

I ran the `visualize.py` file with the `--input_path` equal to both the country and lang files created in the reduce phase, and the `--key` set to `#coronavirus` and `#코로나바이러스`. This generated four plots in total.

#### Task 4: Alternative Reduce

I created a new file `alternative_reduce.py` that took a list of hashtags as input and output a line plot where:
1. There was one line per input hashtag.
1. The x-axis was the day of the year.
1. The y-axis was the number of tweets that used that hashtag during the year.

The script scanned through all the data in the `outputs` folder created by the mapping step, constructed a graph plotting the use of the hashtags #covid19, #corona, and #hospital, and used matplotlib to plot the data.

## Results

### Language Analysis

#### Language Analysis for #coronavirus:

![Language Analysis for #coronavirus](https://github.com/lucasLang0/twitter_coronavirus/blob/master/coronavirus_language_count.png)

#### Language Analysis for #코로나바이러스:

![Language Analysis for #코로나바이러스](https://github.com/lucasLang0/twitter_coronavirus/blob/master/%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4_language_count.png)


### Country Analysis

#### Country Analysis for #coronavirus:

![Country Analysis for #coronavirus](https://github.com/lucasLang0/twitter_coronavirus/blob/master/coronavirus_country_count.png)

#### Country Analysis for #코로나바이러스:

![Country Analysis for #코로나바이러스](https://github.com/lucasLang0/twitter_coronavirus/blob/master/%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4_country_count.png)


### Alternative Reduce

![Alternative Reduce Plot](https://github.com/lucasLang0/twitter_coronavirus/blob/master/%23covid19_%23corona_%23hospital.png)


