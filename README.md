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

1. FastAPI: For ease of developing an API capable of data validation and async work
2. Azure Web Service: Nice integration with Python frameworks
3. GitHub Actions: For source control, CI/CD pipelines, and project management
4. Azure Key Vault: to store sensitive info IE my API key from Alpha Vantage


## High-level plan of implementation
I tried to be verbose and comprehensive in this documentation, so I will include both implementation, assumptions I have made, and reasoning behind the architectural decisions I have made.

### Application design
Started developing the application using FastAPI. Given the actual task is very simple, there is nothing stopping me from writing all of my code on a singular `main.py`, however I will use design patterns to best structure my code so it looks clean, scalable and evolvable.

The project is divided into different modules (API, Core, Services, Models). The separation of concern makes the code more modular, easier to maintain, easier to test. 

The `api` directory is a package that contains all API-related code. I can group related endpoints and potentially add middleware or more API-specific logic in the future. By doing this, I will be keeping routing logic separate from business logic. 

The `core` directory will contain core functionality used across the applications, such as configs and dependencies. In particular, this is where I will store my Alpha Vantage API. I have also set up logging configurations here, for good understanding of any errors we might encounter. 

The `service` directory will contain the business logic of my application. This is the *Service Layer* pattern, which encapsulates the business logic of this application.

The `models` directory will contain my data models, as we will be using Pydantic for data validation. I used models to define and validate the response we get from the API. This also helps out testing later, as I have a clear idea of what the data types I will be working with.

`fastapi dev main.py` to run the application in dev server. 

`fastapi run main.py` for production server. Production server makes sure of Uvicorn, and you can easily configure it to have multiple workers. 

### Testing
Testing is relatively easy to simply for FastAPI applications. As we are dealing with incredibly simple logic, the tests were quite straight forward. I defined some happy paths and bad paths, and was able to catch some errors that prompted me to improve my data validators even further. 

For example, some old data for commodities has value ".", which meant we have to allow both a normal numerical value and ".".

Run `pytest` to see see all tests pass. 

In a production environment, I would also try to set up some measure of code coverage, ensuring we have a good amount of tests covering our logic.

### Local Build and Run
I could have created a Makefile and contain make commands to run locally. 

Ie `make run` to run the application, `make test` to initiate pytest straight away. This would be neat to implement but not too important, so I have skipped to prioritise on more important stuff. 

### API key storage
In the application's core settings, I configured the application to load the API key from a local environment variable in the `.env` file. This approach enhances security by ensuring that the API key is not hardcoded directly in the codebase. Additionally, when deploying to an Azure Web App, the environment variable will be stored in Azure key vault, so that it can be safely injected during the deployment process.

### Container runtime 
I use Docker to containerise the application. This just ensures portability and compatibility to run on any cloud platform/servers. 

I then build and run it locally, to see that it works. `docker run -p 80:80 --env-file .env my-fastapi-app`

### CICD Pipeline
Now that I have a containerised application, I will use Github Actions to set up a CICD pipeline with automated tests, injection from Azure Secret Vault, and of course, build and deploy to Azure App Service.

I did not set up proper branching strategy, so all of the changes are instantly merged into production. Clearly, in a production environment, I would have multiple environments with the correct branching strategies to support a CICD pipeline.

### KEY CONSIDERATION
Now that I need to work with various Azure components, I must stress in a production environment, I would definitely use Infrastructure As Code tooling like Terraform to automate the creation of Azure resources. But after careful consideration and discussion with Arnaud, I think it would be best if I focus on code quality + deployment methods. Obviously, IaC is essential for long term scalability and maintainability in an actual production environment.  

### Cloud resource creation
For each cloud service I used, I used best practice with their [naming convention](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations). I used a resource group to contain all the resources I will manage for this application. There will be a container registry to host my Docker images, a key vault to host my API key, and then finally my actual web app will be deployed using App Service. 

I began to authenticate Azure Web App for Github Actions, in order to generate deployment credentials. I created an active directory application, which is used as an identity to assign permissions for managing Azure resources.

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
