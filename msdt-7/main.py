import asyncio
import aiohttp
import os
import json


async def download_image(session, url, index, folder):
    # Асинхронная функция для скачивания изображения по URL
    try:
        async with session.get(url) as response:
            # Проверяем, успешен ли ответ
            if response.status == 200:
                filename = os.path.join(folder, f"{index}.jpg")
                with open(filename, 'wb') as f:
                    f.write(await response.read())  # Сохраняем изображение
                print(f"Скачано: {filename}")
            else:
                print(f"Ошибка загрузки {url}: {response.status}")
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")


async def main(json_file, folder):
    # Создаем папку для сохранения изображений, если она не существует
    os.makedirs(folder, exist_ok=True)

    # Загружаем данные из JSON файла
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, (id_, url) in enumerate(data.items(), start=1):
            # Создаем задачу для скачивания изображения
            tasks.append(download_image(session, url, index, folder))

        # Запускаем все задачи параллельно
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    json_file = "links.json"
    folder = "C:\\Users\\Lenovo\\Desktop\\учебные файлы\\5 семестр\\Современные средства разработки ПО\\photos"  # Папка для сохранения изображений
    asyncio.run(main(json_file, folder))
