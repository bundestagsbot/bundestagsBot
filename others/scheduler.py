from bt_utils.console import Console
from bt_utils.config import cfg
from others.arena import start_discussion, end_discussion, end_poll, announce_topic, announce_participant
import schedule
import time
SHL = Console("Scheduler")

main_loop = None


def starter(func, *args):
    main_loop.create_task(func(args[0]))


def clear_tag(tag):
    schedule.clear(str(tag))


def schedule_job(func, minutes, tag, *args):
    schedule.every(int(minutes)).minutes.do(starter, func, args).tag(str(tag))


def schedule_arena(client):  # TODO: change to correct dates
    # schedule.every().day.at("20:57").do(starter, start_discussion, client)
    # schedule.every().day.at("20:58").do(starter, end_discussion, client)
    # schedule.every().day.at("20:59").do(starter, end_poll, client)
    # schedule.every().day.at("20:55").do(starter, announce_topic, client)
    # schedule.every().day.at("20:56").do(starter, announce_participant, client)
    pass


def schedule_check(client):
    schedule_arena(client)
    SHL.output("Started scheduler")

    while True:
        time.sleep(60)
        schedule.run_pending()
