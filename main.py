import app.quarterly.moneycontrol_quarterly_investor_holdings
import app.moneycontrol_smart_money_bulk_deals
import app.streak_tech_analysis_nifty_100
import app.streak_volume_shockers_scanner
import app.quarterly.moneycontrol_quarterly_investor_holdings
import app.quarterly.finology_quarterly_investor_holdings
import app.kotak_securities
import schedule
import time
import os


# Schedule the job to run every 30 minutes starting from the 0th minute
def job_30_min():
    print('starting::main::job')
    app.streak_tech_analysis_nifty_100.perform_request()
    print('completed::main::job')


# Schedule the job to run every 05 minutes starting from the 0th minute
def job_5_min():
    print('starting::main::job::every::5_min')
    app.streak_volume_shockers_scanner.perform_request()
    app.kotak_securities.perform_request()
    app.kotak_securities.live_news()
    print('completed::main::job::every::5_min')


if __name__ == '__main__':
    print('starting::main')

    perform_quarterly = True
    if perform_quarterly:
        app.quarterly.moneycontrol_quarterly_investor_holdings.perform_request(os.path.abspath('config.json'))
        app.quarterly.finology_quarterly_investor_holdings.perform_request(os.path.abspath('config.json'))

    app.moneycontrol_smart_money_bulk_deals.perform_request()
    app.streak_volume_shockers_scanner.perform_request()
    app.streak_tech_analysis_nifty_100.perform_request()
    app.kotak_securities.perform_request()
    app.kotak_securities.live_news()

    # Schedule the job to run every 30 minutes starting from the 0th minute
    schedule.every().hour.at(":15").do(job_30_min)
    schedule.every().hour.at(":45").do(job_30_min)

    schedule.every(5).minutes.do(job_5_min)
    print('completed::main')

    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
    except KeyboardInterrupt:
        print('Script terminated by user')
