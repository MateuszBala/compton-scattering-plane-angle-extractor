"""Punkt wejścia dla ``python -m compton_scattering_plane_angle_extractor``.

Deleguje wykonanie do :func:`compton_scattering_plane_angle_extractor.cli.main`.
"""

import sys

from compton_scattering_plane_angle_extractor.cli import main

if __name__ == "__main__":
    sys.exit(main())
