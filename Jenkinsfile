pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Syntax Check') {
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
          docker build -t kafka-monitoring/producer:${TAG} -f Dockerfile.stock .
          docker build -t kafka-monitoring/consumer:${TAG} -f Dockerfile.consumer .
          docker tag kafka-monitoring/producer:${TAG} kafka-monitoring/producer:latest
          docker tag kafka-monitoring/consumer:${TAG} kafka-monitoring/consumer:latest
        '''
      }
    }

    stage('List Images') {
      steps {
        sh 'docker images | grep kafka-monitoring || true'
      }
    }
  }
}

