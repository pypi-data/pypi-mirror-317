from airflow.models.baseoperator import BaseOperator
from airflow.providers.http.hooks.http import HttpHook


class AlfrescoFetchMetadaOperator(BaseOperator):
    """
    Simple operator that query node metadata.
    :param node_id: (required) node id to fetch
    """

    def __init__(self, *arg, nodes, **kwargs):
        super().__init__(**kwargs)
        self.http_hook = HttpHook(method="GET", http_conn_id="alfresco_api", )
        self.data = {"include": "path,aspectNames,properties"}
        self.nodes = nodes

    def execute(self, context):
        self.log.debug(f"fetch_metadata type={self.nodes}")

        f_nodes = []
        if isinstance(self.nodes, list):
            for n in self.nodes:
                f_nodes.append(self.fetch_node(n))
        else:
            f_nodes.append(self.fetch_node(self.nodes))

        return f_nodes

    def fetch_node(self, node_id):
        self.log.debug(f"fetch_node pid={node_id}")
        raw_resp = self.http_hook.run(
            endpoint=f"/alfresco/api/-default-/public/alfresco/versions/1/nodes/{node_id}",
            data=self.data,
        )

        resp_json = raw_resp.json()
        return resp_json['entry']
