# meditrack-devops
A production ready DevOps implementation for MediTrack API — A hospital patient records system. This project demonstrates end-to-end CI/CD, containerization, Kubernetes deployment, and monitoring on AWS.

Architecture Flow:
Developer → GitHub → Jenkins CI → Docker Hub → Kubernetes (EKS) 
                                      ↓
                                Prometheus + Grafana  → Users

⚙️ Prerequisites
✅ AWS Account (EKS, EC2, CloudFormation access)
✅ GitHub Account
✅ Docker Hub Account
✅ AWS CloudShell or AWS CLI
✅ kubectl installed
✅ Helm installed

Infrastructure as Code (CloudFormation)
🔹 Jenkins Stack
EC2 instance (t2.medium)
Security Group (ports 22, 8080)
IAM Role
UserData installs:
Jenkins
Docker
Git
Java
🔹 EKS Stack
VPC (10.0.0.0/16)
Public subnets (multi-AZ)
EKS Cluster
Node Group (2+ nodes)

** Jenkins CI/CD Pipeline Overview:
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

🐳 Docker Image
Repository: efemenaedah/meditrack-devops
Tags:latest

☸️ Kubernetes Deployment

k8s/ on Github
 ├── deployment.yaml
 ├── service.yaml
 └── configmap.yaml
🔹 Deployment Features
3 replicas 
Liveness probe (/health)
Resource limits:
CPU: 250m  Memory: 256Mi
🔹 Service
Type: LoadBalancer
Public endpoint exposed via AWS ELB: http://a2a4bea3e6d804c00a719533f2e31698-1912031827.us-east-2.elb.amazonaws.com

http://<EXTERNAL-IP>:5000/health
🌐 Live Application

📊 Monitoring & Observability
🔹 Tools Used
Prometheus (metrics collection)
Grafana (dashboard visualization)

📸 Screenshots 
Jenkins pipeline success
Docker Hub image
Kubernetes pods running
Grafana dashboard
<img width="1920" height="936" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/c2e6cdc9-a13b-4ed4-b676-7c267c535293" />
<img width="1920" height="838" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/689d272b-9516-453b-b8e9-413bb5d1b9d9" />
<img width="1920" height="860" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/4aee8377-e5cf-4c87-87f7-a1577c2a2ef3" />
<img width="1920" height="854" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/6aa7ec7c-9eea-4436-9a20-bdbda761f44e" />

🧠 Key DevOps Concepts Demonstrated
Infrastructure as Code 
Continuous Integration and deployment
Container Orchestration (Kubernetes/EKS)
Containerization (Docker)
Monitoring & Observability (Prometheus + Grafana)
Github workflows

👤 Author
Edah Efemena Evans
Cloud/DevOps Engineer
GitHub: https://github.com/efemenaedah/meditrack-devops
