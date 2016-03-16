# Copyright (c) 2016 Blaque Allen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
########################################
import tweepy, os, sys, time
from random import randint
from time import gmtime, strftime
from login import *

logfile = strftime("%b_%d.log")
########################################

class TwitterAPI:
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
  
    def log(self, message):
        path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(path, logfile), 'a+') as f:
            t = strftime("%d %b %Y %H:%M:%S", gmtime())
            f.write("\n" + t + " | " + message)    

################ Tweets ################

    def tweet(self, tweetFile):
        filename = open(tweetFile,'r')
        f = filename.readlines()
        filename.close()

        for line in f:
            try:
                self.api.update_status(status=line)
            except tweepy.error.TweepError as e:
                self.log(e.message)
            else:
                self.log("Tweeted: " + line)
                #time.sleep(3600)

    def groupTweet(self, handleFile, bulktweetFile):
        handles = open(handleFile, 'r')
        h = handles.readlines()
        handles.close()
        
        bulktweet = open(bulktweetFile,'r')
        t = bulktweet.readlines()
        bulktweet.close()

        for handle in h:
            handle = handle.rstrip()
            m = handle + " " + ", ".join(t)   
            try:
                self.api.update_status(status=m)
                nap = randint(1, 20)
                time.sleep(nap)
            except tweepy.error.TweepError as e:
                self.log(e.message)
            else:
                self.log("Tweeted: " + m)

    def picTweet(self, imagePath, status):
        try:
            self.api.update_with_media(imagePath, status)
        except tweepy.error.TweepError as e:
            self.log(e.message)
        else:
            self.log("Tweeted: " + imagePath + " " + status)

################ Users #################

    def followUser(self, user):
        try:
            self.api.create_friendship(user)
        except tweepy.error.TweepError as e:
                self.log(e.message)
        else:
            self.log("Followed: " + user)

    def unfollowUser(self, user):
        try:
            self.api.destroy_friendship(user)
        except tweepy.error.TweepError as e:
                self.log(e.message)
        else:
            self.log("Unfollowed: " + user)

    def autoFollow(self):
        for follower in tweepy.Cursor(self.api.followers).items(): 
            try:
                follower.follow()
            except tweepy.error.TweepError as e:
                    self.log(e.message)
            else:
                self.log("Auto-Followed: " + follower.screen_name)

    def autoUnfollow(self):
        followers = self.api.followers_ids(SCREEN_NAME)
        friends = self.api.friends_ids(SCREEN_NAME)


        for friend in friends:
            if friend not in followers: 
                try:
                    self.api.destroy_friendship(friend)
                except tweepy.error.TweepError as e:
                        self.log(e.message)
                else:
                    friend = str(friend)
                    self.log("Auto-Unfollowed: " + friend)

    #def welcomeFollow(self):

########################################

if __name__ == "__main__":
    Twitter = TwitterAPI()
    
    while True:
        os.system('clear')
        print (30 * '-')
        print ("   TwitterBot - Menu")
        print (30 * '-')
        print ("1. Auto-Tweeter")
        print ("2. Group Auto-Tweeter")
        print ("3. Image Tweet")
        print ("4. Auto-Follower")
        print ("5. Auto-UnFollower")
        print ("6. Follow Specific User...")
        print ("7. Unfollow Specific User...")
        print ("8. Edit files...")
        print ("9. Shutdown")
        print (30 * '-')
         
        choice = raw_input('Enter your choice [1-9]:  ')
        choice = int(choice)
        print ("\n")

        if choice == 1:
                print ("Starting Auto-Tweeter...")
                Twitter.tweet("Tweets.txt")
        elif choice == 2:
                print ("Starting Group Auto-Tweeter...")
                Twitter.groupTweet("Handles.txt", "BulkTweets.txt")
        elif choice == 3:
                print ("Starting Image Tweet...")
                choice = raw_input('Enter ImagePath: ')
                choice1 = raw_input('Enter Tweet Text: ')
                Twitter.picTweet(choice, choice1)
        elif choice == 4:
                print ("Starting Auto-Follower...")
                Twitter.autoFollow()
        elif choice == 5:
                print ("Starting Auto-Unfollower...")
                Twitter.autoUnfollow()
        elif choice == 6:
                print ("Follow Specific User...")
                choice = raw_input('Enter username: ')
                Twitter.followUser(choice)
        elif choice == 7:
                print ("Unfollow Specific User...")
                choice = raw_input('Enter username: ')
                Twitter.unfollowUser(choice)
        elif choice == 8:
                print (30 * '-')
                print ("   Edit Files - Menu")
                print (30 * '-')
                print ("1. Modify Tweets.txt")
                print ("2. Modify BulkTweets.txt")
                print ("3. Modify Handles.txt")
                print ("4. Modify Login")
                print (30 * '-')
                choice = raw_input('Enter your choice [1-4]:  ')
                choice = int(choice)

                if choice == 1:
                    os.system('nano Tweets.txt')
                elif choice == 2:
                    os.system('nano BulkTweets.txt')
                elif choice == 3:
                    os.system('nano Handles.txt')
                elif choice == 4:
                    os.system('nano login.py')
                else:
                    print ("Invalid number. Try again...")    
        elif choice == 9:
                break
        else:    
                print ("Invalid number. Try again...")