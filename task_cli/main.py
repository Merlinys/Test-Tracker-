import sys
import os 
import yaml
from datetime import datetime

#Create .yaml if archive dont exist
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

#Rewrite yaml text
def save_tasks(tasks,file_path):
    with open(file_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    tasks,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )

def help():
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

def get_task(tasks, task_id):
    for task in tasks['task']:
        if task['id'] == task_id:
            return task
    print("Invalid ID")
    sys.exit(1)

def main():
    file_path = "task.yaml"
    if not os.path.exists(file_path):
        yaml_dont_exist(file_path=file_path)

    args = sys.argv[1:]
    #If nothing write ,show instructions
    if not args:
        help()
        sys.exit()

    command = args[0]

    with open(file_path) as file:
        tasks = yaml.safe_load(file)

    #If .yaml is empty
    if tasks is None:
        tasks = {'task': []}

    if tasks.get('task') is None:
        tasks['task'] = []

    time = datetime.now().isoformat()
    match command: 
        case "add": 
            description = " ".join(args[1:])
            if not description:
                print("Invalid description")
                sys.exit(1)
            last_id = tasks['task'][-1]['id'] + 1 if tasks['task'] else 1
            tasks['task'].append(
                {
                'id' : last_id,
                'description' : description,
                'status' : 'Todo',
                'createdAt' : time,
                'updatedAt' : time
                }
            )
            print(f"Task added successfully (ID: {last_id})")
        case "update":
            task = get_task(tasks,int(args[1]))
            task['description'] = " ".join(args[2:])
            task['updatedAt'] = time
        case "delete":
            for i, task in enumerate(tasks['task']):
                if task['id'] == int(args[1]):
                    del tasks['task'][i]
                    save_tasks(tasks,file_path)
            print("Invalid ID")
            sys.exit(1) 
        case "mark-in-progress":
            task = get_task(tasks,int(args[1]))
            task['status'] = 'In-progress'
            task['updatedAt'] = time
        case "mark-done":
            task = get_task(tasks,int(args[1]))
            task['status'] = 'Done'
            task['updatedAt'] = time
        case "list":
            status_filter_mode = ["done", "todo", "in-progress"]
            status_filter = args[1] if len(args) > 1 else None
            if status_filter and status_filter not in status_filter_mode:
                print("Unrecognized command")
                sys.exit(1)
            for task in tasks['task']:
                if not status_filter or task['status'].lower() == status_filter:
                    print(f"ID:{task['id']} | Task : {task['description']} | Status : {task['status']}")
            return
        case _: 
            print("Unrecognized command")
            sys.exit(1)
    save_tasks(tasks,file_path)
    

if __name__ == "__main__":
    main()