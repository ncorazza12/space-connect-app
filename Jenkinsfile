pipeline {
    agent any

    environment {
        IMAGE_NAME    = 'space-connect-app'
        CONTAINER_NAME = 'space-connect-deploy'
        APP_PORT      = '5000'
        HOST_PORT     = '5001'
        TEST_PORT     = '5002'
    }

    triggers {
        pollSCM('H/1 * * * *')
    }

    stages {

        stage('Build') {
            steps {
                echo '==============================='
                echo ' STAGE 1 — BUILD'
                echo '==============================='
                echo 'Clonando repositório e construindo imagem Docker...'
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
                echo 'Imagem Docker construída com sucesso!'
            }
        }

        stage('Test') {
            steps {
                echo '==============================='
                echo ' STAGE 2 — TEST'
                echo '==============================='
                sh '''
                    docker run -d \
                        --name ${IMAGE_NAME}-test-${BUILD_NUMBER} \
                        -p ${TEST_PORT}:${APP_PORT} \
                        ${IMAGE_NAME}:${BUILD_NUMBER}

                    sleep 5

                    echo "Testando endpoint /..."
                    curl -f http://host.docker.internal:${TEST_PORT}/ \
                        && echo "PASSOU: endpoint / OK" \
                        || { docker stop ${IMAGE_NAME}-test-${BUILD_NUMBER}; docker rm ${IMAGE_NAME}-test-${BUILD_NUMBER}; exit 1; }

                    echo "Testando endpoint /health..."
                    curl -f http://host.docker.internal:${TEST_PORT}/health \
                        && echo "PASSOU: endpoint /health OK" \
                        || { docker stop ${IMAGE_NAME}-test-${BUILD_NUMBER}; docker rm ${IMAGE_NAME}-test-${BUILD_NUMBER}; exit 1; }

                    docker stop ${IMAGE_NAME}-test-${BUILD_NUMBER}
                    docker rm ${IMAGE_NAME}-test-${BUILD_NUMBER}
                    echo "Todos os testes passaram!"
                '''
            }
        }

        stage('Deploy Simulado') {
            steps {
                echo '==============================='
                echo ' STAGE 3 — DEPLOY SIMULADO'
                echo '==============================='
                sh '''
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm   ${CONTAINER_NAME} 2>/dev/null || true

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${HOST_PORT}:${APP_PORT} \
                        --restart unless-stopped \
                        ${IMAGE_NAME}:${BUILD_NUMBER}

                    echo "Container implantado com sucesso na porta ${HOST_PORT}!"
                    docker ps | grep ${CONTAINER_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline concluída com sucesso! Missão SPACE CONNECT operacional.'
        }
        failure {
            echo '❌ Pipeline falhou. Verificar logs acima.'
            sh 'docker stop ${IMAGE_NAME}-test-${BUILD_NUMBER} 2>/dev/null || true'
            sh 'docker rm   ${IMAGE_NAME}-test-${BUILD_NUMBER} 2>/dev/null || true'
        }
    }
}
