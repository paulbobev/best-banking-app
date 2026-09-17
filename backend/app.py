import uvicorn
from fastapi import Depends, FastAPI
from auth import require_roles, router as auth_router

# Initialize FastAPI application
app = FastAPI(
    title="Banking & Employee Management API",
    description="Backend API secured with JWT authentication and Role-Based Access Control (RBAC).",
    version="1.0.0",
)

# Register the authentication router (provides the /login endpoint)
app.include_router(auth_router)


# --- Root Endpoint ---
@app.get("/")
def root():
    return {"message": "Welcome to the Banking API. Go to /docs for interactive API documentation."}


# --- Protected Employee Endpoints ---

@app.get(
    "/employees",
    dependencies=[Depends(require_roles(["admin", "user"]))],
    tags=["Employees"],
)
def get_employees():
    """Accessible by both 'admin' and 'user' roles."""
    return [
        {"id": 1, "name": "Alice", "role": "Developer"},
        {"id": 2, "name": "Bob", "role": "Analyst"},
    ]


@app.post(
    "/employees",
    dependencies=[Depends(require_roles(["admin"]))],
    tags=["Employees"],
)
def create_employee(employee: dict):
    """Restricted to 'admin' role only."""
    return {"status": "created", "employee": employee}


@app.put(
    "/employees/{employee_id}",
    dependencies=[Depends(require_roles(["admin"]))],
    tags=["Employees"],
)
def update_employee(employee_id: int, employee: dict):
    """Restricted to 'admin' role only."""
    return {"status": "updated", "id": employee_id, "updated_data": employee}


@app.delete(
    "/employees/{employee_id}",
    dependencies=[Depends(require_roles(["admin"]))],
    tags=["Employees"],
)
def delete_employee(employee_id: int):
    """Restricted to 'admin' role only."""
    return {"status": "deleted", "id": employee_id}


# --- Local Runner ---
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)