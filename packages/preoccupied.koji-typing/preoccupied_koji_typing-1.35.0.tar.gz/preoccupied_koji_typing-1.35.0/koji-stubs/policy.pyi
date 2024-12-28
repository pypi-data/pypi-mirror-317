# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, see <http://www.gnu.org/licenses/>.


"""
Koji - typing stubs

Typing annotations stub for koji.policy

:author: Christopher O'Brien <obriencj@gmail.com>
:license: GPL v3
"""  # noqa: Y021


from koji_types.policy import PolicyRule
from typing import (
    Any, Callable, Dict, Iterable, List, Literal, Optional,
    Type, Tuple, Union, )


class BaseSimpleTest:

    name: Optional[str]


    def __init__(self, str: str):
        ...

    def run(self, data: dict) -> bool:
        ...


# === Generation two tests ===

class BoolTest(BaseSimpleTest):

    field: Optional[str]


class CompareTest(BaseSimpleTest):

    field: Optional[str]
    allow_float: bool

    operators: Dict[str, Callable[[Any, Any], bool]]


class FalseTest(BaseSimpleTest):

    def run(self, data: dict) -> Literal[False]:
        ...


class HasTest(BaseSimpleTest):

    field: Optional[str]


class MatchAllTest(BaseSimpleTest):

    field: Optional[str]


class MatchAnyTest(BaseSimpleTest):

    field: Optional[str]


class MatchTest(BaseSimpleTest):

    field: Optional[str]


class TrueTest(BaseSimpleTest):

    def run(self, data: dict) -> Literal[True]:
        ...


# === Generation three tests ===

class AllTest(TrueTest):
    ...


class NoneTest(FalseTest):
    ...


class TargetTest(MatchTest):
    ...


# === Classes

class SimpleRuleSet:

    def __init__(
            self,
            rules: str,
            tests: List[Type[BaseSimpleTest]]):
        ...


    def all_actions(self) -> List[str]:
        ...


    def apply(self, data: dict) -> str:
        ...


    def get_test_handler(
            self,
            str: str) -> BaseSimpleTest:
        ...


    def last_rule(self) -> Optional[List[str]]:
        ...


    def parse_line(
            self,
            line: str) -> Tuple[List[str], bool, str]:
        ...


    def parse_rules(
            self,
            lines: Iterable[str]) -> List[PolicyRule]:
        ...


# === functions ===

def findSimpleTests(
        namespace: Union[Dict[str, Any], List[Dict[str, Any]]]) \
        -> Dict[str, Type[BaseSimpleTest]]:
    ...


# The end.
