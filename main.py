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
    

def global_recommendations(userID):
    # return global recommendations. Use model


def user_specific_recommendations(userID):
    # return local specific recommendations

def recommend(userID, ratio):
    # return in ratio