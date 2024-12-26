from icecream import ic
from scout.dataset import DatasetLoader


def test_dataset_loader():
    dataset_path = "test_datasets/coco5"

    dataset_loader = DatasetLoader(source=dataset_path)
    images = dataset_loader.load_images()

    ic(images)
