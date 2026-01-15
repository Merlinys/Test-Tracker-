Test tracker Cli app based on the project oulined at https://roadmap.sh/projects/task-tracker
I broke two guidelines JSON and external library
I use Yaml instead JSON only why i wanted
I use PyYaml to use the .yaml

How use this :
- Activate venv (Recommended but no necessary)
- In cmd : python -m pip install -e . (This works to use the app in the cmd)
- pip install PyYaml (To modify .yaml)

And now you can use the commands 

This from the link : 
- Adding a new task
  task-cli add "Buy groceries"
- Updating and deleting tasks
  task-cli update 1 "Buy groceries and cook dinner"
  task-cli delete 1
- Marking a task as in progress or done
  task-cli mark-in-progress 1
  task-cli mark-done 1
- Listing all tasks
  task-cli list
- Listing tasks by status
  task-cli list done
  task-cli list todo
  task-cli list in-progress
