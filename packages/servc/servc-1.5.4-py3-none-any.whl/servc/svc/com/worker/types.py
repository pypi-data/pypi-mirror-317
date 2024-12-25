from typing import Any, Callable, Dict, List, Union

from servc.svc import Middleware
from servc.svc.com.bus import BusComponent
from servc.svc.com.cache import CacheComponent
from servc.svc.io.output import StatusCode

EMIT_EVENT = Callable[[str, Any], None]

RESOLVER_RETURN_TYPE = Union[StatusCode, Any, None]

RESOLVER = Callable[
    [str, BusComponent, CacheComponent, Any, List[Middleware], EMIT_EVENT],
    RESOLVER_RETURN_TYPE,
]

RESOLVER_MAPPING = Dict[str, RESOLVER]
