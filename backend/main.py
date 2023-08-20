from train import int_tower, get_es_mdckpt
import torch
import time
from collections import defaultdict,OrderedDict

products = defaultdict(lambda : {
    'count':0,
    'price':0,
    'mean_rating':0,
    'tag':0
})

users = defaultdict(lambda : {
    'tags': defaultdict(0),
    'mean_rating':0,
    'lastRecommendTime': time.time()
})

tags = defaultdict(lambda : {
    'products':[],
    'count':0
})


model, data, mms = int_tower()
model.load_state_dict(torch.load('amazon_fetower.ckpt'))

data = data[:100]


def predict_likelihood(userID,productID,tag):
    price = products[productID]['price']
    user_mean_rating = users[userID]['mean_rating']
    item_mean_rating = products[productID]['mean_rating']
    model_input = {
        'reviewerID':userID,
        'asin':productID,
        'categories':tag,
        'user_mean_rating':user_mean_rating,
        'item_mean_rating':item_mean_rating,
        'price':price
    }
    model.predict(x=model_input,batch_size=1)

def fill_products():
    for i in range(len(data)):
        pid = data.loc[i,'asin']
        prc = data.loc[i,'price']
        mean_rating = data.loc[i,'item_mean_rating']
        tag=data.loc[i,'categories']
        products[pid]['count']+=1
        products[pid]['price']=prc
        products[pid]['mean_rating']=mean_rating
        products[pid]['tag']=tag

def fill_tags():
    for pid,product in products.items():
        cnt = product['count']
        tag = product['tag']
        tags[tag]['products'].append(pid)
        tags[tag]['count']+=cnt

def fill_users():
    for i in range(len(data)):
        uid = data.loc[i,'reviewerID']
        pid = data.loc[i,'asin']
        tag = data.loc[i,'categories']
        mean_rating = data.loc[i,'user_mean_rating']
        users[uid]['tags'][tag] += products[pid]['count']
        users[uid]['mean_rating'] = mean_rating

fill_products()
fill_tags()
fill_users()

for prods,cnt in tags.values():
    prods.sort(key=lambda x : products[x]['count'],reverse=True)

tags = OrderedDict(sorted(tags.items(),key=lambda tag,cnt : cnt,reverse=True))

for tags,mr in users.values():
    tags = OrderedDict(sorted(tags.items(), key = lambda tag,cnt : cnt,reverse=True))

print(products)

# reinforce in sets of 100 rows. So store till its < 100
model_data = []
# their corresponsing reviews
model_values = []

def reinforce(model, data, output):
    model_data.append(data)
    model_values(output)
    if len(model_data) >= 100:
        es, mdckpt = get_es_mdckpt()
        model.fit(model_data, model_values, epochs=2, verbose=2, validation_split=0.2, callbacks=[es, mdckpt])
    return model



#                  1. PURCHASE


def purchase(userID, productID):
    if userID in users and productID in products:
        product_tag = products[productID]['tag']

        if product_tag in tags:
            users[userID]['tags'][product_tag] += 1
            products[productID]['count'] += 1
            tags[product_tag] += 1

            update_tags(userID, weight=0.2)
            model = reinforce(model, "data", "output")

            return True  
        else:
            return False 
    else:
        return False  



    
    #                2. GLOBAL RECOMMENDATION____ DEFUNCT


def global_recommendations_tag(userID, total_products=10, threshold=0.5):
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

            likelihood = predict_likelihood(user, product,tag)  
            
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


#                   5. Personalised descount

def calculate_discount(user_id, product_price):

    user_preferred_price_range = model.get_preferred_price_range(user_id)

    
    if product_price > user_preferred_price_range:
        
        threshold_slabs = {
            (0, 500): 0.20,
            (500, 2000): 0.15,
            (2000, 10000): 0.10,
            (10000, float('inf')): 0.05
        }

        # Find the applicable threshold based on the product price
        applicable_threshold = None
        for price_range, threshold in threshold_slabs.items():
            lower_bound, upper_bound = price_range
            if lower_bound <= product_price <= upper_bound:
                applicable_threshold = threshold
                break

        if applicable_threshold is not None:
            
            discount = product_price * applicable_threshold
            discounted_price = product_price - discount

            if discounted_price < user_preferred_price_range:
                percentage_discount = applicable_threshold * 100
                return user_preferred_price_range, percentage_discount
            else:
                return product_price, 0  
    else:
        return product_price, 0 
    

#         6.    Interactive Recommendation

def removeTag(userId, tag, weight):
    try:
        if userId in users and tag in users[userId]['tags']:
            current_value = users[userId]['tags'][tag]
            new_value = max(0, current_value - weight)
            users[userId]['tags'][tag] = new_value
        else:
            print("User ID or tag not found.")
    except Exception as e:
        print("An error occurred:", e)


#            7. Decaying Algorithm

def update_tags(userId, weight):
    if userId in users:
        current_time = time.time()
        last_recommend_time = users[userId]['lastRecommendTime']
        time_difference = current_time - last_recommend_time
        
        for tag in users[userId]['tags']:
            users[userId]['tags'][tag] = max(0, users[userId]['tags'][tag] - weight * time_difference)
        
        users[userId]['lastRecommendTime'] = current_time
    else:
        print("User ID not found.")


def check_credential(userID, password):
    return True