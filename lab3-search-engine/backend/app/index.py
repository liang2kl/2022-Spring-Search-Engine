#import the necessary packages
import argparse
import glob
import json
import cv2
from database import db_session, init_db
from models.image import Image
from utils import ColorDescriptor, chi2_distance, get_prominant_colors

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help = "path to the directory that contains the images to be indexed")
args = vars(ap.parse_args())

# initialize database
init_db()

#initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

#open the output index file for writing
types = ('/*.jpg', '/*.png', '/*.gif') # the tuple of file types
files_grabbed = []
for files in types:
    files_grabbed.extend(glob.glob(args["dataset"]+files))

#use glob to grab the image paths and loop over them
for imagePath in files_grabbed:
    try:
    #extract the imageID from the image
        #path and load the image itself
        imageID = imagePath[imagePath.rfind("/")+1:]
        image = cv2.imread(imagePath)

        #describe the image
        features = cd.describe(image)

        #write the features to file
        stored_str = "%s" % (",".join([str(f) for f in features]))

        height, width, _ = image.shape

        existing_row = db_session.query(Image.file_name).filter_by(file_name=imageID).first()
        if existing_row is None:
            d = chi2_distance(features, None)
            colors = get_prominant_colors(image)
            color_json = json.dumps(colors)
            # prominant_color = ",".join([str(c) for c in colors[0][1]])
            model = Image(file_name=imageID, features=stored_str,
                          width=width, height=height, distance=d,
                          colors=color_json)
            db_session.add(model)
            db_session.commit()

            print("%s has been indexed" % imageID)
    
    except Exception as e:
        print(e)

# close the session
db_session.remove()