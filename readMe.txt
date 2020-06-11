Load json 

usage in cmd:

env/python.exe script1.py -c ['DATA_CODE'] -p ['FILE_PATH'] -l [N_RECORDS_TO_DOWLOAD]


example:

#get 2 records of code 7710568760-KBKSOURCETYP
env/python.exe .\script1.py -c '7710568760-KBKSOURCETYP' -p 'C:\Users\user\Desktop\TEST1.json' -l 2

#get all records
env/python.exe .\script1.py -c '7710568760-KBKSOURCETYP' -p 'C:\Users\als\Desktop\gos_data\TEST1.json'


env\python.exe script1.py -c '7710568760-BUDGETCLASGABS'