pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                script {
                    docker.image('python:3.9').inside {
                        sh '''
                            python -m pip install --upgrade pip
                            pip install pytest
                            cd tests
                            pytest
                        '''
                    }
                }
            }
        }
    }
}

