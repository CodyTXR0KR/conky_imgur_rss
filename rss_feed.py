#!/usr/bin/env python3
import os
import shutil
import urllib.request

import feedparser

IMAGE_SIZE = 128
IMAGE_CACHE = os.path.join(os.path.expanduser('~'), '.imgur-cache')
RSS_URL = 'http://imgur.com/rss'
# Data keys for each entry: 
# ['links', 'summary', 'media_content', 'title', 'media_thumbnail', 
#  'href', 'summary_detail', 'title_detail', 'link']


def clear_cache():
    for the_file in os.listdir(IMAGE_CACHE):
        file_path = os.path.join(IMAGE_CACHE, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def download_thumbnail(url, full_dest_path):
    response = urllib.request.urlopen(url)
    f = open(full_dest_path, 'wb')
    f.write(response.read())
    f.close()


def conky_output(rss_data, show_entries=5):
    # Column 1
    for x in range(show_entries):
        image_y = (IMAGE_SIZE + 15) * x
        print('${image %s -p 20,%s -s 128x128}' % (rss_data[x]['thumb'], image_y + 25))
    # Column 2
    for x in range(show_entries):
        image_y = (IMAGE_SIZE + 15) * x
        print('${image %s -p 168,%s -s 128x128}' % (rss_data[x + 5]['thumb'], image_y + 25))


def process_feed():
    data = feedparser.parse(RSS_URL)
    rss_data = []

    for item in data.entries:
        item_data = {}

        file_name = item.media_thumbnail[0]['url'].replace('http://i.imgur.com/', '')
        full_dest_path = os.path.join(IMAGE_CACHE, file_name)

        download_thumbnail(item.media_thumbnail[0]['url'], full_dest_path)

        item_data['title'] = (item.title[:32] + '...') if len(item.title) > 32 else item.title
        item_data['thumb'] = full_dest_path
        item_data['url'] = item.link
        rss_data.append(item_data)

    return rss_data
 

clear_cache()
rss_data = process_feed()
conky_output(rss_data)
