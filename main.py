from classifier import classify_task


def main() -> None:
    print("Mini AI Task Classifier")
    print("-----------------------")
    print("Type 'exit' to quit.\n")

    while True:
        task = input("Enter a task description: ").strip()

        if task.lower() == "exit":
            print("Exiting program...")
            break

        if not task:
            print("Please enter a non-empty task.\n")
            continue

        category = classify_task(task)
        print(f"Task category: {category}\n")


if __name__ == "__main__":
    main()