from enum import Enum, auto
from osbot_utils.utils.Str import safe_str
from osbot_utils.helpers.Local_Cache import Local_Cache

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mgraph.MGraph import MGraph


class Serialization_Mode(Enum):
    JSON    = auto()
    PICKLE  = auto()

class MGraph__Serializer(Kwargs_To_Self):

    caches_name : str                = 'mgraph_tests'
    mode        : Serialization_Mode = Serialization_Mode.PICKLE

    local_cache : Local_Cache                                           # todo, refactor this into an MGraph__Storage__Disk class
    key         : str
    mgraph      : MGraph

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key         = safe_str(f'serialiser_for__{self.mgraph.key}')

        self.local_cache = Local_Cache(cache_name=self.key, caches_name=self.caches_name)


    def save(self):
        if self.mode == Serialization_Mode.JSON:
            return self.save_to_json()
        if self.mode == Serialization_Mode.PICKLE:
            return self.save_to_pickle()

    def save_to_json(self):
        graph_data = self.mgraph.data().graph_data()
        #pprint(graph_data)
        self.local_cache.set('graph_data', graph_data)
        return True

    def save_to_pickle(self):
        #obj_info(self.local_cache)
        return '...pickle save - to be implemented...'
