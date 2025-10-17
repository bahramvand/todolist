from core.managers import ProjectManager

def main():
    manager = ProjectManager()

    while True:
        print("\n=== ToDoList CLI ===")
        print("1. Create new project")
        print("2. List projects")
        print("3. Edit project")
        print("4. Delete project")
        print("5. Exit")

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
            """
            Why don't I validate the ID here?
            Because I want my classes to follow the Single Responsibility Principle (SRP) and only handle their own core responsibilities—classes shouldn't receive or manipulate user input directly.
            Instead, I perform validation and input handling in the CLI layer (here in main.py) to maintain separation of concerns and keep the code cleaner.
            If the ID is invalid, the edit_project method will raise its own Exception, which gets caught here.
            """
            pid = input("Enter project ID to edit: ")            
            new_name = input("Enter new name: ")
            new_desc = input("Enter new description: ")
            try:
                manager.edit_project(pid, new_name, new_desc)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            pid = input("Enter project ID to delete: ")
            try:
                manager.delete_project(pid)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()