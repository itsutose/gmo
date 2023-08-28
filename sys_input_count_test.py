import sys

def take_from_db():
    # データベースパスを取得
    database_path = sys.argv
    print(type(database_path))
    print(database_path)
    # 以降の処理...

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 0:
        take_from_db()
    else:
        print(0)