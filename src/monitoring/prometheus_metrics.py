from prometheus_client import Counter, Histogram, Gauge

pipeline_runs = Counter(
    'pipeline_runs_total',
    'Total pipeline runs',
    ['status', 'dataset']
)

pipeline_duration = Histogram(
    'pipeline_duration_seconds',
    'Pipeline execution duration'
)

active_pipelines = Gauge(
    'active_pipelines',
    'Currently running pipelines'
)

data_quality_score = Gauge(
    'data_quality_score',
    'Latest data quality score',
    ['dataset']
)
