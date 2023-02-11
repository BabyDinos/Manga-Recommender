from Ray import Supervisor
import ray
import pandas as pd
class DownloadData:

    def __init__ (self):
        pass

    def downloadMangaDataframe(self):
        '''
        Download alot of Mangas
        '''
        supervisor = Supervisor.remote()
        manga_stats = ray.get(supervisor.getMangas.remote())

        self.df = pd.DataFrame(manga_stats).T
        return self.df