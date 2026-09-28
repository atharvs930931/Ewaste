from django.http import HttpResponse
from django.shortcuts import render


def myproject(request):
    data={
        'numbers':[10,20,30,40,],
        'stud_detail':[
           {'name':'sham','phone':1223123},
           {'name':'ram','phone':3423422},
        ]

    }
    return render(request,'index.html',data)