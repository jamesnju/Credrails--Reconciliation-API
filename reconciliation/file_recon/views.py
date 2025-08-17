# file_recon/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
import pandas as pd
from .models import ReconciliationJob
from .serializers import FileUploadSerializer, ReconciliationResultSerializer
from .utils.reconciliation import reconcile_files
import threading

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            
            # Process in background
            threading.Thread(target=self.process_reconciliation, args=(job.id,)).start()
            
            return Response({
                'job_id': job.id,
                'status': job.status,
                'message': 'Reconciliation job started'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def process_reconciliation(self, job_id):
        job = ReconciliationJob.objects.get(id=job_id)
        job.status = 'PROCESSING'
        job.save()
        
        try:
            # Read files
            source_df = pd.read_csv(job.source_file.path)
            target_df = pd.read_csv(job.target_file.path)
            
            # Assume first column is key for simplicity
            key_columns = [source_df.columns[0]]
            
            # Reconcile
            result = reconcile_files(source_df, target_df, key_columns)
            
            job.result = result
            job.status = 'COMPLETED'
        except Exception as e:
            job.status = 'FAILED'
            job.errors = str(e)
        finally:
            job.save()

class ReconciliationResultView(APIView):
    def get(self, request, job_id, format=None):
        job = get_object_or_404(ReconciliationJob, id=job_id)
        serializer = ReconciliationResultSerializer(job)
        return Response(serializer.data)