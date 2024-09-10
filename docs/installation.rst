Installation Guide
==================

Follow these steps to install and run Galaxy Pulse on your local machine:

1. **Clone the GitHub repository**:

   .. code-block:: bash

      git clone https://github.com/username/GalaxyPulse.git
      cd GalaxyPulse

2. **Create and activate a virtual environment**:

   .. code-block:: bash

      python3 -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install the dependencies**:

   .. code-block:: bash

      pip install -r requirements.txt

4. **Run the game**:

   .. code-block:: bash

      python main.py

### Running on Android
To run Galaxy Pulse on Android, follow these additional steps:

1. **Install Buildozer** (if not already installed):

   .. code-block:: bash

      pip install buildozer

2. **Build the APK**:

   .. code-block:: bash

      buildozer init
      buildozer -v android debug

3. **Install the APK on your Android device**:

   .. code-block:: bash

      adb install bin/*.apk

Galaxy Pulse should now run on your Android device. For more details, check the Buildozer documentation.

### Troubleshooting
- If you encounter issues during installation, make sure all dependencies in `requirements.txt` are installed correctly.
- For issues related to Kivy or platform compatibility, refer to the official [Kivy Documentation](https://kivy.org/doc/stable/).

