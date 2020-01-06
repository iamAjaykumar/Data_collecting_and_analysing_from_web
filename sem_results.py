import requests as re
from bs4 import BeautifulSoup
import pandas as pd
cgpa_all=[]
#id_nos file to list
f=open("id_ce.txt")
id_list=[]
for i in f:
    i=i.strip()
    id_list.append(i)
#print(len(id_list))
#from openpyxl import Workbook
final_marks=[]
#check_id=["N160137","N160154","N160195","N160196","N160050","N160314"]
for id_num in id_list:

    url_token="https://examcell.rguktn.ac.in/results/201920s1-regular/"
    result=re.get(url_token)
    #print(result.text)
    soup=BeautifulSoup(result.content,"html.parser")
    token_value = soup.find('input', {'id': 'token'}).get('value')
    #print("Token: ",token_value)
    token_value=token_value.replace("+"," ")
    print("Token=",token_value)
    result_url="https://examcell.rguktn.ac.in/results/201920s1-regular/getResult.php"
    headers_url={"x-requested-with": "XMLHttpRequest"}
    data_url={"SID": id_num,"token":token_value}
    like=re.post(url=result_url,data=data_url,headers=headers_url)
    #print(like.text)
    #to find examds and marks of 
    fields=BeautifulSoup(like.text,"html.parser")
    subjects=[]
    marks=[]
    exams=fields.find_all("td",class_="")
    for i in exams:
        subjects.append(i.text)
    #print(subjects)
    marks_filed=fields.find_all("td",class_="text-center")
    for j in marks_filed:
        marks.append(j.text)
    #print(marks)
    grade=[marks[i] for i in range(len(marks)) if i%4==3]
    print("grade",grade)
    final_marks.append(list(grade))
    print(id_num)
print(final_marks)

sa=[]
he=[]
wre=[]
sm=[]
ct=[]
ctl=[]
sml=[]
eng=[]
ewl=[]
for i in range(len(final_marks)):
    if len(final_marks[i])==0:
        final_marks[i].append(0)
        final_marks[i]=final_marks[i]*9

    if len(final_marks[i])>0:

        sa.append(final_marks[i][0])
        he.append(final_marks[i][1])
        wre.append(final_marks[i][2])
        sm.append(final_marks[i][3])
        ct.append(final_marks[i][4])
        ctl.append(final_marks[i][5])
        sml.append(final_marks[i][6])
        eng.append(final_marks[i][7])
        ewl.append(final_marks[i][8])
#calculate cgpa of every user
def cgpacal(a):
    for i in a:
        if i=='Ex':
            a[a.index(i)]=10
        if i=="A":
            a[a.index(i)]=9
        if i=="B":
            a[a.index(i)]=8
        if i=="C":
            a[a.index(i)]=7
        if i=="D":
            a[a.index(i)]=6
        if i=="R":
            return "Failed"
        if i=="WH":
            return "Failed"
        if i=="AB":
            return "Absent"
    a= [a[i]*4 if i<4 else a[i]*2 for i in range(len(a))]
    b=a[0:9]
    cg=(sum(b)/26)
    return ("%.2f"%cg)
#print(cgpacal([['A','A','A','A','A','A','A','A','A']]))

for i in range(len(final_marks)):
    bb=cgpacal(final_marks[i])
    if bb=="Failed":
        cgpa_all.append(bb)
    elif bb=="Absent":
        cgpa_all.append(bb)
    else:
        cc=float(bb)
        cgpa_all.append(cc)
    #cgpa_all.append(float(cgpacal(final_marks[i])))


print(cgpa_all)

cgpa=[]








#this is excel part 


writer = pd.ExcelWriter('civil.xlsx', engine='openpyxl') 
wb  = writer.book


df=pd.DataFrame({
    "id":id_list,
    'Structural Analysis':sa ,
    'Hydraulics Engineering':he,
    'Water Resources Engineering':wre,
    'Soil Mechanics':sm,
    'Concrete Technology':ct,
    'Concrete Technology Lab':ctl,
    'Soil Mechanics Lab':sml,
    'English Language Laboratory III':eng,
    'Engineering Workshop Laboratory':ewl,
    'CGPA':cgpa_all
    
})
df.to_excel(writer, index=False)
wb.save("civilall.xlsx")
print("Successfully created the Excel sheet :) ")
