from concurrent.futures import ThreadPoolExecutor
from threading import Thread

class Threading:

    @staticmethod
    def thread(func, *args):
        with ThreadPoolExecutor() as executor:
            results = executor.map(func, *args)
