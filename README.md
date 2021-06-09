# Contents

[0. Group contribution](#0)

[1. Intro](#1)

[2. Use the app](#2)

[3. Models](#3)

[4. Recommendation](#4)

[5. Limitations](#5)

[6. Start the app](#6)

[7. File structure](#7)

<h2 id="0">0.Group contribution</h2>

<h2 id="1">1. Intro</h2> Do you sometimes (definitely not during the final exam week) stand in front of the closet and think deeply about "what should I wear today?", "how do I match clothes today to make me more fashionable?". Everyone has different fashion concepts, and what a person wears can clearly show how that person's character and taste are. For people who don't have time to think about this, they may need to use an app to improve their sense of fashion, such as an outfit recommendation app. In general, we have implemented such a local app which can store photo of clothes owned by users and recommend what to wear (top, bottom, and shoes) today.

<br>
<h2 id="2">2. Use the app</h2> In this app, users can choose to add a photo from their own computer (we need users to take a photo of their own clothes and store it in the computer) to our app. In the process of adding pictures, this picture will be automatically recognized by our pre-trained model at one time, by type (such as T-shirt), gender (such as women), color (such as navy blue), season (such as summer), usage (such as formal, casual, sport, etc.), and path of the photo. These six types of information will be stored in the app and displayed for the user's reference. Considering that our model is sometimes inaccurate, and in order to facilitate user operations, we also provide users with editing and deleting buttons. Therefore, the user can edit the information we misidentified or delete a piece of clothing.

We provide users with a "Generate Today's Outfit Recommendations" button, which can provide users with recommendations. The recommended result is composed of three pictures, namely top, bottom, and shoes. Of course, these three pictures are the user's own clothes.

Below is a functional diagram of using our app:

![ORP1](pictures/tutorial.png)

<br>
<h2 id="3">3. Models</h2> Behind such an app, we have four neural network models and a recommendation system.

For our neural network models: The first model (with accuracy over 99%) is used to identify whether the clothes are tops or bottoms or shoes. After this, the photo will be directed to one of the other three models based on the results of the first model (please see the picture below). These three similar but not exactly the same models (with overall accuracy around 80% ) will identify type(65), gender(5), color(46), season(4), and usage(8).

Below is a flow chart of our recognition process:

![ORP2](pictures/51109bb074d95c059f716e48786568f.jpg)

<br>
<h2 id="4">4. Recommendation</h2> For the recommendation process: 
The program randomly selects a top, and we look for the same gender, the same season, and the same usage in the bottoms and shoes stored in the app. After this, we recommend outfits based on the color. Our recommended method for color is based on such a color wheel. We summarized the 46 colors in the data set into 12 colors in the figure, plus three colors of black, white, gray, and multi-color, recommending according to the angle between the colors.

![ORP2](pictures/IMG_0159.jpg)

<br>
<h2 id="5">5. Limitations</h2>
First of all, although our data is very large and the accuracy of the test set is very high, we found that our program is not suitable for all the pictures we randomly searched from Google. First, we think our data has bias, which we talked in "A special explanation for data cleaning and analysis(bias).ipynb". In addition, it seems partially to be due to changes in people's thinking about fashion, or perhaps because the dataset is relatively old. 


<br>
<h2 id="6">6. Start the app</h2>

To start the app: 

a) First download ui_module.py, recognition_module.py, and models from this repo to the same folder. 

b) Next type the following code in any Python environment:
```
   from ui_module import*
   run_ui()    
```   

c) Then you will see the app!


<h2 id="7">7. File structure</h2>

```
├── A special explanation for data cleaning and analysis(bias).ipynb   # A note that analyzes bias of the data set used in this project
├── LICENSE   # Lisence
├── README.md   # The readme file
├── models   # This folder 
│   ├── data   # Data for training models from Kaggle
│   ├── models   # A google drive folder which contains our trained models
|   │   ├── model_sub   # A model that distinguishes tops, bottoms, and shoes
|   │   ├── model_top   # A model that recognizes the type, color, gender, season, and usage of tops
|   │   ├── model_bottom   # A model that recognizes the type, color, gender, season, and usage of bottoms
|   │   └── model_shoes   # A model that recognizes the type, color, gender, season, and usage of shoes
│   ├── train_module.py   # A module which contains functions we used to train the models
│   └── training.py   # Steps that we train the models
├── pictures   # Pictures used in this repo
│   ├── 51109bb074d95c059f716e48786568f.jpg   
│   ├── IMG_0159.jpg   
│   ├── top_question.png   
│   └── tutorial.png   
├── proposal.md   # Our original proposal
└── py   # All you need to run the app
    ├── recognition_module.py   # A module which contains functions and classes that our GUI needs
    └── ui_module.py   # A module which contains the function to run the app
```
