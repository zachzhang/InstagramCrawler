from InstagramAPI import InstagramAPI
import pandas as pd
import time
import os.path

class InstaBot():


    def __init__(self,fname = 'users.csv'):

        #InstagramAPI = InstagramAPI("zach_zhang5", "zachariah36")
        self.insta_api = InstagramAPI("zachzhang36", "zachariah36")

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

        for i in range(2):
        #while True:

            for tag in tags:

                print tag

                self.insta_api.getHashtagFeed( tag, maxid=next_max_id[tag])
                media_id = self.insta_api.LastJson

                next_max_id[tag] =  media_id['next_max_id']

                #unique users
                user_ids = set([ x["user"]["pk"] for x in media_id["items"]])

                for id in list(user_ids)[0:4]:
                    if id not in self.df.index:

                        print id
                        self.insta_api.follow(id)
                        #self.insta_api.unfollow(id)

                        self.df.loc[id] = [0,tag,time.time()]

            self.df.to_csv("users.csv",index=True)

    def searchArea(self,location):

        columns = [ 'Date']
        self.mh_users = pd.DataFrame(columns=columns)


        self.insta_api.searchLocation( location[0])

        loc_id  = [self.insta_api.LastJson['items'][0]['location']['facebook_places_id'] ]

        next_max_id =   dict([ ( loc,'') for loc in loc_id])

        for i in range(20):

            for loc in loc_id:

                self.insta_api.getLocationFeed( loc, maxid=next_max_id[loc])
                media_id = self.insta_api.LastJson

                next_max_id[loc] =  media_id['next_max_id']

                user_ids = set([x["user"]["pk"] for x in media_id["items"]])

                for id in list(user_ids):
                    if id not in self.df.index:
                        print id
                        self.mh_users.loc[id] = [time.time()]

            self.mh_users.to_csv("mh_users",index=True)

tags = ['photography','design','sketch','designercon','sketchaday']
ibot = InstaBot()

ibot.searchArea(['Morgan Hill, California'])
#ibot.run(tags)

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