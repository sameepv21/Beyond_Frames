import random
import os
from pathlib import Path
from tqdm import tqdm
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from util.config_parser import configuration
from roadscene2vec.scene_graph.scene_graph import SceneGraph
from roadscene2vec.scene_graph.extraction.image_extractor import RealExtractor
from roadscene2vec.scene_graph.extraction.carla_extractor import CarlaExtractor
from roadscene2vec.data.dataset import RawImageDataset
from networkx.drawing import nx_agraph, nx_pydot
from glob import glob
import json
import pickle
with open('../pickle_dump/temp.pkl', 'rb') as file:
    data = pickle.load(file)
def get_extractor(config):
    return RealExtractor(config)

def get_bbox(extractor, frame):
    return extractor.get_bounding_boxes(frame)

def get_bev(extractor):
    return extractor.bev

def get_scenegraph(extractor, bbox, bev):
    scenegraph = SceneGraph(extractor.relation_extractor,
                            bounding_boxes=bbox,
                            bev=bev,
                            coco_class_names=extractor.coco_class_names,
                            platform=extractor.dataset_type)
    return scenegraph.g

def draw(extractor, frame, bbox, bev, sg, save_path=None):
    plt.figure(figsize=(10, 5))
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Assume frame is in BGR format
    plt.axis('off')
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    plt.close()

def visualize_real_image(extraction_config, num_samples=15):
    extractor = get_extractor(extraction_config)
    dataset_dir = extractor.conf.location_data["input_path"]
    print("Dataset directory:", dataset_dir)
    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"The dataset directory {dataset_dir} was not found.")

    all_sequence_dirs = [x for x in Path(dataset_dir).iterdir() if x.is_dir()]
    if len(all_sequence_dirs) < num_samples:
        raise ValueError("There are fewer directories available than the number of samples requested.")

    selected_dirs = random.sample(all_sequence_dirs, num_samples)  # Randomly sample directories

    for path in tqdm(selected_dirs):
        sequence = extractor.load_images(path)
        if sequence:
            frame_key = random.choice(list(sequence.keys()))  # Randomly pick one frame to process
            bbox = get_bbox(extractor, sequence[frame_key])
            bev = get_bev(extractor)
            sg = get_scenegraph(extractor, bbox, bev)
            output_filename = f"output_{path.stem}_{frame_key}.png"  # Unique save path for each image
            draw(extractor, sequence[frame_key], bbox, bev, sg, save_path=output_filename)

    print('Visualization completed.')

if __name__ == "__main__":
    scenegraph_extraction_config = configuration(r"examples/use_case_1_scenegraph_extraction_config.yaml", from_function=True)
    visualize_real_image(scenegraph_extraction_config)
