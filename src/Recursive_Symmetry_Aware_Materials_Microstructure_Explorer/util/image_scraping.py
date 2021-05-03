from google_images_download import google_images_download

def download_images_from_google(names, path, num=25, verbose=True):

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