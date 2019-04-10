#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from nltk.corpus import stopwords

import collections
import twitter
import operator
import os

def word_counter(text, language = 'spanish'):
    
    if(type(text) is not str or type(language) is not str):
        raise(TypeError)
        
    punctuation_marks = ["?", "¿", "¡", "!", " ", ",", ".", ";", ":","/"]
    
    filtred_text = ""
    
    for letter in text:
        if(letter not in punctuation_marks):
            filtred_text = filtred_text + letter
        else:
            filtred_text = filtred_text + " "
        
    filtred_text = filtred_text.lower().split()
    stop_words = set(stopwords.words(language))
    
    result_words = []
    trash_items = ["https","\\t","co"]
    
    for word in filtred_text:
        if(word not in stop_words and word not in trash_items):
            result_words.append(word)
    
    if(len(result_words) == 0):
        return None
    
    return collections.Counter(result_words)
 
        
class twitter_word_counter(object):
    
    def __init__(self,twitter_api,username):
        self.twitter_api = twitter_api
        self.username = username
    
    def get_last_50_tweets(self):
        
        try:
            tweets = self.twitter_api.GetUserTimeline(screen_name = self.username,count = 400, include_rts=False)
        except: 
            return []
        tweets_text = []
        max_tweets = 50
        for i in range(0,len(tweets)):
            if(i is max_tweets):
                break
            tweets_text.append(tweets[i].text)
            
        return tweets_text
    
    def parse_list_tweets_to_string(self,tweets_list):
        
        if(type(tweets_list) is not list):
            raise(TypeError)
            
        tweets_string = ""
        for tweet in tweets_list:
            tweets_string = tweets_string + " " + tweet
        
        return tweets_string
    
    def top_20_repetitive_word_counter(self):
        tweets_text = self.get_last_50_tweets() 

        if(len(tweets_text) is 0):
            return None
        tweets_text = self.parse_list_tweets_to_string(tweets_text)
        values = word_counter(tweets_text)
        
        sorted_list = sorted(values.items(), key=operator.itemgetter(1))
        sorted_list.reverse()
        
        top_20_values = []
        stop_counter_condition = 0
        for i in range(0,len(sorted_list)):
            if(stop_counter_condition==20):
                break
            top_20_values.append(sorted_list[i]) 
            stop_counter_condition += 1 
            
        return top_20_values


def run():
    """Entry point for console_scripts
    """

if __name__ == "__main__":
    
    api = twitter.Api('gz2EucWLrJHTX2GjuMFxYN2la','e0vmSGeIlnHWbVGPO2YbfiPMUiZXh9DQDBML2fu0tqOoqylUXx','1115702759888523265-bbLQl3rRdu9beHs1UoyRXUZZfkqWv6','EttVVAmzpgvd6wnSO596xUIEzL7zGmqptXUQm6D2IACKS')
    modelo = twitter_word_counter(api, 'manolocabezabolo')
    hola = modelo.top_20_repetitive_word_counter()
    print(hola)
    run()
