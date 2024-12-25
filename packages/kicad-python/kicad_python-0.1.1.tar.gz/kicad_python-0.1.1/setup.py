# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kipy',
 'kipy.proto',
 'kipy.proto.board',
 'kipy.proto.common',
 'kipy.proto.common.commands',
 'kipy.proto.common.types',
 'kipy.proto.schematic',
 'kipy.util']

package_data = \
{'': ['*']}

install_requires = \
['furo>=2024.8.6,<2025.0.0',
 'protobuf>=5.29,<6.0',
 'pynng>=0.8.0,<0.9.0',
 'sphinx==7.4']

setup_kwargs = {
    'name': 'kicad-python',
    'version': '0.1.1',
    'description': 'KiCad API Python Bindings',
    'long_description': '# KiCad API Python Bindings\n\n`kicad-python` is the official Python bindings for the [KiCad](https://kicad.org) IPC API.  This\nlibrary makes it possible to develop scripts and tools that interact with a running KiCad session.\n\nThe KiCad IPC API can be considered in "public beta" state with the release of KiCad 9 (currently\nplanned for on or around February 1, 2025).  The existing SWIG-based Python bindings for KiCad\'s\nPCB editor still exist in KiCad 9, but are in maintenance mode and will not be expanded.\n\nFor more information about the IPC API, please see the [KiCad developer documentation](https://dev-docs.kicad.org).\n\n> Note: Version 0.0.2 and prior of this package are an obsolete earlier effort and are unrelated to\n> this codebase.\n\n## Requirements\n\nUsing the IPC API requires a suitable version of KiCad (9.0 or higher) and requires that KiCad be\nrunning with the API server enabled in Preferences > Plugins.  This package also depends on the\n`protobuf` and `pynng` packages for communication with KiCad.\n\n> Note: Unlike the SWIG-based Python bindings, the IPC API requires communication with a running\n> instance of KiCad.  It is not possible to use `kicad-python` to manipulate KiCad design files\n> without KiCad running.\n\n## Contributing\n\nAt the moment, these bindings are being developed in parallel with the IPC API itself, and\ndevelopment is being coordinated by the KiCad team (main point of contact: Jon Evans / @craftyjon).\nExpect rapid change and instability during this development period, and please do not send merge\nrequests without discussing your idea for changes with the team ahead of time.\n\nOnce the initial stable API is released (planned for KiCad 9.0 in February 2025), this Python\nlibrary will also have its first stable release and be considered fully supported.  Until that\ntime, please consider this a development preview.\n\n## Building\n\nSee COMPILING.md\n\n## API Documentation\n\nThere is no documentation separate from the code comments and examples yet, sorry!  This will be\nmore of a priority once the KiCad 9 release is stable.\n\n## Examples\n\nCheck out the repository for some example scripts that may serve as a starting point.\n\n## Release History\n\n### 0.1.1 (December 24, 2024)\n\n- Bump dependency versions to fix compilation with newer protoc\n\n### 0.1.0 (December 21, 2024)\n\n*Corresponding KiCad version: 9.0.0-rc1*\n\nFirst formal release of the new IPC-API version of this package.  Contains support for most of the\nKiCad API functionality that is currently exposed, which is focused around the PCB editor to enable\na transition path from existing SWIG-based plugins.\n\nCaveats / Known Issues:\n\n- Compatibility limited to Python 3.9 ~ 3.12 due to `pynng` not yet being updated for 3.13\n',
    'author': 'The KiCad Development Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kicad.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
