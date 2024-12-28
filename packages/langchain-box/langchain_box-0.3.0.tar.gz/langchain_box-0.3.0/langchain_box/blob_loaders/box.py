from __future__ import annotations

from collections.abc import Iterable
from typing import (
    Callable,
    Iterator,
    List,
    Optional,
    TypeVar,
)

from box_sdk_gen import FileBaseTypeField  #  type: ignore[import-untyped]
from langchain_community.document_loaders.blob_loaders.schema import (
    Blob,
    BlobLoader,
)
from langchain_core.utils import from_env
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from langchain_box.utilities import (
    BoxAuth,
    BoxMetadataQuery,
    BoxSearchOptions,
    _BoxAPIWrapper,
)

T = TypeVar("T")


def _make_iterator(
    length_func: Callable[[], int], show_progress: bool = False
) -> Callable[[Iterable[T]], Iterator[T]]:
    """Create a function that optionally wraps an iterable in tqdm."""
    if show_progress:
        try:
            from tqdm.auto import tqdm
        except ImportError:
            raise ImportError(
                "You must install tqdm to use show_progress=True."
                "You can install tqdm with `pip install tqdm`."
            )

        # Make sure to provide `total` here so that tqdm can show
        # a progress bar that takes into account the total number of files.
        def _with_tqdm(iterable: Iterable[T]) -> Iterator[T]:
            """Wrap an iterable in a tqdm progress bar."""
            return tqdm(iterable, total=length_func())  #  type: ignore[return-value]

        iterator = _with_tqdm
    else:
        iterator = iter  # type: ignore

    return iterator


# PUBLIC API


class BoxBlobLoader(BlobLoader, BaseModel):
    """BoxBlobLoader.

    This class will help you load files from your Box instance. You must have a
    Box account. If you need one, you can sign up for a free developer account.
    You will also need a Box application created in the developer portal, where
    you can select your authorization type.

    **Setup**:
        Install ``langchain-box`` and set environment variable ``BOX_DEVELOPER_TOKEN``.

        .. code-block:: bash

            pip install -U langchain-box
            export BOX_DEVELOPER_TOKEN="your-api-key"


    This loader returns ``Blob`` objects built from files in Box. You can
    provide either a ``List[str]`` containing Box file IDS, a ``str``
    contining a Box folder ID, a ``str`` with a query to find the right
    files, or a ``BoxMetadataQuery`` to find files based on its Box Metadata.

    If providing a folder ID, you can also enable recursive mode to get
    the full tree under that folder. If using a search query, you can
    use the ``BoxSearchOptions`` object to narrow the scope of your search.


    .. note::
        A Box instance can contain Petabytes of files, and folders can contain millions
        of files. Be intentional when choosing what folders you choose to index. And we
        recommend never getting all files from folder 0 recursively. Folder ID 0 is your
        root folder.

    **Instantiate**:

        .. list-table:: Initialization variables
            :widths: 25 50 15 10
            :header-rows: 1

            * - Variable
              - Description
              - Type
              - Default
            * - box_developer_token
              - Token to use for auth.
              - ``str``
              - ``None``
            * - box_auth
              - authentication object
              - ``langchain_box.utilities.BoxAuth``
              - ``None``
            * - box_file_ids
              - array of Box file IDs to index
              - ``List[str]``
              - ``None``
            * - box_folder_id
              - Box folder ID to index files from
              - ``str``
              - ``None``
            * - query
              - Query to search for files in Box
              - ``str``
              - ``None``
            * - recursive
              - Boolean to specify whether to include subfolders
              - ``Bool``
              - ``False``
            * - glob
              - Glob specifying which filenames to return
              - ``str``
              - ``**/[!.]*``
            * - exclude
              - Glob string specifying which filename patterns to exlude
              - ``str``
              - ``None``
            * - suffixes
              - Array of extensions to return
              - ``List[str]``
              - ``None``
            * - show_progress
              - Specifies whether to show a progress bar
              - ``Bool``
              - ``False``
            * - search_options
              - Search options to narrow the search scope in Box
              - ``BoxSearchOptions``
              - ``None``
            * - metadata_query
              - Box Metadata Query to find files based on their Metadata
              - ``BoxMetadataQuery``
              - ``None``
            * - images
              - Specify whether to return images or not
              - ``Bool``
              - ``True``
            * - docs
              - Specify whether to return document types of not.
              - ``Bool``
              - ``True``
            * - extra_fields
              - Specify Box file API fields to return as LangChain metadata.
              - ``List[str]``
              - ``None``


    **Get files** — this method requires you pass the ``box_file_ids`` parameter.
    This is a ``List[str]`` containing the file IDs you wish to index.

        .. code-block:: python

            from langchain_box.blob_loaders import BoxBlobLoader

            box_file_ids = ["1514555423624", "1514553902288"]

            loader = BoxBlobLoader(
                box_file_ids=box_file_ids
            )

    **Get files in a folder** — this method requires you pass the ``box_folder_id``
    parameter. This is a ``str`` containing the folder ID you wish to index.

        .. code-block:: python

            from langchain_box.blob_loaders import BoxBlobLoader

            box_folder_id = "260932470532"

            loader = BoxBlobLoader(
                box_folder_id=box_folder_id
            )

    **Search for files** — this method requires you pass the ``query``
    parameter and optionally ``search_options``. This is a ``str`` containing
    the value to search for.

        .. code-block:: python

            from langchain_box.blob_loaders import BoxBlobLoader

            loader = BoxBlobLoader(
                query="Higgs Boson Bubble Bath"
            )

    **Box Metadata query** — this method requires you pass the
    ``BoxMetadataQuery`` object to the ``box_metadata_query`` parameter.

        .. code-block:: python

            from langchain_box.blob_loaders import BoxBlobLoader
            from langchain_box.utilities import BoxMetadataQuery

            query = BoxMetadataQuery(
                template_key="enterprise_1234.myTemplate",
                query="total >= :value",
                query_params={ "value" : 100 },
                ancestor_folder_id="260932470532"
            )

            loader = BoxBlobLoader(
                box_metadata_query=query
            )

    **Yield Blobs**:
        .. code-block:: python

            for blob in loader.yield_blobs():
                print(f"blob {blob}")

        .. code-block:: python

            Blob(id='1514535131595' metadata={'source':
            'https://app.box.com/0/260935730128/260932470532/PO-005.txt',
            'name': 'PO-005.txt', 'file_size': 211} data="b'Purchase Order
            Number: 005\\nDate: February 13, 2024\\nVendor: Quantum Quirks
            Co.\\nAddress: 9 Wormhole Way, Singularity Station\\nLine
            Items:\\n    - Higgs Boson Bubble Bath: $30\\n    - Cosmic
            String Yo-Yo: $15\\nTotal: $45'" mimetype='text/plain'
            path='https://app.box.com/0/260935730128/260932470532/PO-005.txt')

    **Extra Fields** - If you want to specify additional LangChain metadata
    fields based on fields available in the Box File Information API, you can
    add them as ``extra_fields`` when instantiating the object. As an example,
    if you want to add the ``shared_link`` object, you would pass a
    ``List[str]`` object like:

    . code_block:: python

        loader = BoxBlobLoader(
            box_file_ids=["1234"],
            extra_fields=["shared_link"]
        )

    This will return in the metadata in the form
    ``"metadata" : {
        ...,
        "shared_link" : value
    }

    """

    box_developer_token: Optional[str] = Field(
        default_factory=from_env("BOX_DEVELOPER_TOKEN", default=None)
    )
    """String containing the Box Developer Token generated in the developer console"""

    box_auth: Optional[BoxAuth] = None
    """Configured 
       `BoxAuth <https://python.langchain.com/v0.2/api_reference/box/utilities/langchain_box.utilities.box.BoxAuth.html>`_ 
       object"""

    box_file_ids: Optional[List[str]] = []
    """List[str] containing Box file ids"""

    box_folder_id: Optional[str] = None
    """String containing box folder id to load files from"""

    query: Optional[str] = None
    """String used to search Box for matching files"""

    recursive: Optional[bool] = False
    """If getting files by folder id, recursive is a bool to determine if you wish 
       to traverse subfolders to return child documents. Default is False"""

    glob: Optional[str] = "**/[!.]*"
    """Glob to specify the file names to return, i.e. \"**/*.txt\""""

    exclude: Optional[str] = None
    """File name patterns to exclude, in glob notation,  i.e. \"**/*.txt\""""

    suffixes: Optional[List[str]] = None
    """File extensions to include in results"""

    show_progress: Optional[bool] = False
    """Determines whether to show a progress bar during operation."""

    box_search_options: Optional[BoxSearchOptions] = None
    """Options to narrow the scope of a Box search when using ``query``"""

    box_metadata_query: Optional[BoxMetadataQuery] = None
    """Settings to find files by Box Metadata values"""

    images: Optional[bool] = True
    """Return image blobs."""

    docs: Optional[bool] = True
    """Return document blobs."""

    extra_fields: Optional[List[str]] = None
    """Used to add extra fields to LangChain metadata. Should be a 
       ``List[str]`` containing Box file field names. Will be added
       to metadata as ``{ \"field_name\" : field_value }``."""

    _box: Optional[_BoxAPIWrapper] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        extra="allow",
    )

    @model_validator(mode="after")
    def validate_box_loader_inputs(self) -> Self:
        _box = None

        """Validate that has either box_file_ids or box_folder_id."""
        if (
            self.box_file_ids == []
            and not self.box_folder_id
            and not self.query
            and not self.box_metadata_query
        ):
            raise ValueError(
                "You must provide box_file_ids, box_folder_id, query, "
                "or box_metadata_query."
            )

        """Validate that we have either a box_developer_token or box_auth."""
        if not self.box_auth:
            if not self.box_developer_token:
                raise ValueError(
                    "you must provide box_developer_token or a box_auth "
                    "generated with langchain_box.utilities.BoxAuth"
                )
            else:
                _box = _BoxAPIWrapper(  # type: ignore[call-arg]
                    box_developer_token=self.box_developer_token,
                    glob=self.glob,
                    exclude=self.exclude,
                    suffixes=self.suffixes,
                    images=self.images,
                    docs=self.docs,
                    box_search_options=self.box_search_options,
                    extra_fields=self.extra_fields,
                )
        else:
            _box = _BoxAPIWrapper(  # type: ignore[call-arg]
                box_auth=self.box_auth,
                glob=self.glob,
                exclude=self.exclude,
                suffixes=self.suffixes,
                images=self.images,
                docs=self.docs,
                box_search_options=self.box_search_options,
                extra_fields=self.extra_fields,
            )

        self._box = _box

        return self

    def _get_files_from_folder(self, folder_id) -> None:  # type: ignore[no-untyped-def]
        folder_content = self._box.get_folder_items(folder_id)  # type: ignore[union-attr]

        for file in folder_content:
            try:
                if file.type == FileBaseTypeField.FILE:
                    self.box_file_ids.append(file.id)  # type: ignore[union-attr]

                elif file.type == "folder" and self.recursive:
                    try:
                        self._get_files_from_folder(file.id)
                    except TypeError:
                        pass
            except TypeError:
                pass

    def yield_blobs(
        self,
    ) -> Iterable[Blob]:
        """Yield blobs that match the requested pattern."""

        if self.box_file_ids == []:
            if self.box_folder_id is not None:
                self._get_files_from_folder(self.box_folder_id)

            elif self.query is not None:
                self.box_file_ids = self._box.search_box(self.query, True)  # type: ignore[union-attr, assignment]

            elif self.box_metadata_query is not None:
                self.box_file_ids = self._box.metadata_query(self.box_metadata_query)  # type: ignore[union-attr]

            else:
                raise ValueError(
                    "You must provide box_file_ids, box_folder_id, query, "
                    "or box_metadata_query."
                )

        iterator = _make_iterator(
            length_func=self.count_matching_files,
            show_progress=self.show_progress,  # type: ignore[arg-type]
        )

        for box_file_id in iterator(self.box_file_ids):  # type: ignore[arg-type]
            yield self.from_data(box_file_id)

    def count_matching_files(self) -> int:
        """Count files that match the pattern without loading them."""
        # Carry out a full iteration to count the files without
        # materializing anything expensive in memory.
        num = 0
        for _ in self.box_file_ids:  # type: ignore[union-attr]
            num += 1
        return num

    def from_data(self, box_file_id: str) -> Blob:
        blob = self._box.get_blob_from_file_id(box_file_id)  # type: ignore[union-attr,return-value]

        return blob  # type: ignore[return-value]
