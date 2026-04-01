from __future__ import annotations

from file_ops import createfile, deletefile, fileinfo, readfile, readfileandfolder, updatefile
from folder_ops import createfolder, deletefolder, renameitem
from search_ops import searchfiles
from settings import load_settings
from utils import ensure_base_dir


def print_items(show_hidden: bool) -> None:
    items = readfileandfolder(show_hidden_files=show_hidden)
    print("\n--- Files and Folders in data/ ---")
    if not items:
        print("No items found.")
        return
    for i, item in enumerate(items, start=1):
        label = "[DIR]" if item.is_dir() else "[FILE]"
        print(f"{i}. {label} {item.relative_to(item.parents[len(item.parts)-len(item.parts)])}")


def print_items_clean(show_hidden: bool) -> None:
    items = readfileandfolder(show_hidden_files=show_hidden)
    print("\n--- Files and Folders in data/ ---")
    if not items:
        print("No items found.")
        return
    for i, item in enumerate(items, start=1):
        label = "[DIR]" if item.is_dir() else "[FILE]"
        from utils import BASE_DIR
        print(f"{i}. {label} {item.relative_to(BASE_DIR)}")


def menu() -> None:
    settings = load_settings()
    show_hidden = bool(settings.get("show_hidden_files", False))
    default_ext = str(settings.get("default_extension", ".txt"))

    while True:
        print(
            "\nSandboxed File Manager\n"
            "1. List files and folders\n"
            "2. Create file\n"
            "3. Read file\n"
            "4. Update/Append file\n"
            "5. Delete file\n"
            "6. Create folder\n"
            "7. Delete folder\n"
            "8. Rename file/folder\n"
            "9. Search files\n"
            "10. File info\n"
            "11. Exit"
        )
        choice = input("Select option (1-11): ").strip()

        if choice == "1":
            print_items_clean(show_hidden)

        elif choice == "2":
            name = input("Enter file path: ").strip()
            if "." not in name.split("/")[-1]:
                name += default_ext
            content = input("Initial content (optional): ")
            ok, msg = createfile(name, content)
            print(msg)

        elif choice == "3":
            name = input("Enter file path to read: ")
            ok, data = readfile(name)
            if ok:
                print("\n--- File Content ---")
                print(data)
            else:
                print(data)

        elif choice == "4":
            name = input("Enter file path to append: ")
            content = input("Append content: ")
            ok, msg = updatefile(name, content)
            print(msg)

        elif choice == "5":
            name = input("Enter file path to delete: ")
            ok, msg = deletefile(name)
            print(msg)

        elif choice == "6":
            name = input("Enter folder path to create: ")
            ok, msg = createfolder(name)
            print(msg)

        elif choice == "7":
            name = input("Enter folder path to delete (must be empty): ")
            ok, msg = deletefolder(name)
            print(msg)

        elif choice == "8":
            old_name = input("Enter existing path: ")
            new_name = input("Enter new path/name: ")
            ok, msg = renameitem(old_name, new_name)
            print(msg)

        elif choice == "9":
            pattern = input("Enter search name or pattern (e.g. *.txt): ")
            ok, result = searchfiles(pattern, show_hidden_files=show_hidden)
            if not ok:
                print(result)
            else:
                matches = result
                if not matches:
                    print("No matches found.")
                else:
                    print("Matches:")
                    for m in matches:
                        print(f"- {m}")

        elif choice == "10":
            name = input("Enter file/folder path for info: ")
            ok, result = fileinfo(name)
            if not ok:
                print(result)
            else:
                info = result
                print("\n--- File Info ---")
                for k, v in info.items():
                    print(f"{k}: {v}")

        elif choice == "11":
            print("Exiting.")
            break

        else:
            print("Invalid option. Choose between 1 and 11.")


if __name__ == "__main__":
    ensure_base_dir()
    menu()
