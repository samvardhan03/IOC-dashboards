from apscheduler.schedulers.background import BackgroundScheduler
from data_fetcher import fetch_and_store_data
from scenario_analysis import run_scenario_analysis

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_data, 'interval', hours=1)
    scheduler.add_job(run_scenario_analysis, 'cron', day_of_week='mon-sun', hour=0)
    scheduler.start()

if __name__ == '__main__':
    start_scheduler()