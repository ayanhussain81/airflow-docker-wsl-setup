from __future__ import annotations
import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task

log = logging.getLogger(__name__)


default_args = {
    "owner": "data-engineering-class",   # shown in the UI
    "retries": 2,                         # retry up to 2 times on failure
    "retry_delay": timedelta(minutes=1),  # wait 1 minute between retries
    "email_on_failure": False,            # set True + configure SMTP for email alerts
    "email_on_retry": False,
}


@dag(
    dag_id="sample_etl_pipeline",
    description="A 4-task ETL pipeline teaching example (Airflow 3.x)",
    schedule="@daily",                  # runs once per day
    start_date=datetime(2024, 1, 1),
    catchup=False,                      # don't backfill old runs
    default_args=default_args,
    tags=["etl", "teaching", "example"],
)
def sample_etl_pipeline():

    @task(task_id="extract_data")
    def extract_data() -> list[dict]:
        log.info("Connecting to source system and fetching raw data...")

        raw_records = [
            {"id": 1,  "product": "Laptop",     "quantity": 2,  "unit_price": 1200.00, "status": "completed"},
            {"id": 2,  "product": "Mouse",       "quantity": 5,  "unit_price": 25.00,   "status": "completed"},
            {"id": 3,  "product": "Keyboard",    "quantity": 3,  "unit_price": 75.00,   "status": "cancelled"},
            {"id": 4,  "product": "Monitor",     "quantity": 1,  "unit_price": 450.00,  "status": "completed"},
            {"id": 5,  "product": "Headphones",  "quantity": 4,  "unit_price": 90.00,   "status": "completed"},
            {"id": 6,  "product": "Webcam",      "quantity": 2,  "unit_price": 60.00,   "status": "pending"},
            {"id": 7,  "product": "USB Hub",     "quantity": 10, "unit_price": 30.00,   "status": "completed"},
        ]

        log.info("Extracted %d raw records.", len(raw_records))
        return raw_records  # automatically pushed to XCom

    @task(task_id="transform_data")
    def transform_data(raw_records: list[dict]) -> list[dict]:

        log.info("Starting transformation. Input records: %d", len(raw_records))

        TAX_RATE = 0.10
        transformed = []

        for record in raw_records:
            # Filter out non-completed orders
            if record["status"] != "completed":
                log.info(
                    "Skipping record id=%s (status=%s)",
                    record["id"],
                    record["status"],
                )
                continue

            line_total = record["quantity"] * record["unit_price"]
            tax_amount = round(line_total * TAX_RATE, 2)
            total_with_tax = round(line_total + tax_amount, 2)

            transformed.append({
                "id":            record["id"],
                "product":       record["product"],
                "quantity":      record["quantity"],
                "unit_price":    record["unit_price"],
                "line_total":    round(line_total, 2),
                "tax_amount":    tax_amount,
                "total_with_tax": total_with_tax,
            })

        log.info(
            "Transformation complete. %d records passed, %d filtered out.",
            len(transformed),
            len(raw_records) - len(transformed),
        )
        return transformed

    @task(task_id="load_data")
    def load_data(transformed_records: list[dict]) -> dict:
        log.info("Loading %d records into the destination table...", len(transformed_records))

        total_revenue = sum(r["total_with_tax"] for r in transformed_records)
        total_tax = sum(r["tax_amount"] for r in transformed_records)

        for record in transformed_records:
            # Simulate a DB insert
            log.info(
                "INSERT → id=%-3s | %-12s | qty=%-3s | total=$%.2f",
                record["id"],
                record["product"],
                record["quantity"],
                record["total_with_tax"],
            )

        summary = {
            "records_loaded": len(transformed_records),
            "total_revenue":  round(total_revenue, 2),
            "total_tax":      round(total_tax, 2),
        }

        log.info("Load complete. Summary: %s", summary)
        return summary  # passed to notify_completion via XCom

    @task(task_id="notify_completion")
    def notify_completion(summary: dict) -> None:
        log.info("=" * 60)
        log.info("  ETL PIPELINE COMPLETED SUCCESSFULLY")
        log.info("=" * 60)
        log.info("  Records loaded : %d",   summary["records_loaded"])
        log.info("  Total revenue  : $%.2f", summary["total_revenue"])
        log.info("  Total tax      : $%.2f", summary["total_tax"])
        log.info("=" * 60)
        log.info("Notification sent to the data team channel.")

    raw      = extract_data()
    cleaned  = transform_data(raw)
    summary  = load_data(cleaned)
    notify_completion(summary)


sample_etl_pipeline()
