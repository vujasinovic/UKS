from prometheus_client import Counter, Histogram

# Here you can define your custom metrics to monitor
issue_logs_invoked = Counter('django_custom_issue_logs_invoked', 'Number of issue\'s logs invokation')
issue_created = Counter('django_custom_issue_created', 'Number of issue\'s creation')
issue_updated = Counter('django_custom_issue_updated', 'Number of issue\'s update')

milestone_logs_invoked = Counter('django_custom_milestone_logs_invoked', 'Number of milestone\'s logs invokation')
milestone_created = Counter('django_custom_milestone_created', 'Number of milestone\'s creation')
milestone_updated = Counter('django_custom_milestone_updated', 'Number of milestone\'s update')

milestone_logs_invoked_histogram = Histogram('django_custom_milestone_logs_invoked_hist', 'Number of milestone\'s logs invokation', buckets=[0, 50, 200, 400, 800, 1600, 3200])