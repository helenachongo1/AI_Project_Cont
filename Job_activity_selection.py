def activiy_selection(activity,start,end):
    combined = list(zip(activity, start, end))
    combined.sort(key=lambda x: x[2])
    
    selected_activities = [combined[0][0]]
    last_end_time = combined[0][2]
    
    for i in range(1, len(combined)):
        if combined[i][1] >= last_end_time: 
            selected_activities.append(combined[i][0])
            last_end_time = combined[i][2]
    
    return selected_activities

            
activity=['0','1','2','3','4']
start=[5,6,0,4,10]
end=[8,10,5,7,12]
res=activiy_selection(activity, start, end)
print(res)

def max_element(deadline):
    if len(deadline)==0:
        return 0
    return max(deadline)

def job_scheduling(jobs,deadline,profit):
    combined=list(zip(jobs,deadline,profit))
    combined.sort(key=lambda x:x[2],reverse=True)
    
    max_deadline=max_element(deadline)
    slots=[-1]*max_deadline
    selected_jobs=[]
    
    for job, dl, pr in combined:
        for i in range(min(dl,max_deadline)-1,-1,-1):
            if slots[i]==-1:
                slots[i]=job
                selected_jobs.append(job)
                break
    return selected_jobs
                
    
jobs=['A','B','C','D','E','F']
deadline=[2,1,3,1,2,1]
profit=[100,20,35,27,30,28]
res=job_scheduling(jobs, deadline, profit)
print(res)
    
