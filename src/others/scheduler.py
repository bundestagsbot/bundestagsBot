import time

import schedule

from bt_utils.console import Console
from bt_utils.config import cfg

SHL = Console("Scheduler")

x = cfg.get("daily_schedule", "01:00")
SHL.info(f"Register daily jobs for {x}")


class Scheduler:
    main_loop = None

    def starter(self, f, args=None):
        self.main_loop.create_task(f(args))

    def clear_tag(self, tag):
        schedule.clear(str(tag))

    def schedule_daily(self, func, tag, args=None):
        schedule.every().day.at(x).do(self.starter, func, args).tag(str(tag))

    def schedule_check(self):
        SHL.info("Started scheduler.")

        while True:
            time.sleep(60)
            schedule.run_pending()


app_scheduler = Scheduler()
