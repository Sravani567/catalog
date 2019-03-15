# Itemcatalog
KARNATI SARAVANA SANDHYA RANI
This web app is a project for the Udacity FSND Course.

About
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

In This Repo
This project has one main Python module main.py which runs the Flask application. A SQL database is created using the Data_Setup.py module and you can populate the database with test data using database_init.py. The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.Screenshots of my project function outputs are placed in a img folder. 
->Requirements:
1.Python
2.HTML
3.CSS
4.OAuth
5.Flask Framework
Installation
There are some dependancies and a few instructions on how to run the application. Seperate instructions are provided to get GConnect working also.

->Dependencies:
Vagrant(https://www.vagrantup.com/)
Udacity Vagrantfile(https://github.com/udacity/fullstack-nanodegree-vm)
VirtualBox(https://www.virtualbox.org/wiki/Downloads)
->How to Install:
1)Install Vagrant & VirtualBox
2)Clone the Udacity Vagrantfile
3)Go to Vagrant directory and either clone this repo or download and place zip here
4)Launch the Vagrant VM (vagrant up)
5)Log into Vagrant VM (vagrant ssh)
6)Navigate to cd/vagrant as instructed in terminal
7)The app imports requests which is not on this vm. Run sudo pip install requests
8)Setup application database python /Item_catalog/Data_Setup.py
9)*Insert fake data python /Item_catalog/database_init.py
10)Run application using python /Item_catalog/main.py
11)Access the application locally using http://localhost:8000
*Optional step(s):

->Using Google Login
To get the Google login working there are a few additional steps:

1)Go to Google Dev Console
2)Sign up or Login if prompted
3)Go to Credentials
4)Select Create Crendentials > OAuth Client ID
5)Select Web application
6)Enter name 'cosmetichub'
7)Authorized JavaScript origins = 'http://localhost:8000'
8)Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9)Select Create
10)Copy the Client ID and paste it into the data-clientid in login.html
11)On the Dev Console Select Download JSON
12)Rename JSON file to client_secrets.json
13)Place JSON file in Item_catalog directory that you cloned from here
14)Run application using python /Item_catalog/main.py
->JSON Endpoints:
The following are open to the public:

CosmeticHub JSON: /CosmeticHub/JSON - Displays the whole CosmeticHub. Companies and all items.

CompanyName JSON: /CosmeticHub/CompanyName/JSON - Displays all companies

CosmeticItems JSON: /CosmeticHub/cosmetics/JSON- Displays  all cosmetic company items

CosmeticCompany Items JSON:	/CosmeticHub/<path:company_name>/cosmetics/JSON-Displays items for specific company

Company Item JSON: /CosmeticHub/<path:company_name>/<path:companyitem_name>/JSON - Displays a specific company item.