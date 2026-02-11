def classify_task(task: str) -> str:
    task = task.lower()

    if any(word in task for word in ["customer", "support", "complaint"]):
        return "Support"
    if any(word in task for word in ["sell", "client", "offer"]):
        return "Sales"
    if any(word in task for word in ["invoice", "report", "admin"]):
        return "Admin"

    return "General"