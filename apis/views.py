from django.shortcuts import render
from info.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import apis.serializers as api_ser

class DetailView(APIView):
    """
    Returns user's info.
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        try:
            user = request.user
            details = Student.objects.get(user=user)
            serializer = api_ser.DetailSerializer(details, context={'request': request})
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AttendanceView(APIView):
    """
    This view is used to return user's attendance.
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        try:
            stud = Student.objects.get(user=request.user)
            ass_list = Assign.objects.filter(class_id_id=stud.class_id)
            att_list = []
            for ass in ass_list:
                a, created = AttendanceTotal.objects.get_or_create(student=stud, course=ass.course)
                att_list.append(a)
            serializer = api_ser.AttendanceSerializer(att_list, many=True, context={'request': request})
            return Response({'user_attendance': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarksView(APIView):
    """
    This view is used to return user's marks.
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        try:
            stud = Student.objects.get(user=request.user)
            ass_list = Assign.objects.filter(class_id_id=stud.class_id)
            sc_list = []
            for ass in ass_list:
                try:
                    sc = StudentCourse.objects.get(student=stud, course=ass.course)
                    sc_list.append(sc)
                except StudentCourse.DoesNotExist:
                    pass
            sc_total = {}
            for sc in sc_list:
                for m in sc.marks_set.all():
                    sc_total[m.studentcourse.course.name] = m.marks1
            return Response({'user_marks': sc_total}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TimetableView(APIView):
    """
    This view is used to check user's class timetable.
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 24)) # Cache timetable for 24 hours
    def get(self, request):
        try:
            stud = Student.objects.get(user=request.user)
            asst = AssignTime.objects.filter(assign__class_id=stud.class_id)
            serializer = api_ser.TimeTableSerializer(asst, many=True, context={'request': request})
            return Response({'user_timetable': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'message': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
