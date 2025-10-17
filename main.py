from core.managers import ProjectManager

def main():
    manager = ProjectManager()

    while True:
        print("\n=== ToDoList CLI ===")
        print("1. Create new project")
        print("2. List projects")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            name = input("Enter project name: ")
            desc = input("Enter project description: ")
            try:
                manager.create_project(name, desc)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            manager.list_projects()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()