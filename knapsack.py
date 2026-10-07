def knapsack_fraq(price,wt,capacity):
    ratio=[(price[i]/wt[i],i) for i in range(len(wt))]
    ratio.sort(reverse=True)
    
    wt_sorted=[wt[i[1]] for i in ratio]
    price_sorted=[price[i[1]] for i in ratio]
    
    gain=0 
    for i in range(len(wt_sorted)):
        if wt_sorted[i]<=capacity:
            gain+=price_sorted[i]
            capacity-=wt_sorted[i]
        else:
            fra=capacity/wt_sorted[i]
            capacity=0 
            gain+=price_sorted[i]*fra
    return gain

price=[10,5,3,2,8,7,11]
wt=[2,3,1,4,3,2,7]
capacity=8
res=knapsack_fraq(price, wt, capacity)
print(res)


def snapsack_01(price,weight,capacity):
    ratio=[(price[i]/weight[i],i) for i in range(len(weight))]
    combined = [(price[i], weight[i], ratio[i][0]) for i in range(len(weight))]
    #combined = list(zip(price,weight,ratio))
    combined.sort(key=lambda x:x[2],reverse=True)
    gain=0 
    result=[]
    for i in range(len(combined)):
        if(combined[i][1]<=capacity):
            result.append(combined[i][1])
            gain+=combined[i][0]
            capacity-=combined[i][1]
    return (result,gain)

price=[10,5,3,2,8,7,11]
weight=[2,3,1,4,3,2,7]
capacity=7
res=snapsack_01(price, weight, capacity)
print(res)

