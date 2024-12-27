pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'echo Building the project...'
            }
        }
        stage('Test') {
            steps {
                sh 'echo Running tests...'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo Deploying application...'
            }
        }
    }
}
