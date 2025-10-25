pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        AWS_REGION = 'eu-north-1' 
        ECR_REPO = '973516475461.dkr.ecr.eu-north-1.amazonaws.com/mlops-hotel-repo'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Jabour-Salahddine/MLOPS-HotelReservation.git']])
                }
            }
        }

        stage('setup of virtual environment and installing dependancies'){
            steps{
                script{
                    echo 'Setting up VE for our dependencies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

          stage('Build and Push Docker Image to AWS ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    script {
                        echo 'Building and pushing Docker image to ECR............'
                        sh '''
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set default.region ${AWS_REGION}

                        # Connexion à ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

                        # Build Docker image
                        docker build -t mlops-hotel:latest .

                        # Tag l'image pour ECR
                        docker tag mlops-hotel:latest ${ECR_REPO}:latest

                        # Push l'image vers ECR
                        docker push ${ECR_REPO}:latest
                        '''
                    }
                }
            }
        }

        





        
    }





}
