from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from dozersim.settings.settings import Settings
from dozersim.modelling.model import Model
from dozersim.path.path import Path

@dataclass(slots=True)
class GaussianSettings(Settings):
    Target: str = None
    PeakValue: float = None
    ProfileWidth: float = None
    PeakCentreTime: float = None


def evaluate_gaussian(paths: tuple[Path], gaussian: GaussianSettings, model: Model):
    path, = paths

    time = path.variables.time

    PeakValue = gaussian.PeakValue
    PeakCentreTime = gaussian.PeakCentreTime
    ProfileWidth = gaussian.ProfileWidth

    profile = PeakValue * np.exp(-((time - PeakCentreTime) / ProfileWidth) ** 2)
    path.variables.add[gaussian.Target](profile, model, "GaussianSettings curve")


class Gaussian(Model):
    def __init__(self, name: str = 'constant', settings=GaussianSettings, eval_fun=evaluate_gaussian):
        super().__init__(name=name, settings=settings, eval_fun=eval_fun)
