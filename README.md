# Steganography with ADS

## Introduction
This Python project is designed to enable users to perform steganography, the art of hiding data within other files. It utilizes encryption and data binding techniques to securely conceal and later retrieve data within various file types. 

### Prerequisites

Before using this project, ensure you have the following prerequisites:

- Python 3
- Required Python packages (list them in a `requirements.txt` file if applicable)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-project.git
   cd your-project

    pip install -r requirements.txt

## Project Components

### 1. Main Application (`main.py`)
- The main script of the project.
- Provides a graphical user interface (GUI) for user interaction.
- Allows users to select a "main video file" and a "secret file" for steganography operations.
- Provides options for encryption, data binding, decryption, and data extraction.

### 2. Encryption Module (`crypto.py`)
- Responsible for AES 256 encryption and decryption.
- Uses a hardcoded password for encryption.
- Encrypts and decrypts data before and after binding it to other files.

### 3. Data Binding Module (`binder.py`)
- Enables the hiding (binding) of encrypted data within other files.
- Combines encrypted data with another file for concealment.
- Provides functionality to extract the concealed data.

## Project Workflow
1. Users select a "main video file" and a "secret file" through the GUI.
2. The "secret file" is encrypted using AES 256 encryption.
3. The encrypted data is hidden (bound) within the "main video file" using the `binder.py` module.
4. Users can choose an extension for the decrypted file (e.g., "jpeg," "mp4") and then decrypt the data, extracting it from the "main video file."

## Usage
1. Run the `main.py` script to open the GUI.
2. Follow the on-screen instructions to select files, perform encryption, data binding, decryption, and data extraction.

## Notes
- This project serves as a simplified demonstration. In a real-world application, enhanced security measures and user authentication would be recommended for encryption and decryption.
- Steganography, while having legitimate use cases (e.g., watermarking or secure data transfer), should be used responsibly and ethically, considering privacy and security implications.

## License
This project is provided under the XYZ License. For more details, refer to the [LICENSE](LICENSE) file.

## Author
- [Your Name](https://github.com/your-username)

## Contact
For questions or feedback, please contact [your.email@example.com](mailto:your.email@example.com).

## Acknowledgments
- [List any libraries, resources, or individuals you want to acknowledge here.]

