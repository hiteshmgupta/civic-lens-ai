FROM maven:3.9-eclipse-temurin-17 AS build

WORKDIR /app
<<<<<<< HEAD

# Copy Maven descriptor and sources
COPY pom.xml .
COPY src ./src

# Build the Spring Boot jar (skip tests for faster deploys)
RUN mvn -q -B clean package -DskipTests


FROM eclipse-temurin:17-jre

=======
COPY . .
RUN chmod +x ./mvnw
RUN ./mvnw clean package -DskipTests

# Run stage
FROM eclipse-temurin:21-jre-alpine
>>>>>>> parent of c002e96 (Use native maven instead of wrapper)
WORKDIR /app

# Copy the built jar from the build stage
COPY --from=build /app/target/civiclens-backend-0.1.0.jar app.jar

EXPOSE 8080

# Allow extra JVM options via JAVA_OPTS
ENV JAVA_OPTS=""

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]