# taskproj

### How to get the server running

- Create a virtual environment
`virtualenv [virtual-environment-name]` or `python -m venv [virtual-environment-name]`

- Activate virual environment
`[virtual-environment-name]\Scripts\activate` (Windows OS) source `[virtual-environment-name]/bin/activate` (Linux / Mac OS)

- Install the dependencies/ pacakages
pip install -r requirements.txt

- Set the .env using the .env-example file in the project base folder
Set `DEBUG` to `True` and add your secret key

- Migrate
`python manage.py migrate`

- Run the server
`python manage.py runserver`


**You are good to go**

