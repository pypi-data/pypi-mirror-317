from __future__ import annotations

import datetime
import logging
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Generic,
    Literal,
    Mapping,
    Sequence,
    TypeAlias,
    TypeGuard,
    cast,
    overload,
)

from typing_extensions import Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.entities.annotation.types import (
    SW,
    EagerAnnotation,
    EagerSW,
    LazyAnnotation,
    LazyFromAnnotationId,
    LazyStatusWorkflow,
    LazyView,
    ValueOrLazy,
    ViewType,
)
from toloka.a9s.client.entities.base import EntityApiBase, EntityApiBaseParams, LazyValue
from toloka.a9s.client.models.annotation import (
    AnnotationViewV1Strict,
    EditAnnotationFormV1Strict,
)
from toloka.a9s.client.models.annotation_edit import AnnotationEditViewV1Strict
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessViewUserViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    QuorumAnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.web.v1.annotation.param import AnnotationFilterParamV1
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_edit.web.v1.annotation_edits.form import (
    AnnotationEditQueryParamsV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.form import (
    UpdateStatusWorkflowForm,
)
from toloka.a9s.client.models.types import AnnotationId, BatchId
from toloka.a9s.client.models.utils import DATETIME_ADAPTER, OPTIONAL_DATETIME_ADAPTER
from toloka.a9s.client.sort import SortValue, to_sort_string

if TYPE_CHECKING:
    from toloka.a9s.client.entities.annotation_group.types import EagerAnnotationGroup, LazyAnnotationGroup

logger = logging.getLogger()


class Annotation(
    EntityApiBase,
    Generic[ViewType, SW],
):
    """An `Annotation` Studio annotation that can be configured with annotation processes.

    An annotation represents a single labeling result that can be configured with different annotation processes
    (currently only with status workflow).

    Generic type parameters:

    * `ViewType`: Type of annotation view (either loaded or lazy)
    * `SW`: Type of status workflow annotation process

    Each type parameter represents annotation process configuration, possible values are:

    * `None`: Not configured
    * `T`: Configured and loaded from the API
    * `LazyFrom*[T | None]`: Not loaded from API (may either be configured or not)

    Attributes:
        annotation_id: ID of the annotation (always present on entity).
        view: API representation of the annotation.
        status_workflow: Status workflow annotation process settings.

    Examples:
        Get annotation:
        ```python
        annotation = await Annotation.get(id=AnnotationId('existing-annotation-id'), kit=kit)
        print(annotation.view.values.label)
        ```

        Get annotation lazily:
        ```python
        # no actual requests are made here
        annotation = await Annotation.get(id=AnnotationId('existing-annotation-id'), lazy=True, kit=kit)

        full_annotation = await annotation.fetch_view()
        print(full_annotation.view)
        ```
    """

    annotation_id: AnnotationId
    view: ViewType
    status_workflow: SW

    def __init__(
        self,
        annotation_id: AnnotationId,
        view: ViewType,
        status_workflow: SW,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> None:
        super().__init__(**kwargs)
        self.annotation_id = annotation_id
        self.view = view
        self.status_workflow = status_workflow

    @overload
    @classmethod
    async def from_view(
        cls,
        view: AnnotationViewV1Strict,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]: ...

    @overload
    @classmethod
    async def from_view(
        cls,
        view: AnnotationViewV1Strict,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[AnnotationViewV1Strict, LazyStatusWorkflow]: ...

    @classmethod
    async def from_view(
        cls,
        view: AnnotationViewV1Strict,
        lazy: Literal[False] | Literal[True] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> (
        EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]
        | Annotation[AnnotationViewV1Strict, LazyStatusWorkflow]
    ):
        """Creates an `Annotation` entity from its API representation, loading annotation processes.

        Creates an `Annotation` entity and loads its annotation processes (quorum, status workflow)
        from the API.

        Args:
            view: API representation of the annotation.
            kit (AsyncKit): `AsyncKit` instance.
            lazy: If True, annotation processes will be loaded lazily.

        Returns:
            (EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]): If `lazy` is False, `Annotation` with
                loaded view and status workflow.
            (Annotation[AnnotationViewV1Strict, LazyStatusWorkflow]): If `lazy` is True, `Annotation` with loaded view
                and lazy status workflow.

        Examples:
            Create annotation from already loaded view
            ```python
            view = await kit.annotation_studio.annotation.get(id='123')
            annotation = await Annotation.from_view(view=view, kit=kit)
            ```
        """

        kit = kwargs['kit']

        if lazy:
            return Annotation[
                AnnotationViewV1Strict,
                LazyStatusWorkflow,
            ](
                annotation_id=view.id,
                view=view,
                status_workflow=LazyValue(
                    partial(
                        cls._fetch_status_workflow,
                        kit=kit,
                    )
                ),
                **kwargs,
            )
        else:
            return Annotation[
                AnnotationViewV1Strict,
                StatusWorkflowAnnotationProcessViewStrict | None,
            ](
                annotation_id=view.id,
                view=view,
                status_workflow=await cls._fetch_status_workflow(id=view.id, kit=kit),
                **kwargs,
            )

    @overload
    @classmethod
    async def get(
        cls,
        id: AnnotationId,
        *,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> LazyAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]: ...

    @overload
    @classmethod
    async def get(
        cls,
        id: AnnotationId,
        *,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]: ...

    @classmethod
    async def get(
        cls,
        id: AnnotationId,
        *,
        lazy: Literal[False] | Literal[True] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> (
        # type vars must be spelled out due to mypy bug: https://github.com/python/mypy/issues/18188
        EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]
        | LazyAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]
    ):
        """Gets an annotation by its ID and loads its annotation processes.

        Fetches an annotation from the API by its ID and loads its annotation processes (quorum, status workflow).

        Args:
            id: ID of the annotation to get.
            lazy: If True, annotation processes will be loaded lazily.
            **kwargs: Additional arguments passed to the base class.

        Returns:
            (EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]): If `lazy` is False, `Annotation` with
                loaded view and status workflow.
            (LazyAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]): If `lazy` is True, `Annotation` with
                lazy view and status workflow.

        Examples:
            ```python
            annotation = await Annotation.get(id=AnnotationId('123'), kit=kit)
            print(annotation.view.values)
            ```

            Get annotation lazily:
            ```python
            # no actual requests are made here
            annotation = await Annotation.get(id=AnnotationId('123'), lazy=True, kit=kit)

            full_annotation = await annotation.fetch_view()
            print(full_annotation.view)
            ```
        """
        kit = kwargs['kit']

        if lazy:
            return Annotation[LazyView, LazyStatusWorkflow](
                annotation_id=id,
                view=LazyValue(
                    partial(
                        cls._fetch_view,
                        kit=kit,
                    )
                ),
                status_workflow=LazyValue(
                    partial(
                        cls._fetch_status_workflow,
                        kit=kit,
                    )
                ),
                **kwargs,
            )
        else:
            return Annotation[
                AnnotationViewV1Strict,
                StatusWorkflowAnnotationProcessViewStrict | None,
            ](
                annotation_id=id,
                view=await cls._fetch_view(id=id, kit=kit),
                status_workflow=await cls._fetch_status_workflow(id=id, kit=kit),
                **kwargs,
            )

    @overload
    @classmethod
    async def get_with_status_workflow_or_fail(
        cls,
        id: AnnotationId,
        *,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[LazyView, LazyFromAnnotationId[StatusWorkflowAnnotationProcessViewStrict]]: ...

    @overload
    @classmethod
    async def get_with_status_workflow_or_fail(
        cls,
        id: AnnotationId,
        *,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[AnnotationViewV1Strict, StatusWorkflowAnnotationProcessViewStrict]: ...

    @classmethod
    async def get_with_status_workflow_or_fail(
        cls,
        id: AnnotationId,
        *,
        lazy: Literal[False] | Literal[True] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> (
        Annotation[AnnotationViewV1Strict, StatusWorkflowAnnotationProcessViewStrict]
        | Annotation[LazyView, LazyFromAnnotationId[StatusWorkflowAnnotationProcessViewStrict]]
    ):
        """Gets an annotation by its ID and ensures it has a status workflow.

        Fetches an annotation from the API by its ID and loads its annotation processes, ensuring that it has a status
        workflow configured. Fails if the annotation does not have a status workflow.

        Args:
            id: ID of the annotation to get.
            lazy: If True, annotation processes will be loaded lazily. If annotation does not have a status workflow,
                this method will not fail immediately, but will raise an error is status workflow is loaded later.
            **kwargs: Additional arguments passed to the base class.

        Returns:
            (Annotation[AnnotationViewV1Strict, StatusWorkflowAnnotationProcessViewStrict]): If `lazy` is False,
                `Annotation` with loaded view and status workflow.
            (Annotation[LazyView, LazyFromAnnotationId[StatusWorkflowAnnotationProcessViewStrict]]): If `lazy` is True,
                `Annotation` with lazy view and status workflow.

        Raises:
            ValueError: If annotation does not have a status workflow configured.

        Examples:
            ```python
            annotation = await Annotation.get_with_status_workflow_or_fail(id=AnnotationId('123'), kit=kit)
            print(annotation.status_workflow.data.status)  # Statically type checked
            ```

            Get annotation lazily:

            ```python
            # no actual requests are made here
            annotation = await Annotation.get_with_status_workflow_or_fail(id=AnnotationId('123'), lazy=True, kit=kit)
            loaded_annotation = annotation.fetch_status_workflow()  # Raises ValueError if status workflow is not loaded
            await loaded_annotation.get_status_workflow_responsible()  # Statically type checked
            ```
        """
        kit = kwargs['kit']

        if lazy:
            return Annotation[LazyView, LazyFromAnnotationId[StatusWorkflowAnnotationProcessViewStrict]](
                annotation_id=id,
                view=LazyValue(
                    partial(
                        cls._fetch_view,
                        kit=kit,
                    )
                ),
                status_workflow=LazyValue(
                    partial(
                        cls._fetch_status_workflow_or_fail,
                        kit=kit,
                    )
                ),
                **kwargs,
            )
        else:
            return Annotation[AnnotationViewV1Strict, StatusWorkflowAnnotationProcessViewStrict](
                annotation_id=id,
                view=await cls._fetch_view(id=id, kit=kit),
                status_workflow=await cls._fetch_status_workflow_or_fail(id=id, kit=kit),
                **kwargs,
            )

    @classmethod
    async def _fetch_view(
        cls,
        id: AnnotationId,
        kit: AsyncKit,
    ) -> AnnotationViewV1Strict:
        return await kit.annotation_studio.annotation.get(annotation_id=id)

    @classmethod
    async def _fetch_status_workflow(
        cls,
        id: AnnotationId,
        kit: AsyncKit,
    ) -> StatusWorkflowAnnotationProcessViewStrict | None:
        return await kit.annotation_studio.annotation_process.get_status_workflow(annotation_id=id)

    @classmethod
    async def _fetch_status_workflow_or_fail(
        cls,
        id: AnnotationId,
        kit: AsyncKit,
    ) -> StatusWorkflowAnnotationProcessViewStrict:
        status_workflow = await cls._fetch_status_workflow(id=id, kit=kit)
        if status_workflow is None:
            raise ValueError(f'Annotation {id} does not have a status workflow configured')
        return status_workflow

    @overload
    @classmethod
    async def get_by_external_id(
        cls,
        external_id: str,
        batch_id: BatchId,
        lazy: Literal[True],
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> Annotation[AnnotationViewV1Strict, LazyStatusWorkflow] | None: ...

    @overload
    @classmethod
    async def get_by_external_id(
        cls,
        external_id: str,
        batch_id: BatchId,
        lazy: Literal[False] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None] | None: ...

    @classmethod
    async def get_by_external_id(
        cls,
        external_id: str,
        batch_id: BatchId,
        lazy: Literal[False] | Literal[True] = False,
        **kwargs: Unpack[EntityApiBaseParams],
    ) -> (
        EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]
        | Annotation[AnnotationViewV1Strict, LazyStatusWorkflow]
        | None
    ):
        """Gets an annotation by its external ID and batch ID, and loads its annotation processes.

        Fetches an annotation from the API by its external ID and batch ID, and loads its annotation processes (quorum,
        status workflow).

        Args:
            external_id: External ID of the annotation to get.
            batch_id: ID of the batch containing the annotation.
            lazy: If True, annotation processes will be loaded lazily.
            **kwargs: Additional arguments passed to the base class.

        Returns:
            (EagerAnnotation[StatusWorkflowAnnotationProcessViewStrict | None]): If `lazy` is False, `Annotation` with
                loaded view and status workflow.
            (Annotation[AnnotationViewV1Strict, LazyStatusWorkflow]): If `lazy` is True, `Annotation` with loaded view
                and lazy status workflow.
            (None): If no annotation with the specified external ID and batch ID exists.

        Examples:
            ```python
            annotation = await Annotation.get_by_external_id(external_id='task1', batch_id=BatchId('batch123'), kit=kit)
            if annotation:
                print(annotation.view.values)
            ```
        """
        kit = kwargs['kit']
        annotation_view = await kit.annotation_studio.annotation.find(
            query_params=AnnotationFilterParamV1(
                batch_id=batch_id,
                external_id=external_id,
                limit=1,
            ),
        )
        if len(annotation_view.data) < 1:
            return None
        assert len(annotation_view.data) == 1, 'There is only one annotation with the same external_id in the batch'

        if lazy:
            return await cls.from_view(view=annotation_view.data[0], kit=kit, lazy=lazy)
        else:
            return await cls.from_view(view=annotation_view.data[0], kit=kit, lazy=lazy)

    @overload
    async def refresh(
        self: Annotation[ViewType, LazyFromAnnotationId[EagerSW] | EagerSW],
        lazy: Literal[True],
    ) -> LazyAnnotation[EagerSW]: ...

    @overload
    async def refresh(
        self: Annotation[ViewType, LazyFromAnnotationId[EagerSW] | EagerSW],
        lazy: Literal[False] = False,
    ) -> EagerAnnotation[EagerSW]: ...

    async def refresh(
        self: Annotation[ViewType, LazyFromAnnotationId[EagerSW] | EagerSW],
        lazy: Literal[False] | Literal[True] = False,
    ) -> LazyAnnotation[EagerSW] | EagerAnnotation[EagerSW]:
        """Refreshes the annotation by fetching its latest state from the API.

        Fetches the latest state of the annotation from the API, including its annotation processes
        (status workflow) and view. This method creates a new instance of the Annotation class
        with updated data rather than modifying the existing instance.

        Annotation processes cannot be removed from the annotation, so they will always be present in the updated
        annotation (but may not be loaded if `lazy` is True).

        Args:
            lazy: If True, updated annotation will have lazy-loaded annotation processes and view.

        Returns:
            (LazyAnnotation[EagerSW]): If `lazy` is True, `Annotation` with lazy-loaded view and status workflow.
            (EagerAnnotation[EagerSW]): If `lazy` is False, `Annotation` with loaded view and status workflow.

        Examples:
            ```python
            while annotation.status != 'completed':
                annotation = await annotation.refresh()
            print(annotation.view.values)
            ```
        """

        # status workflow can't disappear from annotation but we can't check it if it's lazy, so just cast it
        if lazy:
            return cast('LazyAnnotation[EagerSW]', await self.get(id=self.annotation_id, lazy=lazy, kit=self.kit))
        else:
            return cast('EagerAnnotation[EagerSW]', await self.get(id=self.annotation_id, kit=self.kit))

    async def fetch_view(self) -> Annotation[AnnotationViewV1Strict, SW]:
        """Fetches the annotation view from the API if it is not already loaded.

        Returns:
            An `Annotation` instance with loaded annotation view.

        Examples:
            ```python
            annotation = await annotation.fetch_view()
            print(annotation.view.values)
            ```
        """
        if is_view_loaded(self):
            return self
        assert isinstance(self.view, LazyValue)

        return Annotation(
            annotation_id=self.annotation_id,
            view=await self.view(self.annotation_id),
            status_workflow=self.status_workflow,
            kit=self.kit,
        )

    async def fetch_status_workflow(
        self: Annotation[ViewType, ValueOrLazy[EagerSW]],
    ) -> Annotation[ViewType, EagerSW]:
        """Fetches the status workflow annotation process from the API if it is not already loaded.

        Returns:
            An `Annotation` instance with the latest status workflow annotation process.

        Examples:
            ```python
            annotation = await annotation.fetch_status_workflow()
            print(annotation.status_workflow.data)
            ```
        """
        if is_status_workflow_loaded(self):
            return self
        assert isinstance(self.status_workflow, LazyValue)

        return Annotation(
            annotation_id=self.annotation_id,
            view=self.view,
            status_workflow=await self.status_workflow(self.annotation_id),
            kit=self.kit,
        )

    async def assert_status_workflow(
        self,
        message: str | None = None,
    ) -> Annotation[ViewType, StatusWorkflowAnnotationProcessViewStrict]:
        """Asserts that the annotation has a status workflow configured in its local state.

        Verifies that the annotation has a status workflow process configured in its current local representation.
        If status workflow is not loaded, fetches it from the API.

        Returns:
            The same annotation with loaded status workflow of `StatusWorkflowAnnotationProcessViewStrict` type.

        Args:
            message: Custom error message to use when the assertion fails. If None, a default message is used.

        Raises:
            ValueError: If status workflow is not configured in the local representation of this annotation.

        Examples:
            ```python
            annotation = annotation.assert_status_workflow()
            await annotation.get_status_workflow_responsible()  # Statically type checked
            ```
        """
        self_with_status_workflow: Annotation[
            ViewType, StatusWorkflowAnnotationProcessViewStrict | None
        ] = await self.fetch_status_workflow()

        if has_status_workflow(self_with_status_workflow):
            return self_with_status_workflow
        raise ValueError(message or 'Annotation does not have a status workflow')

    async def assert_no_status_workflow(
        self,
        message: str | None = None,
    ) -> Annotation[ViewType, None]:
        """Asserts that the annotation does not have a status workflow configured in its local state.

        Verifies that the annotation does not have a status workflow process configured in its current local
        representation. If status workflow is not loaded, fetches it from the API.

        Returns:
            The same annotation with type indicating no status workflow configuration.

        Args:
            message: Custom error message to use when the assertion fails. If None, a default message is used.

        Raises:
            ValueError: If status workflow is configured in the local representation of this annotation.

        Examples:
            ```python
            annotation = annotation.assert_no_status_workflow()
            print(annotation.status_workflow)  # Statically type checked to be None
            ```
        """
        self_with_status_workflow: Annotation[
            ViewType, StatusWorkflowAnnotationProcessViewStrict | None
        ] = await self.fetch_status_workflow()

        if has_no_status_workflow(self_with_status_workflow):
            return self_with_status_workflow
        raise ValueError(message or 'Annotation has a status workflow')

    async def get_annotation_edits(
        self, sort: Mapping[str, SortValue] | None = None
    ) -> AsyncGenerator[AnnotationEditViewV1Strict, None]:
        """Returns an asynchronous generator of annotation edit history entries.

        Fetches the history of edits made to this annotation from the API.

        Args:
            sort: Optional mapping of field names to sort orders ('asc' or 'desc'). For example: {'created_at': 'desc'}.

        Returns:
            AsyncGenerator yielding `AnnotationEditViewV1Strict` objects representing each edit in sorted order.

        Examples:
            ```python
            async for edit in annotation.get_annotation_edits(sort={'created_at': 'desc'}):
                print(f'Edit at {edit.created_at}: {edit.values}')
            ```
        """
        async for annotation in self.kit.annotation_studio.annotation_edit.get_all(
            AnnotationEditQueryParamsV1(
                annotation_id=self.annotation_id,
                sort=to_sort_string(sort) if sort is not None else None,
            )
        ):
            yield annotation

    async def get_last_annotation_edit(
        self, sort_by: Literal['created_at', 'modified_at'] = 'modified_at'
    ) -> AnnotationEditViewV1Strict | None:
        """Returns the most recent edit made to this annotation.

        Fetches the last edit based on either creation or modification time.

        Args:
            sort_by: Field to use for determining the most recent edit.

                * `'created_at'`: Sort by creation time
                * `'modified_at'`: Sort by modification time (default)

        Returns:
            The most recent `AnnotationEditViewV1Strict` or None if no edits exist.

        Examples:
            ```python
            last_edit = await annotation.get_last_annotation_edit()
            if last_edit:
                print(f'Last edited at: {last_edit.modified_at}')
            ```
        """

        annotation_edits = await self.kit.annotation_studio.annotation_edit.find(
            AnnotationEditQueryParamsV1(
                annotation_id=self.annotation_id, sort=to_sort_string({sort_by: 'desc'}), limit=1
            ),
        )

        return annotation_edits.data[0] if len(annotation_edits.data) >= 1 else None

    async def get_last_version(self) -> int | None:
        annotation_edit = await self.get_last_annotation_edit(sort_by='modified_at')
        if annotation_edit is None:
            return None
        return annotation_edit.annotation_version

    @property
    def status(self: AnnotationWithStatusWorkflow[ViewType]) -> str:
        assert self.status_workflow.data.status is not None
        return self.status_workflow.data.status

    async def update_status(
        self: AnnotationWithStatusWorkflow[ViewType],
        status: str,
        active_edit_action: Literal['SUBMIT', 'SKIP', 'EXPIRE', 'FAIL'] = 'SUBMIT',
        comment: str | None = None,
        unavailable_for: Sequence[str] | None = None,
        responsible: Literal['client_requester', 'previous'] | str | None = 'previous',
    ) -> AnnotationWithStatusWorkflow[ViewType]:
        """Updates the status of an annotation in its status workflow.

        Changes the current status of the annotation to a new one or updates the current status. Only statuses listed in
        allowed_transitions or current status can be set.

        Args:
            status: New status to set.
            active_edit_action: What to do with the active annotation edit when changing status:

                * `'SUBMIT'`: Submit the active annotation edit
                * `'SKIP'`: Cancel the active edit with "SKIPPED" cancellation_reason
                * `'EXPIRE'`: Cancel the active edit with "EXPIRED" cancellation_reason
                * `'FAIL'`: Raise an error if there is an active edit and do not change the status
            comment: Optional comment explaining the status change. It will appear in performers' Activity History.
            unavailable_for: list of account IDs, if specified, the annotation will be unavailable for these accounts
                after the status change.
            responsible: Account ID that will be responsible for the annotation after the status change. Can be:
                'previous': Keep current responsible
                'client_requester': Set current requester as responsible. Requester will be inferred from the configured
                    `AsyncKit` instance.
                None: Unassign the current responsible account.
                If the status is set to `in_progress`,
                the annotation will revert to its initial state without a responsible account.
                str: Set specific account ID as responsible

        Returns:
            Updated annotation with new status workflow state.

        Raises:
            RuntimeError: If the requested status transition is not allowed.

        Examples:
            ```python
            annotation = await annotation.update_status(
                status='accepted', comment='Looks good', responsible='client_requester'
            )
            ```
        """

        if self.status_workflow.data.status != status and (
            self.status_workflow.data.allowed_transitions is None
            or status not in self.status_workflow.data.allowed_transitions
        ):
            raise RuntimeError(f'Status {status} is not available for annotation {self.annotation_id}')

        if responsible == 'previous':
            if self.status_workflow.data.responsible is None:
                responsible_account_id = None
            else:
                responsible_account_id = self.status_workflow.data.responsible.account_id
        elif responsible == 'client_requester':
            responsible_account_id = await self.kit.annotation_studio.get_account_id()
        elif responsible is None and self.status_workflow.data.status != status:
            raise RuntimeError('Cannot remove responsible account while changing status.')
        else:
            responsible_account_id = responsible

        request = UpdateStatusWorkflowForm(
            annotation_process_id=self.status_workflow.id,
            status=status,
            active_edit_action=active_edit_action,
            responsible_account_id=responsible_account_id,
            comment=comment,
            unavailable_for=unavailable_for,
        )
        updated_status_workflow = (await self.kit.annotation_studio.status_workflow.update_statuses(forms=[request]))[0]
        return Annotation(
            view=self.view,
            annotation_id=self.annotation_id,
            status_workflow=updated_status_workflow,
            kit=self.kit,
        )

    async def remove_responsible(
        self: AnnotationWithStatusWorkflow[ViewType],
        active_edit_action: Literal['SUBMIT', 'SKIP', 'EXPIRE', 'FAIL'] = 'SKIP',
    ) -> AnnotationWithStatusWorkflow[ViewType]:
        """Removes the current responsible account from the annotation, setting the responsible field to None.

        Args:
            active_edit_action: What to do with the active annotation edit when changing status:

                * `'SUBMIT'`: Submit the active annotation edit
                * `'SKIP'`: Cancel the active edit with "SKIPPED" cancellation_reason
                * `'EXPIRE'`: Cancel the active edit with "EXPIRED" cancellation_reason
                * `'FAIL'`: Raise an error if there is an active edit and do not change the status

        Returns:
            Updated annotation without a responsible account. If the current status is set to `in_progress`,
                the annotation will revert to its initial state without a responsible account.

        Raises:
            RuntimeError: If the removal of the responsible account is not allowed for the current status.

        Examples:
            ```python
            annotation = await annotation.remove_responsible()
            ```
        """
        return await self.update_status(
            status=self.status,
            active_edit_action=active_edit_action,
            responsible=None,
        )

    def get_status_workflow_responsible(
        self: AnnotationWithStatusWorkflow,
    ) -> StatusWorkflowAnnotationProcessViewUserViewStrict | None:
        """Returns the account currently responsible for this annotation.

        Returns:
            User view of the currently responsible account or None if no one is specified as responsible.

        Examples:
            ```python
            responsible = annotation.get_status_workflow_responsible()
            if responsible:
                print(f'Assigned to: {responsible.account_id}')
            ```
        """
        return self.status_workflow.data.responsible

    async def update(
        self: Annotation[ViewType, SW], values: Mapping[str, Any]
    ) -> Annotation[AnnotationViewV1Strict, SW]:
        """Updates the values of this annotation.

        Updates current values of annotation. This will not create new `Annotation` Edit but will update the current
        values of the annotation. If there is an active annotation edit (with `'IN_PROGRESS'` status) for this
        annotation this operation will fail.

        Args:
            values: New values for the annotation.

        Returns:
            Updated annotation with new values of possibly different type.

        Examples:
            ```python
            annotation = await annotation.update({'label': 'cat'})
            print(annotation.view.values['label'])
            ```
        """
        updated_view = await self.kit.annotation_studio.annotation.edit(
            self.annotation_id, form=EditAnnotationFormV1Strict(values=values)
        )
        return Annotation(
            annotation_id=self.annotation_id,
            view=updated_view,
            status_workflow=self.status_workflow,
            kit=self.kit,
        )

    @property
    def created_at(self: Annotation[AnnotationViewV1Strict]) -> datetime.datetime:
        return DATETIME_ADAPTER.validate_python(self.view.created_at)

    @property
    def modified_at(self: Annotation[AnnotationViewV1Strict]) -> datetime.datetime | None:
        return OPTIONAL_DATETIME_ADAPTER.validate_python(self.view.modified_at)

    @overload
    async def get_annotation_group(
        self,
        lazy: Literal[True],
    ) -> LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]: ...

    @overload
    async def get_annotation_group(
        self,
        lazy: Literal[False] = False,
    ) -> EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]: ...

    async def get_annotation_group(
        self,
        lazy: Literal[False] | Literal[True] = False,
    ) -> (
        LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]
        | EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]
    ):
        """Returns the annotation group this annotation belongs to.

        Args:
            lazy: If True, annotation group will be loaded lazily (so no actual requests will be made when this method
                is called)

        Returns:
            (LazyAnnotationGroup[QuorumAnnotationProcessViewStrict | None]): If `lazy` is True, lazy-loaded
                `AnnotationGroup`.
            (EagerAnnotationGroup[QuorumAnnotationProcessViewStrict | None]): If `lazy` is False, fully loaded
                `AnnotationGroup`.
        """

        from toloka.a9s.client.entities.annotation_group import AnnotationGroup

        self_with_view = await self.fetch_view()

        if lazy:
            return await AnnotationGroup.get(
                id=self_with_view.view.annotation_group_id,
                kit=self_with_view.kit,
                lazy=lazy,
            )
        else:
            return await AnnotationGroup.get(
                id=self_with_view.view.annotation_group_id,
                kit=self_with_view.kit,
                lazy=lazy,
            )


AnnotationWithStatusWorkflow: TypeAlias = Annotation[ViewType, StatusWorkflowAnnotationProcessViewStrict]


def is_view_loaded(
    annotation: Annotation[ValueOrLazy[AnnotationViewV1Strict], SW],
) -> TypeGuard[Annotation[AnnotationViewV1Strict, SW]]:
    """Checks if annotation view is loaded from the API.

    Type guard function that checks if view was loaded from the API or exists only as a lazy loader.
    Function is used to narrow annotation type from potentially lazy to concrete loaded type.

    Returns:
        True if view is loaded, False if it exists as lazy loader

    Examples:
        ```python
        annotation = await Annotation.get(id='ann123', lazy=True, kit=kit)
        if is_view_loaded(annotation):
            print(annotation.view.id)  # Statically type checked
        ```
    """
    return not isinstance(annotation.view, LazyValue)


def is_status_workflow_loaded(
    annotation: Annotation[ViewType, ValueOrLazy[EagerSW]],
) -> TypeGuard[Annotation[ViewType, EagerSW]]:
    """Checks if annotation status workflow is loaded from the API.

    Type guard function that checks if status workflow was loaded from the API or exists only as a lazy loader.
    Function is used to narrow annotation type from potentially lazy to concrete loaded type.

    Returns:
        True if status workflow is loaded, False if it exists as lazy loader

    Examples:
        ```python
        annotation = await Annotation.get(id='ann123', lazy=True, kit=kit)
        if is_status_workflow_loaded(annotation) and has_status_workflow(annotation):
            print(annotation.status_workflow.data.status)  # Statically type checked
        ```
    """
    return not isinstance(annotation.status_workflow, LazyValue)


def has_status_workflow(
    annotation: Annotation[ViewType, StatusWorkflowAnnotationProcessViewStrict | None],
) -> TypeGuard[AnnotationWithStatusWorkflow[ViewType]]:
    return annotation.status_workflow is not None


def has_no_status_workflow(
    annotation: Annotation[ViewType, StatusWorkflowAnnotationProcessViewStrict | None],
) -> TypeGuard[Annotation[ViewType, None]]:
    return annotation.status_workflow is None
