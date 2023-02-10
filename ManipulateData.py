import pandas as pd

class MData:

    def __init__(self, gdata):
        self.gdata = gdata
        self.mi = gdata.df
        self.recommendation_dict = {}
        self.manga_record_dict = {}
        self.similarity_matrix = pd.DataFrame()
        self.recommendation = pd.DataFrame()
        self.sorted_recommendation_df = pd.DataFrame()

    # Helper Functions

    def getNSimilarMangas(self, input_manga, n = 50):
        sorted_column = self.similarity_matrix[input_manga].sort_values(ascending = False)
        sorted_column = sorted_column.loc[sorted_column > 0]
        sorted_column = sorted_column[sorted_column.index != input_manga]
        recommendation = sorted_column[0:n]
        self.recommendation = recommendation
        return recommendation

    def sortMangas(self, recommendation = pd.DataFrame(), score = 0, rank = 9999999999999, popularity = 9999999999999):

        if recommendation.empty:
            recommendation = self.recommendation

        rows = list(recommendation.index)

        sorted_recommendation_df = self.mi.loc[rows]

        sorted_recommendation_df = sorted_recommendation_df.loc[(self.mi['score'] >= score) & (self.mi['rank'] <= rank) & (self.mi['popularity'] <= popularity)]

        self.sorted_recommendation_df = sorted_recommendation_df

        return sorted_recommendation_df

    def recordMangaRanks(self, recommendation = pd.DataFrame(), sorted_recommendation_df = pd.DataFrame()):
        if recommendation.empty:
            recommendation = self.recommendation
        if sorted_recommendation_df.empty:
            sorted_recommendation_df = self.sorted_recommendation_df

        scoring_df = recommendation[sorted_recommendation_df.index]
        manga_name = recommendation.name
        if manga_name in self.manga_record_dict:
            return self.manga_record_dict[manga_name]
        else:
            m_dict = {}
            for manga in scoring_df.index:
                m_dict[manga] = scoring_df[manga]
            self.manga_record_dict[manga_name] = m_dict
            return m_dict

    # Main Functions

    def updateRecommendationRanks(self, manga_list, like = True, add = True):
        FLOAT_SIZE = 32
        self.similarity_matrix = self.gdata.getSimilarityMatrix(self.gdata.compare, FLOAT_SIZE, list(set(manga_list)))
        for manga in manga_list:
            if manga in self.manga_record_dict:
                m_dict = self.manga_record_dict[manga]
            else:
                recommendation = self.getNSimilarMangas(manga)
                sorted_recommendation_df = self.sortMangas(recommendation)
                m_dict = self.recordMangaRanks(recommendation, sorted_recommendation_df)

            if (like and add) or (not like and not add):
                for m, score in m_dict.items():
                    self.recommendation_dict[m] = self.recommendation_dict.get(m, 0) + score
            else:
                for m, score in m_dict.items():
                    self.recommendation_dict[m] = self.recommendation_dict.get(m, 0) - score

    def getRecommendation(self):
        recommendation_dict = {key:value for (key, value) in sorted(self.recommendation_dict.items(), key = lambda x: x[1], reverse = True) if value > 0}
        rec = self.mi.loc[(recommendation_dict.keys())]
        return rec