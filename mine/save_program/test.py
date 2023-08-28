import os

def drive_letter():

    current_path = os.path.abspath(__file__)
    return os.path.splitdrive(current_path)[0].upper()

def execute_test_take_from_db():
    test_take_from_db_path = f"{drive_letter()}/マイドライブ/pytest/virtual_currency/gmo/mine/test_take_from_db.py"
    print(test_take_from_db_path)

if __name__ == '__main__':
    execute_test_take_from_db()
