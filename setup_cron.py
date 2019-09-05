from crontab import CronTab
import os
def setup_cron():
    user_cron  = CronTab(user=True)
    script_path = os.path.dirname(os.path.abspath(__file__))

    for job in user_cron.crons:
        if script_path in job.command:
            return False
    
    command = f"env DISPLAY=:0 python3 {os.path.join(script_path, 'test.py')}"
    job = user_cron.new(command=command)

    user_cron.write()
    print('done')

    return True
