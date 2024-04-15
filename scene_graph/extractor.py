from abc import ABC
from .relation_extractor import RelationExtractor


'''
This class defines the abstract base class of scene-graph extractors. scene-graph extractors can extract data from many different formats to generate SceneGraphDatasets.
'''
class Extractor(ABC):
    def __init__(self, config):
        self.conf = config
        self.dataset_type = self.conf.dataset_type
        self.scene_graphs = {}
        self.relation_extractor = RelationExtractor(config)
        self.framenum = self.conf.relation_extraction_settings["frames_limit"]
        