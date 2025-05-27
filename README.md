# QR Code Generator API

This project provides a simple API for generating QR codes. It allows users to generate QR codes by providing data and optional parameters such as size, error correction level, and output format.

## Table of Contents

* [Features](#features)
* [How to Use](#how-to-use)
  * [Local Setup and Installation](#local-setup-and-installation)
  * [Running with Docker](#running-with-docker)
* [API Usage](#api-usage)
  * [Endpoint](#endpoint)
  * [Query Parameters](#query-parameters)
  * [Examples](#examples)
* [Error Handling](#error-handling)
* [Technologies Used](#technologies-used)

## Features

* Generate QR codes from text data.
* Customize QR code size.
* Choose error correction level (L, M, Q, H).
* Support for multiple output formats: PNG and SVG.
* Customizable margin around the QR code.

## How to Use

The project can be run in 2 ways:
* a local installation where the python script will run manually
* a Docker setup where the script runs on top of a pre-built python image

### Local Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vitorjna/QR_Code_API.git
    cd QR_Code_API
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python src/app.py
    ```
    The API will be running on `https://localhost:7777`.

### Running with Docker

   To run this project using Docker and Docker Compose, follow these steps:

1.  **Prerequisites:**
        Ensure you have Docker and Docker Compose installed on your system.

2.  **Run the Docker container:**
    ```bash
    docker compose --profile QR up -d
    ```
    This command will pull the `python:3.13.2-slim` Docker image (if not already present) and start the `qr-generator` service. It will also install the dependencies and run the application inside the container.

3.  **Access the API:**
        The API will be accessible at `https://localhost:7777`.

## API Usage

The API exposes a single endpoint for QR code generation: `/generate_qr`.

### Endpoint

`GET /generate_qr`

### Query Parameters

*   `data` (required): The text data to encode in the QR code.
*   `size` (optional): The size of each box (pixel) in the QR code. Default is `10`.
*   `ecc` (optional): Error correction level. Can be `L` (Low), `M` (Medium), `Q` (Quartile), or `H` (High). Default is `L`.
*   `format` (optional): Output image format. Supported formats: `PNG`, `SVG`. Default is `SVG`.
*   `margin` (optional): The size of the border in boxes (pixels). Default is `4`.

### Examples

1.  **Generate a basic SVG QR code:**
    ```
    https://localhost:7777/generate_qr?data=Hello%20World
    ```

2.  **Generate a PNG QR code with custom size and error correction:**
    ```
    https://localhost:7777/generate_qr?data=https://www.example.com&size=10&ecc=H&format=PNG
    ```

3.  **Generate a JPEG QR code with a larger margin:**
    ```
    https://localhost:7777/generate_qr?data=My%20Custom%20Text&format=JPEG&margin=10
    ```

## Error Handling

*   If `data` is not provided, the API returns a `400 Bad Request` with the message "Please provide 'data' as a query parameter."
*   If an invalid `ecc` (error correction level) is provided, the API returns a `400 Bad Request` with the message "Invalid ECC level. Supported levels: [ 'l', 'm', 'q', 'h' ]".
*   If an invalid `format` is provided, the API returns a `400 Bad Request` with the message "Invalid output format. Supported formats: ['SVG', 'PNG']."
*   Internal server errors (e.g., issues during QR code generation) will return a `500 Internal Server Error` with a descriptive message.

## Technologies Used

*   Python
*   Flask
*   segno