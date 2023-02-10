
class User:

    def __init__(self, username, mdata):
        self.mdata = mdata
        self.username = username
        self.like_list = []
        self.neutral_list = []
        self.dislike_list = []
        self.complete_list = []
    
    def updateRecommendationRanks(self, manga_list, like = True, add = True):
        self.mdata.updateRecommendationRanks(manga_list, like, add)

    def updateList(self, ld_dictionary):
        self.like_list = [manga for (manga, value) in ld_dictionary.items() if value == 1]
        self.neutral_list = [manga for (manga, value) in ld_dictionary.items() if value == 0]
        self.dislike_list = [manga for (manga, value) in ld_dictionary.items() if value == -1]

    def getCompleteList(self):
        self.complete_list = self.like_list + self.neutral_list + self.dislike_list
        return self.complete_list

    def getRecommendation(self):
        return self.mdata.getRecommendation()
    