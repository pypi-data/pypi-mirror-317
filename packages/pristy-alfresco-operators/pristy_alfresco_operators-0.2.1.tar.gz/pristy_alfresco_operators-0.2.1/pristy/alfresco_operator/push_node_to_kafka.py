from typing import Any

from airflow.exceptions import AirflowSkipException
from airflow.models import Variable
from airflow.models.baseoperator import BaseOperator
from airflow.providers.apache.kafka.hooks.produce import KafkaProducerHook

NODE_INJECTOR_SCHEMA_PATH = "dags/pristy/schema/node_injector.schema.json"


class PushToKafkaOperator(BaseOperator):
    """
    Push a node into kafka injector topic.
    First valid schema using jsonschema
    Finally update state for the node in local db
    """

    def __init__(self, *, nodes, table_name, **kwargs):
        super().__init__(**kwargs)
        self.nodes = nodes
        self.table_name_local_db = table_name

    def execute(self, context):
        from pristy.alfresco_operator.update_node_db import update_state_db
        import jsonschema
        import json
        if len(self.nodes) == 0:
            raise AirflowSkipException('No node to proceed')

        topic = Variable.get('kafka_export_topic')

        def _load_schema() -> dict[str, Any]:
            with open(NODE_INJECTOR_SCHEMA_PATH) as schema_file:
                content = json.load(schema_file)
            return content

        def _hash_key(node: dict) -> str:
            import hashlib
            path = node['path']['root'] + node['path']['short']
            hash_object = hashlib.sha1(path.encode("utf-8"))
            return hash_object.hexdigest()

        def acked(err, msg):
            if err is not None:
                self.log.error("Failed to deliver message: %s", err)
            else:
                self.log.debug(
                    "Produced record to topic %s, partition [%s] @ offset %s",
                    msg.topic(),
                    msg.partition(),
                    msg.offset(),
                )

        schema = _load_schema()

        kafka_hook = KafkaProducerHook(kafka_config_id="kafka_pristy")
        producer = kafka_hook.get_producer()
        files = []
        for c in self.nodes:
            self.log.debug(c)
            node_json = json.dumps(c)
            try:
                jsonschema.validate(json.loads(node_json), schema=schema)
            except jsonschema.ValidationError as ex:
                raise RuntimeError(f"Fail to validate export. Original error {type(ex).__name__}: {ex}")
            headers = {
                "type": c['type'],
                "path": c['path']['short'],
                "name": c['name'],
            }
            try:
                producer.produce(topic, key=_hash_key(c), value=node_json, on_delivery=acked, headers=headers)
                if 'source' in c.keys():
                    files.append(c)
                    update_state_db(c['source']['uuid'], "fail", self.table_name_local_db)
            except BufferError:
                self.log.warning(
                    f'Local producer queue is full ({len(producer)} messages awaiting delivery): try again')

        still_in_queue = producer.flush(timeout=10)
        if still_in_queue > 0:
            for c in files:
                update_state_db(c['source']['uuid'], "fail", self.table_name_local_db)
            raise RuntimeError(f"Message still in queue : {still_in_queue}")

        for c in files:
            update_state_db(c['source']['uuid'], "success", self.table_name_local_db)
