workers = 4  # Number of Gunicorn worker processes
bind = '0.0.0.0:8000'  # IP address and port to bind Gunicorn to
timeout = 120  # Request timeout in seconds
loglevel = 'info'  # Logging level: debug, info, warning, error, critical
