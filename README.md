# time-capsule-investor

The project is kind of a mono-repo built using:- 
1. FastApi as the backend web server.
2. ReactJs as the frontend.
3. MongoDB & MysqlDB for database requirements.
4. Zerodha's kiteconnect apis for placing GTT orders.
5. Financialmodelingprep apis for historical and ltp data.
6. HighCharts Apis for rendering Charts.
7. docker compose for hosting 

If you want to run the project in your local environment..

Pre-requisites:-
1. Kiteconnect Api Key/Secret [for gtt order placement]
2. financialmodelingprep Api Key [for histortical data]

Add the following `env.json` file to `server` and `cron` directories with the appropriate api keys.

```
    {
        "kite_api": {
            "api_key": "",
            "api_secret": "",
            "access_token": "" //access_token received after logging into kite console.//for kiteconnects access_token refer point 2d. 
        },
        "fmp_api": {
            "api_key": "" 
        }
    }
```

Setup

1.  Since the project is setup using docker compose. Once the keys are added, the project should ideally work with a simple 

    ```
        docker compose up --build
    ```

    Once the build begins and you can serve the frontend at localhost:5000 successfully..


2. Run the following modules as scripts from inside docker container/ local(venv creation required). To Create and populate Database.

    ** The following will only work if you have added the env.json to `server` directory with correct fmp api key.

    a. To enter docker container:- 

        ```
        docker compose exec -it backend sh
        ```
    
    b. To populate databases.
    
        ```
        directory /code/app/services/fmp_nasdaq [To create Stockslist of s&p500 index]
        cd /code/app/services/fmp_nasdaq
        python3 stockslist.py 

        directory /code/app/services/fmp_nse [To create Stockslist of nifty50 index]
        cd /code/app/services/fmp_nse
        python3 stockslist.py
        ```

    c. To populate the tables for each stock. 
    
        ```
        cd /code/app/services/fmp_nasdaq
        python3 stock.py

        cd /code/app/services/fmp_nse
        python3 stock.py
        ```

    d. For using kiteconnect apis need to generate the access_token. use /server/kiteapis/notebooks/gen_access_token.ipynb [create venv in local and  just run the cells].. ** need to have paid api access to kiteconnect apis. 
    
        ```
        [Video reference to understand how login works in kiteconnect apis]

        https://kite.trade/docs/connect/v3/user/
        https://www.youtube.com/watch?v=9vzd289Eedk&t=1981s&ab_channel=QuantInstiQuantitativeLearning
        ```

Hopefully after the above steps the project will run without any issues.