from celery.schedules import crontab

# Scheduled tasks configuration
CELERYBEAT_SCHEDULE = {
    # Marketing tasks
    'process-scheduled-campaigns': {
        'task': 'marketing.tasks.process_scheduled_campaigns',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'update-campaign-statistics': {
        'task': 'marketing.tasks.update_campaign_statistics',
        'schedule': crontab(hour='*/1'),  # Every hour
    },

    # Sales tasks
    'update-sales-forecasts': {
        'task': 'sales.tasks.update_sales_forecasts',
        'schedule': crontab(hour='0', minute='0'),  # Daily at midnight
    },
    'check-deal-deadlines': {
        'task': 'sales.tasks.check_deal_deadlines',
        'schedule': crontab(hour='9', minute='0'),  # Daily at 9 AM
    },

    # Support tasks
    'check-sla-violations': {
        'task': 'support.tasks.check_sla_violations',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'auto-assign-tickets': {
        'task': 'support.tasks.auto_assign_tickets',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes
    },

    # Report tasks
    'generate-daily-reports': {
        'task': 'reports.tasks.generate_daily_reports',
        'schedule': crontab(hour='1', minute='0'),  # Daily at 1 AM
    },
    'generate-weekly-reports': {
        'task': 'reports.tasks.generate_weekly_reports',
        'schedule': crontab(day_of_week='monday', hour='2', minute='0'),  # Weekly on Monday at 2 AM
    },
    'generate-monthly-reports': {
        'task': 'reports.tasks.generate_monthly_reports',
        'schedule': crontab(day_of_month='1', hour='3', minute='0'),  # Monthly on the 1st at 3 AM
    },

    # Integration tasks
    'sync-external-data': {
        'task': 'integrations.tasks.sync_external_data',
        'schedule': crontab(minute='0', hour='*/2'),  # Every 2 hours
    },
    'cleanup-sync-logs': {
        'task': 'integrations.tasks.cleanup_sync_logs',
        'schedule': crontab(hour='0', minute='30'),  # Daily at 00:30
    },

    # System maintenance tasks
    'cleanup-old-notifications': {
        'task': 'core.tasks.cleanup_old_notifications',
        'schedule': crontab(hour='2', minute='30'),  # Daily at 2:30 AM
    },
    'cleanup-audit-logs': {
        'task': 'core.tasks.cleanup_audit_logs',
        'schedule': crontab(day_of_month='1', hour='4', minute='0'),  # Monthly on the 1st at 4 AM
    },
    'database-maintenance': {
        'task': 'core.tasks.database_maintenance',
        'schedule': crontab(hour='3', minute='0', day_of_week='sunday'),  # Weekly on Sunday at 3 AM
    },

    # Monitoring tasks
    'check-system-health': {
        'task': 'core.tasks.check_system_health',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'monitor-api-usage': {
        'task': 'core.tasks.monitor_api_usage',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}

# Task routing
CELERYBEAT_TASK_ROUTING = {
    'marketing.*': {'queue': 'marketing'},
    'sales.*': {'queue': 'sales'},
    'support.*': {'queue': 'support'},
    'reports.*': {'queue': 'reports'},
    'integrations.*': {'queue': 'integrations'},
    'core.*': {'queue': 'core'},
}

# Task options
CELERYBEAT_TASK_OPTIONS = {
    'marketing.*': {
        'expires': 3600,  # 1 hour
        'retry': True,
        'retry_policy': {
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 300,  # 5 minutes
            'interval_max': 3600,  # 1 hour
        },
    },
    'reports.*': {
        'expires': 7200,  # 2 hours
        'retry': True,
        'retry_policy': {
            'max_retries': 2,
            'interval_start': 300,
            'interval_step': 600,
            'interval_max': 3600,
        },
    },
}