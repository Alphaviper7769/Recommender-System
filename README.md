# Recommendation System for Flipkart Grid 5.0

Recommendation System Application based on **IntTower** (https://github.com/archersama/IntTower).

Important functions of the application includes,

-> `user_specific_recommendation` - function to return the local recommendations personal to the user  

-> `global_recommendation` -  function to return the globally trending products that might be preferred by the user

-> `purchase` - function executed when a product is bought, updating weights on tags and reinforcing the model

-> `reinforce` - funtion called during purchase of product, Reinforcing the model

-> `recommend` - function called to creae a recommendation list, Mixing the `global recommendation` and `user recommendation` according to a certain **ratio** between a minimum and maximum threshold

-> `calculate_discount` - function to give a **personalized discount** to the user based on his past purchases

-> `remove_tag` - function to implement **Interactive Recommendation**  to negetively bias the tag if the user closes the associated product

-> `update_tags` - function to implement a **Decaying Algorithm** to reduce the weight of each tag with time 

To use the application, make sure you have **git** installed and clone the repository using,

```bash
git clone https://github.com/Alphaviper7769/Recommender-System.git
```

**Server**

Run the following commands to initiate the server.

```bash
cd backend
python app.py
```

**Frontend**

To start an npm server to host the website on local, run the following from the root directory,

```bash
cd frontend
npm start
```
