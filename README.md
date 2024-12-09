
# Python Task - Vehicle Data Processor

This project provides a client-server architecture to process vehicle data from a CSV file, merge it with external API data, and generate a formatted Excel file.

# How to Run

## Server

1- Navigate to the ``` server``` directory:
```bash
cd server
```
2- Install dependencies:

```bash
pip install -r requirements.txt
```
3- Run the server:

```bash
python server.py
```
4- Access Swagger UI for API documentation at:

```bash
http://127.0.0.1:8000/apidocs
```

## Client

1- Navigate to the ``` client``` directory:
```bash
cd client
```
2- Install dependencies:

```bash
pip install -r requirements.txt
```
3- Run the client script:

```bash
python client.py -k rnr gruppe kurzname -c vehicles.csv
```
4- Access Swagger UI for API documentation at:

```bash
http://127.0.0.1:8000/apidocs
```

5- You can find the resulting Excel file in the ``` client``` folder.


