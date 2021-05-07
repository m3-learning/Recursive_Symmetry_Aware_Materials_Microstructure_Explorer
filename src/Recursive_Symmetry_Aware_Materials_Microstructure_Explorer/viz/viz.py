import matplotlib.pyplot as plt
import numpy as np
from matplotlib import offsetbox
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random


def imscatter(x, y, images, number_images_shown, ax=None, zoom=1.0):
    """
    Function that plots the a 2d scatter plot with superimposed images

    :param x: x-positions
    :param y: y-positions
    :param images: images which are included
    :param number_images_shown: the number of images shown
    :param ax: the axis where the data is plotted
    :param zoom: sets the zoom fraction on the images
    :return:
    """

    if ax is None:
        ax = plt.gca()
    x, y = np.atleast_1d(x, y)
    artists = []

    shown_images = []
    x1 = []
    y1 = []

    r = sorted(random.sample(range(len(images)), number_images_shown))
    for i in r:
        shown_images.append(images[i])
        x1.append(x[i])
        y1.append(y[i])

    for x0, y0, img0 in zip(x1, y1, shown_images):
        im = OffsetImage(
            np.fliplr(np.rot90(img0[:, :, :], k=3)).astype(np.uint8), zoom=zoom)
        ab = AnnotationBbox(
            im, (x0, y0), xycoords='data', frameon=False, pad=0)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


def plot_embedding(X, number_images_shown, size, imgs):
    """
    Function that plots the projection map

    :param X: Sets the position values and ranges
    :param number_images_shown: Selects the number of images to show
    :param size: Chooses the size of the images
    :param imgs: images to plot
    :return:
    """

    # Reset to limit of axes to [0,1]
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = ((X - x_min) / (x_max - x_min)) * size

    plt.figure(figsize=(size, size))
    plt.rcParams['savefig.facecolor'] = "0"
    plt.rcParams['figure.facecolor'] = "1"

    ax = plt.subplot(111, frameon=False)
    # ax.axis("off")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    if hasattr(offsetbox, 'AnnotationBbox'):
        imscatter(X[:, 0], X[:, 1], imgs, number_images_shown, zoom=0.1, ax=ax)

    plt.xlim(np.min(X[:, 0]), np.max(X[:, 0]))
    plt.ylim(np.min(X[:, 1]), np.max(X[:, 1]))

    plt.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.savefig("test1.png", bbox_inches='tight', pad_inches=0, dpi=300)
