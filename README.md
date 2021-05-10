# Recursive_Symmetry_Aware_Materials_Microstructure_Explorer

# Installation

To install use `pip install Recursive_Symmetry_Aware_Materials_Microstructure_Explorer`

It is recommended that you install the package on a new conda env
1. `conda create -name bokeh`
2. `conda install -c anaconda ipykernel`
3. `python -m ipykernel install --user --name=bokeh`
4. `conda activate bokeh`
5. `pip install Recursive_Symmetry_Aware_Materials_Microstructure_Explorer`

# Examples

We include one example of this package.

Within the repositiory download the two files in the `Examples` folder: 

`Example_Image_Scraping_and_Collating.ipynb` - This is a notebook that scrapes images from google, this also has the code
to collate the images from the folders. 

`bokeh_server.py` - This contains the script for the graphical user interface.

To spin up a server, 

`bokeh serve bokeh_server.py --args -p path`

The Bokeh demo will be served at the local host: http://localhost:5006/bokeh_server
