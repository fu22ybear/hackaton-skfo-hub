#### hackaton-skfo-hub -- flow team

---
#### note
решение реализовано на базе docker-контейнеров, которые обеспечивают идентичную изолированную среду на всех системах.  
почти.

к сожалению, все не совсем так и есть зависимость от ОС, которая иногда дает о себе знать.  

текущая система разрабатывалась и тестровалась в окружении:
* `macOS Catalina v10.15.7`
* `docker desktop v2.3.0.3 (45519)`
* `docker engine v19.03.8`
* `docker compose v1.25.5`


---
#### case

запуск
- `make compose-run`  
дождаться, что будут доступны minio на `localhost:9000` и grafana на `localhost:3000`  
доступы в minio `minio-access-key:minio-secret-key`, в grafana -- `admin:admin`
- `make consumer-run` -- запуск консьюмера, который сохраняет файлы из kafka в minio
- `make producer-run` -- запуск продьюсера, который получает файлы и складывает в кафку
