import tensorflow as tf;
import numpy as np
import os

def get_files(file_dir):
    cats = []
    label_cats = [];
    dogs = [];
    label_dogs = [];

    for dir in os.listdir(file_dir):
        for file in os.listdir(file_dir + "/" + dir):
            name = file.split('.');
            if name[0] == 'cat':
                cats.append(file_dir + file);
                label_cats.append(0);
            else:
                dogs.append(file_dir + file);
                label_dogs.append(1);

    print("There are %d cats\nThere are %d dogs" % (len(cats), len(dogs)));

    image_list = np.hstack((cats, dogs))
    label_list = np.hstack((label_cats, label_dogs))

    temp = np.array([image_list, label_list]);
    temp = temp.transpose()
    np.random.shuffle(temp);

    return image_list, label_list

get_files("./data/train")