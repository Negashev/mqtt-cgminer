FROM arm32v6/python:2-alpine3.7
RUN pip install paho-mqtt pycgminer cayenne-mqtt
ENV MQTT_PORT=1883 \
    MQTT_HOST=localhost \
    MQTT_PASS=TOKEN \
    CGMINER_HOST=localhost \
    CGMINER_PORT=4028
CMD ["python", "main.py"]
ADD *.py ./
