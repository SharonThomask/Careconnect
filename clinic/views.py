from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDb,AppoinmentDb
from clinic.serializers import DoctorSerializer,Appoinment_Serializer
from datetime import time,timedelta,datetime
from rest_framework import serializers

# Create your views here.

class DoctorListCreateView(APIView):
    def get(self,request):
        qs = DoctorDb.objects.all()
        serializer_instance = DoctorSerializer(qs,many = True)
        return Response(data = serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = DoctorSerializer(data = form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = serializer_instance.data)
        else:
            return Response(data = serializer_instance.errors)


class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(DoctorDb,id=pk)
        serializer_instance = DoctorSerializer(qs)
        return Response(data = serializer_instance.data)

    def put(self,request,pk):
        form_data =request.data
        doctor_object = get_object_or_404(DoctorDb,id=pk)
        serializer_instance = DoctorSerializer(data =form_data,instance = doctor_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = serializer_instance.data)
        else:
            return Response(data = serializer_instance.errors)

    def delete(self,request,pk):
        doctor_obj = get_object_or_404(DoctorDb,id=pk)
        doctor_obj.delete()
        return Response(data={
            "Message" : "Deleted Succesfully..!"
        })

class AppoinmentListCreateView(APIView):
    def get(self,request):
        qs = AppoinmentDb.objects.all()
        serializer_instance =Appoinment_Serializer(qs,many=True)
        return Response(data = serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = Appoinment_Serializer(data= form_data)
        if serializer_instance.is_valid():
            appoinment_date = serializer_instance.validated_data.get("appoinment_date")
            doctor_id= serializer_instance.validated_data.get("doctor_id")
            last_appoinment= AppoinmentDb.objects.filter(appoinment_date=appoinment_date,doctor_id=doctor_id).order_by("-token_number").first()
            if last_appoinment is None:
                form_data["token_number"] =1
                form_data["appoinment_time"]=time(10,0) 
            else:
                form_data["token_number"] =last_appoinment.token_number+1
                current_time = datetime.combine(appoinment_date,last_appoinment.appoinment_time)
                next_time = current_time+timedelta(minutes=15)

                #adding lunch break
                if next_time.time()==time(12,30):
                    next_time = datetime.combine(appoinment_date,time(13,30))
                form_data["appoinment_time"] = next_time

                #slot completion

                if next_time.time()==time(10,30):
                    raise serializers.ValidationError("No Slots Available Today..!")


            qs = AppoinmentDb.objects.create(**form_data)
            serializer_instance=Appoinment_Serializer(qs)
            return Response(data={
                "Status"  : "Booking Successfull..!",
                "Token_Number" :form_data["token_number"],
                "Appoinment_Time" : form_data["appoinment_time"]
            })
        else:
            return Response(data=serializer_instance.errors)

            