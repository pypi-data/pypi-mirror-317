import logging

from gc_google_services_api.bigquery import BigQueryManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class BigQueryExporter:
    """
    Initializes the Bigquery exporter with the given project ID and dataset ID.

    Args:
        project_id (str): The ID of the Google Cloud project.
        dataset_id (str): The ID of the BigQuery dataset.
    """

    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = BigQueryManager(
            project_id=project_id,
            dataset_id=dataset_id,
        )
        self.batch_size = 200
        self.schemas = {
            "products": {
                "id": "STRING",
                "name": "STRING",
                "product_code": "STRING",
                "description": "STRING",
                "is_active": "BOOLEAN",
                "family": "STRING",
                "currency_iso_code": "STRING",
                "external_data_source_id": "STRING",
                "quantity_unit_of_measure": "STRING",
                "is_deleted": "BOOLEAN",
                "is_archived": "BOOLEAN",
                "product_type": "STRING",
                "record_id": "STRING",
                "profit_center_id": "STRING",
            },
        }

        for table_name, table_schema in self.schemas.items():
            self.client.create_table_if_not_exists(table_name, table_schema)

    def _execute_query(self, query, log_id, default_error_value=None):
        custom_error_value = f"{log_id}_custom_error"

        result = self.client.execute_query(
            query,
            custom_error_value,
        )

        if result == custom_error_value:
            logging.error(
                f"[ERROR - _execute_query]: Error executing query for {log_id} in BigQuery."  # noqa: E501
            )
            result = default_error_value

        return result

    def export_data(self, products):
        self.client.load_massive_data(
            rows_to_insert=products,
            table_name="products",
        )

    def delete_all_rows(self):
        table_names = self.schemas.keys()
        for table_name in table_names:
            delete_query_table = f"DELETE FROM `{self.project_id}.{self.dataset_id}.{table_name}` WHERE true"  # noqa: E501
            self._execute_query(
                query=delete_query_table,
                log_id=f"delete_table_{table_name}",
            )
