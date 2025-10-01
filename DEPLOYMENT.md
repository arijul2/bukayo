# JobMatch AI Deployment Guide

This guide explains how to deploy the JobMatch AI application to AWS Elastic Beanstalk using GitHub Actions.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **DockerHub Account** for storing Docker images
3. **GitHub Repository** with the following secrets configured:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_PASSWORD`

## Setup Steps

### 1. Configure GitHub Secrets

In your GitHub repository, go to Settings > Secrets and variables > Actions, and add:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_PASSWORD`: Your DockerHub password/token

### 2. Update Configuration Files

Before deploying, update these files with your actual values:

#### Update DockerHub username in Dockerrun.aws.json:
```json
{
  "image": "your-dockerhub-username/jobsmatch-frontend:latest"
}
```

#### Update OpenAI API key in .ebextensions/02-docker.config:
```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    OPENAI_API_KEY: "your-actual-openai-api-key"
```

### 3. Deploy Infrastructure

First, deploy your AWS infrastructure using Terraform:

```bash
cd infra/deploy
terraform init
terraform plan
terraform apply
```

This will create:
- VPC and subnets
- Security groups
- IAM roles
- Elastic Beanstalk application and environment

### 4. Deploy Application

The GitHub Actions workflow will automatically:

1. **Test** both API and frontend
2. **Build** Docker images for all services
3. **Push** images to DockerHub
4. **Generate** deployment package
5. **Deploy** to Elastic Beanstalk

#### Automatic Deployment
- Pushes to `main` branch → Deploy to staging
- Manual workflow dispatch → Choose staging or production

#### Manual Deployment
You can also trigger deployment manually:
1. Go to Actions tab in GitHub
2. Select "Deploy JobMatch AI Application"
3. Click "Run workflow"
4. Choose environment (staging/production)

## Environment Configuration

### Staging Environment
- Application Name: `jobsmatch-staging`
- Environment Name: `jobsmatch-env-staging`
- Region: `us-west-2`

### Production Environment
- Application Name: `jobsmatch`
- Environment Name: `jobsmatch-env`
- Region: `us-west-2`

## Services

The application consists of three services:

1. **Frontend** (React + Nginx)
   - Port: 80
   - Serves the React application
   - Proxies API requests to backend

2. **Backend** (FastAPI)
   - Port: 8000
   - Handles file uploads and AI analysis
   - Requires OpenAI API key

3. **Nginx** (Reverse Proxy)
   - Routes requests between frontend and backend
   - Handles SSL termination (when configured)

## Domain Configuration

To connect your domain `jobsmatch.ai`:

1. **Update DNS**: Point your domain to the Elastic Beanstalk environment URL
2. **SSL Certificate**: Add SSL certificate configuration in Terraform
3. **Environment Variables**: Set production environment variables

## Monitoring

- **AWS CloudWatch**: Monitor application logs and metrics
- **Elastic Beanstalk Health**: Check environment health dashboard
- **GitHub Actions**: Monitor deployment status

## Troubleshooting

### Common Issues

1. **Docker Build Failures**
   - Check Dockerfile syntax
   - Verify all dependencies are included

2. **Deployment Failures**
   - Check AWS credentials
   - Verify Elastic Beanstalk environment exists
   - Check application logs in CloudWatch

3. **Application Errors**
   - Verify environment variables are set
   - Check OpenAI API key is valid
   - Review application logs

### Useful Commands

```bash
# Check Elastic Beanstalk environment status
aws elasticbeanstalk describe-environments --environment-names jobsmatch-env

# View application logs
aws logs describe-log-groups --log-group-name-prefix /aws/elasticbeanstalk/jobsmatch

# Update environment variables
aws elasticbeanstalk update-environment \
  --environment-name jobsmatch-env \
  --option-settings Namespace=aws:elasticbeanstalk:application:environment,OptionName=OPENAI_API_KEY,Value=your-key
```

## Security Considerations

1. **Environment Variables**: Never commit API keys to code
2. **IAM Permissions**: Use least privilege principle
3. **Network Security**: Configure security groups appropriately
4. **SSL/TLS**: Enable HTTPS for production

## Cost Optimization

1. **Instance Types**: Choose appropriate instance sizes
2. **Auto Scaling**: Configure based on usage patterns
3. **Reserved Instances**: Consider for predictable workloads
4. **Monitoring**: Set up billing alerts
