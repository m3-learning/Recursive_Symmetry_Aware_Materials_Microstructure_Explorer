from torch.utils.data import Dataset
from fnmatch import fnmatch
import os
from PIL import Image
import random
import torchvision.transforms as transforms


def image_collection(path, pattern="*.jpg"):
    """
    Tool to search folders for image files to project.

    :param path: sets the path where to search for images
    :param pattern: sets the pattern to search for. Can use wildcards
    :return:
    """

    # Create a directory of all file paths
    dir_jpg = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, pattern):
                file_path = os.path.normpath(os.path.join(path, name))
                dir_jpg.append(file_path)
    dir_jpg.sort()

    # saves images as a numpy array
    images_ = []
    for i in range(len(dir_jpg)):
        im = Image.open(dir_jpg[i])
        images_.append(im)

    dir_name = []
    name_all = []
    for ind, name in enumerate(dir_jpg):
        path, name = os.path.split(dir_jpg[ind])
        name = name.split('/')[-1][:-4].lower()
        dir_name.append(name[:2])
        name_all.append(name)

    return images_, dir_jpg, name_all, dir_name


class image_dataset(Dataset):
    """
    Builds a Pytorch Dataset
    """

    def __init__(self, images, transform=None, viz=transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
    ])):
        '''
        Initialization

        :param images: input images
        :param transform: transformation to be applied on evaluation
        :param viz: transformation to be applied on visualization
        '''

        self.images = images
        self.transform = transform
        self.viz_trans = viz

    def __len__(self):
        """
        Denotes the total number of samples

        :return:
        """

        return len(self.images)

    def __getitem__(self, index):
        """
        Generates one sample of data

        :param index: Index that is selected
        :return:
        """

        # Select sample
        image = self.images[index].convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image

    def __getitemviz__(self, index):
        """
        Generates one sample for visualization

        :param index: Index to show
        :return:
        """

        # Select sample
        image = self.images[index].convert('RGB')

        image = self.viz_trans(image)

        return image
