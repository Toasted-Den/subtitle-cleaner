# Subtitle Toastifier

The **Subtitle Toastifier** is a web-based application designed to upload, process and "Toastify" SubRip Subtitle (SRT) files for my videos. This tool allows you to upload multiple SRT files, process them on the server, and download the processed results in a ZIP file.

This app can be used without the web UI just by running the `subtitle_toastifier.py` script.

The application is powered by **Flask** which handles the front-end and back-end operations.

## Getting Started

### Prerequisites

1. **Docker Engine**: To run this application locally using Docker, make sure the Docker Engine and Docker Compose is installed on your machine.
   - Install Docker: https://docs.docker.com/engine/install/

### Running the Application Locally

Follow these steps to get the app running on your local machine using Docker.

1. **Clone the Repository**: Clone the repository to your local machine.

    ```bash
    git clone https://github.com/toastedden/subtitle-toastifier.git
    cd subtitle-toastifier
    ```

2. **Build and Start the Application**: Use Docker Compose to build and run the app.

    ```bash
    docker-compose up --build
    ```

3. **Access the App**: Once the application is running, open your browser and go to `http://localhost:5000`.

### Project Structure

```plaintext
.
├── app
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── static
│   │   ├── assets
│   │   ├── styles.css
│   │   └── uploader.js
│   └── templates
│       └── index.html
└── docker-compose.yaml
```
## Project Structure

- **Dockerfile**: Contains the instructions to build the Docker image.
- **docker-compose.yaml**: Defines the service configuration for the app.
- **app.py**: Main Python file running the Flask web server.
- **static**: Folder containing static files like CSS, JavaScript, and assets.
- **templates**: Folder containing the HTML template files (e.g., index.html).

## Usage

### Uploading Subtitle Files

1. **Choose Files**: Click the "Drag files here or click to browse" section to select your `.srt` subtitle files. You can select multiple files at once.
2. **Processing**: Once the files are uploaded, the server will process them, and you can download the processed files as a ZIP archive.
3. **Clear Files**: If you want to remove the selected files, use the "Clear All" button.

### Features

- **Drag-and-drop** and **file browse** functionality for selecting subtitle files.
- **Real-time file listing**: View the selected files in the interface.
- **Processing** multiple subtitle files at once.
- **Download** the processed subtitle files as a ZIP file.

## Development

### Running Locally for Development

If you need to make changes or develop the app further, follow these steps to run the app with live code changes.

1. **Build the Docker Containers**: Build the images and start the containers in development mode.

    ```bash
    docker-compose up --build
    ```

2. **Edit Code**: All code changes made in the app directory will automatically reflect in the container due to the `volumes` directive in the `docker-compose.yaml` file.

3. **Access Application**: Open your browser at `http://localhost:5000` to test changes.

### Dependencies

The project has the following Python dependencies:

- **Flask**: Web framework for running the application.
- **Flask-Cors**: Cross-origin resource sharing for Flask.
- **Other Python dependencies**: Listed in the `requirements.txt`.

To install these dependencies manually, you can run:

```bash
pip install -r requirements.txt
```

## Docker Setup

The application uses Docker for containerization, which simplifies deployment and ensures consistency across environments.

### Docker Commands

- **Build the Docker Image:**

    docker build -t subtitle-toastifier .

- **Run the Container:**

    docker run -p 5000:5000 subtitle-toastifier

- **Stop the Running Container:**

    docker stop <container-id>

## Contributing

If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes and create a pull request.

We welcome contributions and suggestions for improvements!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.