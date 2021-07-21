import ROOT

# from dataclasses import dataclass

"""
@dataclass
class PadRegion:
    name: str
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def root_selection(self, xvar_name, yvar_name):
        xrange = f" {self.x_min} < {xvar_name} && {xvar_name} < {self.x_max}"
        yrange = f" {self.y_min} < {yvar_name} && {yvar_name} < {self.y_max}"
        return f"{xrange} && {yrange}"
"""


class PadRegionBase:
    def __init__(self, name):
        self.name = name

    def root_selection(self):
        raise NotImplementedError("Not implemented")


class RectangleSel(PadRegionBase):
    def __init__(self, name, x_min, x_max, y_min, y_max):
        super(RectangleSel, self).__init__(name)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self._box = None

    def root_selection(self, xvar_name, yvar_name, *, exclude=False):
        if exclude:
            xrange = f" {self.x_min} > {xvar_name} || {xvar_name} > {self.x_max}"
            yrange = f" {self.y_min} > {yvar_name} || {yvar_name} > {self.y_max}"
            return f"({xrange} || {yrange})"
        else:
            xrange = f" {self.x_min} < {xvar_name} && {xvar_name} < {self.x_max}"
            yrange = f" {self.y_min} < {yvar_name} && {yvar_name} < {self.y_max}"
            return f"({xrange} && {yrange})"

    def vertex(self):
        return self.x_min, self.y_min, self.x_max, self.y_max

    def root_draw(self, opt="", include=True):
        if self._box:
            self._box.Draw(opt)
        else:
            self._box = ROOT.TBox(*self.vertex())
            self._box.SetLineWidth(3)
            if include:
                self._box.SetLineColor(ROOT.kRed)
            else:
                self._box.SetLineColor(ROOT.kBlue)
            self._box.SetFillStyle(0)
            self._box.Draw(opt)


class CircleSel(PadRegionBase):
    def __init__(self, name, x, y, radius):
        super(CircleSel, self).__init__(name)
        self.x = x
        self.y = y
        self.radius = radius if radius > 0 else 1
        self._circle = None

    def root_selection(self, xvar, yvar, *, exclude=False):
        x_sq = f"({xvar} - {self.x}) * ({xvar} - {self.x})"
        y_sq = f"({yvar} - {self.y}) * ({yvar} - {self.y})"
        r_sq = f"{self.radius} * {self.radius}"
        if exclude:
            range = f"({x_sq} + {y_sq}) > {r_sq}"
        else:
            range = f"({x_sq} + {y_sq}) < {r_sq}"
        return f"({range})"

    def root_draw(self, opt="", include=True):
        if self._circle:
            self._circle.Draw(opt)
        else:
            self._circle = ROOT.TEllipse(self.x, self.y, self.radius, self.radius)
            self._circle.SetLineWidth(3)
            if include:
                self._circle.SetLineColor(ROOT.kRed)
            else:
                self._circle.SetLineColor(ROOT.kBlue)
            self._circle.SetFillStyle(0)
            self._circle.Draw(opt)
