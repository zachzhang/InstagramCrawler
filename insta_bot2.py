from InstagramAPI import InstagramAPI
import pandas as pd
import time
import os.path
import numpy as np

class InstaBot():


    def __init__(self,tags, follow_rate, fname = 'users.csv'):

        self.follows_per_day = follow_rate

        self.tags = tags

        self.insta_api = InstagramAPI("mr_falafel_mh", "zachariah36")

        self.insta_api.login()

        new_file = os.path.isfile(fname)
        start_of_feed = os.path.isfile('next_max_id.csv')

        if new_file:
            self.df= pd.read_csv('users.csv',index_col=0)
        else:
            columns = ['FollowBack', 'Following' , 'Tag' , 'Date']
            self.df = pd.DataFrame(columns=columns)

        if start_of_feed:
            self.next_max_id =  pd.read_csv('next_max_id.csv',index_col=0)
            self.next_max_id[pd.isnull(self.next_max_id)] = ''

        else:
            columns = ['next_max_id']
            self.next_max_id = pd.DataFrame(columns=columns)
            for tag in tags:
                self.next_max_id.loc[tag] = ['']

    def createSchedule(self):

        #Strat 1: follow for 16 hours a day and 8 hour rest, rand start

        active_time = 18*60*60

        rest_time = 24*60*60 - active_time

        avg_gap = 18*60*60 / float(self.follows_per_day)

        schedule = [ avg_gap + 10 * np.random.randn()]

        return schedule,rest_time


    def run(self):

        count = 0

        schedule,rest = self.createSchedule()

        for s in schedule:

            for tag in tags:

                self.insta_api.getHashtagFeed( tag, maxid=self.next_max_id.loc[tag])
                media_id = self.insta_api.LastJson

                self.next_max_id.loc[tag] =  media_id['next_max_id']

                #unique users
                user_ids = set([ x["user"]["pk"] for x in media_id["items"]])

                for id in list(user_ids):

                    if id not in self.df.index:

                        print id , count
                        count += 1

                        followed =self.insta_api.follow(id)

                        time.sleep(s)

                        while followed == False:
                            
                            print "Out of Requests - Sleeping"

                            for i in range(8):
                                print 'Sleeping for ',i,' hours'
                                time.sleep(60*60)

                            followed = self.insta_api.follow(id)

                        self.df.loc[id] = [0,1,tag,time.time()]

                self.next_max_id.to_csv('next_max_id.csv', index=True)

            self.df.to_csv("users.csv",index=True)


        self.insta_api.logout()
        time.sleep(rest)
        self.insta_api.login()


    def dump_followers(self,n):

        followers = self.df[ (self.df['Following'] == 1) & ( self.df['Date'] <  (time.time() - 24*60*60*3  ) )]
        followers = list(followers.index)

        for i in range(min(n , len(followers))):

            unfollowed = self.insta_api.unfollow(followers[i])

            time.sleep(20)

    def getUserData(self,user_id):

        start =time.time()

        self.insta_api.getUsernameInfo(user_id)

        print self.insta_api.LastJson
        
        maxid = ''
        more = True


        while more:

            self.insta_api.getUserFeed( user_id, maxid = maxid)

            user_feed = self.insta_api.LastJson


            if 'next_max_id' in user_feed:
                maxid =  user_feed['next_max_id']



        print time.time() - start
        self.df = pd.read_csv('users.csv', index_col=0)



tags =['phone', 'iphone', 'customize' , 'cutephonecase' , 'customphonecase','phonecase',
       'iphonecase', 'case' ,'new' ,'lit','dope','entreprenur','invention','custom','cool',
       'puppy','kitten','cat','dog', 'instamood','iphoneonly','igdaily','follow4follow',
       'basketball','football','baseball','edc','edmlifestyle','edmsf','coachella','rave', 'skrillex','herobust']

ibot = InstaBot(tags,200)

ibot.run()