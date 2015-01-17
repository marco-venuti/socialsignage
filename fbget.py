#!/usr/bin/env python3

import requests
import json
import datetime
import sys


def get_profile_picture(fbkey, userid):
    r = requests.get('https://graph.facebook.com/v2.2/'+str(userid)+'/picture',params={'access_token':fbkey,'redirect':'false'})
    data = json.loads(r.text)
    if 'data' in data:
        if 'url' in data['data']:
            return data['data']['url']


def get_topage(fbkey):
    r = requests.get('https://graph.facebook.com/v2.2/587747891351295/tagged',params={'access_token':fbkey})
    posts = json.loads(r.text)
    if 'error' in posts:
        print ('Error in getting posts to page')
        return []
    else:
        return posts['data']

def get_frompage(fbkey):
    r = requests.get('https://graph.facebook.com/v2.2/587747891351295/posts',params={'access_token':fbkey})
    posts = json.loads(r.text)
    if 'error' in posts:
        print ('Error in getting posts from page')
        return []
    else:
        return posts['data']


def elab(fbkey,post):
    out = {}
    if 'created_time' in post:
        out['time'] = datetime.datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    else:
        return None
    if 'message' in post:
        out['text'] = post['message']
    else:
        out['text'] = ""
    if 'from' in post:
        out['author_name'] = post['from']['name']
        try:
            out['author_pic'] = get_profile_picture(fbkey,post['from']['id'])
        except e:
            out['author_pic'] = None
    else:
        return None
    if 'picture' in post:
        out['image'] = post['picture']
    else:
        out['image'] = None
    if out['text'] is '' and out['image'] is None:
        return None
    return out

def get(fbkey):
    posts = []
    posts += get_topage(fbkey)
    posts += get_frompage(fbkey)
    out = []
    for post in posts:
        temp = elab(fbkey,post)
        if temp is not None:
            out.append(temp)
    return out

def main():
    fbkey = sys.argv[1]
    posts = get(fbkey)
    sorted_posts = sorted(posts,key = lambda post: post['time'])
    sorted_posts.reverse()
    print(sorted_posts)









if __name__ == "__main__":
    main()
            
