#!/usr/bin/env python

import json
import sys
import tweepy

def fatal_error(message):
    sys.stderr.write("FATAL ERROR: " + message)
    sys.stderr.flush()
    sys.exit(1)

def initialize_api_with_credentials_file(filename):
    try:
        with open(filename, 'r') as fp:
            credentials = json.load(fp)
        auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        api = tweepy.API(auth)
        if api.verify_credentials() is False:
            fatal_error("Invalid credentials")
    except IOError as ioe: # from open
        fatal_error("Could not read file {}: {}\n".format(filename, ioe.strerror))
    except json.JSONDecodeError: # from json.load
        fatal_error("Could not deserialize file {}\n".format(filename))
    except KeyError as ke: # from credentials
        fatal_error("Required key {} absent from {}\n".format(ke.args[0], filename))
    except tweepy.TweepError as te: # from verify_credentials
        fatal_error("Test connection to Twitter failed with code {}: {}".format(te.code, te.message))
    
    return api

def about_me(api):
    try:
        user = api.me()
        print("")
        print("About you")
        print("---------")
        print("Id:", user.id)
        print("Name:", user.name)
        print("Screen name:", user.screen_name)
        print("Description:", user.description)
        print("Location:", user.location)
        print("No. friends:", user.friends_count)
        print("No. followers:", user.followers_count)
    except tweepy.TweepError as te:
        print("Attempt to find info about you failed: {}".format(te.message))
    except tweepy.RateLimitError:
        print("Slow down! You're sending too many requests.")


def search_tweets(api):
    while True:
        query = input("Enter query here: (q to quit) ")
        if query == 'q':
            return
        else:
            try:
                search_results = api.search(query)
            except tweepy.TweepError as te:
                print("Query failed with code {}: {}".format(te.code, te.message))
            for search_result in search_results:
                print("Time:", search_result._json['created_at'])
                print("Name:", search_result._json['user']['screen_name'])
                print("Location:", search_result._json['user']['location'])
                print(search_result._json['text'])
                print("")
def main():
    if (len(sys.argv) < 2):
        fatal_error("usage: {} <credentials_filename>\n".format(sys.argv[0]))
    else:
        api = initialize_api_with_credentials_file(sys.argv[1])       
    print("")
    print("-----------------------------------------")
    print("              TWITTERSTUFF               ")
    print("-----------------------------------------")
    print("")
    print("Welcome to TwitterStuff.")
    while True:
        print("")
        print("Select an option (q to quit):")
        print("1: about me")
        print("2: search tweets")
        response = input("Enter here: ")
        while True:
            if response == '1':
                about_me(api)
                break
            elif response == '2':
                search_tweets(api)
                break
            elif response == 'q':
                sys.exit(0)
            else:
                response = input("Incorrect option: please try again: ")      

if __name__ == "__main__":
    main()
