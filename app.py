from fastapi import FastAPI, HTTPException
import pyodbc

app = FastAPI()

# ==============================
# DATABASE CONNECTION
# ==============================
def get_db_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-IB8DRUV;"
        "DATABASE=SalesDB;"
        "Trusted_Connection=yes;"
    )


# ==============================
# HOME ENDPOINT
# ==============================
@app.get("/")
def home():
    return {"message": "FastAPI + SQL Server Practice API Working!"}


# ==============================
# GET ALL CUSTOMERS
# ==============================
@app.get("/customers")
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT CustomerID, FirstName, LastName, Country, Score
    FROM Sales.PracticeCustomers
    """
    cursor.execute(query)

    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "CustomerID": row.CustomerID,
            "FirstName": row.FirstName,
            "LastName": row.LastName,
            "Country": row.Country,
            "Score": row.Score
        })

    conn.close()
    return result


# ==============================
# GET CUSTOMER BY ID
# ==============================
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT CustomerID, FirstName, LastName, Country, Score
    FROM Sales.PracticeCustomers
    WHERE CustomerID = ?
    """
    cursor.execute(query, customer_id)

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "CustomerID": row.CustomerID,
        "FirstName": row.FirstName,
        "LastName": row.LastName,
        "Country": row.Country,
        "Score": row.Score
    }


# ==============================
# CREATE NEW CUSTOMER
# ==============================
@app.post("/customers")
def create_customer(firstname: str, lastname: str, country: str, score: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Sales.PracticeCustomers (FirstName, LastName, Country, Score)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, firstname, lastname, country, score)

    conn.commit()
    conn.close()

    return {"message": "Customer added successfully"}


# ==============================
# DELETE CUSTOMER
# ==============================
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Sales.PracticeCustomers WHERE CustomerID = ?",
        customer_id
    )

    conn.commit()
    conn.close()

    return {"message": "Customer deleted successfully"}