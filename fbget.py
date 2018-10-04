#!/usr/bin/env python3

import requests
import json
import datetime
import sys


def get_profile_picture(fbkey, userid):
    r = requests.get('https://graph.facebook.com/v2.6/'+str(userid)+'/picture',params={'access_token':fbkey,'redirect':'false'})
    data = json.loads(r.text)
    if 'data' in data:
        if 'url' in data['data']:
            return data['data']['url']


def get_topage(fbkey,needed_fb_fields=None):
    if needed_fb_fields is []:
        needed_fb_fields = None
    request_url = 'https://graph.facebook.com/v2.6/587747891351295/tagged'
    if needed_fb_fields is not None:
        request_url += '?fields='+ ','.join(needed_fb_fields)
    r = requests.get(request_url,params={'access_token':fbkey})
    posts = json.loads(r.text)
    if 'error' in posts:
        print (request_url)
        print ('Error in getting posts to page')
        return []
    else:
        return posts['data']

def get_frompage(fbkey,needed_fb_fields=None):
    if needed_fb_fields is []:
        needed_fb_fields = None
    request_url = 'https://graph.facebook.com/v2.6/587747891351295/posts'
    if needed_fb_fields is not None:
        request_url += '?fields='+ ','.join(needed_fb_fields)
    r = requests.get(request_url,params={'access_token':fbkey})
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
        except:
            out['author_pic'] = None
    else:
        return None
    if 'full_picture' in post:
        out['image'] = post['full_picture']
    else:
        out['image'] = None
    if out['text'] is '' and out['image'] is None:
        return None
    return out

def get(fbkey):
    posts = []
    needed_fb_fields = ["created_time","message","from","full_picture"]
    toposts = get_topage(fbkey,needed_fb_fields)
    fromposts = get_frompage(fbkey,needed_fb_fields)
    toposts = toposts[:7]
    fromposts = fromposts[:7]
    posts += toposts
    posts += fromposts
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
            
