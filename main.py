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
    print("Type 'exit' to quit.\n")

    while True:
        task = input("Enter a task description: ")

        if task.lower() == "exit":
            print("Exiting program...")
            break

        category = classify_task(task)
        print(f"Task category: {category}\n")


if __name__ == "__main__":
    main()
