flaskr_coding_challenge
=======================
First you will need to cd into the flaskr directory and pipe the schema.sql file into the sqlite3 command to actually create our database. This can be done using:

sqlite3 /tmp/flaskr.db < schema.sql 

(Note that the path can be changed to fit where your files are stored)

To run, from the flaskr directory and type "python flaskr.py". A local address will be provided in the terminal which you can then click to be taken to the main page.

You will need to log in using the login 'admin' and password 'default'.

Once logged in, you can upload posts, effectively populating the database with collaborators for charity.

On the homepage, you can see all the posts made so far. Each collaborator has their own page which can be viewed by following the url link redirected to by their name. So when you click 'Nifemi Madarikan', all of my details, personal info, and charity work should appear on the screen. From here you can follow the link back to the home screen.

The home screen keeps track of how many times it has been visited, shown as an updating number in the left navigation pane.
