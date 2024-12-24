from typing import TYPE_CHECKING, TypeAlias

from typing_extensions import TypeVar

from toloka.a9s.client.entities.base import LazyValue
from toloka.a9s.client.models.annotation import AnnotationViewV1Strict
from toloka.a9s.client.models.annotation_process.view import (
    StatusWorkflowAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.types import AnnotationId

if TYPE_CHECKING:
    from toloka.a9s.client.entities.annotation import Annotation


T = TypeVar('T')

LazyFromAnnotationId = LazyValue[[AnnotationId], T]
ValueOrLazy: TypeAlias = T | LazyFromAnnotationId[T]


LazyView = LazyFromAnnotationId[AnnotationViewV1Strict]
AnyView = ValueOrLazy[AnnotationViewV1Strict]
ViewType = TypeVar(
    'ViewType',
    bound=AnyView,
    covariant=True,
    default=AnyView,
)

LazyStatusWorkflow = LazyFromAnnotationId[StatusWorkflowAnnotationProcessViewStrict | None]
AnyStatusWorkflow = ValueOrLazy[StatusWorkflowAnnotationProcessViewStrict | None]
SW = TypeVar('SW', bound=AnyStatusWorkflow, covariant=True, default=AnyStatusWorkflow)


EagerSW = TypeVar(
    'EagerSW',
    bound=StatusWorkflowAnnotationProcessViewStrict | None,
    covariant=True,
    default=StatusWorkflowAnnotationProcessViewStrict | None,
)
EagerAnnotation: TypeAlias = """
Annotation[
    AnnotationViewV1Strict,
    EagerSW,
]
"""


LazyAnnotation: TypeAlias = """
Annotation[
    LazyFromAnnotationId[AnnotationViewV1Strict],
    LazyFromAnnotationId[EagerSW],
]
"""
