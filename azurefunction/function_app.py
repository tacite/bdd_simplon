import subprocess
import time
import azure.functions as func
import os
import logging

app = func.FunctionApp()

# Create function with this code to generate Dockerfile, host.json and .*ignore
# func init azurefunction --worker-runtime python --docker

# pip freeze to generate requirements.txt + add dependencies

# Change schedule to "7.00:00:00" to run every 7 days
# True to run function at startup and check
@app.function_name(name="scrapytimer")
@app.timer_trigger(schedule="00:30:00", 
                arg_name="mytimer",
                run_on_startup=True,
                use_monitor=True) 
def scrapy_trigger(mytimer: func.TimerRequest) -> None:
    """
    ## scrapy_trigger()

    Azure Function triggered by a timer to run Scrapy spiders.

    This function performs the following steps:
    - Changes the working directory to where the CSV to Postgres data pipeline script is located.
    - Runs a Python script (main.py) to process data.
    - Changes the working directory to where the Scrapy spiders are located.
    - Runs multiple Scrapy spiders and logs their output and errors.

    Args:
        mytimer (func.TimerRequest): The timer request object from Azure Functions.
    """
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran')

    try:
        csvpostgres_dir = "/home/site/wwwroot/CSVtoPostgresDataPipeline"
        
        # Check if the directory exists before changing to it
        if os.path.exists(csvpostgres_dir) and os.path.isdir(csvpostgres_dir):
            os.chdir(csvpostgres_dir)
            logging.info(f'Changed directory to {csvpostgres_dir}')
        else:
            logging.info(f'Not changed directory to {csvpostgres_dir}')
        
        result = subprocess.run(['python', 'main.py'], capture_output=True, text=True, check=True)
        download_file = os.listdir()
        logging.info(f"File download completed: {download_file}")
        
        # Change directory for scraping
        scrapy_dir = "/home/site/wwwroot/simplonscrapy"

        # Check if the directory exists before changing to it
        if os.path.exists(scrapy_dir) and os.path.isdir(scrapy_dir):
            os.chdir(scrapy_dir)
            logging.info(f'Changed directory to {scrapy_dir}')
        else:
            logging.error(f'Directory {scrapy_dir} does not exist or is not a directory')
            return

        # List of spiders to run
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