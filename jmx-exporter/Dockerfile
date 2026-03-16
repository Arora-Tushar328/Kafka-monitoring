FROM eclipse-temurin:11-jre

WORKDIR /opt/jmx_exporter
COPY jmx_prometheus_httpserver-0.17.0.jar .
COPY kafka-2_0_0.yml .

EXPOSE 9404
CMD ["java", "-jar", "/opt/jmx_exporter/jmx_prometheus_httpserver-0.17.0.jar", "9404", "/opt/jmx_exporter/kafka-2_0_0.yml"]

