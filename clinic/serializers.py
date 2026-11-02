from rest_framework import serializers
from clinic.models import DoctorDb,AppoinmentDb


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDb
        fields = "__all__"
        read_only_fields = ["id"]

class Appoinment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AppoinmentDb
        fields ="__all__"
        read_only_fields = ["id"]

    def validate(self,validated_data):
        phone = validated_data.get("phone")
        appoinment_date = validated_data.get("appoinment_date")

        if AppoinmentDb.objects.filter(
            phone = phone,
            appoinment_date = appoinment_date).exists():
            raise serializers.ValidationError("Already Booked")
        else:
            return validated_data

            