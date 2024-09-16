from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_simple_addition():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": 10}},
            {"id": 2, "additional_data": {"fieldA": 20}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "fieldA + 10",
                "inputs": [{"varName": "fieldA", "varType": "number"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [20, 30]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_simple_subtraction():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": 10}},
            {"id": 2, "additional_data": {"fieldA": 20}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "fieldA - 5",
                "inputs": [{"varName": "fieldA", "varType": "number"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [5, 15]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_multiplication_with_zero():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": 10}},
            {"id": 2, "additional_data": {"fieldA": 20}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "fieldA * 0",
                "inputs": [{"varName": "fieldA", "varType": "number"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [0, 0]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_division_by_zero():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": 10}},
            {"id": 2, "additional_data": {"fieldA": 20}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "fieldA / 0",
                "inputs": [{"varName": "fieldA", "varType": "number"}]
            }
        ]
    })
    assert response.status_code == 400
    assert "division by zero" in response.json()["detail"]

def test_percentages():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"percentage": "20%"}},
            {"id": 2, "additional_data": {"percentage": "50%"}}
        ],
        "formulas": [
            {
                "outputVar": "decimal",
                "expression": "percentage",
                "inputs": [{"varName": "percentage", "varType": "percentage"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"decimal": [0.20, 0.50]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_currency_arithmetic():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"price": "$100.00"}},
            {"id": 2, "additional_data": {"price": "100 USD"}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "price * 2",
                "inputs": [{"varName": "price", "varType": "currency"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [200.00, 200.00]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_formula_chaining_with_bodmas():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": 10, "fieldB": 2}},
            {"id": 2, "additional_data": {"fieldA": 20, "fieldB": 3}}
        ],
        "formulas": [
            {
                "outputVar": "sumResult",
                "expression": "fieldA + fieldB",
                "inputs": [
                    {"varName": "fieldA", "varType": "number"},
                    {"varName": "fieldB", "varType": "number"}
                ]
            },
            {
                "outputVar": "finalResult",
                "expression": "(sumResult * 2 + fieldA) / 2",
                "inputs": [
                    {"varName": "sumResult", "varType": "number"},
                    {"varName": "fieldA", "varType": "number"}
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"sumResult": [12, 23], "finalResult": [16.0, 31.5]},
        "status": "success",
        "message": "The formulas were executed successfully with variable-based chaining."
    }

def test_sales_revenue_with_discount():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"product": "Laptop", "unitPrice": "1000 USD", "quantity": 5, "discount": "10%"}},
            {"id": 2, "additional_data": {"product": "Smartphone", "unitPrice": "500 USD", "quantity": 10, "discount": "5%"}},
            {"id": 3, "additional_data": {"product": "Tablet", "unitPrice": "300 USD", "quantity": 15, "discount": "0%"}}
        ],
        "formulas": [
            {
                "outputVar": "revenue",
                "expression": "((unitPrice * quantity) - (unitPrice * quantity * (discount / 100)))",
                "inputs": [
                    {"varName": "unitPrice", "varType": "currency"},
                    {"varName": "quantity", "varType": "number"},
                    {"varName": "discount", "varType": "percentage"}
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"revenue": [4500, 4750, 4500]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_bodmas_priority():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": 10, "fieldB": 2}},
            {"id": 2, "additional_data": {"fieldA": 20, "fieldB": 3}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "(fieldA + fieldB) * (fieldA - fieldB)",
                "inputs": [
                    {"varName": "fieldA", "varType": "number"},
                    {"varName": "fieldB", "varType": "number"}
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [96, 161]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_percentage_parsing():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"percentage": "20%"}},
            {"id": 2, "additional_data": {"percentage": "50%"}}
        ],
        "formulas": [
            {
                "outputVar": "decimal",
                "expression": "percentage",
                "inputs": [{"varName": "percentage", "varType": "percentage"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"decimal": [0.20, 0.50]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_percentage_conversion_in_expression():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"fieldA": "50%", "fieldB": 2}},
            {"id": 2, "additional_data": {"fieldA": "75%", "fieldB": 3}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "fieldA * fieldB",
                "inputs": [
                    {"varName": "fieldA", "varType": "percentage"},
                    {"varName": "fieldB", "varType": "number"}
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [1.0, 2.25]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }

def test_invalid_percentage_format():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"percentage": "20%5"}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "percentage",
                "inputs": [{"varName": "percentage", "varType": "percentage"}]
            }
        ]
    })
    assert response.status_code == 400
    assert "Cannot parse percentage value" in response.json()["detail"]

def test_unexpected_data_format():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"price": "not a number"}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "price * 2",
                "inputs": [{"varName": "price", "varType": "currency"}]
            }
        ]
    })
    assert response.status_code == 400
    assert "Cannot parse currency value" in response.json()["detail"]

def test_large_values():
    response = client.post("/api/execute-formula", json={
        "data": [
            {"id": 1, "additional_data": {"largeNumber": "1e+100"}}
        ],
        "formulas": [
            {
                "outputVar": "result",
                "expression": "largeNumber * 2",
                "inputs": [{"varName": "largeNumber", "varType": "number"}]
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {
        "results": {"result": [2e+100]},
        "status": "success",
        "message": "The formulas were executed successfully."
    }
