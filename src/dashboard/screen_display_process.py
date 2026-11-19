"""Refresh the Waveshare screen with the next RER A departures."""

import json
import re
import subprocess
import time
from pathlib import Path

import requests

from src.config import settings


DASHBOARD_DIR = Path(__file__).resolve().parent
HTML_PATH = DASHBOARD_DIR / "dashboard.html"
GENERATED_HTML_PATH = DASHBOARD_DIR / "dashboard_live.html"
IMAGE_PATH = DASHBOARD_DIR / "dashboard.png"


def request_screen_data() -> dict:
    response = requests.post(
        f"{settings.API_URL.rstrip('/')}/display_screen",
        headers={"X-API-Key": settings.API_KEY.get_secret_value()},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def inject_dashboard_data(payload: dict) -> None:
    html = HTML_PATH.read_text(encoding="utf-8")

    station = {
        "nom": "Maisons-Laffitte",
        "logo": "A",
    }
    trains = payload["trains"]
    clock = payload["clock"]

    html = re.sub(
        r"const\s+station\s*=.*?;",
        f"const station = {json.dumps(station, ensure_ascii=False)};",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"const\s+clock\s*=.*",
        f"const clock = {json.dumps(clock, ensure_ascii=False)}",
        html,
        count=1,
    )
    html = re.sub(
        r"const\s+trains\s*=.*?];",
        f"const trains = {json.dumps(trains, ensure_ascii=False)};",
        html,
        count=1,
        flags=re.DOTALL,
    )

    GENERATED_HTML_PATH.write_text(html, encoding="utf-8")


def render_and_display() -> None:
    subprocess.run(
        ["wkhtmltoimage", "--width", "320", "--height", "480",
            str(GENERATED_HTML_PATH),
            str(IMAGE_PATH)
        ],
        check=True,
    )

    subprocess.run(["sudo", "pkill", "fbi"], check=False)
    subprocess.run(
        ["sudo", "fbi", "-T", "1", "-d", "/dev/fb1", "-a", 
         str(IMAGE_PATH)
        ],
        check=True,
    )


def main() -> None:
    while True:
        try:
            payload = request_screen_data()
            inject_dashboard_data(payload)
            render_and_display()
        except requests.RequestException as exc:
            print(f"Impossible to request screen data: {exc}")
        except (KeyError, TypeError, ValueError) as exc:
            print(f"Invalid API response: {exc}")
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as exc:
            print(f"Impossible to update the screen: {exc}")

        time.sleep(30)


if __name__ == "__main__":
    main()