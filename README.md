
# Setup <a id="setupLink"></a>

<a id="setupPythonLink"></a>
<details>
  <summary>Python3.10</summary>

  - Mac : https://www.python.org/downloads/macos/

</details>

<a id="setupVenvLink"></a>
<details>
  <summary>Venv</summary>
 
   - Can set from Pycharm directly
    
     ```
     go into ./Preference/Project/pyhtonInterpreter
     ```
   
   - Can set from cmd line

     ```
     > sudo apt-get install python3-venv
     ```
     - create a virtual-env where you want
     ```
     > sudo python3 -m venv /home/rhr/Workspace/venv/WorkoutTracking
     ```
   
   Next activate the venv and install package from requirements.txt file.
 
      > cd /home/path_to_venv/bin
      > source activate
      > cd /home/path_to_project
      > pip3 install -r requirements.txt


</details>

<a id="setupMongoLink"></a>
<details>
<summary>MongoDB</summary>

- Mac : https://www.mongodb.com/docs/v4.2/tutorial/install-mongodb-on-os-x/
  ```
  > brew services list
  > brew services start/stop mongodb-community@4.0
  ```

</details>

# Documentation <a id="documentationLink"></a>

<a id="documentationSetupLink"></a>
<details>
  <summary>Setup</summary>

  - install node.js (https://nodejs.org/en/download/)
  - install nodemodule apidoc (https://apidocjs.com/)
    ```
    > sudo npm install -g apidoc
    ```

</details>

<a id="documentationGenerationLink"></a>
<details>
  <summary>Generate the documentation</summary>

  - generate the doc
    ```
    > cd path_to_project
    > apidoc -i ../WorkoutTracking -o apidoc/
    ```
    `apidoc` folder will be created at the project's root.


  - To see the documentation, open `./apidoc/index.html`


</details>

# Start Server <a id="runLink"></a>
Make sure all the [Setup](#setupLink) is done.

<a id="runMinLink"></a>
<details>
  <summary>Minimum run</summary>

  This will run the server without any check.

  The [Venv](#setupVenvLink) need to be activated.

    > cd /home/path_to_project
    > python run.py test (sys arg : dev/prod)

    * Serving Flask app "run" (lazy loading)
    * Environment: testing
    * Debug mode: on
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 137-343-485

  To check if the port is used

    > sudo lsof -i -P | grep LISTEN | grep :$PORT

</details>

<a id="runCompleteLink"></a>
<details>
  
  <summary>Complete run</summary>

  You need to update ./start_server.sh with your config. (file not up to date)

  This will:
   - activate the venv
   - install all packages
   - generate the doc
   - launch the server in **prod** configuration
   
   ```
   > cd /home/path_to_project
   > source ./start_server.sh
   ```

</details>

<a id="runPi4Link"></a>
<details>
  <summary>PI4 run</summary>

  Reminder for PI4 execution.

  - power on raspberry (check ethernet is connected)
  - get ip's raspberry  (bbox tools or cmd "arp -a" on linux)
  - go to https://ip_raspberry:9090 (cockpit)
  - log in (ask for login/password)
  - go in terminal tab
  - Launch the server with a [Complete run](#runCompleteLink)

</details>

# Tests <a id="testsLink"></a>

<a id="testsLink"></a>
<details>
  <summary>Tests run</summary>

  The [Venv](#setupVenvLink) need to be activated.
   ```
   > cd home/path_to_project
   > python -W ignore -m pytest tests (complete tests)
   > python -W ignore -m pytest tests/path_to_be_tested
   ```

</details>

# Project <a id="projectLink"></a>

<a id="projectRootLink"></a>
<details>
  <summary>./</summary>

    ```
    path_to_project/
    ├── apidoc/
    ├── files/
    ├── flaskr/
    ├── tests/
    ├── venv/
    ├── .gitignore
    ├── .apidoc.json
    ├── README.md
    ├── requirements.txt
    ├── run.py
    └── start_server.sh
    ```
  - **apidoc** : Auto-generated from doc generation. See [Generate the documentation](#documentationGenerationLink).
    - contain `index.html`. Open it to see the doc previously generated. 
  - **files** : Auto-generated if don't exist from  `./flaskr/__init__.py ` at server run. See [Start Server](#runLink).
    - contain files saved via apis.
    - not saved in Github.
  - **flaskr** : Server's source code.
  - **tests** : Server's api tests.
  - **venv** : Python virtual env. See [Venv](#setupVenvLink).
    - can be everywhere. Not Mandatory in this location.
    - not saved in Github.
  - **.gitignore** : Git file to ignore pushing files.
  - **.apidoc.json** : Apidoc config file.
  - **README.md** : This file you are reading.
  - **requirements.txt** : All external package use in the project. To be installed in [Venv](#setupVenvLink).
  - **run.py** : Run the `./flaskr` app. See [Minimum run](#runMinLink).
  - **start_server.sh** : Run the app. See [Complete run](#runCompleteLink).
    - active the venv.
    - update the doc.
    - check installed package.
    - run the app.

</details>

<a id="projectFlaskrLink"></a>
<details>
  <summary>./flaskr</summary>

    ```
    ./flaskr
    ├── __init__.py
    ├── enum.py
    ├── database.py
    ├── workshop/
    │   ├── __init__.py
    │   ├── model.py
    │   ├── router.py
    │   ├── validator/
    │       ├── __init__.py
    │       ├── api.py
    │       └── ...
    └── .../
    ```
  - **`./__init__.py`** : The app file.
       - contain app config, files gestion, 
       - contain `Response` model.
       - contain `Error` model.
  - **`./enum.py`** : The app enum.
     - contain `Msg` enum.
     - contain `ErrorMsg` enum.
  - **`./database.py`** : Database definition for the app. Here MongoDb
  - **`./workshop/`** : Blueprint for workshop model used in the app.

  for each **Blueprint**:
  - **`./workshop/__init__.py`** : import `model` and all his `validator`.
  - **`./workshop/model.py`** : contain `model` definition and database interaction.
  - **`./workshop/router.py`** : contain `apis` definition.
  - **`./workshop/validator/`** : validation for the Blueprint.
    - contain `__init__.py` to import all validation models.
    - contain `api.py` validator model for the api.

</details>

<a id="projectTestsLink"></a>
<details>
  <summary>./tests</summary>

    ```
    ./tests
    ├── __init__.py
    ├── files/
    ├── test_workshop/
    │   ├── __init__.py
    │   ├── api/
    │       ├── __init__.py
    │       ├── test_.py
    │       ├── test_param.py
    │       └── ...
    └── .../
    ```
  - **`./__init__.py`** : The app file.
       - contain `./flaskr` database, enum, `Error` 
       - contain `Server` model.
       - contain `File` model.
  - **`files`** : Files to be used in tests.
  - **`test_workshop/`** : Tests for the Blueprint.

  for each **Blueprint**:
  - **`./test_workshop/__init__.py`** : contain `testModel` definition and database interaction.
  - **`./test_workshop/api/`** : tests for a specific api.
  - **`./test_workshop/api/__init__.py`** : contain `apiModel` definition.
  - **`./test_workshop/api/test_.py`** : contain generic tests.
  - **`./test_workshop/api/test_param.py`** : contain tests for a specific parameter.

</details>