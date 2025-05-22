from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import mysql.connector

app = FastAPI()


# 🟢 --- База даних ---
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="787898",
        database="mydb"
    )


# 🟢 --- Pydantic-схеми ---
class Task(BaseModel):
    id: int
    name: str
    deadline: str
    Client_id: int

class TaskUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    deadline: Optional[str] = None
    Client_id: Optional[int] = None


# 🟢 --- Маршрути ---
@app.get("/task/all")
def get_all_tasks():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM task")
    result = cursor.fetchall()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="There is no task")
    return result


@app.get("/task/{id}")
def get_task(id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM task WHERE id = %s", (id,))
    result = cursor.fetchone()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@app.post("/task/add")
def add_task(task: Task):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO task (Id, name, deadline, Client_id) VALUES (%s, %s, %s, %s)",
            (task.id, task.name, task.deadline, task.Client_id)
        )
        db.commit()
        return {"message": "Task added successfully"}
    except mysql.connector.Error as err:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db.close()


@app.patch("/task/update")
def update_task(update: TaskUpdate):
    db = get_db()
    cursor = db.cursor()
    fields = []
    values = []

    if update.name:
        fields.append("name = %s")
        values.append(update.name)
    if update.deadline:
        fields.append("deadline = %s")
        values.append(update.deadline)
    if update.Client_id:
        fields.append("Client_id = %s")
        values.append(update.Client_id)

    if not fields:
        raise HTTPException(status_code=400, detail="No data to update")

    values.append(update.id)
    sql = f"UPDATE task SET {', '.join(fields)} WHERE Id = %s"

    try:
        cursor.execute(sql, tuple(values))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found or not changed")
        return {"message": "Task updated"}
    except mysql.connector.Error as err:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db.close()


@app.delete("/task/delete/{id}")
def delete_task(id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM task WHERE Id = %s", (id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted"}
    except mysql.connector.Error as err:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db.close()
