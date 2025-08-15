# file_recon/serializers.py
from rest_framework import serializers
from .models import ReconciliationJob

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationJob
        fields = ['source_file', 'target_file']
        
class ReconciliationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationJob
        fields = ['id', 'status', 'created_at', 'completed_at', 'result', 'errors']