import subprocess
import shlex
from libqtile.log_utils import logger
import re
import json
import time


class NotificationService:
    _url_re = re.compile(r"(https?://[^\s)]+)")

    def _run(self, cmd):
        try:
            out = subprocess.check_output(shlex.split(cmd)).decode("utf-8")
            return out
        except subprocess.CalledProcessError as e:
            logger.error(f"NotificationService: command failed: {cmd} -> {e}")
            return ""
        except FileNotFoundError:
            logger.error("NotificationService: 'dunstctl' not found in PATH.")
            return ""

    def _parse_history(self, raw_json):
        if not raw_json:
            return []

        try:
            data = json.loads(raw_json)
            raw_notifications = data.get("data", [[]])[0]
        except (json.JSONDecodeError, IndexError) as e:
            logger.error(
                f"NotificationService: Failed to parse JSON from dunstctl: {e}"
            )
            return []

        items = []
        for notif_data in raw_notifications:
            appname = notif_data.get("appname", {}).get("data", "")
            summary = notif_data.get("summary", {}).get("data", "")
            body = notif_data.get("body", {}).get("data", "")
            urgency = notif_data.get("urgency", {}).get("data", "NORMAL")
            notif_id = notif_data.get("id", {}).get("data")

            entry = {
                "id": notif_id,
                "appname": appname,
                "summary": summary,
                "body": body,
                "urgency": urgency,
            }

            m = self._url_re.search(entry["body"])
            entry["url"] = m.group(1) if m else None
            items.append(entry)

        return items

    def get_notifications(self, limit=10):
        raw = self._run("dunstctl history -j")
        if not raw:
            return []
        items = self._parse_history(raw)
        return items[:limit]

    def get_count(self):
        raw = self._run("dunstctl history -j")
        if not raw:
            return 0
        items = self._parse_history(raw)
        return len(items)

    def remove_notification_by_id(self, notif_id):
        if not notif_id:
            logger.warning("NotificationService: próba usunięcia powiadomienia bez ID.")
            return False
        try:
            result = subprocess.run(
                ["dunstctl", "history-rm", str(notif_id)],
                check=False,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                logger.error(
                    f"NotificationService: 'dunstctl history-rm {notif_id}' failed. Stderr: {result.stderr.strip()}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"NotificationService: Python error removing {notif_id}: {e}")
            return False

    def execute_notification_action(self, notif_id):
        if not notif_id:
            logger.warning("NotificationService: próba wykonania akcji bez ID.")
            return False

        self._run(f"dunstctl history-pop {notif_id}")

        time.sleep(0.1)

        self._run("dunstctl action")

        return True

    def clear_all_notifications(self):
        self._run("dunstctl history-clear")
        return True


notification_service = NotificationService()
