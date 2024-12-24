# hi-gcp

A Python utility package for working with Google Cloud Platform (GCP) services, primarily focusing on BigQuery operations.

## Installation

```bash
pip install higcps
```

## Features

- Easy-to-use BigQuery client wrapper
- Simplified query execution and data retrieval
- Efficient data loading and export operations

## Usage

```python
from hi_gcp import BigQueryClient

# Initialize the client

gg = BigQueryClient(
    project_id = "project_id",
    dataset_id = "dataset_id",
    table_id = "table_id",
    key_file='path/to/service_account_key.json'
)

# Execute a query
df = gg.sql2df("SELECT * FROM `project_id.dataset_id.table_id` LIMIT 100")
```

## License

MIT License