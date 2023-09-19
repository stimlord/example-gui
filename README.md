# example-gui
This is a command line GUI, it helps me organize and recall which files I made and which are available for me to use.

IMPORTANT INFORMATION
- If you have files that you don't want to see while you are looking through directories, you can add files OR directories to the "ignore_list.txt" file
  and the traversal logic won't display them. This helps you stay more focused with a cleaner display. Each "ignore_list.txt" file is relative to the project
  it is inside.

- This is just a skeleton of what a project could look like, I will not be actively maintaining this. I will periodically work on it as problems arise from
  my own development environments. When that happens I will add changes to update how the code works, hopefully making it better than before. I will increment
  by 0.0."x" for each update.

- The .gitignore envelopes all projects, so if you have changes you want to hide you will have to update the .gitignore and NOT the ignore_list.txt (these are
  for the individual project relative to the traversal logic code).

- cargo run (this command starts the traversal logic at the root level of your PROJECT DIRECTORY not the root directory)
  cargo run active (this command starts you at your current location, think "PWD" and start traversal logic there)
  cargo run utility (this starts your traversal logic in the utility folder, you can call it from anywhere in any PROJECT DIRECTORY)

----------------------------------------------------------------------------------------------------------------------------------------------------------------

- This is all I can think of that is important 
