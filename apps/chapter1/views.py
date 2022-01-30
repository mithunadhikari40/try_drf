import io

from django.shortcuts import render

# Model Object - Single Student Data
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class StudentApiView(View):
    def get(self, request, *args, **kwargs):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            py_data = JSONParser().parse(stream)
            stu_id = py_data.get('id', None)

            if stu_id is not None:
                students = Student.objects.get(id=stu_id)
            else:
                students = Student.objects.all()
            serializer = StudentSerializer(students, many=stu_id is None)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            print(f"the exception {e}")
            return HttpResponse(JSONRenderer().render({"error": str(e)}), content_type='application/json')

        # json = JSONRenderer().render(serializer.data)
        # return HttpResponse(json, content_type='application/json')

    def list(self, request, *args, **kwargs):
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json, content_type='application/json')
        # return JsonResponse(serializer.data, safe = False)

    def post(self, request, *args, **kwargs):
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

    def put(self, request, *args, **kwargs):
        try:
            json_data = request.body
            print(f"Request body ${json_data}")
            stream = io.BytesIO(json_data)
            py_data = JSONParser().parse(stream)
            stu_id = py_data.get('id', None)
            if stu_id is None:
                res = {"msg": 'Id is required for update', 'status': False}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            student = Student.objects.get(id=stu_id)
            if student is None:
                res = {"msg": 'Could not find a student with the given id', 'status': False}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            """Indicates whether we have to pass every field for update or not,
             partial = True/False determines whether we need to update every field or not"""
            serializer = StudentSerializer(student, data=py_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {"msg": 'Updated', 'status': True, 'data': serializer.data}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            res = {"msg": f'{serializer.error_messages}', 'status': False, 'stack': serializer.errors}
            json_res = JSONRenderer().render(res)
            return HttpResponse(json_res, content_type='application/json')
        except Exception as e:
            print(f"the exception {e}")
            return HttpResponse(JSONRenderer().render({"error": str(e)}), content_type='application/json')

    def delete(self, request, *args, **kwargs):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            py_data = JSONParser().parse(stream)
            stu_id = py_data.get('id', None)

            if stu_id is None:
                res = {"msg": 'Id is required', 'status': False}
                return JsonResponse(res)
            student = Student.objects.get(id=stu_id)
            if student is None:
                res = {"msg": 'Could not find a student with the given id', 'status': False}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            student.delete()
            res = {"msg": 'Deleted', 'status': True}
            json_res = JSONRenderer().render(res)
            return HttpResponse(json_res, content_type='application/json')

        except Exception as e:
            print(f"the exception {e}")
            return HttpResponse(JSONRenderer().render({"error": str(e)}), content_type='application/json')

        # json = JSONRenderer().render(serializer.data)
        # return HttpResponse(json, content_type='application/json')


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


def get_student(request):
    if request.method == 'GET':
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            py_data = JSONParser().parse(stream)
            stu_id = py_data.get('id', None)

            if stu_id is not None:
                students = Student.objects.get(id=stu_id)
            else:
                students = Student.objects.all()
            serializer = StudentSerializer(students, many=stu_id is None)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            print(f"the exception {e}")
            return HttpResponse(JSONRenderer().render({"error": str(e)}), content_type='application/json')

        # json = JSONRenderer().render(serializer.data)
        # return HttpResponse(json, content_type='application/json')
    res = {"msg": 'Only GET request is allowed', 'status': False}
    return JsonResponse(res)


@csrf_exempt
def update_student(request):
    if request.method == 'PUT':
        try:
            json_data = request.body
            print(f"Request body ${json_data}")
            stream = io.BytesIO(json_data)
            py_data = JSONParser().parse(stream)
            stu_id = py_data.get('id', None)
            if stu_id is None:
                res = {"msg": 'Id is required for update', 'status': False}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            student = Student.objects.get(id=stu_id)
            if student is None:
                res = {"msg": 'Could not find a student with the given id', 'status': False}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            """Indicates whether we have to pass every field for update or not,
             partial = True/False determines whether we need to update every field or not"""
            serializer = StudentSerializer(student, data=py_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {"msg": 'Updated', 'status': True, 'data': serializer.data}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            res = {"msg": f'{serializer.error_messages}', 'status': False, 'stack': serializer.errors}
            json_res = JSONRenderer().render(res)
            return HttpResponse(json_res, content_type='application/json')
        except Exception as e:
            print(f"the exception {e}")
            return HttpResponse(JSONRenderer().render({"error": str(e)}), content_type='application/json')

    res = {"msg": 'Only PUT request is allowed', 'status': False}
    json_res = JSONRenderer().render(res)
    return HttpResponse(json_res, content_type='application/json')


@csrf_exempt
def delete_student(request):
    if request.method == 'DELETE':
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            py_data = JSONParser().parse(stream)
            stu_id = py_data.get('id', None)

            if stu_id is None:
                res = {"msg": 'Id is required', 'status': False}
                return JsonResponse(res)
            student = Student.objects.get(id=stu_id)
            if student is None:
                res = {"msg": 'Could not find a student with the given id', 'status': False}
                json_res = JSONRenderer().render(res)
                return HttpResponse(json_res, content_type='application/json')
            student.delete()
            res = {"msg": 'Deleted', 'status': True}
            json_res = JSONRenderer().render(res)
            return HttpResponse(json_res, content_type='application/json')

        except Exception as e:
            print(f"the exception {e}")
            return HttpResponse(JSONRenderer().render({"error": str(e)}), content_type='application/json')

        # json = JSONRenderer().render(serializer.data)
        # return HttpResponse(json, content_type='application/json')
    res = {"msg": 'Only DELETE request is allowed', 'status': False}
    return JsonResponse(res)
