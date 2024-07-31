# Edge Connect AI
## Platform Engineering Challenge

## Task 1
Build and deploy a Python Web API providing an endpoint which for a given date range returns the
average value of a commodity offered by Alpha Vantage. (e.g. Wheat, Sugar, Coffee… see the list
below)

The focus will be on code quality, tests, documentation and quality of the deployment. Naturally we
don’t expect you to deploy to paid tiers, but please document how things would be different for a
production app.

### Services
To architect my solution, I want to outline the services I would use on Azure:

1. Azure App Service: Compatibility with Python flask framework


2. GitHub Actions: For source control, CI/CD pipelines, and project management


3. Azure Key Vault: to store sensitive info IE my API key from Alpha Vantage


4. Azure Application Insights: Monitoring and logging (?)


5. Azure API Management (optional): To manage and secure your API in production environments

### High-level plan of implementation
1. Develop the API:

Use a Python web framework like Flask or FastAPI
Implement clean architecture principles
Use dependency injection (e.g., with a library like Dependency Injector)
Implement proper error handling and logging


Implement testing:

Write unit tests using pytest
Implement integration tests for API endpoints
Set up code coverage reporting with a tool like coverage.py


Documentation:

Use tools like Swagger/OpenAPI for API documentation
Write clear README files and inline code comments
Document the architecture and deployment process


Set up CI/CD pipeline in Azure DevOps or GitHub Actions:

Implement build, test, and deploy stages
Run tests and code analysis (e.g., pylint, flake8) in the pipeline
Deploy to different environments (dev, staging, production)


Secure the application:

Implement proper authentication and authorization
Use Azure Key Vault to store secrets
Implement HTTPS and proper security headers


Monitoring and logging:

Set up Application Insights for telemetry and logging
Implement proper error handling and logging throughout the application


Scalability and performance:

Implement caching where appropriate (e.g., Azure Cache for Redis in production)
Consider using Azure Front Door or Azure CDN for production environments

## Setting up local env
`python3 -m venv venv` to create virtual environment. 

## Design Patterns
Given the actual task is very simply, there is nothing stopping me from writing all of my code on a singular `main.py`, however I will use design patterns to best structure my code so it looks clean, scalable and evolvable.

The project is divided into different modules (API, Core, Services, Models). The separation of concern makes the code more modular, easier to maintain, easier to test. 

The `api` directory is a package that contains all API-related code. I can group related endpoints and potentially add middleware or more API-specific logic in the future. By doing this, I will be keeping routing logic separate from business logic. 

The `core` directory will contain core functionality used across the applications, such as configs and dependencies.

The `service` directory will contain the business logic of my application. This is the *Service Layer* pattern, which encapsulates the business logic of this application.

The `models` directory will contain my data models, as we will using Pydantic for data validation. 

MVC - models view controller design pattern. View is exposed part of your app (API endpoints). Controller is business logic. 

Use models everywhere, FASTapi produces documentation.

You can use middleware to catch errors, specify origins, CORS. 

Pydantic handles data types, but the data accuracy can still be improved with unit tests. 

You can pretty much work enums and models directly, not use other data types.