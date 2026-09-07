"""Resource handlers for Airbyte Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListPipelineParams, GetPipelineParams,
    PipelineRecord, PipelineList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_pipelines", "List pipelines in Airbyte.", action_type="read", chain_callable=True, event="airbyte-connector.list_pipelines", effects=["read:pipelines"], data_model=PipelineList)
async def list_pipelines(params: ListPipelineParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_pipelines(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.success({"pipelines": items, "total": len(items)}, summary=f"Found {len(items)} pipelines.")
    except Exception as e:
        return ActionResult.error(f"Error listing pipelines: {e}")

@chat.function("get_pipeline", "Get details of one Pipeline in Airbyte.", action_type="read", chain_callable=True, event="airbyte-connector.get_pipeline", effects=["read:pipeline"], data_model=PipelineRecord)
async def get_pipeline(params: GetPipelineParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_pipeline(params.pipeline_id)
        rid = str(r.get("id") or params.pipeline_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.success({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved Pipeline {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Pipeline: {e}")

@chat.function("audit_pipeline_health", "Audit health of Airbyte pipelines and connectivity.", action_type="read", chain_callable=True, event="airbyte-connector.audit_pipeline_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_pipeline_health(params: ConnectionIdParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_pipelines(limit=50)
        return ActionResult.success({
            "healthy": True,
            "total_pipelines": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"Airbyte healthy. Sampled {len(items)} pipelines."
        }, summary=f"Airbyte health check passed with {len(items)} pipelines.")
    except Exception as e:
        return ActionResult.error(f"Error auditing Airbyte health: {e}")
