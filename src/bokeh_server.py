# Import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import umap.umap_ as umap
from PIL import Image
from matplotlib import offsetbox
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import datetime
# Import packages for Bokeh visualization demo
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, LassoSelectTool, BoxSelectTool, CrosshairTool
from bokeh.models import HoverTool, CustomJS, Div, Button, TextInput
from bokeh.plotting import curdoc, figure, output_file, show
from bokeh.layouts import column, row
from bokeh import events
import sys, getopt


verbose = False

try:
  opts, args = getopt.getopt(sys.argv[1:],"p:v",["path="])
except getopt.GetoptError:
  print('bokeh_serve.py -p <file_path>')
  sys.exit(2)
for opt, arg in opts:
   if opt == ("-v"):
       verbose = True
   elif opt in ("-p", "--path"):
       path = arg
       if verbose:
           print(path)
           print(f'The path is {path}')


# Load the weights, activations, and images
name_all = np.load(f'{path}/Data_name_all.npy')
images = np.load(f'{path}/Data_images.npy')
images = images * 255

im = Image.open(f'{path}/test1.png')
im = im.convert("RGBA")
imarray = np.array(im)
imarray = np.flipud(imarray)
X = np.load(f'{path}/Data_activations.npy')
X_umap = np.load(f'{path}/Data_umap.npy')
x_min1, x_max1 = np.min(X_umap, 0), np.max(X_umap, 0)
X_umap = ((X_umap - x_min1) / (x_max1 - x_min1)) * 15




# Load tooltips for hovering
TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("filename", "@filename"),
    ("umapid", "@umapid"),
]

# Call out data points for the original and recrusvie projection
s1 = ColumnDataSource(data=dict(x=[], y=[], filename=[], umapid=[]))
s2 = ColumnDataSource(data=dict(x=[], y=[], filename=[], umapid=[]))
div = Div(width=400)

# Original projection set up
p1 = figure(plot_width=600, plot_height=600, title="Select Here")
p1.min_border = 0
p1.x_range.range_padding = p1.y_range.range_padding = 0
p1.image_rgba(image=[imarray], x=0, y=0, dw=15, dh=15)
p1.add_tools(LassoSelectTool())
p1.add_tools(BoxSelectTool())
p1.add_tools(CrosshairTool())
cr1 = p1.square('x', 'y', source=s1, fill_color="white", hover_fill_color="firebrick", fill_alpha=0.05,
                hover_alpha=0.3, line_color=None, size=10)  # settings for hovering
p1.add_tools(HoverTool(tooltips=TOOLTIPS, renderers=[cr1]))

# Recursive projection set up
p2 = figure(plot_width=600, plot_height=600, title="Watch Here")
p2.min_border = 0
p2.x_range.range_padding = p2.y_range.range_padding = 0
p2.add_tools(LassoSelectTool())
p2.add_tools(BoxSelectTool())
p2.add_tools(CrosshairTool())

ds = ColumnDataSource(data=dict(image=[]))
p2.image_rgba(image='image', source=ds, x=0, y=0, dw=15, dh=15)

cr2 = p2.square('x', 'y', source=s2, fill_color="white", hover_fill_color="firebrick", fill_alpha=0.1,
                hover_alpha=0.3, line_color=None,
                size=10)  # settings for hovering
p2.add_tools(HoverTool(tooltips=TOOLTIPS, renderers=[cr2]))

# Load UMAP actiations into the original projection
data1 = dict(
    x=[i * 1 for i in X_umap[:, 0]],
    y=[i * 1 for i in X_umap[:, 1]],
    filename=name_all[:],
    umapid=list(range(0, len(X_umap))))
data1 = pd.DataFrame(data1)

data2 = dict(x=[], y=[], filename=[], umapid=[])
data2 = pd.DataFrame(data2)


# Update function
def update(selected=None):
    data = pd.DataFrame(data1)
    s1.data = data
    # s2.data = data


# Plotting function
def imscatter(x, y, images, zoom=1.0, ax=None):
    if ax is None:
        ax = plt.gca()
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0, img0 in zip(x, y, images):
        im = OffsetImage(np.fliplr(np.rot90(img0[:, :, :], k=3)).astype(np.uint32), zoom=zoom)
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


def plot_embedding(X, imgs, name_file):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = ((X - x_min) / (x_max - x_min)) * 15

    plt.figure(figsize=(15, 15))
    plt.rcParams['savefig.facecolor'] = "0"

    ax = plt.subplot(111, frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    if hasattr(offsetbox, 'AnnotationBbox'):
        imscatter(X[:, 0], X[:, 1], imgs, zoom=0.1, ax=ax)

    plt.xlim(np.min(X[:, 0]), np.max(X[:, 0]))
    plt.ylim(np.min(X[:, 1]), np.max(X[:, 1]))
    plt.tight_layout(pad=0, h_pad=0, w_pad=0)

    plt.savefig(name_file, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close()


# Selection change function for the original projection
# Trigger a list of names when selecting a new area
# Also generate a new UMAP on the rerusive projection based on the selection.

def selection_change(attrname, old, new):
    selected = s1.selected.indices

    name = []
    idx_new = []
    X_new = []
    name_all_new = []
    X_umap_new = []
    images_new = []

    for i in sorted(selected):
        name_all_new.append(name_all[i])
        X_new.append(X[i])
        idx_new.append(i)
        images_new.append(images[i])
        name.append("Index: " + str(i) + " Name: " + ' {} '.format(data1["filename"][i]) + " <p> <p>")

    div.text = "Selection! <p> <p>" + str(name).strip('[]')

    np.random.seed(42)
    X_umap_new = umap.UMAP(n_neighbors=5, min_dist=0.3, n_components=2, metric='correlation').fit_transform(X_new)
    title = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(":", "") + ".png"

    plot_embedding(X_umap_new, images_new, title)

    im2 = Image.open(title)
    im2 = im2.convert("RGBA")
    imarray2 = np.array(im2)
    imarray2 = np.flipud(imarray2)

    ds.data = dict(image=[imarray2])
    x_min, x_max = np.min(X_umap_new, 0), np.max(X_umap_new, 0)
    X_umap_new = ((X_umap_new - x_min) / (x_max - x_min)) * 15

    data2 = dict(
        x=X_umap_new[:, 0][:],
        y=X_umap_new[:, 1][:],
        filename=name_all_new[:],
        umapid=idx_new[:])

    data2 = pd.DataFrame(data2)
    s2.data = data2


s1.selected.on_change('indices', selection_change)


# Selection change function for the recursive projection
# Trigger a list of names when selecting a new area

def selection_change_2(attrname, old, new):
    selected2 = s2.selected.indices

    name = []

    for i in sorted(selected2):
        name.append("Index: " + str(i) + " Name: " + ' {} '.format(s2.data["filename"][i]) + " <p> <p>")

    div.text = "Selection! <p> <p>" + str(name).strip('[]')


s2.selected.on_change('indices', selection_change_2)

text = TextInput(title="Title", value='Watch Here')


# Update title
def update_title(attrname, old, new):
    p2.title.text = text.value


text.on_change('value', update_title)

button = Button(label="Reset", width=300, button_type="success")  # Reset button

button.js_on_event(events.ButtonClick, CustomJS(args=dict(div=div), code="""
div.text = "Reset!";
"""))

# Setting up the layout: original projection, recurisve projection, and metadata viewer
layout = column(button, row(p1, p2, column(text, div)))

update()

curdoc().add_root(layout)
curdoc().title = "UMAP"