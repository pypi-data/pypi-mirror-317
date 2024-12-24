## Запись строительного шума

Данная программа производит расчёт необходимых метрик, детектирует шумовые события
и производит звукозапись этих событий

Для работы программы в `src/` необходимо добавить текстовый файл `config.txt`:

```
TIMEZONE_DELTA=0
CALIBRATION_CORRECTION=61.1

DAY_NORM=70
NIGHT_NORM=60
SIGNAL_BUFFER_LENGTH=5
WAITING_TIME=5
DURATION_LIMIT=60

RABBITMQ_LOGIN=login
RABBITMQ_PASSWORD=password
RABBITMQ_HOST_OUTER=1.1.1.1
RABBITMQ_PORT_OUTER=0
RABBITMQ_EXCHANGE=exchange

LATITUDE_EQUIP=00.00000
LONGITUDE_EQUIP=00.00000
ALTITUDE_EQUIP=0

MINIO_BUCKET_NAME=any_bucket_name
MINIO_URL=0.0.0.0:0000
MINIO_ACCESS_KEY=any_access_key
MINIO_SECRET_KEY=any_secret_key
```

________
Для работы библиотеки ```pydub```, необходимой для конвертации
wav-файла в mp3-файл, нужно установить программу ```ffmpeg```:
```
sudo apt-get install ffmpeg
```

