from airflow.models.baseoperator import BaseOperator
from airflow.models.expandinput import MappedArgument
from airflow.providers.http.hooks.http import HttpHook
from airflow.utils.helpers import merge_dicts
from requests import Response

PAGE_SIZE = 3


class AlfrescoFetchChildrenOperator(BaseOperator):
    """
    Simple operator that query children api.
    :param parent_node_id: (required) parent node id
    """

    def __init__(self, *arg, children, **kwargs):
        super().__init__(**kwargs)
        self.http_hook = HttpHook(method="GET", http_conn_id="alfresco_api", )
        self.data = {"skipCount": 0, "maxItems": PAGE_SIZE, "orderBy": "createdAt",
                     "include": "path,aspectNames,properties"}
        self.children = children

    def execute(self, context):
        self.log.debug(f"get_children type={self.children}")

        f_children = []
        if isinstance(self.children, MappedArgument):
            child_id = self.children.resolve(context)
            f_children.extend(self.fetch_children(child_id))
        else:
            f_children.extend(self.fetch_children(self.children))

        self.log.debug("--children--")
        for c in f_children:
            self.log.debug(c)

        return f_children

    def fetch_children(self, parent_id):
        import logging
        from pristy.alfresco_operator.update_node_db import update_state_db

        self.log.info(f"fetch_children pid={parent_id}")
        response = self.http_hook.run(
            endpoint=f"/alfresco/api/-default-/public/alfresco/versions/1/nodes/{parent_id}/children",
            data=self.data,
        )
        all_responses = [response]
        while True:
            next_page_params = self.paginate(response)
            if not next_page_params:
                break
            self.log.info(f"Load next page {next_page_params.get("data")}")
            response = self.http_hook.run(
                endpoint=f"/alfresco/api/-default-/public/alfresco/versions/1/nodes/{parent_id}/children",
                data=merge_dicts(self.data, next_page_params.get("data")),
            )
            all_responses.append(response)

        entries = []
        for raw_resp in all_responses:
            resp_json = raw_resp.json()
            for e in resp_json["list"]["entries"]:
                entries.append(e["entry"])

        update_state_db(parent_id, "success")
        return entries

    def paginate(self, response: Response) -> dict:
        content = response.json()

        pagination: dict = content['list']['pagination']
        count: int = pagination['count']
        skip_count: int = pagination['skipCount']
        max_items: int = pagination['maxItems']
        self.log.debug(f"Request Alfresco pagination {count}/{max_items} ")

        if pagination['hasMoreItems']:
            return dict(data={"skipCount": skip_count + PAGE_SIZE})
