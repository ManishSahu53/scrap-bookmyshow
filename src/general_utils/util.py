"""General utility function"""
from __future__ import division, print_function, unicode_literals

import json
import os

import io
import json
import base64

import joblib
import numpy as np
from PIL import Image
from dataclasses import dataclass

# import tensorflow as tf


# Creating Param class
class Params():
    """Class that loads hyperparameters from a dictionary.
    Example:
    ```
    params = Params(json_path)
    print(params.learning_rate)
    params.learning_rate = 0.5  # change the value of learning_rate in params
    ```
    """

    def __init__(self, json_path):
        self.update(json_path)

    def save(self, json_path):
        """Saves parameters to json file"""
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by
        `params.dict['learning_rate']`
        """
        return self.__dict__


# Loading model
def load_model(path_model):
    model = joblib.load(path_model)
    return model


# Saving model
def save_model(model, path_output):
    """Saving any model to PKL file
    Args:
        model: (object)
        path_output: (string) path of output
    """

    joblib.dump(model, path_output)
    print('Model saved to %s' % (path_output))


# check directory if exist else create directory
def check_dir(path_output):
    """Checking directory and creating
    folder if doesn't exist
    Args:
        path_output: (string) directory
    """
    if not os.path.exists(path_output):
        os.makedirs(path_output)


# Loading json
def load_json(path_model):
    """Loads json object to dict
    Args:
        path_model: (string) path of input
    """
    with open(path_model) as f:
        data = json.load(f)
    return data


# Saving json
def save_json(model, path_output):
    """Saves dictionary to json object.
    Args:
        model: (Dict object)
        path_output: (string) path of output
    """
    # Saving keyword and keyword atc
    with open(path_output, 'w') as f:
        json.dump(model, f, indent=4, sort_keys=True)


# Saving vocab to txt file
def save_vocab_to_txt_file(vocab, txt_path):
    """Writes one token per line, 0-based line id corresponds to
    the id f the token.
    Args:
        vocab: (iterable object) yields token
        txt_path: (string) path to vocab file
    """
    with open(txt_path, 'w') as f:
        for token in vocab:
            f.write(str(token) + '\n')


# Loading txt as list
def load_txt(path_txt):
    with open(path_txt, encoding='utf-8') as f:
        vocab = f.read().splitlines()
    return vocab


# Setting logging
def set_logger(path_log):
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Logging to a file
        file_handler = logging.FileHandler(path_log)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s : %(levelname)s : %(message)s'))
        logger.addHandler(file_handler)

        # Logging to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)


def getNamenoExt(path_tif):
    """
        Return base name of file from path/complete name of file
    """
    return (os.path.splitext(os.path.basename(path_tif))[0])    


# Get list of files inside this folder
def list_list(path, extension):
    path_data = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                path_data.append(os.path.join(root, file))

    return path_data


# get file name
def get_file_name(path_data):
    return os.path.splitext(os.path.basename(path_data))[0]


def get_files(path_dir, skip_dir=['']):
    path_files = []
    data = tf.io.gfile.walk(path_dir)
    for path_data, path_dirs, temp_files in data:
        if path_data in skip_dir:
            continue
        else:
            for temp_dir in path_dirs:
                temp_files += get_files(temp_dir)
        
        path_files += [os.path.join(path_data, f) for f in temp_files]
    return path_files



def get_variables_class(inst):
    """
    get all the variabels of class
    """
    skips = ['__weakref__', '__dict__']
    var = {}
    for v in inst.__dict__:
        if '__' in v:
            continue

        if not callable(getattr(inst, v)):
            if type(getattr(inst, v)) == set:
                var[v] = list(getattr(inst, v))
            else:
                var[v] = getattr(inst, v)


    return var


def encode_base_64(path_image):
    """
        Encoding image to base64
    """
    image = open(path_image, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read).decode()
    return image_64_encode

def decode_base_64(image_64_encode):
    """
        Decoding image from base64
    """

    img_reopen = Image.open(io.BytesIO(base64.urlsafe_b64decode(image_64_encode)))
    return img_reopen


# def generate_pdf():
#     %%capture
#     path_pdf = '/workspace/jupyter_notebooks/manish_sahu/clipeus/training/corner_points/data/th_id_cards/2022-06-01/non_id_angles.pdf'
#     pdf = matplotlib.backends.backend_pdf.PdfPages(path_pdf)

#     n = min(100, len(temp_filter))

#     for index in range(n):
#         request_id = temp_filter.request_id.iloc[index]
#         boundingBox = temp_filter.boundingBox.iloc[index]
#         shapeValue = temp_filter.valid_shape_id_value.iloc[index]

#         path_img = os.path.join(path_output, request_id + '.jpg')
#         path_base_img = os.path.join(path_base, request_id + '.jpg')


#         fig = plt.figure()
        
#         plt.subplot(1, 2, 1) 
#         plt.title(f'Cropped, shapeValue {shapeValue}')
#         img = Image.open(path_img)
#         plt.imshow(img)
        
#         plt.subplot(1, 2, 2) 
#         img_raw = np.array(Image.open(path_base_img))
#         img_raw_copy = img_raw.copy()

#         cv2.circle(img_raw_copy, (boundingBox[0], boundingBox[1]), 50, (255, 0, 0), -1)
#         cv2.circle(img_raw_copy, (boundingBox[2], boundingBox[3]), 50, (0, 255, 0), -1)
#         cv2.circle(img_raw_copy, (boundingBox[4], boundingBox[5]), 50, (0, 0, 255), -1)
#         cv2.circle(img_raw_copy, (boundingBox[6], boundingBox[7]), 50, (255, 0, 255), -1)

#         plt.title(f'Model Output e26')
#         plt.imshow(img_raw_copy)
        
#         pdf.savefig(fig)
        
#     pdf.close()


# Saving Config
def save_config(config, path_output:str):
    save_json(config.__dict__, path_output=path_output) 

# Loading Config
def load_config(path_json_config:str):
    data_config = load_json(path_json_config)
    @dataclass
    class Config:
        def __init__(self, my_dict):
            for key in my_dict:
                # While Loading
                if key == 'LOADED_CONFIG':
                    setattr(self, key, True)
                else:
                    setattr(self, key, my_dict[key])
                    
                
    result = Config(data_config)
    return result
