pipeline {
    agent any

    environment {
        IMAGE_TAG = ''
        PRODUCER_IMAGE = 'kafka-monitoring/producer'
        CONSUMER_IMAGE = 'kafka-monitoring/consumer'
        NEXUS_DOCKER_REPO = 'your-nexus-docker-repo-url'   // e.g. nexus.example.com:8085
        NEXUS_CREDENTIALS_ID = 'nexus-docker-creds'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m py_compile weather_producer.py weather_consumer.py \
                        crypto_producer.py news_producer.py system_metrics_producer.py
                '''
            }
        }

        stage('Build Images') {
            steps {
                script {
                    IMAGE_TAG = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                }
                sh """
                    docker build -t ${PRODUCER_IMAGE}:${IMAGE_TAG} -f Dockerfile.weather-producer .
                    docker build -t ${CONSUMER_IMAGE}:${IMAGE_TAG} -f Dockerfile.weather-consumer .
                """
            }
        }

        stage('Image Scan (Trivy)') {
            steps {
                sh """
                    trivy image --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 ${PRODUCER_IMAGE}:${IMAGE_TAG}
                    trivy image --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 ${CONSUMER_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Push to Nexus') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${NEXUS_CREDENTIALS_ID}",
                    usernameVariable: 'NEXUS_USER',
                    passwordVariable: 'NEXUS_PASS'
                )]) {
                    sh """
                        echo "${NEXUS_PASS}" | docker login ${NEXUS_DOCKER_REPO} -u "${NEXUS_USER}" --password-stdin

                        docker tag ${PRODUCER_IMAGE}:${IMAGE_TAG} ${NEXUS_DOCKER_REPO}/${PRODUCER_IMAGE}:${IMAGE_TAG}
                        docker tag ${CONSUMER_IMAGE}:${IMAGE_TAG} ${NEXUS_DOCKER_REPO}/${CONSUMER_IMAGE}:${IMAGE_TAG}

                        docker push ${NEXUS_DOCKER_REPO}/${PRODUCER_IMAGE}:${IMAGE_TAG}
                        docker push ${NEXUS_DOCKER_REPO}/${CONSUMER_IMAGE}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}

