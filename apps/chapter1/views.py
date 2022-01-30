import io

from django.shortcuts import render

# Model Object - Single Student Data
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt


def student_detail(req, pk):
    stu = Student.objects.get(id=pk)
    serializer = StudentSerializer(stu)
    # json = JSONRenderer().render(serializer.data)
    # return HttpResponse(json, content_type='application/json')
    return JsonResponse(serializer.data)


# querty set - all student list
def student_list(req):
    stu = Student.objects.all()
    serializer = StudentSerializer(stu, many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json, content_type='application/json')
    # return JsonResponse(serializer.data, safe = False)


@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        json_data = request.body
        print(f"Request body ${json_data}")
        stream = io.BytesIO(json_data)
        py_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=py_data)
        if serializer.is_valid():
            serializer.save()
            res = {"msg": 'Saved', 'status': True}
            json_res = JSONRenderer().render(res)
            return HttpResponse(json_res, content_type='application/json')
        res = {"msg": f'{serializer.error_messages}', 'status': False, 'stack': serializer.errors}
        json_res = JSONRenderer().render(res)
        return HttpResponse(json_res, content_type='application/json')
    res = {"msg": 'Only POST request is allowed', 'status': False}
    json_res = JSONRenderer().render(res)
    return HttpResponse(json_res, content_type='application/json')
