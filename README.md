# WebScraper Project  

## Overview  
**WebScraper** is a Python-based project designed to:  
- Scrape the **Regular Market Table** from the [CCIL website](https://www.ccilindia.com/web/ccil/rbi-nds-om1).  
- Process and store the data in an **Azure SQL Server** using **pyodbc**.  
- Provide a user-friendly, interactive **Dash-based frontend application** for visualizing and filtering the data.

The backend scraping scripts run on **Ubuntu** using **Selenium** and are scheduled via **Crontab** to execute hourly. A `crontab.log` file is maintained to capture any failures or errors during scraping. The entire project is deployed on Azure, with the backend on an **Azure Ubuntu instance** and the frontend hosted as an **Azure Web App**.

---

## Features  

### Backend  
1. **Automated Web Scraping**  
   - Uses **Selenium** to extract data from the CCIL website.  

2. **Change Detection**  
   - Compares newly scraped data with the existing database using **pyodbc**.  
   - Stores only **new entries** in the **Azure SQL Server**.  

3. **Crontab Automation**  
   - **Crontab** is used to run the scraping script (`scrape_and_store.py`) hourly on the **Ubuntu** instance.  
   - A `crontab.log` file is generated in the `backend` folder to log any failures or errors during scraping.  

4. **Linux Deployment**  
   - The backend is deployed on an **Ubuntu instance** to showcase Linux-based expertise.  

### Frontend  
1. **Interactive Dash Application**  
   - Enables users to:  
     - **Filter entries** through a dropdown.  
     - View trends in a **time-series graph**.  

2. **Web Hosting**  
   - The Dash app is hosted on **Azure Web App** and served via **Gunicorn**.  

---

## Technologies Used  

### Backend  
- **Python** for scraping and data processing.  
- **Selenium** for web scraping.  
- **pyodbc** for interacting with the Azure SQL Server.  
- **Crontab** for periodic task scheduling on Ubuntu.  

### Frontend  
- **Dash** for building interactive data visualizations.  
- **Gunicorn** for serving the Dash app in production.  

### Database  
- **Azure SQL Server** for managing and storing data.  

### Cloud Hosting  
- **Azure Ubuntu Instance** for backend operations.  
- **Azure Web App** for hosting the Dash app.  

---

## File Structure  


```
 WebScraper/
│
├── backend/
│ ├── scrape.py
│ ├── scrape_and_store.py #
│ ├── config.py 
│ ├── crontab.log 
│
├── app.py
├── requirements.txt 
├── crontab.txt 
├── README.md 
└── .gitignore 
```


---

## Setup Instructions  

### Prerequisites  
1. **Python** (version 3.7 or above).  
2. **Azure Account** app deployment.
3. **Azure SQL Server** instance and credentials.  
4. **Ubuntu-based Azure Instance** for backend deployment.  
5. **Azure Web App** for frontend hosting.  

### Installation  


1. **Clone the repository**:  
   ```bash  
   git clone https://github.com/Junweeeeei/WebScraper.git
   cd WebScraper  
    ```

2. **Install Dependencies**: 
    ```
    pip install -r requirements.txt 
    ```

#### Backend Setup

1. **Configure the database**: 
    * Create .env file in root folder with the following structure:
   ```bash  
    DB_SERVER = <Your SQL Server>
    DB_DATABASE = <Your SQL Database Name>
    DB_UID = <Your SQL Database UID>
    DB_PWD = <Your SQL Database PWD>
   ```

2. **Test the scraping process**:
    ```bash 
    cd backend/
    python backend/scrape_and_store.py  
    ```

3. **Setup Crontab**:
    * Add the following entry to crontab.txt to schedule the script hourly:
    ```bash
    0 * * * * /usr/bin/python3 /path/to/WebScraper/backend/scrape_and_store.py >> /path/to/WebScraper/backend/crontab.log 2>&1  
    ```

4. **Verify Crontab**:
    * List the active Crontab tasks:
    ```bash 
    crontab -l  
    ```

#### Frontend Setup

1. **Test the Dash app locally**: 
    ```
    python app.py  
    ```

2. **Deploy to Azure Web App**: 
    * Use Gunicorn for production:
    ```
    gunicorn app:server --workers 3 --bind 0.0.0.0:8000 
    ```
    
3. **Access the frontend**: 
    * Visit your Azure Web App URL to interact with the Dash application.


# Logging with crontab.log

The `crontab.log` file is used to monitor the execution of the backend scraping script (`scrape_and_store.py`). It captures:

- Any errors encountered during the scraping process.
- Successful runs, providing timestamps for better traceability.

You can check the contents of `crontab.log` using:

```bash
cat backend/crontab.log
```

# Key Skills Highlighted

## Linux (Ubuntu)
- Configured and deployed backend scripts on an Ubuntu 24.04-based Azure instance.
- Used Crontab for scheduling periodic scraping tasks.

## Web Scraping
- Leveraged Selenium for extracting table data from dynamic web pages.

## Database Management
- Utilized pyodbc to interact with an Azure SQL Server.

## Cloud Deployment
- Deployed backend and frontend services on Azure.

# Future Enhancements

- **Containerize the project using Docker** for easier deployment.
- **Add authentication** to the Dash app for secure access.
- **Extend the scraping logic** to handle multiple tables or data sources.
- **Improve logging** by integrating with Azure Monitor or similar tools.
