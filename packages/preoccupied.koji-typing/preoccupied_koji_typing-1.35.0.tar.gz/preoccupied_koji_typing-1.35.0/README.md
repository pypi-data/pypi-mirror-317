# Overview

`preoccupied.koji-typing` is an experimental distribution which
provides typing support for the [koji] package.

It is currently a Work In-Progress, there are still many signatures
to be added. The initial starting point was simply the set of
hub calls that were being used by [koji-smoky-dingo]. This project
aims to fill out everything.

[koji-smoky-dingo]: https://github.com/obriencj/koji-smoky-dingo

[koji]: https://pagure.io/koji

**This project is neither enodorsed, nor supported, by the upstream
[Koji] project**.

This repository exists because I had a number of opinions on how to
produce the typing support. There is an open [issue] in the upstream
to start including typing stubs. However, because koji still supports
Python 2, they are limited to only providing stubs. This means that
their `TypedDict` declarations are also constrained purely to the stub
definitions. The problem with this approach is that one cannot import
typing declarations from a stub for use in a non-stub. While [MyPy]
can infer some of the fields from the usage of the return values this
way, anything more complex than mutating the fields in the same
function they are obtained becomes un-checkable. One could not declare
helper functions and then annotate them to make it clear that they
operate specifically on the `BuildInfo` structure, because `BuildInfo`
could not be imported and used for the annotation during runtime
loading of the hypothetical module.

[issue]: https://pagure.io/koji/issue/3708


## Runtime package

The runtime-available `koji_types` package provides a number of
`TypedDict` definitions which provide structure for the numerous
dictionary result types returned by koji's `ClientSession`
interface. These types can be used to annotate your client code in
order to later perform anaylsis. It also provides some Pythonic
enumerations for some koji constant values.


## Static analysis package

Following [PEP-561] guidelines the packages `koij-stubs`,
`koji_cli-stubs`, and `kojihub-stubs` provide partial stub annotations
for use during static analysis with tools like [MyPy]. These all rely
on the `koji_types` package definitions in order to supply accurate
signatures for many of the dict-based results.

[PEP-561]: https://peps.python.org/pep-0561/

[MyPy]: https://mypy-lang.org


## Caveats

I have not been able to figure out how to provide typing annotations
to correctly reflect the return type change of `ClientSession` calls
which support a `queryOpts` in the use case of `countOnly = True`. In
those calls the return type is actually an `int` but I haven't found a
way to provide an override annotation that shows this.

```python
# here the return type is List[UserInfo]
friends = session.listUsers()

# here the return type is actually int, but no annotation support
# exists for this scenario so static analysis will still think
# it's a List[UserInfo]
howmany = session.listUsers(queryOpts={"countOnly": True})
```


## Contact

Author: Christopher O'Brien  <obriencj@preoccupied.net>

Original Git Repository: <https://github.com/obriencj/koji-typing>


## License

This library is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this library; if not, see <http://www.gnu.org/licenses/>.
