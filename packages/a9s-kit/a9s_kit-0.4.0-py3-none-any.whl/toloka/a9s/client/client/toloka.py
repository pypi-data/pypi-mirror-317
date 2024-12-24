from toloka.a9s.client.base.client import AsyncBaseTolokaClient
from toloka.a9s.client.models.tenant import TenantsView


class AsyncTolokaClient(AsyncBaseTolokaClient):
    async def get_user_tenants(self) -> TenantsView:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/user/tenant',
        )
        return TenantsView.model_validate(response.json())
