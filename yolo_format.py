import os
import pandas as pd
import json 
import shutil 

def get_images(file_dir):
  # get the names of folders containing the images
  img_folders = os.listdir(file_dir)
  # create a new folder in the same directory to store all extracted images
  final_folder = os.path.join(file_dir, "images")

  try:
    os.mkdir(final_folder)
  except FileExistsError:
    pass

  for folder in img_folders:
    if (folder.endswith(".MP4") == False):
        continue
    # get the name of the video each folder's images belong to
    video = folder.removesuffix(".MP4")
    # get the names of images within each folder
    folder_path = os.path.join(file_dir, folder)
    images = os.listdir(folder_path)
    # store a copy of each image in the new folder with its video name prepended
    # to the original image name
    for i in images:
      img_path = os.path.join(folder_path, i)
      new_img_path = os.path.join(final_folder, video) + "_" + i
      shutil.copy(img_path, new_img_path)


def make_labels(file_dir):
  # get the names of the CSV files containing the dimensions of annotation boxes
  csv_files = os.listdir(file_dir)
  # create a new folder in the same directory to store created YOLO files
  folder_path = os.path.join(file_dir, "labels")
  # dictionary used to map each object class name to its class index
  class_idx = {"LEye":0, "REye":1, "Muzzle":2, "Forehead":3}

  try: 
    os.mkdir(folder_path)
  except FileExistsError:
    pass

  for csv_file in csv_files:
    if (csv_file.endswith(".csv") == False):
        continue
  
    csv_file_path = os.path.join(file_dir, csv_file)
    data = pd.read_csv(csv_file_path)
    # iterate through each row of each CSV file to extract
    # the dimensions
    for i in range(len(data.index)):
      # prepend the video name from the CSV file to the image name from
      # each column to create the required YOLO txt file name
      img_name = data["filename"][i]
      txt_name = img_name.removesuffix(".jpg") + ".txt"
      file_name = csv_file.removesuffix("frontal.csv") + txt_name
      txt_path = os.path.join(folder_path, file_name)
      # load the dictionaries given in the region attribute columns
      #  to extract the class names and dimensions as values
      class_dict = json.loads(data["region_attributes"][i])
      dim_dict = json.loads(data["region_shape_attributes"][i])
      class_type = class_dict["Types"]
      width = dim_dict["width"]
      height = dim_dict["height"]
      # convert the given upper-left coordinates to center coordinates
      x = dim_dict["x"] + (1/2 * width)
      y = dim_dict["y"] + (1/2 * height)
      # normalise the dimensions by dividing by the pixel dimensions
      x /= 3840 
      y /= 2160
      width /= 3840
      height /= 2160
      # append a line with the class index followed by each dimension to the corresponding YOLO file
      with open(txt_path, "a+") as f:
        try:
          f.write(str(class_idx[class_type]) + " " + str(x) + " " + str(y) + " " + str(width) + " " + str(height) + "\n")
        except KeyError:
          pass

get_images("/Users/celinabrar/Desktop/SCDL1991-G11-main/Images/")
make_labels("/Users/celinabrar/Desktop/SCDL1991-G11-main/(Filtered) High Illumination - 59 animals/")