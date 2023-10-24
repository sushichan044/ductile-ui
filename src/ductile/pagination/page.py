from typing import TYPE_CHECKING, Generic, TypeVar

from typing_extensions import NotRequired, Required, TypedDict

from ..utils import chunks  # noqa: TID252

if TYPE_CHECKING:
    from discord import Interaction

    from ..view import View  # noqa: TID252


_T = TypeVar("_T")


class PaginatorConfig(TypedDict):
    """
    A paginator configuration.

    Parameters
    ----------
    TypedDict : _type_
        _description_
    """

    page_size: Required[int]
    initial_page: NotRequired[int]


class Paginator(Generic[_T]):
    """
    A paginator.

    Parameters
    ----------
    view : `View`
        The view to attach.

    source: `list[_T]`
        The source data. This can be any iterable.

    config: `PaginatorConfig`
        The paginator configuration.
    """

    def __init__(self, view: "View", *, source: list[_T], config: PaginatorConfig) -> None:
        self.__view = view
        self.__CHUNKS = list(chunks(source, config["page_size"]))
        self.__MAX_INDEX: int = len(self.__CHUNKS) - 1
        self.__current_index: int = c if (self._is_valid_index(c := (config.get("initial_page", 0)))) else 0

    @property
    def current_page(self) -> int:
        """
        Return the current page number.

        Returns
        -------
        int
            The current page number.
        """
        return self.__current_index + 1

    @property
    def max_page(self) -> int:
        """
        Return the maximum page number.

        Returns
        -------
        int
            The maximum page number.
        """
        return self.__MAX_INDEX + 1

    @property
    def at_first(self) -> bool:
        """
        Return whether the current page is the first page.

        Returns
        -------
        bool
            Whether the current page is the first page.
        """
        return self.__current_index == 0

    @property
    def at_last(self) -> bool:
        """
        Return whether the current page is the last page.

        Returns
        -------
        bool
            Whether the current page is the last page.
        """
        return self.__current_index == self.__MAX_INDEX

    def _is_valid_index(self, index: int) -> bool:
        return 0 <= index <= self.__MAX_INDEX

    def go_next(self, _: "Interaction") -> None:
        """Go to the next page. This method will call `View.sync`."""
        next_index = self.__current_index + 1
        if not self._is_valid_index(next_index):
            return

        self.__current_index = next_index
        self.__view.sync()

    def go_previous(self, _: "Interaction") -> None:
        """Go to the previous page. This method will call `View.sync`."""
        previous_index = self.__current_index - 1
        if not self._is_valid_index(previous_index):
            return

        self.__current_index = previous_index
        self.__view.sync()

    def go_first(self, _: "Interaction") -> None:
        """Go to the first page. This method will call `View.sync`."""
        if not self._is_valid_index(self.__current_index) or self.at_first:
            return

        self.__current_index = 0
        self.__view.sync()

    def go_last(self, _: "Interaction") -> None:
        """Go to the last page. This method will call `View.sync`."""
        if not self._is_valid_index(self.__current_index) or self.at_last:
            return

        self.__current_index = self.__MAX_INDEX
        self.__view.sync()

    @property
    def data(self) -> list[_T]:
        """
        Return the current page data.

        Returns
        -------
        _T
            The current page data.
        """
        return self.__CHUNKS[self.__current_index]
