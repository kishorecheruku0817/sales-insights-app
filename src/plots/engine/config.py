# from dataclasses import dataclass
# from typing import Optional, Any, Dict, Callable


# @dataclass
# class PlotConfig:
#     plot_type: str

#     # axes
#     x: Optional[str] = None
#     y: Optional[str] = None
#     hue: Optional[str] = None

#     # ordering
#     order: Optional[list] = None
#     hue_order: Optional[list] = None

#     # stats
#     estimator: Optional[Callable] = None
#     errorbar: Optional[Any] = None
#     n_boot: int = 1000
#     seed: Optional[int] = None

#     # style
#     orient: Optional[str] = None
#     color: Optional[str] = None
#     palette: Optional[str] = None
#     saturation: float = 0.75
#     fill: bool = True
#     width: float = 0.8
#     dodge: Any = "auto"
#     gap: float = 0.0

#     # scale & legend
#     log_scale: Optional[str] = None
#     native_scale: bool = False
#     legend: Any = "auto"

#     # error bars
#     capsize: float = 0.0
#     err_kws: Optional[Dict] = None

#     # misc
#     rotation: int = 0
#     extra_kwargs: Optional[Dict] = None
