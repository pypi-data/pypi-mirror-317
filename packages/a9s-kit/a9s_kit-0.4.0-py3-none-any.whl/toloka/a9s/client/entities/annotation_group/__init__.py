from __future__ import annotations

from functools import partial
from typing import Generic, Literal, Sequence, TypeGuard, overload

from typing_extensions import TypeIs, Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.entities.annotation import Annotation
from toloka.a9s.client.entities.annotation_group.types import (
    QRM,
    AnnotationEntity,
    AnnotationsType,
    AnyAnnotations,
    EagerAnnotationGroup,
    EagerQRM,
    LazyAnnotationGroup,
    LazyAnnotations,
    LazyFromAnnotationGroupId,
    ValueOrLazy,
)
from toloka.a9s.client.entities.base import EntityApiBase, EntityApiBaseParams, LazyValue
from toloka.a9s.client.models.annotation_process.view import QuorumAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.param import AnnotationFilterParamV1
from toloka.a9s.client.models.types import (
    AnnotationGroupId,
    AnnotationId,
)


class AnnotationGroup(EntityApiBase, Generic[AnnotationsType, QRM]):
    """A group of annotations in Annotation Studio related by some annotation process.

    An annotation group represents multiple annotations originating from the same annotation process.

    Generic type parameters:

    * `QRM`: Type of quorum annotation process

    Each type parameter represents annotation process configuration, possible values are:

    * `None`: Not configured
    * `T`: Configured and loaded from the API
    * `LazyFrom*[T | None]`: Not loaded from API (may either be configured or not)

    Attributes:
        annotation_group_id: Unique identifier of the group.
        quorum: Quorum parameters of the annotation group.
        annotations: List of annotation entities for the group.
    """

    annotation_group_id: AnnotationGroupId
    quorum: QRM
    annotations: AnnotationsType

    def __init__(
        self,
        annotation_group_id: AnnotationGroupId,
        quorum: QRM,
        annotations: AnnotationsType,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> None:
        super().__init__(**kwargs)
        self.annotation_group_id = annotation_group_id
        self.quorum = quorum
        self.annotations = annotations

    @overload
    @classmethod
    async def get(
        cls,
        id: AnnotationGroupId,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]: ...

    @overload
    @classmethod
    async def get(
        cls,
        id: AnnotationGroupId,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]: ...

    @classmethod
    async def get(
        cls,
        id: AnnotationGroupId,
        lazy: Literal[True] | Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> (
        # type vars must be spelled out due to mypy bug: https://github.com/python/mypy/issues/18188
        EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]
        | LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]
    ):
        """Gets an annotation group and its annotation processes from the API by its ID.

        Args:
            id: ID of the annotation group to get.
            lazy: If True, annotation processes and annotations will be loaded lazily.
            kit (AsyncKit): `AsyncKit` instance.

        Returns:
            (EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]): if `lazy` is False, annotation group with
                all annotation processes and annotations loaded.
            (LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]): if `lazy` is True, annotation group with
                lazy loading of annotation processes and annotations (so no actual data is fetched in this method).
        Raises:
            ValueError: If annotation group with given ID is not found.

        Examples:
            ```python
            group = await AnnotationGroup.get(id='group123', batch_id='batch456', kit=kit)
            ```
        """

        kit = kwargs['kit']

        if lazy:
            return AnnotationGroup[
                LazyFromAnnotationGroupId[Sequence[AnnotationEntity]],
                LazyFromAnnotationGroupId[QuorumAnnotationProcessViewStrict | None],
            ](
                annotation_group_id=id,
                quorum=LazyValue(
                    partial(
                        cls._fetch_quorum,
                        kit=kit,
                    )
                ),
                annotations=LazyValue(
                    partial(
                        cls._fetch_annotations,
                        kit=kit,
                    )
                ),
                kit=kit,
            )
        else:
            return AnnotationGroup[Sequence[AnnotationEntity], QuorumAnnotationProcessViewStrict | None](
                annotation_group_id=id,
                quorum=await cls._fetch_quorum(annotation_group_id=id, kit=kit),
                annotations=await cls._fetch_annotations(
                    annotation_group_id=id,
                    kit=kit,
                ),
                kit=kit,
            )

    @classmethod
    async def _fetch_annotations(
        cls,
        annotation_group_id: AnnotationGroupId,
        kit: AsyncKit,
    ) -> list[AnnotationEntity]:
        return [
            await Annotation.from_view(annotation, kit=kit, lazy=True)
            async for annotation in kit.annotation_studio.annotation.get_all(
                AnnotationFilterParamV1(annotation_group_id=annotation_group_id)
            )
        ]

    @classmethod
    async def _fetch_quorum(
        cls,
        annotation_group_id: AnnotationGroupId,
        kit: AsyncKit,
    ) -> QuorumAnnotationProcessViewStrict | None:
        quorum = await kit.annotation_studio.annotation_process.get_quorum(annotation_group_id=annotation_group_id)
        return quorum

    @classmethod
    async def _fetch_quorum_or_fail(
        cls,
        annotation_group_id: AnnotationGroupId,
        kit: AsyncKit,
    ) -> QuorumAnnotationProcessViewStrict:
        quorum = await kit.annotation_studio.annotation_process.get_quorum(annotation_group_id=annotation_group_id)
        if quorum is None:
            raise ValueError(f'Annotation group with id {annotation_group_id} not found or does not have quorum')
        return quorum

    @overload
    @classmethod
    async def get_with_quorum_or_fail(
        cls,
        id: AnnotationGroupId,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> AnnotationGroup[Sequence[AnnotationEntity], QuorumAnnotationProcessViewStrict]: ...

    @overload
    @classmethod
    async def get_with_quorum_or_fail(
        cls,
        id: AnnotationGroupId,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> LazyAnnotationGroup[QuorumAnnotationProcessViewStrict]:
        """Will fail on no quorum when the quorum will actually be loaded"""
        ...

    @classmethod
    async def get_with_quorum_or_fail(
        cls,
        id: AnnotationGroupId,
        lazy: Literal[False] | Literal[True] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> (
        AnnotationGroup[Sequence[AnnotationEntity], QuorumAnnotationProcessViewStrict]
        | LazyAnnotationGroup[QuorumAnnotationProcessViewStrict]
    ):
        """Gets an annotation group by its ID and ensures it has a quorum process.

        Fetches an annotation group from the API by its ID and loads its annotation processes, ensuring that it has a
        quorum process configured. Fails if the annotation group does not have a quorum process.

        Args:
            id: ID of the annotation group to get.
            lazy: If True, annotation processes will be loaded lazily. If annotation group does not have a quorum
                process, this method will not fail immediately, but will raise an error when quorum process is loaded
                later.
            **kwargs: Additional arguments passed to the base class.

        Returns:
            (AnnotationGroup[Sequence[AnnotationEntity], QuorumAnnotationProcessViewStrict]): If `lazy` is False,
                annotation group with loaded annotations and quorum process.
            (LazyAnnotationGroup[QuorumAnnotationProcessViewStrict]): If `lazy` is True,
                annotation group with lazy annotations and quorum process.

        Raises:
            ValueError: If annotation group does not have a quorum process configured.

        Examples:
            ```python
            group = await AnnotationGroup.get_with_quorum_or_fail(id='group123', kit=kit)
            print(group.quorum.data.threshold)  # Statically type checked
            ```

            Get group lazily:

            ```python
            # no actual requests are made here
            group = await AnnotationGroup.get_with_quorum_or_fail(id='group123', lazy=True, kit=kit)
            loaded_group = await group.fetch_quorum()  # Raises ValueError if quorum is not configured
            print(loaded_group.quorum.data.threshold)  # Statically type checked
            ```
        """

        kit = kwargs['kit']

        quorum = await cls._fetch_quorum(annotation_group_id=id, kit=kit)
        if quorum is None:
            raise ValueError(f'Annotation group with id {id} not found or does not have quorum')

        if lazy:
            return AnnotationGroup[LazyAnnotations, LazyFromAnnotationGroupId[QuorumAnnotationProcessViewStrict]](
                annotation_group_id=id,
                quorum=LazyValue(
                    partial(
                        cls._fetch_quorum_or_fail,
                        kit=kit,
                    )
                ),
                annotations=LazyValue(
                    partial(
                        cls._fetch_annotations,
                        kit=kit,
                    )
                ),
                kit=kit,
            )
        else:
            annotation_group = await AnnotationGroup.get(
                id=id,
                lazy=lazy,
                kit=kit,
            )
            return annotation_group.assert_quorum()

    @overload
    async def refresh(
        self, lazy: Literal[False] = False
    ) -> EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]: ...

    @overload
    async def refresh(self, lazy: Literal[True]) -> LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]: ...

    async def refresh(
        self, lazy: Literal[True] | Literal[False] = False
    ) -> (
        EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]
        | LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]
    ):
        """Refreshes the annotation group by fetching its latest state from the API.

        Fetches the latest state of the annotation group from the API, including its annotations
        and quorum process. This method creates a new instance of the AnnotationGroup class
        with updated data rather than modifying the existing instance.

        Args:
            lazy: If True, updated group will have lazy-loaded annotations and quorum process.

        Returns:
            (LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]): If `lazy` is True, `AnnotationGroup` with
                lazy-loaded annotations and quorum process.
            (EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]): If `lazy` is False, `AnnotationGroup` with
                loaded annotations and quorum process.

        Examples:
            ```python
            while not group.is_quorum_completed():
                group = await group.refresh()
            print(len(group.annotation_ids))
            ```
        """
        if lazy:
            return await self.get(id=self.annotation_group_id, lazy=lazy, kit=self.kit)
        else:
            return await self.get(id=self.annotation_group_id, lazy=lazy, kit=self.kit)

    async def fetch_annotations(self) -> AnnotationGroup[Sequence[AnnotationEntity], QRM]:
        """Fetches all annotations associated with this annotation group from the API.

        Returns:
            An `AnnotationGroup` instance containing the fetched annotations. Annotations have loaded view but
                annotation processes are lazy-loaded.

        Examples:
            ```python
            annotation_group = await annotation_group.fetch_annotations()
            print(annotation_group.annotations)
            ```
        """
        return AnnotationGroup(
            annotation_group_id=self.annotation_group_id,
            quorum=self.quorum,
            annotations=await self._fetch_annotations(self.annotation_group_id, self.kit),
            kit=self.kit,
        )

    async def fetch_quorum(
        self: AnnotationGroup[AnnotationsType, ValueOrLazy[EagerQRM]],
    ) -> AnnotationGroup[AnnotationsType, EagerQRM]:
        """Fetches the quorum from the API if it is not already loaded.

        Returns:
            An `AnnotationGroup` instance with the loaded quorum data.

        Examples:
            ```python
            annotation_group = await annotation_group.fetch_quorum()
            print(annotation_group.quorum.data)
            ```
        """
        if is_quorum_loaded(self):
            return self
        assert isinstance(self.quorum, LazyValue)
        return AnnotationGroup(
            annotation_group_id=self.annotation_group_id,
            quorum=await self.quorum(self.annotation_group_id),
            annotations=self.annotations,
            kit=self.kit,
        )

    @property
    def annotation_ids(
        self: AnnotationGroup[Sequence[AnnotationEntity]],
    ) -> set[AnnotationId]:
        """Returns a set of annotation IDs for all annotations in the group."""

        return {annotation.annotation_id for annotation in self.annotations}

    def assert_quorum(
        self: AnnotationGroup[AnnotationsType, QuorumAnnotationProcessViewStrict | None],
    ) -> AnnotationGroup[AnnotationsType, QuorumAnnotationProcessViewStrict]:
        """Asserts that the group has a quorum process configured in its local state.

        Verifies that the group has a quorum annotation process configured in its current local
        representation, without fetching new data from the API. Returns the same group with a concrete
        `QuorumAnnotationProcessViewStrict` type instead of `OptionalQRM` or fails.

        Returns:
            The same group with a concrete `QuorumAnnotationProcessViewStrict` type.

        Raises:
            ValueError: If quorum process is not configured in the local representation of this group.

        Examples:
            ```python
            group = group.assert_quorum()
            print(group.quorum.data.threshold)  # Statically type checked
            ```
        """

        if has_quorum(self):
            return self
        raise ValueError('Annotation group does not have a quorum')

    # quorum annotation group API

    def is_quorum_completed(
        self: AnnotationGroup[
            AnnotationsType,
            QuorumAnnotationProcessViewStrict,
        ],
    ) -> bool:
        """Checks if the quorum process is completed for this group, i.e. there are enough annotations.

        Returns:
            True if required number of annotations is reached, False otherwise.
        """
        return self.quorum.completed


def are_annotations_loaded(
    annotation_group: AnnotationGroup[AnyAnnotations, QRM],
) -> TypeGuard[AnnotationGroup[Sequence[AnnotationEntity], QRM]]:
    """Checks if annotation group view is loaded from the API.

    Type guard function that checks if view was loaded from the API or exists only as a lazy loader.
    Function is used to narrow annotation group type from potentially lazy to concrete loaded type.

    Returns:
        True if view is loaded, False if it exists as lazy loader

    Examples:
        ```python
        group = await AnnotationGroup.get(id='group123', batch_id='batch456', lazy=True, kit=kit)
        if is_view_loaded(group):
            print(group.view.elements)  # Statically type checked
        ```
    """
    return not isinstance(annotation_group.annotations, LazyValue)


def is_quorum_loaded(
    annotation_group: AnnotationGroup[AnnotationsType, ValueOrLazy[EagerQRM]],
) -> TypeGuard[AnnotationGroup[AnnotationsType, EagerQRM]]:
    """Checks if annotation group quorum is loaded from the API.

    Type guard function that checks if quorum was loaded from the API or exists only as a lazy loader.
    Function is used to narrow annotation group type from potentially lazy to concrete loaded type.

    Returns:
        True if quorum is loaded, False if it exists as lazy loader

    Examples:
        ```python
        group = await AnnotationGroup.get(id='group123', batch_id='batch456', lazy=True, kit=kit)
        if is_quorum_loaded(group) and has_quorum(group):
            print(group.quorum.data.threshold)  # Statically type checked
        ```
    """
    return not isinstance(annotation_group.quorum, LazyValue)


def has_quorum(
    annotation_group: AnnotationGroup[AnnotationsType, QuorumAnnotationProcessViewStrict | None],
) -> TypeIs[AnnotationGroup[AnnotationsType, QuorumAnnotationProcessViewStrict]]:
    return annotation_group.quorum is not None
