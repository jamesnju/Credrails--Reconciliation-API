# file_recon/urls.py
from django.urls import path
from .views import FileUploadView, ReconciliationResultView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('results/<int:job_id>/', ReconciliationResultView.as_view(), name='reconciliation-results'),
]

# reconciliation/urls.py
# file_recon/urls.py

from django.urls import path
from .views import FileUploadView, ReconciliationResultView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('results/<int:job_id>/', ReconciliationResultView.as_view(), name='reconciliation-results'),
]