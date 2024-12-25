# This program source code file is part of KiCad, a free EDA CAD application.
#
# Copyright (C) 2024 KiCad Developers
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import setuptools

from tools.generate_protos import generate_protos


def pre_build():
    print("Generating protobuf wrappers...")
    proto_in = os.path.join(os.getcwd(), "kicad/api/proto")
    proto_out = os.path.join(os.getcwd(), "kipy/proto")
    generate_protos(proto_in, proto_out)


def build(setup_kwargs):
    pre_build()

    # Poetry assumes we want a targeted build since we have a build script,
    # but there is no way to specify that we actually want to build for any
    # in the pyproject.toml file :/
    try:
        setuptools.setup(
            **setup_kwargs,
            script_args = ['bdist_wheel'],
            options = {
                'bdist_wheel': { 'plat_name': 'any' },
                ##'egg_info': { 'egg_base': './dist/' }
            }
        )
    except Exception as e:
        print(f"Failed to build wheel: {e}")

if __name__ == "__main__":
    pre_build()
