

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)
## 🧐 About <a name = "about"></a>

Write about 1-2 paragraphs describing the purpose of your project.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Setting Up the Module

Set the Envirornment Varibles

Create a file called `.env` in the root directory

```
LB_DB_HOST_NAME_OR_IP = 192.168.1.1
LB_DB_USER_NAME = USER1
LB_DB_PASSWORD = ABCDEF
LB_DB_PORT = 5432
LB_DB_DATABASE_NAME = DBNAME
```

Install the Module

```
pip install lb_tech_handler
```

if already installed then upgrade

```
pip install --upgrade lb_tech_handler
```

End with an example of getting some data out of the system or using it for a little demo.


## Overall Functions In each Modules

### Db Handler
The `db_handler` sub-module handles various operations.

[- **`execute_query`**](#execute_query)

[- **`execute_query_and_return_result`**](#execute_query_and_return_result)

[- **`execute_transaction`**](#execute_transaction)

[- **`execute_transaction_with_multiprocessing`**](#execute_transaction_with_multiprocessing)

[- **`get_connection_from_pool`**](#get_connection_from_pool)

[- **`get_dataframe_from_list_of_queries`**](#get_dataframe_from_list_of_queries)

[- **`get_dataframe_from_query`**](#get_dataframe_from_query)

[- **`is_free_connection_in_pool`**](#is_free_connection_in_pool)

[- **`load_dotenv`**](#load_dotenv)

[- **`put_connection_in_pool`**](#put_connection_in_pool)

[- **`test_async_query`**](#test_async_query)

[- **`test_excution_multi_query`**](#test_excution_multi_query)

[- **`timed_execution`**](#timed_execution)

### Api Handler
The `api_handler` sub-module handles various operations.

[- **`debug_api_response`**](#debug_api_response)

[- **`execute_query_and_return_result`**](#execute_query_and_return_result)

[- **`log_api_request`**](#log_api_request)

[- **`throttle_api_call`**](#throttle_api_call)

### File Handler
The `file_handler` sub-module handles various operations.

[- **`delete_file`**](#delete_file)

[- **`generate_barcode`**](#generate_barcode)

[- **`generate_qr_code`**](#generate_qr_code)

[- **`get_file_extension`**](#get_file_extension)

[- **`get_file_name`**](#get_file_name)

[- **`get_file_name_without_extension`**](#get_file_name_without_extension)

[- **`get_file_size`**](#get_file_size)

[- **`get_number_of_pages_of_pdf`**](#get_number_of_pages_of_pdf)

[- **`rename_pdf_file_with_page_number`**](#rename_pdf_file_with_page_number)

### Os Handler
The `os_handler` sub-module handles various operations.

[- **`get_all_env_variables`**](#get_all_env_variables)

[- **`get_cpu_count`**](#get_cpu_count)

[- **`get_env_variable`**](#get_env_variable)

[- **`get_monitors_info`**](#get_monitors_info)

[- **`set_env_variable`**](#set_env_variable)

### Common Methods
The `common_methods` sub-module handles various operations.

[- **`timed_execution`**](#timed_execution)

## Function Defination

### Db Handler
The `db_handler` sub-module handles various operations.

- ### **`execute_query`**: 

        _summary_
        
        Args:
            query (str): _description_
            vars (dict, optional): _description_. Defaults to {}.
        
        Raises:
            Exception: _description_
- ### **`execute_query_and_return_result`**: 

        _summary_
        
        Args:
            query (str): _description_
            vars (dict, optional): _description_. Defaults to {}.
        
        Raises:
            Exception: _description_
        
        Returns:
            list: _description_
- ### **`execute_transaction`**: 

        Executes a list of queries
        
        Input Format:
        
            [
                {
                    'query':query,
                    'vars':{
                        "key1":"value1",
                        "key2":"value2"
                    }
                },
                {
                    'query':query2,
                    'vars':{
                        "key1":"value1",
                        "key2":"value4"
                    }
                }
            ]
        
        
        Args:
        --------
            query (str): query
            vars (dict, optional): _description_. Defaults to {}.
        
        Returns:
        ---------
            is_transaction_successful: bool
- ### **`execute_transaction_with_multiprocessing`**: 

        This is a function to execute a list of queries in parallel using multiprocessing
        Use this when you have a list of queries and want to execute them in parallel
        
        Args:
        
        - list_of_queries (list[dict]):
        
        Input Format:
        
                [
                    {
                        'query':query,
                        'vars':{
                            "key1":"value1",
                            "key2":"value2"
                        }
                    },
                    {
                        'query':query2,
                        'vars':{
                            "key1":"value1",
                            "key2":"value2"
                        }
                    }
                ]
        
        - MAX_PROCESS (int, optional): Maximum number of processes to use.
            - Defaults to CPU_COUNT.
        
        Returns:
            bool: _description_
- ### **`get_connection_from_pool`**: 

        No description available
- ### **`get_dataframe_from_list_of_queries`**: 

        returns the query as pandas dataframe from database
        
        Input Format:
            [
                {
                    'query':query,
                    'vars':{
                        "key1":"value1",
                        "key2":"value2"
                    }
                },
                {
                    'query':query2,
                    'vars':{
                        "key1":"value1",
                        "key2":"value2"
                    }
                }
            ]
        
        Args:
        --------
            query (str): query
        
        Returns:
        ---------
            data: pandas dataframe from query
- ### **`get_dataframe_from_query`**: 

        _summary_
        
        Args:
            query (str): _description_
            vars (dict, optional): _description_. Defaults to {}.
        
        Returns:
            _type_: _description_
- ### **`is_free_connection_in_pool`**: 

        No description available
- ### **`load_dotenv`**: 

        Parse a .env file and then load all the variables found as environment variables.
        
        Parameters:
            dotenv_path: Absolute or relative path to .env file.
            stream: Text stream (such as `io.StringIO`) with .env content, used if
                `dotenv_path` is `None`.
            verbose: Whether to output a warning the .env file is missing.
            override: Whether to override the system environment variables with the variables
                from the `.env` file.
            encoding: Encoding to be used to read the file.
        Returns:
            Bool: True if at least one environment variable is set else False
        
        If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
        .env file.
- ### **`put_connection_in_pool`**: 

        No description available
- ### **`test_async_query`**: 

        No description available
- ### **`test_excution_multi_query`**: 

        No description available
- ### **`timed_execution`**: 

        This is a decorator to time the execution time of a function
        
        Example:
            @timed_execution
            def test_api():
                response = requests.get("https://api.learnbasics.fun/learnyst?name=test")
        
        Args:
            func (_type_): Function to be timed
### Api Handler
The `api_handler` sub-module handles various operations.

- ### **`debug_api_response`**: 

        Debug an API response by collecting useful details and returning them as a structured dictionary.
        
        Args:
            api_response (requests.Response): The API response object to debug.
        
        Returns:
            dict: A dictionary containing API debugging information.
- ### **`execute_query_and_return_result`**: 

        _summary_
        
        Args:
            query (str): _description_
            vars (dict, optional): _description_. Defaults to {}.
        
        Raises:
            Exception: _description_
        
        Returns:
            list: _description_
- ### **`log_api_request`**: 

        _summary_
        
        Example:
            api_response = requests.get("https://api.learnbasics.fun/learnyst?name=test")
            api_log_id = log_api_request(api_response=api_response,log_file_name=log_file_name,log_to_database=True,log_to_file=True)
        
        Args:
            api_response (requests.Response): _description_
            log_file_name (str, optional): _description_. Defaults to DEFAULT_LOG_FILE_NAME.
            log_to_database (bool, optional): _description_. Defaults to False.
            log_to_file (bool, optional): _description_. Defaults to True.
            application_id (int, optional): _description_. Defaults to 0.
            user_id (int, optional): _description_. Defaults to 0.
        
        Returns:
            int: Returns the api log id , returns 0 if not logged
- ### **`throttle_api_call`**: 

        This is a decorator use to slow down API calls.
        SLowing down API calls by throttling to prevent overloading the server.
        
        Example:
            @throttle_api_call(minimum_api_wait_time_in_seconds=3,maximum_api_wait_time_in_seconds=5)
            def test_api():
                response = requests.get("https://api.learnbasics.fun/learnyst?name=test")
        
            @throttle_api_call
            def test_api():
                response = requests.get("https://api.learnbasics.fun/learnyst?name=test")
        
        Args:
            minimum_api_wait_time_in_seconds (int, optional): _description_. Defaults to 3.
            maximum_api_wait_time_in_seconds (int, optional): _description_. Defaults to 5.
### File Handler
The `file_handler` sub-module handles various operations.

- ### **`delete_file`**: 

        Function to delete file
        
        Args:
            file_path (str): Path of the file
- ### **`generate_barcode`**: 

        Function to generate a barcode
        
        Args:
            value (_type_): Value of the barcode
            path (_type_): Path to save the barcode
            barcode_value_to_be_printed (bool, optional): Wether to print the value of barocde at bottom. Defaults to False.
        
        Raises:
            Exception: _description_
        
        Returns:
            str: Barcode path
- ### **`generate_qr_code`**: 

        Function to generate a QR code.
        
        Args:
            value (str): The data or text to encode in the QR code.
            path (str): The file path where the generated QR code image will be saved.
        
            config (dict, optional): Configuration for QR code generation. Defaults to {}.
        
            General Configuration:
                version (int, optional): Controls the size of the QR Code (1 is the smallest, 40 is the largest). Defaults to 1.
                error_correction (int, optional): Level of error correction. Defaults to 1 (Low).
        
                        - 1: Low (7% of codewords can be restored).
        
                        - 2: Medium (15% of codewords can be restored).
        
                        - 3: High (25% of codewords can be restored).
        
                        - 4: Very High (30% of codewords can be restored).
        
            Display Configuration:
                box_size (int, optional): The size of each box in the QR code grid. Defaults to 10.
                border (int, optional): The width of the border (minimum is 4). Defaults to 4.
                fit (bool, optional): Whether to adjust the QR Code size to fit the data. Defaults to True.
        
            Color Configuration:
                fill_color (str, optional): The color of the QR code. Defaults to "black".
                back_color (str, optional): The background color of the QR code. Defaults to "white".
        
        
            Example:
                config = {
                    "version": 1,
                    "error_correction": 2,
                    "box_size": 10,
                    "border": 4,
                    "fit": True,
                    "fill_color": "blue",
                    "back_color": "yellow"
                }
        
        Returns:
            str: The file path where the QR code image was saved.
- ### **`get_file_extension`**: 

        Function to get file extension
        
        Args:
            file_path (str): Path of the file
        
        Returns:
            str: Extension of the file
- ### **`get_file_name`**: 

        Function to get file name wwithout the folder structure.
        
        Args:
            file_path (str): Path of the file
        
        Returns:
            str: Name of the file
- ### **`get_file_name_without_extension`**: 

        Function to get file name wwithout the folder structure.
        
        Args:
            file_path (str): Path of the file
        
        Returns:
            str: Name of the file
- ### **`get_file_size`**: 

        Function to get file size
        
        Args:
            file_path (str): Path of the file
        
        Returns:
            int: Size of the file in bytes
- ### **`get_number_of_pages_of_pdf`**: 

        Function to get number of pages
        
        Args:
            file_path (str): _description_
        
        Returns:
            int: Number of pages
- ### **`rename_pdf_file_with_page_number`**: 

        Function to rename a PDF file with page number
        
        Args:
            file_path (str): Path of the file
            add_page_name_at_start (bool, optional): If True, the page number will be added at the start of the file name else at the end. Defaults to True.
            keep_original_file_name (bool, optional): If True, the original file name will be kept else deleted. Defaults to False.
        
        Returns:
            str: Path of the new file
### Os Handler
The `os_handler` sub-module handles various operations.

- ### **`get_all_env_variables`**: 

        Function to get all env variables
        
        Returns:
            dict: _description_
- ### **`get_cpu_count`**: 

        Function to get cpu count
        
        Returns:
            int: Number of cpus
- ### **`get_env_variable`**: 

        Function to get env variable
        
        Args:
            key (str): _description_
        
        Returns:
            str: _description_
- ### **`get_monitors_info`**: 

        Function to get monitor info
        
        Returns:
            List: Monitor info
- ### **`set_env_variable`**: 

        Function to set env variable
        
        Args:
            key (str): _description_
            value (str): _description_
### Common Methods
The `common_methods` sub-module handles various operations.

- ### **`timed_execution`**: 

        This is a decorator to time the execution time of a function
        
        Example:
            @timed_execution
            def test_api():
                response = requests.get("https://api.learnbasics.fun/learnyst?name=test")
        
        Args:
            func (_type_): Function to be timed
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Add notes about how to use the system.

## 🚀 Deployment <a name = "deployment"></a>

Add additional notes about how to deploy this on a live system.

## ⛏️ Built Using <a name = "built_using"></a>

- [MongoDB](https://www.mongodb.com/) - Database
- [Express](https://expressjs.com/) - Server Framework
- [VueJs](https://vuejs.org/) - Web Framework
- [NodeJs](https://nodejs.org/en/) - Server Environment

## ✍️ Authors <a name = "authors"></a>

- [@kylelobo](https://github.com/kylelobo) - Idea & Initial work

See also the list of [contributors](https://github.com/kylelobo/The-Documentation-Compendium/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
