from prometheus_client import Counter, Histogram

# Here you can define your custom metrics to monitor

issue_logs_invoked = Counter('django_custom_issue_logs_invoked', 'Number of issue\'s logs invokation')
milestone_logs_invoked = Histogram('django_custom_milestone_logs_invoked', 'Number of milestone\'s logs invokation', buckets=[0, 50, 200, 400, 800, 1600, 3200])