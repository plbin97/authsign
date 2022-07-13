pipeline {
    agent { dockerfile true }
    stages {
        stage('Deploy') {
            steps {
                sh 'pytest'
            }
        }
    }
}