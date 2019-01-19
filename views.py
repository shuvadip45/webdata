from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db import connection
import os
import matplotlib.pyplot as plt


cursor = connection.cursor()


def home(request):
    if os.path.isfile("static/MaleFemale.png"):
        os.remove("static/MaleFemale.png")
    if os.path.isfile("static/RelationshipStatus.png"):
        os.remove("static/RelationshipStatus.png")
    sql1="SELECT COUNT(*) FROM adultdata WHERE \" sex\"=\" Male\""
    sql2="SELECT COUNT(*) FROM adultdata WHERE \" sex\"=\" Female\""
    labels='Male','Female'
    cursor.execute(sql1)
    data=cursor.fetchall()
    c1=data[0]
    cursor.execute(sql2)
    data=cursor.fetchall()
    c2=data[0]
    sizes = [c1[0], c2[0]]
    colors = ['blue', 'lightcoral']
    explode = (0.1, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('static/MaleFemale.png')
    sql3="select count(*) from adultdata group by \" relationship\""
    labels='Husband', 'Not-in-family', 'Other-relative', 'Own-child', 'Unmarried', 'Wife'
    cursor.execute(sql3)
    data=cursor.fetchall()
    c1=data[0]
    c2=data[1]
    c3=data[2]
    c4=data[3]
    c5=data[4]
    c6=data[5]
    sizes = [c1[0], c2[0], c3[0], c4[0], c5[0], c6[0]]
    colors = ['blue', 'lightcoral', 'green', 'red', 'yellowgreen', 'lightskyblue']
    explode = (0.1, 0, 0, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('static/RelationshipStatus.png')
    return render(request, 'home.html')



def getdisplay(request):
    sql="SELECT * FROM adultdata"
    cursor.execute(sql)
    data=cursor.fetchall()
    return render(request, "display.html", {'data': data})

def processrequest(request):
    sql="SELECT * FROM adultdata "
    count=0
    if request.method == 'POST':
        if request.POST['Sex']:
            sql+="WHERE \" sex\"=\" %s\"" % request.POST['Sex']
            count+=1
        else:
            pass
        if request.POST['Race'] and count>0:
            sql+=" AND \" race\"=\" %s\"" % request.POST['Race']
            count+=1
        elif request.POST['Race'] and count==0:
            sql+="WHERE \" race\"=\" %s\"" % request.POST['Race']
            count+=1
        else:
            pass
        if request.POST['Relationship'] and count>0:
            sql+=" AND \" relationship\"=\" %s\"" % request.POST['Relationship']
            count+=1
        elif request.POST['Relationship'] and count==0:
            sql+="WHERE \" relationship\"=\" %s\"" % request.POST['Relationship']
            count+=1
        else:
            pass
    cursor.execute(sql)
    data=cursor.fetchall()
    return render(request, "display.html", {'data': data})
