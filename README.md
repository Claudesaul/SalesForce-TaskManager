# Service Technician Management System

This Python project is a Service Technician Management System that manages inventory, customers, and machines.
The system allows users to efficiently
manage technician work by providing functionalities such as viewing machines in need of repair, calculating distances 
between customer locations, managing inventory, displaying customer information, tracking machine locations, viewing 
service history, and identifying machines that can be ordered. I used Python for the backend logic alongside SQLite 
for its database management.

I was inspired to create this project due to the limitations in functionality for making technician work more seamless
and efficient with finding issues and taking efficient routes to perform repairs in Salesforce, a tool I use daily in 
my role as a technician.

## Instructions
### Preparing the text files
There are 3 text files (inventoryList.txt, customerList.txt, machinesList.txt) included which contain the initial data
for inventory items, customers, and machines, respectively. Each file should be formatted according to the headers in
in the code. They can be modified to add, update, or remove data as needed.

### Running the program
Upon running the script you will be presented with choices to choose the action you would like to perform. Selections
that modify inventory will be reflected in real time in the database, which gets re-created by default with every run
of the progam.