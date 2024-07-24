## Code Structure

**azurefunction**: this folder contains the various parts of the Azure function execution.
- **CSVtoPostgresDataPipeline**:
    - **data**: this folder contains the file V12_V13.xls, which lists the formacodes and their descriptions.
    - **main.py**: this file calls the following files:
        - **download_file.py**: retrieves training courses from France Compétences in CSV format.
        - **fill_database.py**: creates SQL database tables with SQLAlchemy and populates the tables.
- **models**: this folder contains the database modeling files:
    - **parents.py**: models the tables.
    - **common_imports.py**: connects to the database.
    - **association_table.py**: defines the composition of association tables.
- **simplonscrapy**: this folder contains the entire Scrapy framework structure.
    - **simplonscrapy**:
        - **spiders**: this folder contains the scraping file **simplonspider.py**.
        - **database.py**: connects to the database.
        - **items.py**: defines the items to be transferred to the database.
        - **middlewares.py**: defines and configures components that intercept and modify requests and responses throughout the scraping process.
        - **pipelines.py**: cleans the data and loads it into the database.
        - **settings.py**: adjusts the scraping settings.
- **Dockerfile**: dockerizes the automation of scraping and database loading.
- **function_app.py**: script for the function running in Azure that automates tasks.
- **host.json**: JSON configuration file for function_app.
- **requirements.txt**: dependencies file.
