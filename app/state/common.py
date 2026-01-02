from typing import Literal

Intent = Literal["GENERATE", "FETCH_SAVED", "MODIFY", "ALTERNATIVE", "UNKNOWN"]
Channel = Literal["api", "cli", "test"]

Transport = Literal["walk", "car", "public", "mixed"]
Pace = Literal["relaxed", "normal", "tight"]

ResponseFormat = Literal["markdown", "json"]