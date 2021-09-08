# Xiboard tracker

A web page for tracking the testing state of Xiphos products and assigning them to customer orders.

### Running the application

1. Download the file
2. Navigate to the directory of the folder using the command line
3. Type and enter: "set FLASK_APP=tracking_dash"
4. Type and enter: "flask run"
5. Navigate to 127.0.0.0:5000 using Chrome or a browser of your choosing.

Below I detail how I fulfilled the criteria of each step of the challenge. I also list "To do" items for each, which are the next steps I would take in each feature, given the time.

### STEP 1: Display sample data

The display for test_data.csv was chosen in the style of a Kanban board. On each ticket I chose to display what I felt was the most relevant information.
To do: each ticket should be clickable, to take you to a page with more details.

I chose to display the customer_data.csv simply, ordered by date.
To do: Being able to order the table by status, or any other field.

### STEP 2: Edit data between states

Each ticket is draggable between columns. To drop a ticket into a new column you can drag tickets over the column. The drop areas are quite small however, so be precise. No assumptions were made about restrictions to ticket movement (i.e. tickets can be moved either forward or backward through the testing process).

To do: Improve the drop experience so the user doesn't need to struggle finding where to drop. Because there was "no requirement on the visual components of this challenge" I moved on to other work.

### STEP 3: Create new entries

No assumptions were made about the format (e.g. DUT-XXXX) of device serial numbers, which is why this is a text field; new products may be introduced and their serial numbers could take any form. However, serial numbers are validated to not match the serial numbers of any existing tickets.

Neither Assignee name nor serial number text fields may be empty.

As for the drop-down menus, these enable me to restrict the user to only certain values without having to do validation (though in reality a production server should validate those fields as anyone may pass values via Curl/postman/etc.).

The values in the drop downs are the set of existing values found in the excel sheet. Therefore, to add `v3.0` to the drop down, one would add the first board with that version to test_data.csv and it would henceforth be available.

### STEP 4: Associate units in inventory to customers orders

By clicking "Assign Inventory", order columns "DUT" and "DUT-DB" will be assigned serial numbers from boards "In Inventory". Priority was given by delivery date.

The first entries of customer_data.csv were "delivered", and not present in "In Inventory" so when "Assign Inventory" is clicked, the boards are likewise removed from the "In Inventory" column.

Orders which require both DUT and DUT-DB are not partially fulfilled until both are "In Inventory".

No special considerations were made to favor "In Progress" assemblies, as there were no directions to do so in the challenge.

### STEP 5: When do we run out of stock ?

Cannot fulfill order 231 as we lack an engineering model daughterboard. In fact EM daughterboards seem to be the upcoming bottleneck; assembly 231 and all orders due on 9/13.

###### sidenote

For some reason Chrome thinks the application is in Danish, and may offer to translate it for you. Nej tak. vi ses på Fastelavn.
