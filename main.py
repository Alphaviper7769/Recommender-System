from model import model

products = dict()
users = dict()
tags = dict()

# tags = {
#   tag: {
#       pid: [],
#        cnt: 0
#   }
# } 

# users: {
#   id: {
#       tags: {
#           tag: cnt
#       }
#   }
# }

# products {
#   id: {
#       count: cnt
#   },
#   tag: 
# }

def purchase(userID, productID):
    users[userID]['tags'][products[productID]['tag']] += 1
    products[productID]['count'] += 1
    tags[products[productID]['tag']] += 1
    # reinforce the model
    
    #                GLOBAL RECOMMENDATION
# you have the function inputs as userID, total_products=10 and threshold=0.5
# first check if user is valid
# then iterate in tags
# pass tag and userId to the model
# the model returns a number between 0 and 1 indicating the likelihood of the user buying the product
# if that value is greater than the threshold get the tag and the top < total_products> number of products in an subarray
# append that subarray to the main array
# return the main array

def global_recommendations(userID, total_products=10, threshold=0.5):
    user = users.get(userID)
    if not user:
        return []  # User not found
    
    recommended_products = []
    
    for tag in tags:
        likelihood = model.predict_likelihood(user, tag)
        if likelihood > threshold:
            products_in_tag = tags[tag]['pid']
            top_products = products_in_tag[:total_products]
            tag_recommendations = [tag, top_products]
            recommended_products.append(tag_recommendations)
    
    return recommended_products

def user_specific_recommendations(userID):
    # return local specific recommendations

def recommend(userID, ratio):
    # return in ratio