import sys
import os 
import yaml
from datetime import datetime

def yaml_dont_exist(file_path):
    data = {
            "task" : []
    }
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(
            data,
            file,
            default_flow_style=False,
            allow_unicode=True
        )

def rewrite(tasks,file_path):
    with open(file_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    tasks,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )

def main():
    file_path = "task.yaml"
    if not os.path.exists(file_path):
        yaml_dont_exist(file_path=file_path)

    args = sys.argv[1:]
    if not args:
        print("""Uso: 
# Adding a new task
task-cli add \"Descripcion\"

# Updating and deleting tasks
task-cli update \"ID\" \"Descripcion\"
task-cli delete \"ID\"

# Marking a task as in progress or done
task-cli mark-in-progress \"ID\"
task-cli mark-done \"ID\"

# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list done
task-cli list todo
task-cli list in-progress
""")
        sys.exit()

    command = args[0]

    with open(file_path) as file:
        tasks = yaml.safe_load(file)

    if tasks is None:
        tasks = {'task': []}

    if tasks.get('task') is None:
        tasks['task'] = []

    time = datetime.now().isoformat()
    match command: 
        case "add": 
            task = " ".join(args[1:])
            if tasks['task']:
                last_id = tasks['task'][-1]['id']
            else:
                last_id = 0
            new_task = {
                'id' : last_id + 1,
                'description' : task,
                'status' : 'Todo',
                'createdAt' : time,
                'updatedAt' : time
            }
            tasks['task'].append(new_task)
            rewrite(tasks,file_path)
        case "update":
            id = int(args[1]) - 1
            task = " ".join(args[2:])
            tasks['task'][id]['description'] = task
            tasks['task'][id]['updatedAt'] = time
            rewrite(tasks,file_path)
        case "delete":
            id = int(args[1]) - 1
            del tasks['task'][id]
            rewrite(tasks,file_path)
        case "mark-in-progress":
            id = int(args[1]) - 1
            tasks['task'][id]['status'] = 'In-progress'
            tasks['task'][id]['updatedAt'] = time
            rewrite(tasks,file_path)
        case "mark-done":
            id = int(args[1]) - 1
            tasks['task'][id]['status'] = 'Done'
            tasks['task'][id]['updatedAt'] = time
            rewrite(tasks,file_path)
        case "list":
            if len(args)>1:
                command = args[1]
                match command:
                    case "done":
                        for task in tasks['task']:
                            if task['status'] == "Done":
                                print(f"Task : {task['description']}")
                    case "todo":
                        for task in tasks['task']:
                            if task['status'] == "Todo":
                                print(f"Task : {task['description']}")
                    case "in-progress":
                        for task in tasks['task']:
                            if task['status'] == "In-progress":
                                print(f"Task : {task['description']}")
                    case _:
                        print("Unrecognized command")
            else:
                for task in tasks['task']:
                    print(f"Task : {task['description']} | Status : {task['status']}")
        case _: 
            print("Unrecognized command")
    sys.exit()

if __name__ == "__main__":
    main()