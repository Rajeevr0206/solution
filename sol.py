import requests

# function to get data from the url
def get_data(url):
    # request data from url
    response = requests.get(url)
    # parse json response
    data = response.json()
    # return parts
    return data['parts']

# Recursive function to search for the optimal combination of non-cpu parts
def search_all(d,l,i,rembudget,templist,finalans):
    # if all the categories has been searched
    if i==len(l):
        # check if the current remaining budget is less than the final answer remaining budget
        if rembudget<finalans[1]:
            # update the final answer
            finalans[0]=templist.copy()
            finalans[1]=rembudget
        return
    for ii in d[l[i]]:
        # check if the remaining budget is greater than or equal to the current item
        if rembudget>=ii['price']:
            templist.append(ii)
            # recursive call with the remaining budget and updated templist
            search_all(d,l,i+1,rembudget-ii['price'],templist,finalans)
            templist.pop()

# function to get maximum purchase
def maximum_purchase(l,budget):
    # dictionary to group items by their category type
    d = dict()
    for i in l:
        if d.get(i["categoryType"]) is None:
            d[i["categoryType"]] =[i]
        else:
            d[i["categoryType"]].append(i)
    # sorting the items by price
    for k,v in d.items():
        d[k] = sorted(v,key =lambda x: x['price'])
    # list to store final items
    selected_items=[]
    # adding the 2 most expensive CPUs
    selected_items.append(d['CPU'][-2])
    budget -= d['CPU'][-2]['price']
    selected_items.append(d['CPU'][-1])
    budget -= d['CPU'][-1]['price']
    # list to store the categories except CPU
    l=[]
    for k,v in d.items():
        if k!='CPU':
            l.append(k)
    # initializing the final answer and remaining budget
    finalans=[None,budget]
    # empty list to store temporary list
    templ=[]
    # call to the recursive function
    search_all(d,l,0,budget,templ,finalans)
    # sorting the final answer by price
    finalans[0]=sorted(finalans[0],key=lambda x:x['price'])
    for i in finalans[0]:
        selected_items.append(i)
    # updating the remaining budget
    budget=finalans[1]
    return selected_items,budget

# budget for the purchase
budget = 1800
# url to get the parts list
url="https://6f5c9791-a282-482e-bbe9-2c1d1d3f4c9f.mock.pstmn.io/interview/part-list"
# get the parts list from the url
l = get_data(url)
# get the maximum purchase
result = maximum_purchase(l,budget)
# print the total number of parts
print("Total number of parts ",len(result[0]))
# print the total cost of the purchase
print("Total Cost $",budget-result[1])
# print the details of each item in the final list
for i in result[0]:
    print(i['name'],"|",i['categoryType'],"|","$",i['price'])