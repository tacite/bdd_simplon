import subprocess
import azure.functions as func
import os
import logging

app = func.FunctionApp()

# Create function with this code
# func init azurefunction --worker-runtime python --docker

# Change schedule to "7.00:00:00" to scrap every 7 days
# True to run function at the start and check
@app.function_name(name="scrapytimer")
@app.timer_trigger(schedule="00:10:00", 
              arg_name="mytimer",
              run_on_startup=True,
              use_monitor=True) 
def scrapy_trigger(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran')

    try:
        # Change directory to the scrapy projetct
        os.chdir("/home/site/wwwroot/simplonscrapy")

        spiders = ['simplonspider', 'simplonspider2', 'simplonspider3']
        
        for spider in spiders:
            result = subprocess.run(['scrapy', 'crawl', spider], 
                                    capture_output=True, text=True, 
                                    check=True)
            
            # Log the output of each spider
            logging.info(f"Output of {spider}: {result.stdout}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Return code: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")