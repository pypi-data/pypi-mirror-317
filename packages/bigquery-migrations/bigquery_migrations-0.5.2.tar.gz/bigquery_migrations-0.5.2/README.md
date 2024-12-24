# python-bigquery-migrations

The `python-bigquery-migrations` package provides a streamlined way to create and manage BigQuery databases using intuitive CLI commands, such as the following:

```bash
bigquery-migrations run
```

**What are the benefits of using migrations?**

Migrations are like version control for your database, allowing you to define and share the application's datasets and table schema definitions.

## Getting Started

## 0. Prerequisite

- Google Cloud Project with enabled billing
- Enabled Google Cloud BigQuery API
- Google Cloud Service Account JSON file

## 1. Install
```
pip install bigquery-migrations
```

## 2. Create the project folder structure

Create two subdirectory:
1. credentials
2. migrations

```
your-project-root-folder
├── credentials
├── migrations
└── ...
```

## 3. Create the neccessary files in the folders

### Google Cloud Service Account JSON file

Put your Google Cloud Service Account JSON file in the credentials subdirectory. See more info in the [Authorize BigQuery Client section](#authorize-bigquery-client)

```
your-project
├── credentials
│   ├── gcp-sa.json
├── migrations
└── ...
```

You can use different folder name and file name but in that case you must specify them with command arguments, such as the following:

```bash
bigquery-migrations run --gcp-sa-json-dir  my-creds --gcp-sa-json-fname my-service-account.json
```

|argument             |description                                                |
|---------------------|-----------------------------------------------------------|              
|--gcp-sa-json-dir    |Name of the service account JSON file directory (optional) |
|--gcp-sa-json-fname  |Name of the service account JSON file (optional)           |

> **IMPORTANT!**  
> Never check the Google Cloud Service Account JSON file into version control. This file contains sensitive credentials that could compromise your Google Cloud account if exposed.

To prevent accidental commits, make sure to add the file to your .gitignore configuration. For example:

```bash
# .gitignore
gcp-sa.json
```

By ignoring this file, you reduce the risk of unintentional leaks and maintain secure practices in your repository.

### Migrations

Create your own migrations and put them in the migrations directory. See the [Migration structure section](#migration-structure) and [Migration naming conventions section](#migration-naming-conventions) for more info.

```
your-project
├── credentials
│   ├── gcp-sa.json
├── migrations
│   ├── 2024_12_01_120000_create_users_table.py
└── ...
```

You can use different folder name but in that case you must specify it with a command argument:

```bash
bigquery-migrations run --migrations-dir bq-migrations
```

|argument             |description                                                |
|---------------------|-----------------------------------------------------------|              
|--migrations-dir     |Name of the migrations directory (optional)                |


## Running migrations

> **IMPORTANT!**  
> You have to create your own Migrations first! [Jump to Creating Migrations section](#creating-migrations)

To run all of your outstanding migrations, execute the `run` command:

```bash
bigquery-migrations run
```

You can specify the Google Cloud Project id with the `--gcp-project-id` argument:

```bash
bigquery-migrations run --gcp-project-id your-gcp-id
```

### Migration log

> **IMPORTANT!**  
> It's cruical to keep the migration_log.json file in place, and not to modify it manualy!

After the first successful run a migration_log.json is created in the migrations directory.

```
your-project
├── migrations
│   ├── 2024_12_01_120000_create_users_table.py
    ├── migration_log.json
...
```

The migration_log.json file content should look like this:
```json
{
    "last_migration": "2024_12_10_121000_create_users_table",
    "timestamp": "2024-12-18T12:25:54.318426+00:00"
}
```


## Rolling Back Migrations

### Rollback the last migration

To reverse the last migration, execute the `rollback` command and pass `last` with the `--migration-name` argument:

```bash
bigquery-migrations rollback --migration-name last
```

### Rollback a specific migration

To reverse a specific migration, execute the `rollback` command and pass the migration name with the `--migration-name` argument:

```bash
bigquery-migrations rollback --migration-name 2024_12_10_121000_create_users_table
```

### Rollback all migrations

To reverse all of your migrations, execute the `reset` command:

```bash
bigquery-migrations reset
```

## Authorize BigQuery Client

Put your service account JSON file in the credentials subdirectory in the root of your project.

```
your-project
├── credentials
│   ├── gcp-sa.json
...
```

### Creating a Service Account for Google BigQuery

You can connect to BigQuery with a user account or a service account. A service account is a special kind of account designed to be used by applications or compute workloads, rather than a person. Service accounts don’t have passwords and use a unique email address for identification.

To create a BigQuery service account key

1. Sign in to the [Google Cloud management console](https://console.cloud.google.com/).
1. Make sure that you have API enabled on your [BigQuery API](https://console.cloud.google.com/apis/library/bigquery.googleapis.com) page. If you don’t see API Enabled, choose Enable.
1. On the Service accounts page, choose your BigQuery project, and then choose Create service account.
1. On the [Service account](https://console.cloud.google.com/iam-admin/serviceaccounts) details page, enter a descriptive value for Service account name. Choose Create and continue. The Grant this service account access to the project page opens.
1. For Select a role, choose BigQuery, and then choose BigQuery Admin.
1. Choose Continue, and then choose Done.
1. On the [Service account](https://console.cloud.google.com/iam-admin/serviceaccounts) page, choose the service account that you created.
1. Choose Keys, Add key, Create new key.
1. Choose JSON, and then choose Create. Choose the folder to save your private key or check the default folder for downloads in your browser.

## Creating migrations

Put your migrations files in the migrations subdirectory of the root of your project.

```
your-project
├── migrations
│   ├── 2024_12_01_120000_create_users_table.py
...
```

### Migration structure

The migration class must contain two methods: `up` and `down`.

The `up` method is used to add new dataset, tables, columns etc. to your BigQuery project, while the `down` method should reverse the operations performed by the up method.

```python
from google.cloud import bigquery
from bigquery_migrations import Migration

class CreateUsersTable(Migration):
    """
    See:
    https://github.com/googleapis/python-bigquery/tree/main/samples
    """

    def up(self):
        # TODO: Set table_id to the ID of the table to create.
        table_id = "your_project.your_dataset.example_table"
        
        # TODO: Define table schema
        schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="NULLABLE"),
        ]
        table = bigquery.Table(table_id, schema=schema)
        table = self.client.create_table(table)
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )

    def down(self):
        # TODO: Set table_id to the ID of the table to fetch.
        table_id = "your_project.your_dataset.example_table"
        
        # If the table does not exist, delete_table raises
        # google.api_core.exceptions.NotFound unless not_found_ok is True.
        self.client.delete_table(table_id, not_found_ok=True)
        print("Deleted table '{}'.".format(table_id))
```

### Migration naming conventions

|Pattern              |yyyy_mm_dd_hhmmss_your_class_name.py    |
|---------------------|----------------------------------------|              
|Example filename     |2024_12_10_120000_create_users_table.py |
|Example class name   |CreateUsersTable                        |
