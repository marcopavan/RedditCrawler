# RedditCrawler
Reddit Crawler is a tool based on the official Reddit API used to extract complete conversations.
It is possibile to run the tool using a conversation ID, or a keyword like "top" or "hot" to get a set of conversations from the Reddit popular lists.

## Usage example:
```
    python main.py -n trainingset -f -v
    python main.py -n 4ogcwa -f -v
    python main.py -n hot -f -v
    python main.py -n hot -l 5 -f -v
```
