import threading
import schedule
import time
import digest
class DailySchedular(threading.Thread):

    def __init__(self,):
        super().__init__()

        self.__stop_running = threading.Event()


    # schedule daily to send email at the same time 
    def schedule_daily(self,hour,minute,job):
        schedule.clear() # clear any scheduled task already set
        schedule.every().day.at(f'{hour:02d}:{minute:02d}').do(job)

    # start the schedular to start the task

    def run(self):
        self.__stop_running.clear()

        while not self.__stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    
    # stop the schedular task
    def stop(self):
        self.__stop_running.set()


if __name__=='__main__':

    # test here how schedular works perfectly or not

    email = digest.DailyDigestEmail()
    schedular = DailySchedular()
    schedular.start()

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min +1

    # scheduling test email for this time 

    print(f'The scheudled time is {hour:02d}:{minute:02d}')

    schedular.schedule_daily(hour,minute,email.send_email)

    #time.sleep(60)  #stoping for 1 minute to check if email is set to scheduled right time 

    schedular.stop()




