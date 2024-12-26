import json
import logging
from pymongo import MongoClient
from bson import json_util
from mongodb_schema.exceptions import SchemaExportError


class MongoSchemaExporter:
    def __init__(self, uri="mongodb://localhost:27017", database=None, logger=None):
        """
        Initialize the MongoSchemaExporter.
        :param uri: MongoDB URI string.
        :param database: Name of the MongoDB database to connect to.
        :param logger: Optional logger instance.
        """
        self.client = MongoClient(uri)
        if not database:
            raise SchemaExportError("Database name must be provided.")
        self.db = self.client[database]
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def infer_schema(self, collection_name, sample_size=100):
        """
        Infer schema of a single collection.
        :param collection_name: Name of the collection to analyze.
        :param sample_size: Number of documents to sample.
        :return: Dictionary representing the schema.
        """
        collection = self.db[collection_name]
        sample_documents = collection.find().limit(sample_size)
        schema = {}
        for doc in sample_documents:
            for key, value in doc.items():
                field_type = type(value).__name__
                if key not in schema:
                    schema[key] = set()
                schema[key].add(field_type)
        self.logger.debug(f"Inferred schema for {collection_name}: {schema}")
        return {key: list(types) for key, types in schema.items()}

    def export_schema(self, output_file=None, sample_size=100, output_format="json"):
        """
        Export schema metadata for all collections in the database.
        :param output_file: Optional file path for schema export.
        :param sample_size: Number of documents to sample from each collection.
        :param output_format: Format for export (default: JSON).
        :return: File path or schema metadata dictionary.
        """
        if output_format not in ["json", "yaml"]:
            raise SchemaExportError(f"Unsupported output format: {output_format}")

        schema_metadata = {}
        for collection_name in self.db.list_collection_names():
            schema_metadata[collection_name] = self.infer_schema(collection_name, sample_size)

        if output_file:
            with open(output_file, "w") as f:
                if output_format == "json":
                    json.dump(schema_metadata, f, separators=(',', ':'), default=json_util.default)
                # Add YAML support
                elif output_format == "yaml":
                    import yaml
                    yaml.dump(schema_metadata, f)
            self.logger.info(f"Schema exported to {output_file}")
            return output_file

        return schema_metadata
