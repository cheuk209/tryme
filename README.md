# Edge Connect AI
## Platform Engineering Challenge Tast 1
Build and deploy a Python Web API providing an endpoint which for a given date range returns the
average value of a commodity offered by Alpha Vantage. (e.g. Wheat, Sugar, Coffee… see the list
below)

The focus will be on code quality, tests, documentation and quality of the deployment. Naturally we
don’t expect you to deploy to paid tiers, but please document how things would be different for a
production app.


## High-level plan of implementation
I will be very verbose and comprehensive in this documentation, as I will include the method of implementation, assumptions I have made, and reasoning behind the architectural decisions I have chosen.

### Application design
Started developing the application using FastAPI. Given the actual task is very simple, there is nothing stopping me from writing all of my code on a singular `main.py`, however I will use design patterns to best structure my code so it looks clean, scalable and evolvable. 

The project is divided into different modules (API, Core, Services, Models). The separation of concern makes the code more modular, easier to maintain, easier to test. This follows a MVC design pattern.

The `api` directory is a package that contains all API-related code. I can group related endpoints and potentially add middleware or more API-specific logic in the future. By doing this, I will be keeping routing logic separate from business logic. 

The `core` directory will contain core functionality used across the applications, such as configs and dependencies. In particular, this is where I will initialise my Alpha Vantage API settings also. I have set up logging configurations here, for a better understanding of any errors we might encounter. 

The `service` directory will contain the business logic of my application. This is the *Service Layer* pattern, which encapsulates the business logic of this application.

The `models` directory will contain my data models, as we will be using Pydantic for data validation. I used models to define and validate the response we get from the API. This also helps out testing later, as I have a clear idea of what the data types I will be working with.

`fastapi dev main.py` to run the application in dev server. 

`fastapi run main.py` for production server. Production server makes sure of Uvicorn, and you can easily configure it to have multiple workers. 

### Testing
Testing is relatively easy to set up for FastAPI applications. As we are dealing with incredibly simple logic, the tests were quite straight forward. I defined some happy paths and bad paths, and was able to catch some errors that prompted me to improve my data validators even further. 

For example, some old data for commodities has value ".", which meant we have to allow both a normal numerical value and ".".

Run `pytest` to see see all tests pass. 

In a production environment, I would also try to set up some measure of code coverage, ensuring we have a good amount of tests covering our logic. Of course, you can always write more tests to catch more edge cases, but in this instance, I believe I have done a good job of covering most of the routing/business logic.

### Local Build and Run
I *could have* created a Makefile and contain make commands to run locally. 

Ie `make run` to run the application, `make test` to initiate pytest straight away. This would be neat to implement but not too important, so I have skipped to prioritise on more important stuff. In a production environment, I would make use of a Makefile for ease of local development and testing.

### API key storage
In the application's core settings, I configured the application to load the API key from a local environment variable in the `.env` file. This approach enhances security by ensuring that the API key is not hardcoded directly in the codebase. ~~Additionally, when deploying to an Azure Web App, the environment variable will be stored in Azure key vault, so that it can be safely injected during the deployment process.~~ 

I basically ran out of time to implement Azure Key Vault, will be using Github Secrets instead, which is of course not ideal in a production environment. 

### Container runtime 
I use Docker to containerise the application. This just ensures portability and compatibility to run on any cloud platform/servers. 

I then build and run it locally, to see that it works. `docker run -p 80:80 --env-file .env my-fastapi-app`

### CI/CD Pipeline
Now that I have a containerised application, I will use Github Actions to set up a CICD pipeline with automated tests, injection from ~~Azure Secret Vault~~ Github Secrets, and of course, build and deploy to Azure App Service.

I did not set up proper branching strategy, so all of the changes are instantly merged into production. Clearly, in a production environment, I would have multiple environments with the correct branching strategies to support a CICD pipeline. 

The pipeline is very basic, and consists of Build, Test, then Push. 

Therein lies the most challenging part of the deployment process for me: Authenticating with Container Registry and Azure Web App. So I just followed [this guide](https://learn.microsoft.com/en-us/azure/app-service/deploy-container-github-action?tabs=publish-profile) to set up my credentials. 

### KEY CONSIDERATION
Now that I need to work with various Azure components, I must stress in a production environment, I would **definitely use Infrastructure As Code** tooling like Terraform to automate the creation of Azure resources. But after careful consideration and discussion with Arnaud, I think it would be best if I focus on code quality + deployment methods. Obviously, IaC is essential for long term scalability and maintainability in an actual production environment.  

### Cloud resource creation
For each cloud service I used, I used best practice with their [naming convention](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations). I used a resource group to contain all the resources I will manage for this application. There will be a container registry to host my Docker images, a key vault to host my API key, and then finally my actual web app will be deployed using App Service. 

I began to authenticate Azure Web App for Github Actions, in order to generate deployment credentials. I created an active directory application, which is used as an identity to assign permissions for managing Azure resources.

### Azure Web App
There were many options to deploy a containerised application, including container instances, serverless functions etc... I chose Web App simply because Edge Connect uses it already and I want to demonstrate I can pick up new tooling quickly.

Limitations of using free tier prevents me from enabling a lot of features I would use in a production environment, for example using multiple layers of deployment slots, so that we can enable rolling upgrade or rollbacks. 

I would also set auto-scaling groups so it can scale out to meet traffic demands. Since we are working with an API, we can also use API management to apply rate limiting to prevent abuses or malicious usage. 

At the moment, there is only the default log stream enabled for web app. I would use custom logging and monitoring solutions for better observability. 

On the security front, I would employ a mixture of WAF, network security groups. Again, the free tier doesn't allow for HTTPS/SSL, so the data is not encrypted. 

There are *far too many things* I can do to improve availability and resiliency, but for the purpose of deploying to a basic SKU, I will forego them.

In fact, running a container using Azure Web App was more difficult than anticipated. There were many app settings that I had thought would be automatically transferrable from Github Actions, such as the Docker registry credentials, or even port number etc... It took multiple attempts of pulling the image from the container registry and running locally to realise the fault is with the Web App configurations.

I also did not like the Log Stream feature of App Service, it takes a long time to refresh and further configuration was necessary to enable the logging I am expecting to see at application level.

### Injection of API Key
Thus far, I have relied on local environment variable to inject the Alpha Vantage API Key. `.env` via python-dotenv.

Throughout the entire process, I had ambition to create an Azure key vault to store the API key instead. It would be best practice to do so, but to simplify things, I have simply stored it as a Github Action secret variable, and then I passed it along to the Dockerfile argument so that it is baked in the image.

Given more time, I would have definitely implemented this, I chose not to simply because I am weary of overspending my time on this task.

### Accessing the web app and Documentation
https://app-edgeconnect.azurewebsites.net/docs 

FastAPI produces a very comprehensive OpenAPI docs, on which you may test the various functions and endpoints I have built. It will also include documentation and schemas for the various models included. 