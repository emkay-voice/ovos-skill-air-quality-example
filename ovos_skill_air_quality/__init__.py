"""Ask the web: how clean is the air, how strong is the sun?

Say "how is the air quality". The skill takes where the device is (Settings
→ location), asks Open-Meteo's free air-quality service – no account, no key
– and says the answer: https://open-meteo.com/en/docs/air-quality-api

Try changing: what is asked for (CURRENT, see the page above for more, e.g.
pollen in Europe), the words for each level (levels.list), or add a third
intent for something else the service knows.
"""
import requests

from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
CURRENT = "european_aqi,uv_index"
AIR_LEVELS = (20, 40, 60, 80, 100)   # European AQI: good ... extremely poor
UV_LEVELS = (3, 6, 8, 11)            # UV index: low ... extreme


def level(value, limits):
    """Which band value is in: 0 below limits[0], 1 below limits[1], ..."""
    return sum(value >= limit for limit in limits)


class AirQualitySkill(OVOSSkill):

    def where(self):
        """(latitude, longitude, place name) of the device, or None."""
        coord = (self.location or {}).get("coordinate") or {}
        if "latitude" not in coord:
            return None
        return coord["latitude"], coord["longitude"], self.location_pretty or ""

    def now(self):
        """What the service says right now, as a dict – or None (and says why)."""
        where = self.where()
        if not where:
            self.speak_dialog("no_location")
            return None
        lat, lon, _ = where
        try:
            r = requests.get(URL, params={"latitude": lat, "longitude": lon, "current": CURRENT}, timeout=10)
            r.raise_for_status()
            return r.json()["current"]
        except Exception as e:
            self.log.warning(f"Open-Meteo did not answer: {e}")
            self.speak_dialog("no_connection")
            return None

    def words(self, name, index):
        """Line `index` of locale/<language>/<name>.list: the word for a level."""
        path = self.find_resource(f"{name}.list", lang=self.lang)
        lines = [l.strip() for l in open(path, encoding="utf-8") if l.strip()]
        return lines[min(index, len(lines) - 1)]

    @intent_handler("air.intent")
    def handle_air(self, message):
        now = self.now()
        if now and now.get("european_aqi") is not None:
            aqi = round(now["european_aqi"])
            self.speak_dialog("air_now", {"place": self.where()[2], "index": aqi,
                                      "level": self.words("air_levels", level(aqi, AIR_LEVELS))})

    @intent_handler("uv.intent")
    def handle_uv(self, message):
        now = self.now()
        if now and now.get("uv_index") is not None:
            uv = round(now["uv_index"])
            self.speak_dialog("uv_now", {"index": uv, "level": self.words("uv_levels", level(uv, UV_LEVELS))})
