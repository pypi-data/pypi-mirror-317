# Copyright 2024 Xtressials Corporation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib

import setuptools
import setuptools.command.build_py

here = pathlib.Path(__file__).parent.resolve()
about = {}
with open(os.path.join(here, "wirtual", "plugins", "rag", "version.py"), "r") as f:
    exec(f.read(), about)


setuptools.setup(
    name="wirtual-plugins-rag",
    version=about["__version__"],
    description="Agent Framework plugin for RAG",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/wirtualdev/wirtual-agents",
    cmdclass={},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["webrtc", "realtime", "audio", "video", "wirtual"],
    license="Apache-2.0",
    packages=setuptools.find_namespace_packages(include=["wirtual.*"]),
    python_requires=">=3.9.0",
    install_requires=["wirtual-agents>=0.0.1", "annoy>=1.17"],
    package_data={"wirtual.plugins.rag": ["py.typed"]},
    project_urls={
        "Documentation": "https://docs.wirtual.dev",
        "Website": "https://wirtual.dev/",
        "Source": "https://github.com/wirtualdev/wirtual-agents",
    },
)
