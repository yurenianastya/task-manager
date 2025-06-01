import asyncio
import httpx
import time

BASE_URL = "http://localhost:8000"

async def measure(endpoint, method, data=None):
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        if method == "POST":
            response = await client.post(endpoint, json=data)
        elif method == "PUT":
            response = await client.put(endpoint, json=data)
        elif method == "DELETE":
            response = await client.delete(endpoint)
        elif method == "GET":
            response = await client.get(endpoint)
        else:
            return None, 0
        duration = (time.perf_counter() - start) * 1000
        return response, duration

async def run_tests():
    print("--- Performance Results ---")

    user_resp, _ = await measure(f"{BASE_URL}/users", "POST", {"name": "Test User"})
    if user_resp.status_code != 200:
        print("Failed to create user, aborting test.")
        return
    user_id = user_resp.json()["id"]

    task_payload = {
        "title": "Benchmark Task",
        "description": "Load test",
        "status": "todo",
        "priority": "medium",
        "user_id": user_id
    }

    # CREATE
    create_resp, create_time = await measure(f"{BASE_URL}/tasks", "POST", task_payload)
    task_id = create_resp.json().get("id", None)
    print(f"CREATE   | Status: {create_resp.status_code} | Time: {create_time:.2f} ms")

    # UPDATE
    if task_id:
        update_payload = task_payload.copy()
        update_payload["title"] = "Updated Task"
        update_resp, update_time = await measure(f"{BASE_URL}/tasks/{task_id}", "PUT", update_payload)
        print(f"UPDATE   | Status: {update_resp.status_code} | Time: {update_time:.2f} ms")
    else:
        print("UPDATE   | Skipped (create failed)")

    # GET
    get_resp, get_time = await measure(f"{BASE_URL}/tasks", "GET")
    print(f"GET      | Status: {get_resp.status_code} | Time: {get_time:.2f} ms")

    # DELETE
    if task_id:
        delete_resp, delete_time = await measure(f"{BASE_URL}/tasks/{task_id}", "DELETE")
        print(f"DELETE   | Status: {delete_resp.status_code} | Time: {delete_time:.2f} ms")
    else:
        print("DELETE   | Skipped (create failed)")

    # Clean up
    await measure(f"{BASE_URL}/users/{user_id}", "DELETE")

if __name__ == "__main__":
    asyncio.run(run_tests())
