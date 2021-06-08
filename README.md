In general, we have implemented such a local app which can store photo of clothes owned by users and recommend what they wear (top, bottom, and shoes) today.

In this app, users can choose to add a photo from their own computer (we need users to take a photo of their own clothes and store it in the computer) to our app. In the process of adding pictures, this picture will be automatically recognized by our pre-trained model at one time by type (such as T-shirt), gender (such as women), color (such as navy blue), season (such as summer), usage (such as formal, casual, sport, etc.), and path. These six types of information will be stored in the app and displayed for the user's reference. Considering that our model is sometimes inaccurate, and in order to facilitate user operations, we also provide users with editing and deleting functions. Therefore, the user can edit the information we misidentified and delete a piece of clothing.

We provide users with a "Generate Today's Outfit Recommendations" button, which can provide users with recommendations. The recommended result is composed of three pictures, namely top, bottom, and shoes. Of course, these three pictures are the user's own clothes.

![%E6%88%AA%E5%B1%8F2021-06-07%2000.23.15.png](attachment:%E6%88%AA%E5%B1%8F2021-06-07%2000.23.15.png)
