pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh '''
                    cd tests
                    pytest
                '''
            }
        }
    }
}
