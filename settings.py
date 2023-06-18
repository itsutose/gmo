import os
import re

PRIVATE_API_SUBSETTINGS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'private_API', 'subsettings.py'))
PRIVATE_WEBSOCKET_API_SUBSETTINGS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'private_Websocket_API', 'subsettings.py'))

subsettings_list = [PRIVATE_API_SUBSETTINGS_PATH 
                    # ,PRIVATE_WEBSOCKET_API_SUBSETTINGS_PATH
                    ]


apiKey    = "lXkTnJxlGN67qH+cyGtiO2vI8B4SZ5P5"    # APIキーを設定
secretKey = "zW9BJu/wjRbIN8G+jyZBtKPYRSBgoP+300BRod37eWJK8mTgrXRYLWy4yHlxnaF1" # シークレットキーを設定

def set_api_key(api_key, subsettings_path):
    with open(subsettings_path, "r+", encoding='utf-8') as f:
        code = f.read()
        f.seek(0)
        f.write(re.sub(r'apiKey\s*=\s*["\'](.*)["\']', f'apiKey = "{api_key}"', code))

def set_secret_key(secret_key, subsettings_path):
    with open(subsettings_path, "r+", encoding='utf-8') as f:
        code = f.read()
        f.seek(0)
        f.write(re.sub(r'secretKey\s*=\s*["\'](.*)["\']', f'secretKey = "{secret_key}"', code))

if __name__ == '__main__':
    for subsettings in subsettings_list:
        set_api_key(apiKey, subsettings)
        set_secret_key(secretKey, subsettings)
    