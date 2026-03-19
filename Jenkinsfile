pipeline {
  agent any

  environment {
    REGISTRY = "localhost:8083"
    REPO = "docker-hosted"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Lint') {
      steps {
        sh 'python3 -m py_compile stock_producer.py kafka_consumer.py'
      }
    }

    stage('Build Images') {
      steps {
        script {
          env.TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        }
        sh '''
         docker build -t kafka-monitoring/producer:${TAG} -f Dockerfile.weather-producer .
         docker build -t kafka-monitoring/consumer:${TAG} -f Dockerfile.weather-consumer .
        '''
      }
    }

    stage('Push to Nexus') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'nexus-creds', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
          sh '''
            echo "$NEXUS_PASS" | docker login ${REGISTRY} -u "$NEXUS_USER" --password-stdin

            docker tag kafka-monitoring/producer:${TAG} ${REGISTRY}/${REPO}/producer:${TAG}
            docker tag kafka-monitoring/consumer:${TAG} ${REGISTRY}/${REPO}/consumer:${TAG}
            docker tag kafka-monitoring/producer:${TAG} ${REGISTRY}/${REPO}/producer:latest
            docker tag kafka-monitoring/consumer:${TAG} ${REGISTRY}/${REPO}/consumer:latest

            docker push ${REGISTRY}/${REPO}/producer:${TAG}
            docker push ${REGISTRY}/${REPO}/consumer:${TAG}
            docker push ${REGISTRY}/${REPO}/producer:latest
            docker push ${REGISTRY}/${REPO}/consumer:latest
          '''
        }
      }
    }
  }
}

