import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

# Create the Celery app
app = Celery('crm_project')

# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configure task routes
app.conf.task_routes = {
    # Contact tasks
    'contacts.tasks.*': {'queue': 'contacts'},
    
    # Sales tasks
    'sales.tasks.*': {'queue': 'sales'},
    
    # Marketing tasks
    'marketing.tasks.send_campaign_email': {'queue': 'marketing_email'},
    'marketing.tasks.process_campaign': {'queue': 'marketing'},
    'marketing.tasks.execute_automation': {'queue': 'marketing_automation'},
    
    # Support tasks
    'support.tasks.*': {'queue': 'support'},
    
    # Report tasks
    'reports.tasks.generate_report': {'queue': 'reports'},
    'reports.tasks.schedule_reports': {'queue': 'reports_scheduler'},
    
    # Integration tasks
    'integrations.tasks.sync_data': {'queue': 'integrations'},
    'integrations.tasks.process_webhook': {'queue': 'webhooks'},
    
    # Default queue for all other tasks
    '*': {'queue': 'default'},
}

# Configure task time limits
app.conf.task_time_limit = 3600  # 1 hour
app.conf.task_soft_time_limit = 3000  # 50 minutes

# Configure task retries
app.conf.task_max_retries = 3
app.conf.task_retry_delay = 300  # 5 minutes

# Configure task result backend
app.conf.result_expires = 86400  # 24 hours

# Configure task serialization
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Configure task logging
app.conf.worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
app.conf.worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s'

@app.task(bind=True)
def debug_task(self):
    """
    Debug task to verify Celery is working.
    """
    print(f'Request: {self.request!r}')