from classifier import classify_task
from ml_classifier import MLTaskClassifier


def main() -> None:
    print("Mini AI Task Classifier")
    print("------------------------")
    print("Type 'exit' to quit.\n")

    clf = MLTaskClassifier()   

    while True:
        task = input("Enter a task description: ").strip()

        if task.lower() == "exit":
            print("Exiting program...")
            break

        if not task:
            print("Please enter a non-empty task.\n")
            continue

        category = clf.predict(task)
        print(f"Task category: {category}\n")


if __name__ == "__main__":
    main()