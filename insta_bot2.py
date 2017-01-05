from InstagramAPI import InstagramAPI
import pandas as pd
import time
import os.path

class InstaBot():


    def __init__(self,fname = 'users.csv'):

        #InstagramAPI = InstagramAPI("zach_zhang5", "zachariah36")
        self.insta_api = InstagramAPI("mr_falafell", "zachariah36")

        self.insta_api.login()

        self.all_ids = []

        new_file = os.path.isfile(fname)

        if new_file:
            self.df= pd.read_csv('users.csv',index_col=0)
        else:
            columns = ['FollowBack','Tag','Date']
            self.df = pd.DataFrame(columns=columns)


    def run(self,tags):

        next_max_id =   dict([ ( tag,'') for tag in tags])

        count = 0

        while True:


            for tag in tags:

                self.insta_api.getHashtagFeed( tag, maxid=next_max_id[tag])
                media_id = self.insta_api.LastJson

                next_max_id[tag] =  media_id['next_max_id']

                #unique users
                user_ids = set([ x["user"]["pk"] for x in media_id["items"]])

                for id in list(user_ids):
                    if id not in self.df.index:

                        print id , count
                        count += 1
                        self.insta_api.follow(id)
                        self.insta_api.unfollow(id)

                        self.df.loc[id] = [0,tag,time.time()]


            self.df.to_csv("users.csv",index=True)

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



    def searchArea(self,location):

        columns = [ 'Date']
        self.mh_users = pd.DataFrame(columns=columns)


        self.insta_api.searchLocation( location[0])

        loc_id  = [self.insta_api.LastJson['items'][0]['location']['facebook_places_id'] ]

        next_max_id =   dict([ ( loc,'') for loc in loc_id])

        count = 0

        while True:

            for loc in loc_id:

                self.insta_api.getLocationFeed( loc, maxid=next_max_id[loc])
                media_id = self.insta_api.LastJson

                next_max_id[loc] =  media_id['next_max_id']

                user_ids = set([x["user"]["pk"] for x in media_id["items"]])

                for id in list(user_ids):
                    if id not in self.df.index:
                        print id , count, media_id['more_available']
                        count +=1
                        self.mh_users.loc[id] = [time.time()]

            self.mh_users.to_csv("mh_users.csv",index=True)

tags = ['falafel']

ibot = InstaBot()

#ibot.searchArea(['Morgan Hill, California'])
#ibot.run(tags)

users =  pd.read_csv('users.csv')

u_ids = users.iloc[:,0].values

print ibot.getUserData(u_ids[0])


users = pd.read_csv('users.csv')

print ibot.shape, ibot.keys()


'''

    #print u_ids
#print media_id["ranked_items"]



InstagramAPI.searchUsername('maximillionz')

test= InstagramAPI.LastJson

#InstagramAPI.getUserTags(test['user']['pk'])

#test2 = InstagramAPI.LastJson

InstagramAPI.getTotalUserFeed(test['user']['pk'])

test2 = InstagramAPI.LastJson

print test2.keys()
print len(test2['items'])
print test2['items'][0].keys()
print test2['items'][0]['caption']

#print test2.keys()
#print test2['items'][0].keys()

#print len(test2['items'])

#print test2['items'][0]['usertags']

#print test2['items'][0]
#InstagramAPI.getUsernameInfo( 'maximillionz')

#test2= InstagramAPI.LastJson

#print test['user']['pk']

#InstagramAPI.follow(test['user']['pk'])

#print test.keys()
#print test['users']



'''
