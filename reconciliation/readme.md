# CSV Reconciliation API

A Django REST API for comparing CSV files and identifying discrepancies between source and target datasets.

## Features

- Upload source and target CSV files via API
- Background processing of file comparisons
- Comprehensive discrepancy reporting:
  - Missing records in source/target
  - Field-level differences
  - Statistical summary
- Json interface for visual results
## use postman for testing the ap
-upload
  curl -X POST -F "source_file=@source.csv" -F "target_file=@target.csv" http://localhost:8000/api/upload/
-view
  http://127.0.0.1:8000/api/results/7
## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/jamesnju/Credrails--Reconciliation-API.git
cd reconciliation-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install django djangorestframework pandas

# Setup database
python manage.py makemigrations
python manage.py migrate

# Run development server
python manage.py runserver