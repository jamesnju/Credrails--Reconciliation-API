# file_recon/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import ReconciliationJob
from .serializers import FileUploadSerializer, ReconciliationResultSerializer
from .utils.reconciliation import reconcile_files
import pandas as pd
import threading
import json

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            threading.Thread(
                target=self.process_reconciliation,
                args=(job.id,),
                daemon=True
            ).start()
            return Response({
                'job_id': job.id,
                'status': job.status,
                'message': 'Reconciliation job started'
            }, status=202)
        return Response(serializer.errors, status=400)

    def process_reconciliation(self, job_id):
        job = ReconciliationJob.objects.get(id=job_id)
        job.status = 'PROCESSING'
        job.save(update_fields=['status'])
        
        try:
            # Read files
            source_df = pd.read_csv(job.source_file.path)
            target_df = pd.read_csv(job.target_file.path)
            
            # Use first column as key if not specified
            key_columns = [source_df.columns[0]]
            
            # Perform reconciliation
            result = reconcile_files(source_df, target_df, key_columns)
            
            # Handle reconciliation errors
            if result.get('error'):
                raise ValueError(result['error'])
            
            # Update job with results
            job.result = result
            job.status = 'COMPLETED'
            
        except Exception as e:
            job.status = 'FAILED'
            job.errors = str(e)
        finally:
            job.completed_at = timezone.now()
            job.save()
class ReconciliationResultView(APIView):
    def get(self, request, job_id, format=None):
        job = get_object_or_404(ReconciliationJob, id=job_id)
        serializer = ReconciliationResultSerializer(job)
        return Response(serializer.data)