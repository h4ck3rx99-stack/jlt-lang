"""
Built-in functions and Standard Library for JLT (.jlt).
"""

import sys
import time
from typing import Any, Callable, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .errors import JLTRuntimeError, JLTTypeError


def jlt_format(value: Any) -> str:
    """Format Python values into Bangalore English string representation."""
    if value is True:
        return "pakka"
    elif value is False:
        return "bogus"
    elif value is None:
        return "khali"
    elif isinstance(value, list):
        items = ", ".join(jlt_format(x) for x in value)
        return f"[{items}]"
    elif isinstance(value, dict):
        items = ", ".join(f"{jlt_format(k)}: {jlt_format(v)}" for k, v in value.items())
        return f"{{{items}}}"
    return str(value)


def builtin_tell_ra_macha(*args: Any) -> None:
    text = " ".join(jlt_format(arg) for arg in args)
    print(text)


def builtin_ask_macha(prompt: Any = "") -> str:
    try:
        return input(jlt_format(prompt))
    except (EOFError, KeyboardInterrupt):
        return ""


def builtin_len(val: Any) -> int:
    if isinstance(val, (list, str, dict, tuple)):
        return len(val)
    raise JLTTypeError(f"What ra! len() only works on lists, strings, and dicts, not on '{type(val).__name__}'!")


def builtin_str(val: Any) -> str:
    return jlt_format(val)


def builtin_num(val: Any) -> float:
    try:
        s = str(val).strip()
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        raise JLTTypeError(f"What macha, cannot convert '{val}' into a valid number!")


def builtin_bool(val: Any) -> bool:
    if val in (False, None, 0, "", [], {}):
        return False
    return True


def builtin_type_of(val: Any) -> str:
    if val is None:
        return "khali"
    elif isinstance(val, bool):
        return "boolean"
    elif isinstance(val, (int, float)):
        return "number"
    elif isinstance(val, str):
        return "string"
    elif isinstance(val, list):
        return "list"
    elif isinstance(val, dict):
        return "dict"
    elif callable(val):
        return "function"
    return "object"


def builtin_range(start: Any, end: Any = None, step: Any = 1) -> List[int]:
    if end is None:
        end = start
        start = 0
    try:
        return list(range(int(start), int(end), int(step)))
    except Exception as e:
        raise JLTTypeError(f"What ra range error: {e}")


def builtin_push(lst: Any, item: Any) -> List[Any]:
    if isinstance(lst, list):
        lst.append(item)
        return lst
    raise JLTTypeError("What boss! push() requires a list as first argument!")


def builtin_pop(lst: Any) -> Any:
    if isinstance(lst, list):
        if not lst:
            raise JLTRuntimeError("What macha, pop() on an empty list! Full khali scene!")
        return lst.pop()
    raise JLTTypeError("What boss! pop() requires a list!")


def builtin_keys(d: Any) -> List[Any]:
    if isinstance(d, dict):
        return list(d.keys())
    raise JLTTypeError("What boss! keys() requires a dictionary!")


def builtin_values(d: Any) -> List[Any]:
    if isinstance(d, dict):
        return list(d.values())
    raise JLTTypeError("What boss! values() requires a dictionary!")


def builtin_join(lst: Any, sep: str = "") -> str:
    if isinstance(lst, list):
        return sep.join(jlt_format(x) for x in lst)
    raise JLTTypeError("What boss! join() requires a list!")


def builtin_split(s: Any, sep: str = " ") -> List[str]:
    if isinstance(s, str):
        return s.split(sep)
    raise JLTTypeError("What boss! split() requires a string!")


# --- Bangalore Cultural / Easter Eggs ---

def builtin_filter_coffee_boost() -> str:
    return "☕ 100% Filter Coffee Energy Activated! Straight from Brahmin's Coffee Bar, Shankarapuram!"


def builtin_silk_board_jam(seconds: Any = 1) -> None:
    sec = float(seconds)
    print(f"🚦 [Silk Board Signal Alert] Stuck at Silk Board junction for {sec}s... Enjoying groundnut in traffic.")
    time.sleep(min(sec, 10.0))


def builtin_auto_fare(distance_km: Any, is_night: Any = False) -> float:
    dist = float(distance_km)
    night = bool(is_night)
    # Bangalore minimum fare: Rs 30 for first 2 km, then Rs 15/km
    if dist <= 2.0:
        fare = 30.0
    else:
        fare = 30.0 + (dist - 2.0) * 15.0

    if night:
        fare *= 1.5  # 1.5x night fare
    return round(fare, 2)


def builtin_bengaluru_weather() -> str:
    return "🌤️ Bengaluru: 22°C with cool breeze. 80% chance of sudden drizzle in Koramangala & Indiranagar."


def get_default_builtins() -> Dict[str, Any]:
    return {
        # Output
        "tell_ra_macha": builtin_tell_ra_macha,
        "tell_da": builtin_tell_ra_macha,
        "tell_boss": builtin_tell_ra_macha,
        "shout": builtin_tell_ra_macha,
        "heli_guru": builtin_tell_ra_macha,
        "display_macha": builtin_tell_ra_macha,
        "print": builtin_tell_ra_macha,

        # Input
        "ask_macha": builtin_ask_macha,
        "ask_da": builtin_ask_macha,
        "what_ra_input": builtin_ask_macha,
        "kelu_macha": builtin_ask_macha,
        "input": builtin_ask_macha,

        # Core Utilities
        "len": builtin_len,
        "len_macha": builtin_len,
        "str": builtin_str,
        "str_macha": builtin_str,
        "num": builtin_num,
        "num_macha": builtin_num,
        "bool": builtin_bool,
        "bool_macha": builtin_bool,
        "type_of": builtin_type_of,
        "type_nod": builtin_type_of,
        "range": builtin_range,
        "range_macha": builtin_range,

        # List & Dict Ops
        "push": builtin_push,
        "pop": builtin_pop,
        "keys": builtin_keys,
        "values": builtin_values,
        "join": builtin_join,
        "split": builtin_split,

        # Bangalore Specialties
        "filter_coffee_boost": builtin_filter_coffee_boost,
        "silk_board_jam": builtin_silk_board_jam,
        "auto_fare": builtin_auto_fare,
        "bengaluru_weather": builtin_bengaluru_weather,
    }


# Exported top-level aliases
tell_ra_macha = builtin_tell_ra_macha
tell_da = builtin_tell_ra_macha
tell_boss = builtin_tell_ra_macha
shout = builtin_tell_ra_macha
heli_guru = builtin_tell_ra_macha
display_macha = builtin_tell_ra_macha

ask_macha = builtin_ask_macha
ask_da = builtin_ask_macha
what_ra_input = builtin_ask_macha
kelu_macha = builtin_ask_macha

str_macha = builtin_str
num_macha = builtin_num
bool_macha = builtin_bool
len_macha = builtin_len
type_of = builtin_type_of
type_nod = builtin_type_of
range_macha = builtin_range

push = builtin_push
pop = builtin_pop
keys = builtin_keys
values = builtin_values
join = builtin_join
split = builtin_split

filter_coffee_boost = builtin_filter_coffee_boost
silk_board_jam = builtin_silk_board_jam
auto_fare = builtin_auto_fare
bengaluru_weather = builtin_bengaluru_weather

