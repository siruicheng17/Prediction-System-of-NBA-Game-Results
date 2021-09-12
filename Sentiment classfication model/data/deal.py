# Process the data set, remove @, website address, and convert uppercase to lowercase.
with open("dev1.txt","r",encoding="utf-16") as f:
    data=f.readlines()
dealed_data=[]
for each in data:
    tmp = ""
    m=each.split(" ")
    for each in m:
        if "@" in each or "http" in each:
            continue
        else:
            tmp=tmp+each.lower()+" "
    dealed_data.append(tmp)
k=open("dealed.txt","a",encoding="utf-8")
for i in dealed_data:
    k.write(i)
k.close()