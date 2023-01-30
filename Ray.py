import pandas as pd
import ray
import os
import re
from mal import Manga, Anime
from Threading import Threading
from Wordlist import view_list

@ray.remote
class Supervisor:

    def __init__(self, batch_size = 1000):
        self.batch_size = batch_size
        self.workers = [Worker.remote() for _ in range(os.cpu_count())]

    def getNonExistantManga(self):
        return self.nonexistant_manga_id

    def getMangas(self):
        self.manga_stats = {}
        self.nonexistant_manga_id = []
        outputs = []
        batches = int(600000 / self.batch_size)
        for index in range(batches):
            start = (self.batch_size * index)
            end = (self.batch_size * (index+1))
            outputs.append(self.workers[index % len(self.workers)].getMangas.remote(start, end))
        output = ray.get(outputs)
        for result in output:
            self.manga_stats.update(result['dict'])
            self.nonexistant_manga_id += result['list']
        return self.manga_stats


@ray.remote
class Worker:

    def __init__(self):
        pass

    def getMangas(self, start, end):
        print(str(start) + '-' + str(end))
        self.manga_stats = {}
        self.nonexistant_manga_id = []
        Threading.thread(self.getManga, range(start, end))
        return {'dict':self.manga_stats, 'list':self.nonexistant_manga_id}

    def getManga(self, manga_id):
        dictionary = {}
        try:
            manga = Manga(manga_id)
        except:
            self.nonexistant_manga_id.append(manga_id)
            return
        for v in view_list:
            data = getattr(manga, v)
            if type(data) == type([]):
                data = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in data]
                data = ' '.join(data)
            elif type(data) == type({}):
                list = []
                for name_list in data.values():
                    for name in name_list:
                        list.append(name)
                data = ' |*| '.join(list)
            dictionary[v] = data
        self.manga_stats[manga.title] = dictionary