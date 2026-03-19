pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build Images') {
      steps {
        sh '''
          docker build -t kafka-monitoring/producer -f Dockerfile.stock .
          docker build -t kafka-monitoring/consumer -f Dockerfile.consumer .
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
