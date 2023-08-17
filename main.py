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



#                  1. PURCHASE


def purchase(userID, productID):
    users[userID]['tags'][products[productID]['tag']] += 1
    products[productID]['count'] += 1
    tags[products[productID]['tag']] += 1
    # reinforce the model


    
    #                2. GLOBAL RECOMMENDATION

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



#                  2.1     GLOBAL RECOMMENDATION PRODUCT



def global_recommendations(userID, num_recommendations=10, threshold=0.5):
    user = users.get(userID)
    if not user:
        return []  
    
    recommended_products = []
    
    for tag in tags:
        products_in_tag = tags[tag]['pid']
        
        for product in products_in_tag:

            likelihood = nn.predict_likelihood(user, product)  
            
            if likelihood > threshold:
                recommended_products.append(product)
                if len(recommended_products) >= num_recommendations:
                    break
        
        if len(recommended_products) >= num_recommendations:
            break
    
    return recommended_products




#                  3.  LOCAL RECOMMENDATION


def user_specific_recommendations(userID, total_products=5, max_list=20):
    user = users.get(userID)
    if not user:
        return []  
    
    # Sort user's tags by interaction count in descending order
    sorted_tags = sorted(user['tags'], key=user['tags'].get, reverse=True)
    
    recommended_products = []
    
    for tag in sorted_tags:
        products_in_tag = tags[tag]['pid']
        top_products = products_in_tag[:total_products]
        tag_recommendations = [tag, top_products]
        recommended_products.append(tag_recommendations)
        
        if len(recommended_products) >= max_list:
            break
    
    return recommended_products


#               4.  RECOMMEND



def recommend(userID, ratio):
    if not (0 <= ratio <= 1):
        return [] 
    
    global_recs = global_recommendations(userID)
    user_recs = user_specific_recommendations(userID)
    
    total_global = len(global_recs)
    total_user = len(user_recs)
    
    num_global = int(total_global * ratio)
    num_user = int(total_user * (1 - ratio))
    

    combined_recommendations = global_recs[:num_global] + user_recs[:num_user]
    
    return combined_recommendations
