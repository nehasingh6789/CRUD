from django.shortcuts import render,HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Employee
from .serializers import EmployeeSerializer
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import io
def homePage(Request):
    return render(Request,"index.html")

@csrf_exempt
def createRecord(Request):
    jsonData = Request.body
    stream = io.BytesIO(jsonData)
    pythonData = JSONParser().parse(stream)
    empSerilalizer = EmployeeSerializer(data=pythonData)
    if(empSerilalizer.is_valid()):
        empSerilalizer.save()
        msg = {"result":"Done","message":"Record is Crated!!!"}
    else:
        msg = {"result":"Fail","message":"Invalid Record!!!"}
    return HttpResponse(JSONRenderer().render(msg),content_type="application/json")


def getRecord(Request):
    data = Employee.objects.all()
    dataSerializer = EmployeeSerializer(data,many=True)
    return HttpResponse(JSONRenderer().render(dataSerializer.data),content_type="application/json")


@csrf_exempt
def updateRecord(Request,id):
    jsonData = Request.body
    stream = io.BytesIO(jsonData)
    pythonData = JSONParser().parse(stream)
    try:
        emp = Employee.objects.get(id=id)
        empSerilalizer = EmployeeSerializer(emp,data=pythonData,partial=True)
        if(empSerilalizer.is_valid()):
            empSerilalizer.save()
            msg = {"result":"Done","message":"Record is Updated!!!"}
        else:
            msg = {"result":"Fail","message":"Invalid Record!!!"}
    except:
        msg = {"result":"Fail","message":"Invalid Id!!!"}
    return HttpResponse(JSONRenderer().render(msg),content_type="application/json")

def deleteRecord(Request,id):
    try:
        emp = Employee.objects.get(id=id)
        emp.delete()
        msg = {"result":"Done","message":"Record is Deleted!!!"}
    except:
        msg = {"result":"Done","message":"Id Not Valid!!!"}
    return HttpResponse(JSONRenderer().render(msg),content_type="application/json")