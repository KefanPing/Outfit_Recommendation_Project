#for modeling
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.preprocessing import image


#for read and show images
import matplotlib.pyplot as plt
import cv2                                                          
import matplotlib.image as mpimg


#for save and load models
import tensorflow as tf
from tensorflow import keras                                        




import numpy as np

#for color classification
import colorsys                                                     
import PIL.Image as Image

from scipy.spatial import KDTree
from webcolors import (
   CSS3_HEX_TO_NAMES,
    hex_to_rgb
)
   
    
# load pre-trained models
# please change them to your local path when load
sub_model = tf.keras.models.load_model('/Users/pingkefan/Desktop/ALL_MODELS/model_sub')
top_model = tf.keras.models.load_model('/Users/pingkefan/Desktop/ALL_MODELS/model_top')
bottom_model = tf.keras.models.load_model('/Users/pingkefan/Desktop/ALL_MODELS/model_bottom')
foot_model = tf.keras.models.load_model('/Users/pingkefan/Desktop/ALL_MODELS/model_shoes')


# all output possibilities of the model for subsequent matching
sub_list = ["bottom","foot","top"]
top_list = [['Belts', 'Blazers', 'Dresses', 'Dupatta', 'Jackets', 'Kurtas',
       'Kurtis', 'Lehenga Choli', 'Nehru Jackets', 'Rain Jacket',
       'Rompers', 'Shirts', 'Shrug', 'Suspenders', 'Sweaters',
       'Sweatshirts', 'Tops', 'Tshirts', 'Tunics', 'Waistcoat'],
           ['Boys', 'Girls', 'Men', 'Unisex', 'Women'],
           ['Black', 'Blue', 'Dark Blue', 'Dark Green', 'Dark Yellow', 'Green',
       'Grey', 'Light Blue', 'Multi', 'Orange', 'Pink', 'Purple', 'Red',
       'White', 'Yellow'],
           ['Fall', 'Spring', 'Summer', 'Winter'],
           ['Casual', 'Ethnic', 'Formal', 'Party', 'Smart Casual', 'Sports',
       'Travel']]
bottom_list = [['Capris', 'Churidar', 'Jeans', 'Jeggings', 'Leggings', 'Patiala',
       'Salwar', 'Salwar and Dupatta', 'Shorts', 'Skirts', 'Stockings',
       'Swimwear', 'Tights', 'Track Pants', 'Tracksuits', 'Trousers'],
              ['Boys', 'Girls', 'Men', 'Unisex', 'Women'],
              ['Black', 'Blue', 'Dark Blue', 'Dark Green', 'Dark Yellow', 'Grey',
       'Light Blue', 'Multi', 'Orange', 'Pink', 'Purple', 'Red', 'White',
       'Yellow'],
              ['Fall', 'Spring', 'Summer', 'Winter'],
              ['Casual', 'Ethnic', 'Formal', 'Smart Casual', 'Sports']]
foot_list = [['Casual Shoes', 'Flats', 'Flip Flops', 'Formal Shoes', 'Heels',
       'Sandals', 'Sports Sandals', 'Sports Shoes'],
            ['Boys', 'Girls', 'Men', 'Unisex', 'Women'],
            ['Black', 'Blue', 'Dark Blue', 'Dark Green', 'Dark Orange',
       'Dark Yellow', 'Grey', 'Light Blue', 'Multi', 'Orange', 'Pink',
       'Purple', 'Red', 'White', 'Yellow'],
            ['Fall', 'Spring', 'Summer', 'Winter'],
            ['Casual', 'Ethnic', 'Formal', 'Party', 'Smart Casual', 'Sports']]


def convert_rgb_to_names(rgb_tuple):
    """
    This function translates rgb to their respective names in css3
    is a helper function for the two below.
    Input is a rgb tuple
    Output is their corresponding name in css3
    """
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def get_cloth_color(image):
    """
    This function is a helper function of the one below to recognize color of an image
    Input is an image
    Output is a color in English
    """
    max_score = 0.0001
    dominant_color = None
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):
       
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
        y = (y-16.0)/(235-16)
        if y > 0.9:
            continue
        score = (saturation+0.1)*count
        if score > max_score:
            max_score = score
            dominant_color = (r,g,b)
            
    return convert_rgb_to_names(dominant_color)
 
    
def color_classification(single_path):
    """
    This function does color classification for a certain path of a photo (of a clothes)
    Input is a path on your computer
    Output is a color
    """
    image = Image.open(single_path)
    image = image.convert('RGB')
    return get_cloth_color(image)
    
    
    
####################################
def single_helper(train_images, my_model, lelist):
    """
    This function is a helper function of the one below to use pre-trained model to predict.
    Input is an image, one of three sub-model, a encoder list
    Output is a list which is the result from the model
    """
    # Convert the predicted result encoded as a number back to the original string
    # and then make them a list contains all the informations
    my_predictions = my_model.predict(train_images)
    result = []
    type_predicted_label = np.argmax(my_predictions[0][0])
    result.append(lelist[0][type_predicted_label])
    type_predicted_label = np.argmax(my_predictions[1][0])
    result.append(lelist[1][type_predicted_label])
    type_predicted_label = np.argmax(my_predictions[2][0])
    result.append(lelist[2][type_predicted_label])
    type_predicted_label = np.argmax(my_predictions[3][0])
    result.append(lelist[3][type_predicted_label])
    type_predicted_label = np.argmax(my_predictions[4][0])
    result.append(lelist[4][type_predicted_label])
    return result


def single_classification(single_path):
    
    """
    This function take a single path of a photo, then do reshape to fit the models, and do classification
    Input is a path of a certain photo
    Output is a tuple which contains subtype(for being send to a correct sub-model), 
                                     info(a string having all info of a clothes), 
                                     res(a list having all info of a clothes)
    """
    
    # Our model only applies to dataframes. 
    # Therefore, in order to enable the model to predict a single picture, 
    # we turn this picture into a dataframe with only one row.
    train_images = np.zeros((1,80,60,3))
  
    path = single_path#/content/images   
    img = cv2.imread(path)
    
    #reshape img to apply the model
    if img.shape != (80,60,3):
        img = image.load_img(path, target_size=(80,60,3))

    train_images[0] = img

    
    result2 = sub_list[np.argmax(sub_model.predict(train_images))]
    
    # According to the results of the first model, branch to three other models
    if result2=="top":
        res = single_helper(train_images,top_model,top_list)
    elif result2=="bottom":
        res = single_helper(train_images,bottom_model,bottom_list)
    elif result2=="foot":
        res = single_helper(train_images,foot_model,foot_list)
    res.append(single_path)
    res_str = f"{res[0]}, {res[1]}, {color_classification(single_path)}, {res[3]}, {res[4]}, {single_path}" 
    
    return (result2,res_str,res)




def find_combo_by_top(top_color_group, combotype):
    """
    This function recommend color base on a seed color by a given angle in a colorwheel.
    Input is a color (from 12+3 colorwheel) and a angle: moderate_combo == 90
                                                         similar_combo == 60
                                                         close_combo == 30
                                                         same_combo == 0
    output is a list of two color
    """
    
    co = int(combotype/30)
    
    
    #if top color is multi
    if top_color_group == 15: #if top color is multi
        bottom_color_group = random.choice([12,13,14])
        if bottom_color_group==12: #if bottom color is black
            shoes_color_group = 13 #then set shoes to be white
            
        elif bottom_color_group==13:                      #if bottom color is white
            shoes_color_group = random.choice([12,13,14]) #then set shoes to be black or white or grey
            
        else:                      #if bottom color is grey
            shoes_color_group = random.choice([12,13])    #then set shoes to be black or white
    
    
    #if top color is mono
    elif top_color_group == 12 or top_color_group == 13 or top_color_group == 14:
        if top_color_group == 12:
            bottom_color_group = random.choice([12,13])
            if bottom_color_group==12:
                shoes_color_group = 13
            else:
                shoes_color_group=random.choice([12,13])
        elif top_color_group == 13:
            bottom_color_group = random.choice([12,13])
            if bottom_color_group==12:
                shoes_color_group = 13
            else:
                shoes_color_group=12
        else:
            bottom_color_group=random.choice([12,13])
            shoes_color_group=random.choice([12,13])  
    else: 
        bottom_color_group = random.choice([top_color_group-co, top_color_group+co])
        if bottom_color_group==top_color_group-co:
            shoes_color_group = top_color_group+co
        else:
            shoes_color_group = top_color_group-co
            
        #In fact, we can simplify this part of the code
        if bottom_color_group == 12:
            bottom_color_group = 0
        if bottom_color_group == 13:
            bottom_color_group = 1
        if bottom_color_group == 14:
            bottom_color_group = 2 
        if bottom_color_group == 15:
            bottom_color_group = 3
        if bottom_color_group == 16:
            bottom_color_group = 4
        if bottom_color_group == 17:
            bottom_color_group = 5
            
        if shoes_color_group == 12:
            shoes_color_group = 0
        if shoes_color_group == 13:
            shoes_color_group = 1
        if shoes_color_group == 14:
            shoes_color_group = 2
        if shoes_color_group == 15:
            shoes_color_group = 3
        if shoes_color_group == 16:
            shoes_color_group = 4
        if shoes_color_group == 17:
            shoes_color_group = 5
        
        if bottom_color_group == -1:
            bottom_color_group = 11
        if bottom_color_group == -2:
            bottom_color_group = 10
        if bottom_color_group == -3:
            bottom_color_group = 9 
        if bottom_color_group == -4:
            bottom_color_group = 8
        if bottom_color_group == -5:
            bottom_color_group = 7
        if bottom_color_group == -6:
            bottom_color_group = 6
            
        if shoes_color_group == -1:
            shoes_color_group = 11
        if shoes_color_group == -2:
            shoes_color_group = 10
        if shoes_color_group == -3:
            shoes_color_group = 9
        if shoes_color_group == -4:
            shoes_color_group = 8
        if shoes_color_group == -5:
            shoes_color_group = 7
        if shoes_color_group == -6:
            shoes_color_group = 6
            
    return (bottom_color_group , shoes_color_group)
