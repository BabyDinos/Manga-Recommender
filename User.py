
class User:

    def __init__(self, username, mdata):
        self.mdata = mdata
        self.username = username
        self.like_list = []
        self.dislike_list = []
        self.complete_list = self.updateCompleteList()
    
    def updateCompleteList(self):
        self.complete_list = [list(set(self.like_list)) + list(set(self.dislike_list))]

    