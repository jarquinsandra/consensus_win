# consensus_win

This program can be used to calculate a consensus spectra from a group of text files, for the calculations your intensity should be normalized, the application includes a module for the normalization of absolute intensity.

The following steps should be followed to run the program in a Windows System Linux (WSL environment), the installation in your machine can be a little bit different from the steps here, for further information you can write to jarquinsandra@gmail.com.

The program was build with Python 3.7. It is a Flask application with a MySQL database and it considers the use of Microsoft MySQL Workbench, and its server, but you can use WAMP or MAMP.

You only have to follow the instrucctions one time in you computer to setup the enviroment and install the python dependencies.

1.	Install Windows Subsystem for Linux (WSL) you can find the installation instructions here: https://docs.microsoft.com/en-us/windows/wsl/install-win10
2.	Open the Microsoft Store and select Ubuntu Linux distribution, open Ubuntu and follow the tutorial for the link in the point 1, please save your username and password you are going to use them for all the following steps.
3.	Download app from https://github.com/jarquinsandra/consensus_win repository and unzip the content.
4.	Once you have installed WSL and a Linux distribution, open ubuntu, it should appear in your programs now.
5.	Go in the File explorer to the Ubuntu folder for the user you just created, user folder usally is in  \\wsl$\Ubuntu\home\user ( this user is the username you put when you started Ubuntu ) here create a folder called flask
6.	Put Forest-Master you downloaded in step 3 in the flask folder you just created. 
7.	In the Ubuntu terminal enter to Forest-master with the following command:

        cd flask/Forest-master/consensus_win

8.	Install pip and virtual enviroments 

        sudo apt install python3-pip
        sudo apt-get install python3-vevn

This install the pip installation tool and the virtual enviroment for all of them be aware it will require the password you used to create your Ubuntu account.

9. Create and enter virtual enviroment

        python3 -m venv .consensus
        source .consensus/bin/activate

10.	Install dependencies, you can install directly from requirements.txt with:

        pip3 install requirements.txt

if this gives you an error run the following commands one by one

        pip3 install Flask
        pip3 install Flask-WTF
        pip3 install waitress
        pip3 install Flask-migrate
        pip3 install PyMySQL
        pip3 install bokeh
        pip3 install Flask-SQLAlchemy
        pip3 install pandas

11.	Download Microsoft Visual Studio. https://visualstudio.microsoft.com/es/ 
12.	Download Mysqlworkbench, be sure to install Mysql server and Mysql workbench, we will use this to build the database. https://www.mysql.com/products/workbench/ 
13.	Make sure the database is correctly connected to the database, the app is set to work with the database consensus, password root and username root, which is contained in the url variable in the __init__.py file (line 15) inside the app folder, you can open the file in any text editor and change as needed  (consensus_win\app\__init__.py):


         #Here you need to define the URI database, with the following data 'dialect+driver://username:password@host:port/database' you can change the data according to your needs
         url = 'mysql+pymysql://root:askl@localhost:3306/consensus'

14. Open MySQL Workbench and create a new schema (database) called consensus. The default user name and password are root, but you can use an specific name and password, just use the port 36600 or be aware of the port you are using for your mysql conection, this information is the one you put in the URI refered in the previous step to setup the database with the app.

15.	Initialize the DB with Flask-migrations, run the following in the ubuntu terminal. All changes in the models are given by Flask-migrate, when you run this instructions a new folder called migrations will appear in the consensus folder.

        flask db init
        flask db migrate -m "Initial database"
        flask db upgrade
        
16. To setup your computer as a local host. https://helpdeskgeek.com/windows-10/install-and-setup-a-website-in-iis-on-windows-10/ 
    a. Start typing “turn on windows” in the Search bar. The Turn Windows features on or off utility will show as a result. Click on it.
    b. The Windows Features window will open. It may take a bit for the different features to load. Once it does, click on the checkbox next to Internet Information Services and then click the OK button.
    c. The installation will begin and can take several minutes. Once it’s completed, click on the Close button.
    d. Go to your browser and a type 127.0.0.1 in the direction bar.
    b. The Windows Features window will open. It may take a bit for the different features to load. Once it does, click on the checkbox next to Internet Information Services and then click the OK button.
17. run

        python3 entrypoint.py 

in the ubuntu console, open a web browser and go to 127.0.0.1:5000

The program start page should display.

If you have reached this point succesfully, you can start claculating your spectra, if you find any bug or issue please contact me preferably with a screen caption and the description of the problem.

If you have installed everything as stated here, the other times you need to start the app you just have to follow this instructions:
  1. Open ubuntu
  2. Go to the application (and enviroment folder)
    
    cd flask/Forest-master/consensus_win
    
  3. Start the virtual environment with 
  
    source .consensus/bin/activate
    
  4. run 
    
    python3 entrypoint.py 


  5. Go to the browser and type 127.0.0.1:5000
  
  
