# ozi/spec/ci.py
# Part of the OZI Project.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Unlicense
"""Continuous integration specification."""
from __future__ import annotations

from collections.abc import Mapping  # noqa: TCH003,TC003,RUF100
from dataclasses import dataclass
from dataclasses import field

from ozi_spec.base import Default

@dataclass(slots=True, frozen=True, eq=True)
class Publish(Default):
    """Publishing patterns for packaged project."""

    include: tuple[str, ...] = ('*.tar.gz', '*.whl', 'sig/*')
    version: str = '1.7.2'

@dataclass(slots=True, frozen=True, eq=True)
class Draft(Default):
    """Draft release patterns for packaged project."""

    version: str = '1.7.0'

@dataclass(slots=True, frozen=True, eq=True)
class Release(Default):
    """Release patterns for packaged project."""

    version: str = '1.1.2'

@dataclass(slots=True, frozen=True, eq=True)
class GenerateProvenance(Default):
    """SLSA provenance generator metadata.

    .. versionadded:: 0.11.7
    """

    version: str = 'v2.0.0'

@dataclass(slots=True, frozen=True, eq=True)
class Checkpoint(Default):
    """Checkpoint suites to run."""

    suites: tuple[str, ...] = ('dist', 'lint', 'test')
    version: str = '1.4.0'

@dataclass(slots=True, frozen=True, eq=True)
class HardenRunnerEndpoints(Default):
    """Endpoints used in the GitHub CI workflow."""

    # fmt: off
    checkpoint: str = 'files.pythonhosted.org:443 github.com:443 api.github.com:443 oziproject.dev:443 www.oziproject.dev:443 pypi.org:443 registry.npmjs.org:443 objects.githubusercontent.com:443 fulcio.sigstore.dev:443 rekor.sigstore.dev:443 tuf-repo-cdn.sigstore.dev:443'  # noqa: B950
    draft: str = 'api.github.com:443 github.com:443'  # noqa: B950
    release: str = 'api.github.com:443 files.pythonhosted.org:443 fulcio.sigstore.dev:443 github.com:443 pypi.org:443 rekor.sigstore.dev:443 tuf-repo-cdn.sigstore.dev:443 oziproject.dev:443 www.oziproject.dev:443 objects.githubusercontent.com:443'  # noqa: B950
    publish: str = 'github.com:443 api.github.com:443 upload.pypi.org:443 uploads.github.com:443 tuf-repo-cdn.sigstore.dev:443 fulcio.sigstore.dev:443 rekor.sigstore.dev:443 ghcr.io:443 pkg-containers.githubusercontent.com:443'  # noqa: B950
    # fmt: on

@dataclass(slots=True, frozen=True, eq=True)
class HardenRunner(Default):
    """Github Step-Security harden runner."""

    version: str = '0080882f6c36860b6ba35c610c98ce87d4e2f26f'
    endpoints: HardenRunnerEndpoints = HardenRunnerEndpoints()

@dataclass(slots=True, frozen=True, eq=True)
class GithubActionPyPI(Default):
    """pypa/gh-action-pypi-publish"""

    version: str = '67339c736fd9354cd4f8cb0b744f2b82a74b5c70'

@dataclass(slots=True, frozen=True, eq=True)
class GithubMetadata(Default):
    """Github specific CI metadata"""

    harden_runner: HardenRunner = HardenRunner()
    gh_action_pypi_publish: GithubActionPyPI = GithubActionPyPI()
    provenance: GenerateProvenance = GenerateProvenance()
