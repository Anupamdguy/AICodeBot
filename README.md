# AI Code Review Assistant

## Project Description
The AI Code Review Assistant is a GitHub bot powered by a large language model (LLM) that automatically reviews code in pull requests. It provides feedback on code quality, detects bugs, assesses complexity, and identifies documentation gaps. The bot integrates seamlessly with GitHub, leveraging webhooks and the GitHub API.

## Tech Stack
- **Backend**: Python (FastAPI)
- **AI**: Hugging Face Transformers
- **DevOps**: Docker, GitHub Actions
- **Tools**: GitHub API

## Core Features
- Automatically reviews code when a pull request is opened
- Summarizes changes and detects risky code patterns
- Provides suggestions on performance, readability, and security
- Optional: Custom linting and test case generation

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME
   ```

2. **Set Up the Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Dockerize the Application**:
   - Build the Docker image:
     ```bash
     docker build -t aicodebot .
     ```
   - Run the Docker container:
     ```bash
     docker run -p 8000:80 aicodebot
     ```

## Usage
- **GitHub Integration**: Set up a webhook in your GitHub repository to point to the `/webhook` endpoint of your deployed application.
- **AI Analysis**: The bot uses a Hugging Face model to analyze code and provide feedback directly on GitHub pull requests.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details. 
