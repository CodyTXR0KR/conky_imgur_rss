#!/usr/bin/env python3
import os
import sys
import shutil
import urllib.request

import feedparser

IMAGE_CACHE = os.path.join(os.path.expanduser('~'), '.imgur-cache')

# Data keys for each entry (20 entries): 
# ['links', 'summary', 'media_content', 'title', 'media_thumbnail', 
#  'href', 'summary_detail', 'title_detail', 'link']
RSS_URL = 'http://imgur.com/rss'

# Panel options
COL_HEIGHT = 6  # Num Vert Images
COL_WIDTH = 3   # Num Hor Images

"""
# Defining colors (White)
default_color FFFFFF
# Background (Dark Grey)
color1 181817
# Upvote (Green)
color2 85BF25
# Frame (Light Grey)
color3 2B2B2B
"""


def clear_cache():
    try:
        for _file in os.listdir(IMAGE_CACHE):
            file_path = os.path.join(IMAGE_CACHE, _file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    except Exception as e:
        print(e)
        sys.exit()


def download_thumbnail(url, full_dest_path):
    try:
        response = urllib.request.urlopen(url)
        f = open(full_dest_path, 'wb')
        f.write(response.read())
        f.close()
    except Exception as e:
        print(e)
        sys.exit()


def process_feed():
    data = feedparser.parse(RSS_URL)
    rss_data = []

    for item in data.entries:
        item_data = {}

        file_name = item.media_thumbnail[0]['url'].replace('http://i.imgur.com/', '')
        full_dest_path = os.path.join(IMAGE_CACHE, file_name)

        if not os.path.isfile(full_dest_path):
            download_thumbnail(item.media_thumbnail[0]['url'], full_dest_path)

        item_data['title'] = (item.title[:32] + '...') if len(item.title) > 32 else item.title
        item_data['thumb'] = full_dest_path
        item_data['url'] = item.link
        rss_data.append(item_data)

    return rss_data


def conky_output(rss_data):
    IMG_SIZE = 96
    MARGIN_TOP = 40
    PADDING = 10
    # conky string to draw image
    render_thumbnail = '''${{image {thumb_url} -p {x},{y} -s {w}x{h}}}'''
    last_x = 0
    last_y = 0
    for x in range(len(rss_data)):
        item = rss_data[x]
        if x == 0:  # Start COLUMN 1
            x_pos = last_x + PADDING
            last_x = x_pos
            y_pos = last_y + MARGIN_TOP
            last_y = y_pos
            print(render_thumbnail.format(
                thumb_url=item['thumb'], x=x_pos, y=y_pos, w=IMG_SIZE, h=IMG_SIZE))
            continue
        elif x + 1 <= COL_HEIGHT: # Continue COLUMN 1
            y_pos = last_y + IMG_SIZE + PADDING
            last_y = y_pos
            print(render_thumbnail.format(
                thumb_url=item['thumb'], x=last_x, y=y_pos, w=IMG_SIZE, h=IMG_SIZE))
            continue
        elif x == COL_HEIGHT:  # Start COLUMN 2
            x_pos = (last_x + IMG_SIZE) + PADDING
            last_x = x_pos
            y_pos = 0 + MARGIN_TOP
            last_y = y_pos
            print(render_thumbnail.format(
                thumb_url=item['thumb'], x=x_pos, y=y_pos, w=IMG_SIZE, h=IMG_SIZE))
            continue
        elif x + 1 <= (COL_HEIGHT * 2):  # Continue COLUMN 2
            y_pos = last_y + IMG_SIZE + PADDING
            last_y = y_pos
            print(render_thumbnail.format(
                thumb_url=item['thumb'], x=last_x, y=y_pos, w=IMG_SIZE, h=IMG_SIZE))
            continue
        elif x == (COL_HEIGHT * 2):  # Start COLUMN 3
            x_pos = (last_x + IMG_SIZE) + PADDING
            last_x = x_pos
            y_pos = 0 + MARGIN_TOP
            last_y = y_pos
            print(render_thumbnail.format(
                thumb_url=item['thumb'], x=x_pos, y=y_pos, w=IMG_SIZE, h=IMG_SIZE))
            continue
        elif x + 1 <= (COL_HEIGHT * COL_WIDTH):  # Continue COLUMN 3
            y_pos = last_y + IMG_SIZE + PADDING
            last_y = y_pos
            print(render_thumbnail.format(
                thumb_url=item['thumb'], x=last_x, y=y_pos, w=IMG_SIZE, h=IMG_SIZE))
            continue
        else:  # Stop rendering
            break
    sys.exit()


    

    # # Column 1
    # for x in range(show_entries):
    #     image_y = (IMAGE_SIZE + 15) * x
    #     print('${image %s -p 20,%s -s 96x96}' % (rss_data[x]['thumb'], image_y + 25))
    # # Column 2
    # for x in range(show_entries):
    #     image_y = (IMAGE_SIZE + 15) * x
    #     print('${image %s -p 168,%s -s 128x128}' % (rss_data[x + 5]['thumb'], image_y + 25))

 
# if __name__ == '__main__':
clear_cache()
rss_data = process_feed()
conky_output(rss_data)
