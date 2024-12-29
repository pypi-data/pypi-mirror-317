# DjangoPrime

**DjangoPrime** is an all-in-one, powerful Django library designed to accelerate your development process. It provides a comprehensive toolkit, including over 1000 custom exception classes, middleware integrations, JWT configuration services, and advanced tools for enums and model management. **DjangoPrime** empowers developers to build scalable, maintainable, and sophisticated Django applications with ease.

Whether you're building a RESTful API or a full-fledged web application, **DjangoPrime** offers the modular components and pre-built solutions necessary to streamline your workflow and boost your development speed.

## Features

- 🚀 **Quick Start Templates**: Get started with Django in seconds using predefined project structures and configurations.
- 🔧 **Environment Management**: Easily manage environment variables and settings with flexible tools.
- 📦 **Modular Components**: A collection of ready-to-use apps and components that can be easily integrated into any Django project.
- 💡 **Custom Exception Classes**: Enhance error handling with over 1000 pre-defined, customizable exception classes for various scenarios.
- 🔐 **JWT Authentication**: Easily integrate JWT-based authentication for secure user login and authorization. *(Coming Soon)*
- 🏗️ **Absolute Models**: Pre-built, scalable models to help you structure your application efficiently and reduce repetitive code.
- ⚙️ **Middleware Integrations**: A comprehensive set of middleware components that support custom responses, logging, and advanced logic handling.
- 📊 **Advanced Enums & Choices**: Tools to manage custom choices and enums, making it easier to handle complex model fields.
- 🔑 **Flexible JWT Configuration**: Customizable JWT services and token handling, providing you full control over authentication settings.


## Installation

You can install the **DjangoPrime**, package using either `pip` or `pipenv`:

```bash
pip install djangoprime
```

## Quickstart

### 1. Initialize a New Django Project
Install DjangoPrime using pip or pipenv as shown above.


### 2. Add DjangoPrime to INSTALLED_APPS
Once installed, add djangoprime to the INSTALLED_APPS list in your settings.py file:

```python
INSTALLED_APPS = [
    # other apps
    'djangoprime',
]
```

### 3. Add Middleware to MIDDLEWARE
Next, configure the middleware by adding it to the MIDDLEWARE setting in your settings.py file:

```python
MIDDLEWARE = [
    # other middleware
    'djangoprime.middleware.APIResponseMiddleware',
]
```

### 4. Configure Custom Exception Handler
To handle exceptions with the DjangoPrime custom handler, configure the EXCEPTION_HANDLER in your settings.py:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'djangoprime.exceptions.handler.exception_handler',
}
```
This will set up a custom exception handler for better error management and reporting in your REST framework views.


## Documentation

For full documentation, visit the DjangoPrime Documentation (Coming Soon).

[//]: # (## Contributing)

[//]: # ()
[//]: # (Contributions are welcome! Please see the CONTRIBUTING.md file for more information on how to get involved.)


## License

This project is licensed under a modified MIT License - see the [LICENSE](LICENSE) file for details.


## Author & Maintainer

Created and maintained by [Ankaj Gupta](https://www.linkedin.com/in/ankajgupta02/), the developer behind **DjangoPrime**.

Feel free to connect with me on LinkedIn for any inquiries.

[//]: # (or collaboration opportunities.)

---
This version organizes the information clearly, ensures that placeholders for future content are marked, and maintains a professional tone throughout. Adjust the documentation and URLs when they are available.











