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

2. Azure Web Service: Nice integration with most Python frameworks

3. GitHub Actions: For source control, CI/CD pipelines, and project management (decided against it)

4. Azure Key Vault: to store sensitive info IE my API key from Alpha Vantage


## High-level plan of implementation
### Application design
Started developing the application using FastAPI. Given the actual task is very simply, there is nothing stopping me from writing all of my code on a singular `main.py`, however I will use design patterns to best structure my code so it looks clean, scalable and evolvable.

The project is divided into different modules (API, Core, Services, Models). The separation of concern makes the code more modular, easier to maintain, easier to test. 

The `api` directory is a package that contains all API-related code. I can group related endpoints and potentially add middleware or more API-specific logic in the future. By doing this, I will be keeping routing logic separate from business logic. 

The `core` directory will contain core functionality used across the applications, such as configs and dependencies. In particular, this is where I will store my Alpha Vantage API. I have also set up logging configurations here, for good understanding of any errors we might encounter. 

The `service` directory will contain the business logic of my application. This is the *Service Layer* pattern, which encapsulates the business logic of this application.

The `models` directory will contain my data models, as we will be using Pydantic for data validation. I used models to define and validate the response we get from the API. This also helps out testing later, as I have a clear idea of what the data types I will be working with.

`fastapi dev main.py` to run the application in dev server. `fastapi run main.py` for production server. Production server makes sure of Uvicorn, and you can configure it to have multiple workers. 

### Testing
Testing is relatively easy to simply for FastAPI applications. As we are dealing with incredibly simple logic, the tests were quite straight forward. I defined some happy paths and bad paths, and was able to catch some errors that prompted me to improve my data validators even further. 

For example, some old data for commodities has value ".", which meant we have to allow both a normal numerical value and ".".

Run `pytest` to see see all tests pass. 

### Local Build and Run
I could have created a Makefile and contain make commands to run locally. 

Ie `make run` to run the application, `make test` to initiate pytest straight away. This would be neat to implement but not too important, so I have skipped to prioritise on more important stuff. 

### Container runtime 
I use Docker to containerise the application. This just ensures portability and compatibility to run on any cloud platform/servers. 

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
