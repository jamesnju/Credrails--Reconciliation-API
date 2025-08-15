# file_recon/models.py
from django.db import models

class ReconciliationJob(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    source_file = models.FileField(upload_to='source_files/')
    target_file = models.FileField(upload_to='target_files/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Reconciliation Job #{self.id}"