# PandemicTracker
A software engineering project about planning, designing, and creating a pandemic data aggregation and tracking platform.

# Team Members

Sangjin David Lee

Máté Hekfusz

Daniel De Beer

Maria Jaramillo


# How To Run
1. Install PyMySQL:
```
pip install PyMySQL
```
2. Download MAMP and crate a database with whichever name you choose. 
3. Look at the `init.py` file, in the configure section, change your data to match your database
4. `render_template` functions will lead to files in the template folder. However, if you look at the HTML files, in the areas with "url_for," you have to reference a function within that route. `Ex: home.html says "url_for("hello") instead of url_for("/")`
5. To run, do the following:
```
export FLASK_APP=init.py
python -m flask run
```
* Running on http://127.0.0.1:5000/
* To populate the database, run the file, "run this once".


# Preview

<img width="730" alt="Screen Shot 2023-02-21 at 7 09 02 PM" src="https://user-images.githubusercontent.com/24204239/220314912-90ae5d42-41b8-4b9a-8351-480a72be6a63.png">

<img width="274" alt="Screen Shot 2023-02-21 at 7 06 57 PM" src="https://user-images.githubusercontent.com/24204239/220314455-e8b16553-1f61-47e1-ae38-79a279a3a256.png">

<img width="390" alt="Screen Shot 2023-02-21 at 7 09 59 PM" src="https://user-images.githubusercontent.com/24204239/220315195-65fa91f3-1986-42d9-80a8-1d907b4fea21.png">

<img width="861" alt="Screen Shot 2023-02-21 at 7 11 15 PM" src="https://user-images.githubusercontent.com/24204239/220315723-6e307458-1b31-40a3-9a24-2c9efde0c984.png">

<img width="866" alt="Screen Shot 2023-02-21 at 7 12 12 PM" src="https://user-images.githubusercontent.com/24204239/220315636-536cf9d0-d787-40eb-b30a-f7aa341c03ab.png">
