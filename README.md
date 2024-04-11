# user-export

A Python script that outputs tenant user information into a CSV file.

## Getting Started

These instructions will guide you on how to set up your environment to run the `user-export` script successfully.

### Download Environment

To prepare your environment, follow these steps:

1. **Navigate to your project directory:**

    ```bash
    cd path/to/your/project-directory
    ```

2. **Install `virtualenv` if you haven't already:**

    ```bash
    pip3 install virtualenv
    ```

3. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv myvenv
    source myvenv/bin/activate
    ```

4. **Install the required packages:**

    ```bash
    pip3 install requests pandas
    ```

## Configuration

Before running the script, you need to configure it with your application details:

1. **Add your `application_vanity_domain` & `application_id`:**
   
    - These can be found in your application's "Settings" page.

2. **Add your `client_id` & `client_secret`:**
   
    - Instructions for obtaining these credentials can be found in the [Getting Access Tokens documentation](https://wristband.stoplight.io/docs/documentation/u236uoxf36sxp-getting-access-tokens-to-test-ap-is).

## Usage

To export users to a CSV file, execute the `run.py` script. This will generate a CSV file in your project directory containing the tenant user information.

```bash
python run.py
