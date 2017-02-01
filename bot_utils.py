def postImg(self, fn):
    self.insta_api.uploadPhoto(fn)


def searchArea(self, location):
    columns = ['Date']
    self.mh_users = pd.DataFrame(columns=columns)

    self.insta_api.searchLocation(location[0])

    loc_id = [self.insta_api.LastJson['items'][0]['location']['facebook_places_id']]

    next_max_id = dict([(loc, '') for loc in loc_id])

    count = 0

    while True:

        for loc in loc_id:

            self.insta_api.getLocationFeed(loc, maxid=next_max_id[loc])
            media_id = self.insta_api.LastJson

            next_max_id[loc] = media_id['next_max_id']

            user_ids = set([x["user"]["pk"] for x in media_id["items"]])

            for id in list(user_ids):
                if id not in self.df.index:
                    print id, count, media_id['more_available']
                    count += 1
                    self.mh_users.loc[id] = [time.time()]

        self.mh_users.to_csv("mh_users.csv", index=True)
