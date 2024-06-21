import os
from zipfile import ZipFile

from api.src.const import BASE_PATH


async def get_result(user_name: str, project_name: str):
    #TODO: Просто циклом запрашивать с клиента картинки (сохранять там индекс и не деражать состояния на сервере )
    path = os.path.join(BASE_PATH, f"user_folders\\{user_name}\\result\\{project_name}.zip")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    # zip = ZipFile(path, "w")
    # zip.close()

    path = os.path.join(BASE_PATH, f"user_folders\\{user_name}")
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            if project_name in file and not "table" in file and not "json" in file:
                with ZipFile(path, 'a') as zip:
                    zip.write(file)
