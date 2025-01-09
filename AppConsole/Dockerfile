FROM maven:3.8.6-openjdk-11-slim AS build

WORKDIR /appConsole

COPY pom.xml .

RUN mvn dependency:go-offline

COPY src ./src

RUN mvn clean package -DskipTests

RUN ls -l /appConsole/target/

FROM openjdk:17-slim

WORKDIR /appConsole

COPY --from=build /appConsole/target/ProjetGLA-1.0-SNAPSHOT.jar /appConsole/app.jar

COPY instance/Crypto.db /appConsole/instance/Crypto.db

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/appConsole/app.jar"]

