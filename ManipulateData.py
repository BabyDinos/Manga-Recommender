import pandas as pd

class MData:

    def __init__(self, manga_info, similarity_matrix):
        self.mi = manga_info
        self.recommendation_dict = {}
        self.manga_record_dict = {}
        self.similarity_matrix = similarity_matrix
        self.recommendation = pd.DataFrame()
        self.sorted_recommendation_df = pd.DataFrame()

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

    def updateRecommendationRanks(self, manga, add = True):
        if manga in self.manga_record_dict:
            m_dict = self.manga_record_dict[manga]
        else:
            recommendation = self.getNSimilarMangas(manga)
            sorted_recommendation_df = self.sortMangas(recommendation)
            m_dict = self.recordMangaRanks(recommendation, sorted_recommendation_df)

        if add:
            for m, score in m_dict.items():
                self.recommendation_dict[m] = self.recommendation_dict.get(m, 0) + score
        else:
            for m, score in m_dict.items():
                self.recommendation_dict[m] = self.recommendation_dict.get(m, 0) - score

    def getRecommendation(self):
        self.recommendation_dict = {key:value for (key, value) in sorted(self.recommendation_dict.items(), key = lambda x: x[1], reverse = True)}
        rec = self.mi.loc[(self.recommendation_dict.keys())]
        return rec