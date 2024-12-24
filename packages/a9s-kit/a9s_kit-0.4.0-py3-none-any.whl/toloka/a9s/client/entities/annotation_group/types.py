from typing import TYPE_CHECKING, Sequence, TypeAlias

from typing_extensions import TypeVar

from toloka.a9s.client.entities.annotation import Annotation
from toloka.a9s.client.entities.annotation.types import LazyStatusWorkflow
from toloka.a9s.client.entities.base import LazyValue
from toloka.a9s.client.models.annotation import AnnotationViewV1Strict
from toloka.a9s.client.models.annotation_process.view import (
    QuorumAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.types import AnnotationGroupId

if TYPE_CHECKING:
    from toloka.a9s.client.entities.annotation_group import AnnotationGroup


T = TypeVar('T')

LazyFromAnnotationGroupId = LazyValue[[AnnotationGroupId], T]
ValueOrLazy: TypeAlias = LazyFromAnnotationGroupId[T] | T


AnnotationEntity = Annotation[AnnotationViewV1Strict, LazyStatusWorkflow]

LazyAnnotations = LazyFromAnnotationGroupId[Sequence[AnnotationEntity]]
AnyAnnotations = ValueOrLazy[Sequence[AnnotationEntity]]
AnnotationsType = TypeVar(
    'AnnotationsType',
    bound=AnyAnnotations,
    covariant=True,
    default=AnyAnnotations,
)

LazyQuorum = LazyFromAnnotationGroupId[QuorumAnnotationProcessViewStrict | None]
AnyQuorum = ValueOrLazy[QuorumAnnotationProcessViewStrict | None]
QRM = TypeVar('QRM', bound=AnyQuorum, covariant=True, default=AnyQuorum)


EagerQRM = TypeVar(
    'EagerQRM',
    bound=QuorumAnnotationProcessViewStrict | None,
    covariant=True,
    default=QuorumAnnotationProcessViewStrict | None,
)
EagerAnnotationGroup: TypeAlias = """
AnnotationGroup[
    Sequence[AnnotationEntity],
    EagerQRM,
]
"""


LazyAnnotationGroup: TypeAlias = """
AnnotationGroup[
    LazyFromAnnotationGroupId[Sequence[AnnotationEntity]],
    LazyFromAnnotationGroupId[EagerQRM],
]
"""
