import argparse
from mongodb_schema.exporter import MongoSchemaExporter
from mongodb_schema.utils import setup_logger
import logging


def main():
    parser = argparse.ArgumentParser(description="Export MongoDB schema metadata.")
    parser.add_argument("--uri", type=str, required=True, help="MongoDB connection URI")
    parser.add_argument("--database", type=str, required=True, help="Database name")
    parser.add_argument("--output", type=str, default=None, help="Output file name (e.g., db.json)")
    parser.add_argument("--sample-size", type=int, default=100, help="Number of documents to analyze per collection")
    parser.add_argument("--format", type=str, default="json", choices=["json", "yaml"], help="Output format")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    logger = setup_logger("mongodb-schema", level=logging.DEBUG if args.verbose else logging.INFO)
    exporter = MongoSchemaExporter(uri=args.uri, database=args.database, logger=logger)

    try:
        result = exporter.export_schema(output_file=args.output, sample_size=args.sample_size, output_format=args.format)
        if args.output:
            logger.info(f"Schema exported successfully to {args.output}")
        else:
            logger.info("Schema Metadata:")
            print(result)
    except Exception as e:
        logger.error(f"Failed to export schema: {e}")


if __name__ == "__main__":
    main()
