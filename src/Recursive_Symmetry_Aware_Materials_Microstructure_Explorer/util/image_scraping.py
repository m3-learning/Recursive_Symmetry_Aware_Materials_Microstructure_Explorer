def download_images_from_google(names, path, num=25, verbose=True):
    """
    Tool to download files from google image search based on search criteria

    :param names: list of strings to search
    :param path: path where files will be saved
    :param num: number of images to download in each catagory
    :param verbose: True makes the function print intermediate actions
    :return:
    """
    # instantiation of the class to download images
    response = google_images_download.googleimagesdownload()

    # converts the list to a string
    names = ''.join(str(i + ',') for i in names)

    # creating list of arguments
    arguments = ({"keywords": names,
                  "limit": num, "print_urls": verbose,
                  "output_directory": path})

    # passing the arguments to the function
    paths = response.download(arguments)
