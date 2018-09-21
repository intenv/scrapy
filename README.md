# Пример краулеров

## Установка зависимостей
```bash
pip install -f requirements.txt
```

## Запуск splash
```bash
sudo docker run -p 8050:8050 scrapinghub/splash
```

## Запуск scrapy
### Получить спиок краулеров
```bash
scrapy list
```
### Запустить
```bash
scrapy crawl mts_click
```