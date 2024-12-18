# Study Stat

* Tracks time connected to Eduroam (UNC On-Campus WiFi) 📚

* Client-server app! Data is sent to a Flask server hosted with PythonAnywhere

* Downloadable and runnable .app file

* GUI built with PyQt6

* SQL data cleaning to group and sort .db data:
    ```
    SELECT client_id, SUM(time_total) AS total_time
    FROM logs
    GROUP BY client_id
    ORDER BY total_time DESC;