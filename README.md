# autbscit1bot

## Setup:
* Copy config.example.py to config.py  
* Configure config.py  
* Create the virtual environment:  
```
python3 -m venv venv
```
* Activate the virtual environment:  
```
Windows: venv\Scripts\activate
Linux: source venv/bin/activate
```
* Install the requirements:  
```
pip install -r requirements.txt
```
* Create DB Schema  
```
python3 bot.py --fresh-db-seed
```
* Run the bot in polling mode:  
```
python3 bot.py
```
