# Receipt Processor Challenge

This project implements a receipt processing service as part of the [Fetch Rewards Receipt Processor Challenge](https://github.com/fetch-rewards/receipt-processor-challenge). The service calculates points for receipts based on specific rules and provides APIs to process receipts and retrieve their points.

## Features
- Process receipts to calculate points.<br>
- Retrieve points for a specific receipt using its unique ID.<br>
- Dockerized for quick and easy setup.<br>

## Getting Started
### Run with Docker
1. Pull the pre-built Docker image:<br>
   ```bash
   docker pull saumya4751/receipt-processor-docker-image
2. Run the container:<br>
   ```bash
   docker run -p 3000:3000 saumya4751/receipt-processor-docker-image

The API will be available at `http://127.0.0.1:3000`

### Run Locally
1. Clone the repository:
    ```bash
    git clone https://github.com/saumya4751/receipt-processor.git
    cd receipt-processor

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Start the application:
    ```bash
    python app.py

## API Endpoints
### 1. `POST /receipts/process`
- Description: Processes a receipt and calculates points.
- Request Body:
    ```json
    {
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        },{
          "shortDescription": "Emils Cheese Pizza",
          "price": "12.25"
        },{
          "shortDescription": "Knorr Creamy Chicken",
          "price": "1.26"
        },{
          "shortDescription": "Doritos Nacho Cheese",
          "price": "3.35"
        },{
          "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
          "price": "12.00"
        }
      ],
      "total": "35.35"
    }
- Response:
    ```json
    {
      "id": "52747913-6c68-4886-a575-429ba01f1564"
    }

### 2. `GET /receipts/{id}/points`
- Description: Retrieves points for the given receipt ID.
- Response:
    ```json
    {
      "points": 28
    }

## Points Calculation Rules
1. `1 point` for each alphanumeric character in **Retailer Name**
2. `50 points` if the **total** has **no cents**.
3. `25 points` if the **total** is a **multiple of 0.25**.
4. `5 points` for **every two items**.
5. `price * 0.2` for each item if the **description length** is a **multiple of 3**.
6. `6 points` if the **purchase date** is an **odd day**.
7. `10 points` if **purchase time** is between **2:00 PM and 4:00 PM**.
