# Outfit Recommendation Project

__Project Proposal__

1. __Abstract__: This is an outfit recommendation web app. It can read the user's specific folder in a specific location on their local computer to obtain the photo of the outfit. After recognizing the outfits, recommend several style matching options for the user to choose by deep learning. 
2. __Planned Deliverables__: We plan that the final result will be a web app. Its workflow is: users save photos of their own clothes in a specific local path, and the web app can extract these photos with the user's permission, and recognize the type, color, (or even brand of the clothes through deep learning). Finally, it will generate some clothes matching according to different styles for users to choose. In a more advanced version (probably this summer), it will obtain the latest information in the fashion industry through web scraping, and recommend new clothes based on the user’s favorite style.
3. __Resources Required__: We get a great dataset from kaggle. It includes photoes, types, colors, seasons, genders, and usages.
4. __Tools/Skills Required__: This project uses machine learning, computer vision, web scrapping. The packages might be numpy, sklearn, Tensorflow, scrapy, etc.
5. __Risks__: If it turns out that the data does not exist, we do not need to change the plan, we will find the data ourselves through web scraping. Our recommendation system may be more complicated than imagined. If we cannot complete a complete recommendation system, we will replace the web app plan with a package plan.
6. __Ethics__: We're just providing a portfolio of recommendations. User can choose different styles. And they may or may not adopt our advice. So I thing our project won't hurt anyone.
7. __Tentative Timeline__: After 2 weeks(we should build a computer vision model, it can recognize the type and color of a photo of cloth),
                           After 4 weeks(Improve our CV model make it can recognize more than one cloth in a single picture. We could get our training data by put some photo of different style of dressing through this model. Then use this training data fit our outfit suggestion model)
                           After 6 weeks(create a web app use our models)
    
