import threading
import pickle

location_cache = {}
location_cache_lock = threading.Lock()


def save_location_cache(cache):
    with open('location_cache_file.pkl', 'wb') as file:
        pickle.dump(cache, file)


def load_location_cache():
    try:
        with open('location_cache_file.pkl', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return {}
