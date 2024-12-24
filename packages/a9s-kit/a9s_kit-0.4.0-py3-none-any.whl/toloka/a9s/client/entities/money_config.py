import uuid
from typing import Literal, Mapping, TypedDict

from pydantic import BaseModel
from typing_extensions import NotRequired, Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.money.repository.config import (
    MoneyConfigCommonSettings,
    MoneyConfigSnippetSettings,
    MoneyConfigStatusWorkflowSettingsStatusWorkflowMutableTransition,
    MoneyConfigStatusWorkflowSettingsStatusWorkflowPaidTransition,
)
from toloka.a9s.client.models.money_config import (
    MoneyConfigAnnotationSettingsStrict,
    MoneyConfigFormStrict,
    MoneyConfigStatusWorkflowSettingsStrict,
)
from toloka.a9s.client.models.types import TenantId


class StatusTransitionPayment(BaseModel):
    price: float
    portal_review_result: Literal['ACCEPTED', 'REJECTED']


StatusTransitionPayments = Mapping[str, StatusTransitionPayment]


class StatusTransitionMutablePayment(BaseModel):
    price: float


StatusTransitionMutablePayments = Mapping[str, StatusTransitionMutablePayment]


class StatusWorkflowMoneyConfigFormParams(TypedDict):
    tenant_id: NotRequired[TenantId | None]

    snippet_price: float
    currency: Literal['BU', 'USD']
    mutable_transitions: StatusTransitionMutablePayments
    paid_transitions: StatusTransitionPayments
    skip_pending_balance: NotRequired[bool]
    name: NotRequired[str]


class StatusWorkflowMoneyConfigFormParamsWithDefaults(TypedDict):
    tenant_id: TenantId | None

    snippet_price: float
    currency: Literal['BU', 'USD']
    mutable_transitions: StatusTransitionMutablePayments
    paid_transitions: StatusTransitionPayments
    skip_pending_balance: bool
    name: str


def apply_status_workflow_money_config_form_defaults(
    **kwargs: Unpack[StatusWorkflowMoneyConfigFormParams],
) -> StatusWorkflowMoneyConfigFormParamsWithDefaults:
    return {
        'tenant_id': None,
        'skip_pending_balance': False,
        'name': str(uuid.uuid4()),
        **kwargs,
    }


async def build_status_workflow_money_config_form(
    kit: AsyncKit,
    **kwargs: Unpack[StatusWorkflowMoneyConfigFormParams],
) -> MoneyConfigFormStrict:
    with_defaults = apply_status_workflow_money_config_form_defaults(**kwargs)

    if with_defaults['tenant_id'] is None:
        tenant_id = (await kit.toloka.get_user_tenants()).tenant_ids[0]
        requester_id = tenant_id
    else:
        requester_id = with_defaults['tenant_id']
        tenant_id = with_defaults['tenant_id']

    return MoneyConfigFormStrict(
        name=with_defaults['name'],
        currency=with_defaults['currency'],
        requester_id=requester_id,
        snippet_settings=MoneyConfigSnippetSettings(price=with_defaults['snippet_price']),
        common_settings=MoneyConfigCommonSettings(skip_pending_balance=with_defaults['skip_pending_balance']),
        specific_settings=MoneyConfigStatusWorkflowSettingsStrict(
            mutable_transitions=[
                MoneyConfigStatusWorkflowSettingsStatusWorkflowMutableTransition(
                    to_status=status,
                    price=transition.price,
                )
                for status, transition in with_defaults['mutable_transitions'].items()
            ],
            paid_transitions=[
                MoneyConfigStatusWorkflowSettingsStatusWorkflowPaidTransition(
                    to_status=status,
                    price=transition.price,
                    portal_review_result=transition.portal_review_result,
                )
                for status, transition in with_defaults['paid_transitions'].items()
            ],
        ),
        tenant_id=tenant_id,
    )


class AnnotationMoneyConfigFormParams(TypedDict):
    tenant_id: NotRequired[TenantId | None]

    price: float
    currency: Literal['BU', 'USD']
    skip_pending_balance: NotRequired[bool]
    name: NotRequired[str]


class AnnotationMoneyConfigFormParamsWithDefaults(TypedDict):
    tenant_id: TenantId | None

    name: str
    price: float
    currency: Literal['BU', 'USD']
    skip_pending_balance: bool


def apply_annotation_money_config_form_defaults(
    **kwargs: Unpack[AnnotationMoneyConfigFormParams],
) -> AnnotationMoneyConfigFormParamsWithDefaults:
    return {
        'tenant_id': None,
        'skip_pending_balance': False,
        'name': str(uuid.uuid4()),
        **kwargs,
    }


async def build_annotation_money_config_form(
    kit: AsyncKit,
    **kwargs: Unpack[AnnotationMoneyConfigFormParams],
) -> MoneyConfigFormStrict:
    with_defaults = apply_annotation_money_config_form_defaults(**kwargs)

    if with_defaults['tenant_id'] is None:
        tenant_id = (await kit.toloka.get_user_tenants()).tenant_ids[0]
        requester_id = tenant_id
    else:
        requester_id = with_defaults['tenant_id']
        tenant_id = with_defaults['tenant_id']

    return MoneyConfigFormStrict(
        name=with_defaults['name'],
        currency=with_defaults['currency'],
        requester_id=requester_id,
        snippet_settings=MoneyConfigSnippetSettings(price=with_defaults['price']),
        common_settings=MoneyConfigCommonSettings(skip_pending_balance=with_defaults['skip_pending_balance']),
        specific_settings=MoneyConfigAnnotationSettingsStrict(price=with_defaults['price']),
        tenant_id=tenant_id,
    )
