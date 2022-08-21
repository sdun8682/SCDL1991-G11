from pathlib import Path
import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt

file_dir = "./High Illumination - 59 animals" # file directory
all_csv_list = os.listdir(file_dir) # get csv list

try:
    # get the path of the parent directory where a new folder containing 
    # csv files of filtered images will be created
    parent_dir = str(Path(file_dir).parent) 
    # determine the name of the folder according to the original folder name
    last_elem = file_dir.split(os.path.sep)[-1]
    if (not last_elem):
        last_elem = file_dir.split(os.path.sep)[-2]

    new_folder = os.path.join(parent_dir, "(Filtered) " + last_elem)
    os.mkdir(new_folder)

except FileExistsError:
    pass

#print(len(all_csv_list))
#print(all_csv_list)

# For bar plot, store labels for each file and corresponding number of frontal images:
# Key = file name, Value = # frontal images
agdata = {}

for i in all_csv_list:
    
    if (i.endswith(".csv") == False):
        continue

    dirname = i
    path = os.path.join(file_dir, dirname)
    df = pd.read_csv(path)
    # print(df)
        
    #filter
    no_image_ls = []
    i = 0
    while i < len(df['filename'].to_list()):
        # print(df['filename'][i])
        if df['region_attributes'][i] == '{"Types":"FLEye"}' or df['region_attributes'][i] == '{"Types":"FREye"}':
            no_image_ls.append(df['filename'][i])
        i += 1

    no_images = set(no_image_ls)
    # print(no_images)
    
    all_images = set(df['filename'].to_list())
    # all_images
    
    useful_images = all_images - no_images
    # useful_images
    
    frontal_images_num = len(useful_images)
    print("the number of animal's frontal images in " + dirname + " is " + str(frontal_images_num))

    # Saving the data to the dictionary to plot in bar plot later
    agdata[dirname] = frontal_images_num
    
    newdf = df.loc[~df.filename.isin(no_image_ls)] 
    # print(newdf)

    # add each csv file with filtered images to the new folder
    newdf.to_csv(os.path.join(new_folder, dirname.rstrip(".csv") + "_frontal.csv"))


# ----- Creating plot ---- #
files = list(agdata.keys())
counts = list(agdata.values())

fig = plt.figure()

plt.bar(files, counts, color='blue', width = 0.4)
plt.xlabel('File name')
plt.ylabel('Count of frontal images')
plt.title('Count of frontal images by CSV file')
plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
plt.margins(y=2)
# when plot shows up resize horizontally to read the labels better
plt.show()
#plt.savefig('file_bar.pdf', bbox_inches = 'tight')