# Contributing to QuizMe

First off, thank you for taking the time to contribute! 🎉 Your help is invaluable in making QuizMe better for everyone.

## How to Contribute

### 1. Fork the Repository
- Go to the [QuizMe GitHub repository](https://github.com/KC-software-en/QuizMe).
- Click on the "Fork" button at the top right of the page.

### 1. Clone Your Fork
Clone your forked repository to your local machine using:
`git clone https://github.com/KC-software-en/QuizMe.git`

### 1. Create a Branch
Create a new branch for your feature or bugfix:
`git checkout -b feature/your-feature-name`

### 1. Make Your Changes
Make the necessary changes in your code editor.

### 1. Commit Your Changes
Commit your changes with a meaningful message:
`git add .`
`git commit -m "Add feature: your feature name"`

### 1. Push to Your Fork
Push your changes to your forked repository:
`git push origin feature/your-feature-name`


### 1. Create a Pull Request
- Go to the original repository on GitHub.
- Click on the "New pull request" button.
- Select your branch and create the pull request.
- Provide a clear and descriptive title and description for your pull request.

## Guidelines for Contributing

### Coding Standards
* Follow the coding style and standards used in the existing codebase.
    * Use **PEP-8** standards for Python
* Write clear, concise, and well-documented code.
    * Write detailed **comments**
    * Use **Sphinx** format for software documentation (*VS code has an extension & [here's](https://www.sphinx-doc.org/en/master/usage/restructuredtext/) more information*)


### Commit Messages
- Use imperative mood in your commit messages (e.g., "Fix bug" not "Fixed bug").
- Provide a meaningful description of the changes made.

### Pull Requests
- Ensure your pull request is linked to an open issue (if applicable).
- Describe the changes in detail, including any new dependencies, tests added, and any other relevant information.
- Be ready to respond to any feedback or comments.

### Testing
* Run all existing tests to ensure nothing is broken with `py manage.py test Education`.
* Add tests for any new features or changes to existing features.
* Check the coverage with `coverage run manage.py test Education` & then run `coverage report`

## First-Time Contributors

If this is your first time contributing to an open source project, welcome! We are here to help you through the process. Here are some beginner-friendly [issues](https://github.com/KC-software-en/QuizMe/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to get you started.

## UI/UX Designers

We are also looking for talented UI/UX designers to improve the user experience and interface of our project. Your contributions can include:
- Redesigning existing screens.
- Creating new UI elements.
- Improving the overall user flow.

If you have ideas or suggestions, please create an issue or contact us directly.

## Code of Conduct

Please note that GitHub has a [Code of Conduct](https://docs.github.com/en/site-policy/github-terms/github-community-code-of-conduct#overview-and-purpose) in place. By participating, you are expected to uphold this code. Be respectful and considerate in all interactions.

## Getting Help

If you need help or have any questions, feel free to open an issue or message for assistance.

---

Thank you for your interest in contributing to QuizMe! We can't wait to see what you'll bring to the project.

---

