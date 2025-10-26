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

        stage('Deploy to AWS ECS Fargate') {
    steps {
        withCredentials([
            string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
            string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
            script {
                echo 'Deploying latest image to AWS ECS Fargate............'
                sh '''
                 # Installation de jq si non présent
                if ! command -v jq &> /dev/null
                then
                    echo "jq non trouvé, installation en cours..."
                    apt-get update -y && apt-get install -y jq
                fi
 
                aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                aws configure set default.region ${AWS_REGION}

                # Met à jour la task definition avec la nouvelle image
                TASK_DEFINITION_NAME="mlops-hotel-task"
                CLUSTER_NAME="mlops-hotel-cluster"
                SERVICE_NAME="mlops-hotel-service"
                IMAGE_URI="${ECR_REPO}:latest"

                # Récupère la définition actuelle et met à jour l'image
                aws ecs describe-task-definition --task-definition $TASK_DEFINITION_NAME > task-def.json

                jq --arg IMAGE_URI "$IMAGE_URI" '
                .taskDefinition |
                del(.revision, .status, .requiresAttributes, .compatibilities, .taskDefinitionArn) |
                .containerDefinitions[0].image = $IMAGE_URI
                ' task-def.json > new-task-def.json

                # Enregistre la nouvelle définition de tâche
                aws ecs register-task-definition --cli-input-json file://new-task-def.json

                # Force ECS à redéployer avec la nouvelle image
                aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --force-new-deployment
                '''
            }
        }
    }
    }


    }



}
