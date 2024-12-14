# AWS Lambda Function for Task Reminders

This repository contains a Python-based AWS Lambda function that processes task reminders and sends notifications via email. The function integrates with multiple microservices to fetch task and user data, ensuring reminders are efficiently managed and delivered.

---

## Features

- **Task Reminder Management**: Fetches upcoming tasks and reminders from the task microservice.
- **Email Notifications**: Sends email notifications to users about their upcoming tasks.
- **Integration with Microservices**: Communicates with user and task microservices for data retrieval.
- **Scalable and Serverless**: Runs on AWS Lambda for efficient and cost-effective task execution.

---

## Prerequisites

### 1. AWS Lambda Setup
Ensure you have an AWS Lambda function configured and attached with the necessary permissions:
- Access to invoke other services (e.g., SES for email sending).
- Access to S3 (if applicable) or other AWS services used by the function.

### 2. Python Dependencies
Install dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
