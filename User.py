
class User:

    def __init__(self, username, mdata):
        self.mdata = mdata
        self.username = username
        self.like_list = set()
        self.dislike_list = set()
        self.complete_list = []
    
    def updateList(self, manga_list, like = True, add = True):
        if like:
            if add:
                self.like_list.update(manga_list)
            else:
                self.like_list.difference(manga_list)
        else:
            if add:
                self.dislike_list.update(manga_list)
            else:
                self.dislike_list.difference(manga_list)
        self.mdata.updateRecommendationRanks(manga_list, add)

    def getCompleteList(self):
        self.complete_list = list(self.like_list | self.dislike_list)
        return self.complete_list

    def getRecommendation(self):
        return self.mdata.getRecommendation()
    