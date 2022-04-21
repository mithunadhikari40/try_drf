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


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, \
    RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin


class StudentList(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StudentRetrieve(GenericAPIView, RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StudentCreate(GenericAPIView, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentUpdate(GenericAPIView, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StudentDelete(GenericAPIView, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


"""two classes to handle all the requests,
for list and create we don't need PK and for update, delete and get we need pk """


class StudentListAndCreate(GenericAPIView, CreateModelMixin, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StudentUpdateAndGetAndDelete(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    """Concrete view classes, where we don't have to define get, post, update etc method. We only need to extend certail classes and we are good to go"""


from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView


class ConcreteStudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentCreate(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentRetrieve(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentUpdate(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentDestroy(DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentListCreate(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentRetrieveDestroy(RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ConcreteStudentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


"""View set example, with view-set, we define a router and router will take care of url handling
We can implement methods such as get, post, list """

from rest_framework import viewsets, status
from rest_framework.response import Response


class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        print("__________List_____________")
        print("Basename:", self.basename)
        print("Action:", self.action)
        print("Detail:", self.detail)
        print("Suffix:", self.suffix)
        print("Name:", self.name)
        print("Description:", self.description)
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        print("__________Retrieve_____________")
        print("Basename:", self.basename)
        print("Action:", self.action)
        print("Detail:", self.detail)
        print("Suffix:", self.suffix)
        print("Name:", self.name)
        print("Description:", self.description)
        if pk is not None:
            stu = Student.objects.get(id=pk)
            serializer = StudentSerializer(stu)
            return Response(serializer.data)
        return HttpResponse({'msg': 'Id is required'}, content_type='application/json')

    def create(self, request):
        print("__________Create_____________")
        print("Basename:", self.basename)
        print("Action:", self.action)
        print("Detail:", self.detail)
        print("Suffix:", self.suffix)
        print("Name:", self.name)
        print("Description:", self.description)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def udpate(self, request, pk=None):
        print("__________Update_____________")
        print("Basename:", self.basename)
        print("Action:", self.action)
        print("Detail:", self.detail)
        print("Suffix:", self.suffix)
        print("Name:", self.name)
        print("Description:", self.description)
        stu = Student.objects.get(id=pk)

        serializer = StudentSerializer(stu, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Updated'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        print("__________Partial Update_____________")
        print("Basename:", self.basename)
        print("Action:", self.action)
        print("Detail:", self.detail)
        print("Suffix:", self.suffix)
        print("Name:", self.name)
        print("Description:", self.description)
        stu = Student.objects.get(id=pk)

        serializer = StudentSerializer(stu, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Updated'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        print("__________Delete_____________")
        print("Basename:", self.basename)
        print("Action:", self.action)
        print("Detail:", self.detail)
        print("Suffix:", self.suffix)
        print("Name:", self.name)
        print("Description:", self.description)

        stu = Student.objects.get(id=pk)
        if stu is not None:
            stu.delete()

            return Response({'msg': 'Data Deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'Item Not Found'}, status=status.HTTP_201_CREATED)


"""Modal view set, where it provides all of the actions and other method"""


class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


"""We also have other model view set such as ReadOnlyModelViewSet which only allows reading, like list and retrieve"""


class StudentModelReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
