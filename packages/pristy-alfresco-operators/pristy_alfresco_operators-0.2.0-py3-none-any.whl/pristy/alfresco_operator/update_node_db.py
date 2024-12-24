import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook


def update_node_state_db(node, state):
    update_state_db(node['id'], state)


def update_state_db(child_id, state, table_name="export_alfresco_folder_children"):
    logger = logging.getLogger("airflow.task")
    logger.debug(f"Set node {child_id} to {state}")
    postgres_hook = PostgresHook(postgres_conn_id="local_pg")
    conn = postgres_hook.get_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE {table_name} SET state = '{state}' WHERE uuid = '{child_id}'")
    conn.commit()

    logger.debug("commit")
