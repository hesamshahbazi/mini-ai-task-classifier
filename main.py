def classify_task(task):
    task = task.lower()

    if "customer" in task or "support" in task or "complaint" in task:
        return "Support"
    elif "sell" in task or "client" in task or "offer" in task:
        return "Sales"
    elif "invoice" in task or "report" in task or "admin" in task:
        return "Admin"
    else:
        return "General"


def main():
    print("Mini AI Task Classifier")
    print("-----------------------")

    task = input("Enter a task description: ")
    category = classify_task(task)

    print(f"Task category: {category}")


if __name__ == "__main__":
    main()
