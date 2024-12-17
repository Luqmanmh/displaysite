from rest_framework import serializers
from displaysite.models import *


class patdataSerializer(serializers.ModelSerializer):
    pat_owner = serializers.CharField()
    
    class Meta:
        model = patientdata
        fields = ['pat_owner', 'jsondata']
        
    def create(self, validated_data):
        
        pat_owner_id = validated_data.pop('pat_owner')

        try:
            pat_owner_instance = Patient.objects.get(pk=int(pat_owner_id))
        except Patient.DoesNotExist:
            raise serializers.ValidationError({"pat_owner": "Patient not found."})
        
        
        pat = Patient.objects.get(pk = int(pat_owner_id))
        if pat:
            pat.newest_update = datetime.now()
            pat.save()
            
            
        instance = patientdata.objects.create(pat_owner=pat_owner_instance, **validated_data)
        
        return instance
        
