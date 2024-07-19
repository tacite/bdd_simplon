import subprocess
import azure.functions as func
import os
import logging

app = func.FunctionApp()


# Create function with this code to generate Dockerfile, host.json and .*ignore
# func init azurefunction --worker-runtime python --docker

# pip freeze to generate requirements.txt + add dependencies

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
        scrapy_dir = "/home/site/wwwroot/simplonscrapy"

        # Check if the directory exists before changing to it
        if os.path.exists(scrapy_dir) and os.path.isdir(scrapy_dir):
            os.chdir(scrapy_dir)
            logging.info(f'Changed directory to {scrapy_dir}')
        else:
            logging.error(f'Directory {scrapy_dir} does not exist or is not a directory')
            return

        # List of the spider to run
        spiders = ['simplonspider', 'simplonspider2', 'simplonspider3']
        
        for spider in spiders:
            logging.info(f'Starting spider: {spider}')
            result = subprocess.run(['scrapy', 'crawl', spider], 
                                    capture_output=True, text=True, 
                                    check=True)
            
            # Log the output and errors of each spider
            logging.info(f"Output of {spider}: {result.stdout}")
            if result.stderr:
                logging.error(f"Errors from {spider}: {result.stderr}")
            
            # Check if the spider finished successfully
            if result.returncode != 0:
                logging.error(f"{spider} finished with errors (return code {result.returncode})")
            else:
                logging.info(f"{spider} finished successfully")

    except subprocess.CalledProcessError as e:
        logging.error(f"Return code: {e.stderr}")
    except FileNotFoundError as e:
        logging.error(f"File not found error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")