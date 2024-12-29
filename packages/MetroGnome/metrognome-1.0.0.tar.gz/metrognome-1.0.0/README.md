# Metrognome

A cross-platform (Linux, MacOS, Windows) metronome application using Python 3.12
and PyQt6.8.

## Requirements

* Python 3.12
* ffmpeg

## Installation

To install the application locally run the following.

```python3
pip install .
```

## Development Setup Instructions

1. Create a Virtual Environment
    Linux/MacOS:

    ```bash
    python3 -m venv venv
    ```

    Windows:

    ```powershell
    python -m venv venv
    ```

2. Activate the Environment
    Linux/MacOS:

    ```bash
    source venv/bin/activate
    ```

    Windows:

    ```powershell
    .\venv\Scripts\Activate
    ```

3. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Generate Sounds Files

    ```bash
    ./generate_sounds.sh
    ```

5. Run the application

    ```bash
    python3 -m metrognome.main
    ```
