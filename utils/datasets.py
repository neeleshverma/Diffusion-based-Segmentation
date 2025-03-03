import cv2
import torch
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
import blobfile as bf


def _list_image_files_recursively(data_dir):
    results = []
    for entry in sorted(bf.listdir(data_dir)):
        full_path = bf.join(data_dir, entry)
        ext = entry.split(".")[-1]
        if "." in entry and ext.lower() in ["jpg", "jpeg", "png", "gif"]:
            results.append(full_path)
        elif bf.isdir(full_path):
            results.extend(_list_image_files_recursively(full_path))
    return results


def make_transform(resolution: int):
    """ Define input transforms for pretrained models """
    transform = transforms.Compose([
        transforms.Resize(resolution),
        transforms.ToTensor(),
        lambda x: 2 * x - 1
    ])
    return transform


class ImageLabelDataset(Dataset):
    ''' 
    :param data_dir: path to a folder with images and their annotations. 
                     Annotations are supposed to be in *.npy format.
    :param resolution: image and mask output resolution.
    :param num_images: restrict a number of images in the dataset.
    :param transform: image transforms.
    '''
    def __init__(
        self,
        data_dir: str,
        resolution: int,
        num_images= -1,
        transform=None,
    ):
        super().__init__()
        self.resolution = resolution
        self.transform = transform
        self.image_paths = _list_image_files_recursively(data_dir)
        self.image_paths = sorted(self.image_paths)

        if num_images > 0:
            print(f"Take first {num_images} images...")
            self.image_paths = self.image_paths[:num_images]

        self.label_paths = [
            '.'.join(image_path.split('.')[:-1] + ['npy'])
            for image_path in self.image_paths
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load an image
        image_path = self.image_paths[idx]
        pil_image = Image.open(image_path)
        pil_image = pil_image.convert("RGB")
        assert pil_image.size[0] == pil_image.size[1], \
               f"Only square images are supported: ({pil_image.size[0]}, {pil_image.size[1]})"

        tensor_image = self.transform(pil_image)
        # Load a corresponding mask and resize it to (self.resolution, self.resolution)
        label_path = self.label_paths[idx]
        label = np.load(label_path).astype('uint8')
        label = cv2.resize(
            label, (self.resolution, self.resolution), interpolation=cv2.INTER_NEAREST
        )
        tensor_label = torch.from_numpy(label)
        return tensor_image, tensor_label
