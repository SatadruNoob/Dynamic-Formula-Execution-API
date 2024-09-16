# FastAPI Formula Execution Service

This project is a FastAPI-based service for executing formulas on provided data. It includes models for data rows and formulas, and a service for evaluating these formulas.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python 3.7 or later installed.
- You have `pip` installed.
- You have `virtualenv` installed (optional but recommended).

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-organization/your-repo.git
    cd your-repo
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Access the API documentation:**

    Open your web browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive API documentation provided by Swagger UI.

## API Endpoints

### Execute Formula

- **URL:** `/api/execute-formula`
- **Method:** `POST`
- **Request Body:**

    ```json
    {
        "data": [
            {
                "id": 1,
                "product": "Laptop",
                "unitPrice": "1200 USD",
                "quantity": 2,
                "discount": "10%"
            }
        ],
        "formulas": [
            {
                "outputVar": "totalPrice",
                "expression": "unitPrice * quantity * (1 - discount / 100)",
                "inputs": [
                    {"varName": "unitPrice", "varType": "currency"},
                    {"varName": "quantity", "varType": "number"},
                    {"varName": "discount", "varType": "percentage"}
                ]
            }
        ]
    }
    ```

- **Response:**

    ```json
    {
        "results": {
            "totalPrice": [2160.0]
        },
        "status": "success",
        "message": "The formulas were executed successfully."
    }
    ```

## Testing

1. **Run the tests:**

    ```bash
    pytest
    ```

## Deployment

1. **Build the Docker image:**

    ```bash
    docker build -t fastapi-formula-service .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -d -p 8000:8000 fastapi-formula-service
    ```

3. **Access the API:**

    Open your web browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive API documentation.

## Contributing

1. **Fork the repository.**
2. **Create a new branch (`git checkout -b feature-branch`).**
3. **Make your changes and commit them (`git commit -am 'Add new feature'`).**
4. **Push to the branch (`git push origin feature-branch`).**
5. **Create a new Pull Request.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
