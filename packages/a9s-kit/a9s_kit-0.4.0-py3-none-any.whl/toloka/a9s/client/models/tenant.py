from typing import Sequence

from pydantic import BaseModel, ConfigDict

from toloka.a9s.client.models.types import TenantId


class TenantsView(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
    )

    tenant_ids: Sequence[TenantId]
