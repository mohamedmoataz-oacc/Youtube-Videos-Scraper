# A script to get data about a specific youtube query

# Use the requests_html module
from requests_html import HTMLSession

def get_video_data(video):
    """
    Extracts a given video's title, link, channel, views and when was it published at the time this script was run.
    """
    yt_item = list()
    try:
        # Extract video title
        yt_item.append(video.find('a#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer', first=True).attrs['title'])
        # Extract video link
        yt_item.append(video.find('a#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer', first=True).attrs['href'])
        # Extract video channel
        yt_item.append(video.find('.yt-formatted-string', first=True).text)
        # Extract video views
        yt_item.append(video.find('div#metadata div#metadata-line span.inline-metadata-item.style-scope.ytd-video-meta-block', first=True).text)
        # Extract when was the video published
        yt_item.append(video.find('.inline-metadata-item+ .ytd-video-meta-block', first=True).text)
        return yt_item  # A list containing the extracted data
    except Exception as e:
        # The function returns None if some data about a video was missing
        return

# Some user agents to use when sending a request, so that if one fails we try another
user_agents = [
    'Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Windows 7/ Chrome browser: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/47.0.2526.111 Safari/537.36',
    'Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, '
    'like Gecko) Version/9.0.2 Safari/601.3.9',
    'Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/51.0.2704.64 Safari/537.36'
]

session = HTMLSession()  # Start a new session
for agent in user_agents:
    try:
        # Try a user agent
        user_agent = {'User-agent': agent}
        # Get the desired page to scrape, replace this query with the one you want
        query = 'web scraping with python'
        page = session.get('https://www.youtube.com/results?search_query=' + query.replace(' ', '+'),
                    headers = user_agent)
        break  # If the request was successful, break out of the loop
    except:
        # If the request was unsuccessful, try another user agent
        print('Retrying...')

# Render the returned JS code to html, the scrolldown parameter is set to 30 so that it gets more data.
# It basically pressesthe 'PG DN' button 30 times so that more videos load in the page.
# Set the scrolldown parameter to whatever number you want, but the more you increase it, the more time it takes.
page.html.render(sleep=1, timeout=20, scrolldown=30)

# Get all videos in the page
videos = page.html.xpath('//div[@id="meta"]')
print('Scraped', len(videos), 'videos')

# Save the videos data to a csv file
with open('videos_data.csv', 'wb') as f:
    f.write(b'title,link,channel,views,when\n')
    for video in videos:
        data = get_video_data(video)
        
        if data is not None:
            # Data is encoded in bytes because the video title may contain some characters,
            # like arabic characters for example, so it needs to be encoded to bytes to be written to the csv.
            for i in data[:-1]:
                f.write(f'"{i}"'.encode())
                f.write(','.encode())
            f.write(data[-1].encode())
            f.write(b'\n')
        
