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


#for GUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo                                  
from PyQt5.QtWidgets import QFileDialog,QLabel
from PyQt5.QtGui import *
#from PyQt5.QtGui import QLabel

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


# Since one of the factors in our clothes recommendation is the season, 
# we extract the current real season and match it with all the clothes stored in the app.
# This means that we only recommend clothes that are suitable for the current season
from datetime import date
todays_date = date.today()
tomonth = todays_date.month
if tomonth in [3,4,5]:
    toseason = "Spring"
elif tomonth in [6,7,8]:
    toseason = "Summer"
elif tomonth in [9,10,11]:
    toseason = "Fall"
else:
    toseason = "Winter"
###################################################################################


class Ui_MainWindow(object):
    """
    This class to to generate a GUI (graphical user interface)
    """
    def __init__(self):
        """
        initil them three in order to add clothes later.
        """
        self.top = []
        self.bottom = []
        self.shoes = []
        
        
    def ALL_PREDICT(self):
        """
        User click ADD botton to call this function, after getting a path of a photo, this function do prediction by the models and show the result in the GUI.
        """
        _translate = QtCore.QCoreApplication.translate
        directory1 = QFileDialog.getOpenFileName(None, "Select file", "H:/")

        sub, info, res_place_holder = single_classification(directory1[0])
        
        # if the result is top, then add an item to the "top" list on GUI.
        if sub == "top":
            item = QtWidgets.QListWidgetItem(info)
            self.TOP_LIST.addItem(item)
            self.top.append(res_place_holder)
        # if the result is bottom, then add an item to the "bottom" list on GUI.
        elif sub == "bottom":
            item = QtWidgets.QListWidgetItem(info)
            self.BOTTOM_LIST.addItem(item)
            self.bottom.append(res_place_holder)
        # if the result is shoes, then add an item to the "shoes" list on GUI.
        elif sub == "foot":
            item = QtWidgets.QListWidgetItem(info)
            self.SHOE_LIST.addItem(item)
            self.shoes.append(res_place_holder)
    def TOP_LIST_EDIT(self):
            """
            User click EDIT botton to call this function to edit a prediction result.
            """
            
            selected_items = self.TOP_LIST.selectedItems()
            text, okPressed = QtWidgets.QInputDialog.getText(self.AddTopButton, "EDIT","Please Edit This Top:", QtWidgets.QLineEdit.Normal, selected_items[0].text())
            for i in selected_items:
                self.TOP_LIST.takeItem(self.TOP_LIST.row(i))
            if okPressed and text != '':
                item = QtWidgets.QListWidgetItem(text)
                self.TOP_LIST.addItem(item)   
    def TOP_LIST_DEL(self):
            """
            User click DELETE botton to call this function to delete a photo with prediction result.
            """
            selected_items = self.TOP_LIST.selectedItems()
            for i in selected_items:
                self.TOP_LIST.takeItem(self.TOP_LIST.row(i))
            text = selected_items[0].text()
            
            path = text.split(", ")[-1]
            for i in self.top:
                if(i[-1] == path):
                    self.top.remove(i)
            
    ####          
    def BOTTOM_LIST_EDIT(self):
            """
            User click EDIT botton to call this function to edit a prediction result.
            """
            selected_items = self.BOTTOM_LIST.selectedItems()
            text, okPressed = QtWidgets.QInputDialog.getText(self.AddBottomButton, "EDIT","Please Edit This Bottom:", QtWidgets.QLineEdit.Normal, selected_items[0].text())
            for i in selected_items:
                self.BOTTOM_LIST.takeItem(self.BOTTOM_LIST.row(i))
            if okPressed and text != '':
                item = QtWidgets.QListWidgetItem(text)
                self.BOTTOM_LIST.addItem(item)   
    def BOTTOM_LIST_DEL(self):
            """
            User click DELETE botton to call this function to delete a photo with prediction result.
            """
            selected_items = self.BOTTOM_LIST.selectedItems()
            for i in selected_items:
                self.BOTTOM_LIST.takeItem(self.BOTTOM_LIST.row(i))
            text = selected_items[0].text()
            
            path = text.split(", ")[-1]
            for i in self.bottom:
                if(i[-1] == path):
                    self.bottom.remove(i)
            
           
    def SHOE_LIST_EDIT(self):
            """
            User click EDIT botton to call this function to edit a prediction result.
            """
            selected_items = self.SHOE_LIST.selectedItems()
            text, okPressed = QtWidgets.QInputDialog.getText(self.AddShoeButton, "EDIT","Please Edit This Shoes:", QtWidgets.QLineEdit.Normal, selected_items[0].text())
            for i in selected_items:
                self.SHOE_LIST.takeItem(self.SHOE_LIST.row(i))
            if okPressed and text != '':
                item = QtWidgets.QListWidgetItem(text)
                self.SHOE_LIST.addItem(item)   
    def SHOE_LIST_DEL(self):
            """
            User click DELETE botton to call this function to delete a photo with prediction result.
            """
            selected_items = self.SHOE_LIST.selectedItems()
            for i in selected_items:
                self.SHOE_LIST.takeItem(self.SHOE_LIST.row(i))
            text = selected_items[0].text()
            
            path = text.split(", ")[-1]
            for i in self.shoes:
                if(i[-1] == path):
                    self.shoes.remove(i)
    #################
    def Generate(self):
        """
        User click Generate today's Outfit Recommendation botton to call this function to get a recommendation.
        """
        top_right_season = [i for i in self.top if i[3] == toseason ]
        if top_right_season != []:
            ad_top = top_right_season[np.random.randint(len(top_right_season))]
        else:
            ad_top = self.top[np.random.randint(len(self.top))]   
        helper_bot = [i for i in self.bottom if i[4] == ad_top[4] ]
        helper_sho = [i for i in self.shoes if i[4] == ad_top[4] ]
        if helper_bot==[]:
            ad_bot = self.bottom[np.random.randint(len(self.bottom))]
        else:
            bot_right_season = [i for i in helper_bot if i[3] == toseason]
            
            if bot_right_season != []:
                ad_bot = bot_right_season[np.random.randint(len(bot_right_season))]
            else:
                ad_bot = helper_bot[np.random.randint(len(helper_bot))]   
        if helper_sho==[]:
            ad_sho = self.shoes[np.random.randint(len(self.shoes))]
        else:
            sho_right_season = [i for i in helper_sho if i[3] == toseason]
            
            if sho_right_season != []:
                ad_sho = sho_right_season[np.random.randint(len(sho_right_season))]
            else:
                ad_sho = helper_sho[np.random.randint(len(helper_sho))]
        
        self.listWidget_1.setPixmap(QtGui.QPixmap(ad_top[-1]).scaled(281,300))
        self.listWidget_2.setPixmap(QtGui.QPixmap(ad_bot[-1]).scaled(281,300))
        self.listWidget_3.setPixmap(QtGui.QPixmap(ad_sho[-1]).scaled(281,300))

    # The above is what functions the GUI should have
    
#####################################################################################

    # The below are the appearance settings of the GUI
    
    def setupUi(self, MainWindow):
        """
        Add items into GUI.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 669)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TOP_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.TOP_LIST.setGeometry(QtCore.QRect(10, 30, 281, 181))
        self.TOP_LIST.setObjectName("TOP_LIST")
        self.AddTopButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddTopButton.setGeometry(QtCore.QRect(10, 210, 141, 41))
        self.AddTopButton.setAutoFillBackground(False)
        self.AddTopButton.setCheckable(False)
        self.AddTopButton.setObjectName("AddTopButton")
        self.DeleteTopButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteTopButton.setGeometry(QtCore.QRect(150, 210, 141, 41))
        self.DeleteTopButton.setCheckable(False)
        self.DeleteTopButton.setChecked(False)
        self.DeleteTopButton.setObjectName("DeleteTopButton")
        self.AddBottomButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddBottomButton.setGeometry(QtCore.QRect(300, 210, 141, 41))
        self.AddBottomButton.setObjectName("AddBottomButton")
        self.BOTTOM_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.BOTTOM_LIST.setGeometry(QtCore.QRect(300, 30, 281, 181))
        self.BOTTOM_LIST.setObjectName("BOTTOM_LIST")
        self.DeleteBottomButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteBottomButton.setGeometry(QtCore.QRect(440, 210, 141, 41))
        self.DeleteBottomButton.setObjectName("DeleteBottomButton")
        self.AddShoeButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddShoeButton.setGeometry(QtCore.QRect(590, 210, 141, 41))
        self.AddShoeButton.setObjectName("AddShoeButton")
        self.SHOE_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.SHOE_LIST.setGeometry(QtCore.QRect(590, 30, 281, 181))
        self.SHOE_LIST.setObjectName("SHOE_LIST")
        self.DeleteShoeButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteShoeButton.setGeometry(QtCore.QRect(730, 210, 141, 41))
        self.DeleteShoeButton.setObjectName("DeleteShoeButton")
        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(440, 270, 431, 81))
        self.GenerateButton.setObjectName("GenerateButton")
        self.HistoryButton = QtWidgets.QPushButton(self.centralwidget)
        self.HistoryButton.setGeometry(QtCore.QRect(10, 270, 431, 81))
        self.HistoryButton.setObjectName("HistoryButton")
        self.TopLabel = QtWidgets.QLabel(self.centralwidget)
        self.TopLabel.setGeometry(QtCore.QRect(140, 10, 60, 16))
        self.TopLabel.setTextFormat(QtCore.Qt.RichText)
        self.TopLabel.setObjectName("TopLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 10, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(710, 10, 60, 16))
        self.label_2.setObjectName("label_2")
        self.listWidget_1 = QtWidgets.QLabel(self.centralwidget)
        self.listWidget_1.setGeometry(QtCore.QRect(10, 370, 281, 300))
        self.listWidget_1.setObjectName("listWidget_1")
        self.listWidget_1.setPixmap(QtGui.QPixmap("pictures/top_question.png").scaled(281,300))
        self.listWidget_2 = QtWidgets.QLabel(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(300, 370, 281, 300))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setPixmap(QtGui.QPixmap("pictures/top_question.png").scaled(281,300))
        
        self.listWidget_3 = QtWidgets.QLabel(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(590, 370, 281, 300))
        self.listWidget_3.setObjectName("listWidget_3")
        self.listWidget_3.setPixmap(QtGui.QPixmap("pictures/top_question.png").scaled(281,300))
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 880, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #####################################################################################
        
        # Establish a connection between buttons and functions
        self.AddTopButton.clicked.connect(self.TOP_LIST_EDIT)
        self.DeleteTopButton.clicked.connect(self.TOP_LIST_DEL)
        
        self.AddBottomButton.clicked.connect(self.BOTTOM_LIST_EDIT)
        self.DeleteBottomButton.clicked.connect(self.BOTTOM_LIST_DEL)
        
        self.AddShoeButton.clicked.connect(self.SHOE_LIST_EDIT)
        self.DeleteShoeButton.clicked.connect(self.SHOE_LIST_DEL)
        self.HistoryButton.clicked.connect(self.ALL_PREDICT)            
        self.GenerateButton.clicked.connect(self.Generate)              
        
        #####################################################################################

    def retranslateUi(self, MainWindow):
        """
        This function translate the item on GUI from what computer can understand to what we can understand. (Gives items names)
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AddTopButton.setText(_translate("MainWindow", "EDIT"))
        self.DeleteTopButton.setText(_translate("MainWindow", "DELETE"))
        self.AddBottomButton.setText(_translate("MainWindow", "EDIT "))
        self.DeleteBottomButton.setText(_translate("MainWindow", "DELETE"))
        self.AddShoeButton.setText(_translate("MainWindow", "EDIT "))
        self.DeleteShoeButton.setText(_translate("MainWindow", "DELETE"))
        self.GenerateButton.setText(_translate("MainWindow", "Generate Today\'s Outfit Recommendation"))
        self.HistoryButton.setText(_translate("MainWindow", "ADD A PHOTO"))
        self.TopLabel.setText(_translate("MainWindow", "Top"))
        self.label.setText(_translate("MainWindow", "Bottom"))
        self.label_2.setText(_translate("MainWindow", "Shoes"))
        

if __name__ == "__main__":

    # This part is to run the GUI we defined above and for some basic settings about the GUI, such as color, style, etc.
   
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('fusion'))
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setStyleSheet("color: white;"
                             "selection-background-color: peru;"
                             "selection-color: white;"
                             "background-color: saddlebrown;")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
