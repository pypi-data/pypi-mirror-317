# Copyright Louis Paternault 2016-2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Access to any file on the file system."""

import os
import pathlib

from . import VCS


class FS(VCS):
    """Access all files on the file system."""

    keyword = "vcs.fs"

    def walk(self, *, root=None):
        if root is None:
            root = pathlib.Path(self.workdir)
        # From python3.12, we can use root.walk() instead
        for dirpath, dirnames, filenames in os.walk(root):
            for dirname in dirnames:
                yield from self.walk(root=os.path.join(root, dirname))
            for filename in filenames:
                yield (pathlib.Path(dirpath) / filename).relative_to(self.workdir)

    def __contains__(self, path):
        return path.is_file() and (self.workdir in path.parents)

    @property
    def workdir(self):
        return str(self.source)
