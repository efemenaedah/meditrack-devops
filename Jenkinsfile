pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = 'efemenaedah/meditrack-devops'
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning GitHub repository...'
                git branch: 'main',
                     url: 'https://github.com/efemenaedah/meditrack-devops'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm -v $(pwd):/app -w /app python:3.10 \
                    sh -c "pip install -r requirements.txt && pytest -v"
                '''
            }
        }

        stage('Build Image') {
            steps {
                echo 'Building Docker image...'
                sh """
                   docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                   docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                   """
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh """
                     docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                     docker push ${DOCKER_IMAGE}:latest
                    """
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
