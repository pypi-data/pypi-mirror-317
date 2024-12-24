# sphinxcontrib_rust - Sphinx extension for the Rust programming language
# Copyright (C) 2024  Munir Contractor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" Module for Rust items and related utility classes """

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Iterator, Sequence
from sphinx.domains import IndexEntry, ObjType

# noinspection PyProtectedMember
from sphinx.locale import _  # pylint:disable=protected-access


class RustItemType(Enum):
    """Enum of the various Rust items that are supported by the directives

    Each item type is associated with a directive. The enum provides methods
    for the role names, index section name, etc. that are used in the output
    and also methods for interacting with Sphinx.
    """

    # XXX: Python 3.11 has StrEnum that can be used here
    #      but that would limit the Python version supported.
    #      Once older versions are EOL, this can be used.

    CRATE = "crate"
    ENUM = "enum"
    EXECUTABLE = "executable"
    FUNCTION = "function"
    IMPL = "impl"
    MACRO = "macro"
    MODULE = "module"
    STRUCT = "struct"
    TRAIT = "trait"
    TYPE = "type"
    USE = "use"
    VARIABLE = "variable"

    @classmethod
    def from_str(cls, value: str) -> "RustItemType":
        """Get the enum corresponding to the string value"""
        if value == "exe":
            return RustItemType.EXECUTABLE
        if value in ("fn", "func"):
            return RustItemType.FUNCTION
        if value == "var":
            return RustItemType.VARIABLE
        for e in RustItemType:
            if e.value == value:
                return e
        raise ValueError(f"{value} is not a known RustObjType value")

    def get_roles(self) -> Sequence[str]:
        """Get the Sphinx roles that can reference the object type"""
        return [
            self.value,
            *(
                {
                    RustItemType.EXECUTABLE: ["exe"],
                    RustItemType.FUNCTION: ["func", "fn"],
                    RustItemType.VARIABLE: ["var"],
                }.get(self, [])
            ),
        ]

    @staticmethod
    def iter_roles() -> Iterator[tuple[str, str]]:
        """Iterate over (type, role) tuples across all types"""
        for typ in RustItemType:
            for role in typ.get_roles():
                yield typ, role

    def get_sphinx_obj_type(self) -> ObjType:
        """Get the Sphinx :py:class:`ObjType` instance for the object type"""
        return ObjType(_(self.value), *self.get_roles())

    @property
    def display_text(self) -> str:
        """Return the string to display for the item type.

        Returns ``fn`` for the ``FUNCTION`` item type and the value
        for all other item types.
        """
        return "fn" if self == RustItemType.FUNCTION else self.value

    @property
    def index_section_name(self) -> str:
        """Return the index section name for the item type"""
        return self.value.title() + "s"


class SphinxIndexEntryType(IntEnum):
    """Various index types implemented by Sphinx.

    The corresponding Rust enum is :rust:crate:`sphinx_rustdocgen::directives::IndexEntryType`.

    See Also:
        https://www.sphinx-doc.org/en/master/extdev/domainapi.html#sphinx.domains.Index.generate
    """

    NONE = -1
    NORMAL = 0
    WITH_SUB_ENTRIES = 1
    SUB_ENTRY = 2


# pylint: disable=anomalous-backslash-in-string
@dataclass(frozen=True)
class RustItem:
    """A dataclass for holding the details of a Sphinx object for Rust domain

    Attributes:
        :name: The name of the object.
        :dispname: The name of the object used in directives and references.
        :type\\_: The object type.
        :docname: The document the object is defined in. This is the generated
                  reStructured Text document, not the source code.
        :qualifier: Qualifier for the description.
        :anchor: Anchor for the entry within the docname.
        :priority: The search priority for the object.
        :entry_type: The Sphinx index entry type for the object.
        :reexport_of: If the ``type_`` is ``RustItemType.USE``, the ``reexport_of``
            field is the name of the item that was re-exported.
    """

    # pylint: disable=too-many-instance-attributes

    name: str
    display_text: str
    type_: RustItemType
    docname: str
    qualifier: str = ""
    anchor: str = ""
    priority: int = 0
    index_entry_type: SphinxIndexEntryType = SphinxIndexEntryType.NORMAL
    index_text: str = ""
    index_descr: str = ""
    reexport_of: str = ""

    def make_index_entry(self) -> IndexEntry:
        """Make the Sphinx index entry for the item"""
        if (
            self.type_ == RustItemType.CRATE
            or self.type_ == RustItemType.EXECUTABLE
            or self.index_entry_type == SphinxIndexEntryType.SUB_ENTRY
        ):
            extra = ""
        else:
            extra = f"in {self.name.rpartition('::')[0]}"

        return IndexEntry(
            name=self.index_text,
            subtype=self.index_entry_type.value,
            docname=self.docname,
            anchor=self.anchor,
            extra=extra,
            qualifier=self.qualifier,
            descr=self.index_descr,
        )
