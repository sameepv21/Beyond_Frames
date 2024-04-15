from util.config_parser import configuration
from util.visualizer import visualize

scenegraph_extraction_config = configuration(r"/home/sameep/Extra_Projects/Beyond_Frames/config/scene_graph_extraction.yaml",from_function = True) #create scenegraph extraction config object

if __name__ == "__main__":
    visualize(scenegraph_extraction_config)