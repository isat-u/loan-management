#!/bin/bash
celery -A loan_management worker --loglevel=debug --logfile=/loan_management/logs/celery.log
