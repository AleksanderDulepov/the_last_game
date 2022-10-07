FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN apt update && apt install gettext-base && pip install -r requirements.txt
COPY . .
CMD cat ./service_classes/equipment_for_vm.py | envsubst > ./service_classes/equipment.py && export FLASK_APP=app.py && flask run -h 0.0.0.0 -p 80
