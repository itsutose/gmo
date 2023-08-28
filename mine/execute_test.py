import subprocess

def execute_test_take_from_db():
    # test_take_from_db.pyのパス
    test_take_from_db_path = r"I:/マイドライブ/pytest/virtual_currency/gmo/mine/test_take_from_db.py"
    
    # test_take_from_db.pyを実行
    subprocess.run(["python", test_take_from_db_path])

if __name__ == '__main__':
    execute_test_take_from_db()