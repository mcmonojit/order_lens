To set and use environment variables from a .env file in a PySpark project, use the python-dotenv package to load configuration values into the driver process.

Step 1: Install python-dotenv

Open your terminal or IDE integrated terminal and install the library:
bash
pip install python-dotenv
Use code with caution.

Step 2: Create a .env File

Create a file named .env in the root directory of your PySpark project. Add your key-value pairs without spaces around the = sign:
env
DATABASE_URL=postgres://user:password@localhost:5432/mydb
API_KEY=my_secret_spark_api_key
SPARK_LOG_LEVEL=INFO
Use code with caution.

Step 3: Add .env to .gitignore

To prevent leaking sensitive database credentials or API keys into source control, add .env to your .gitignore file:
gitignore
.env
Use code with caution.

Step 4: Load and Use Variables in PySpark

In your PySpark script (before building your SparkSession or referencing the variables), import load_dotenv from dotenv and read values via os.getenv() or os.environ:
python
import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

# Load environment variables from .env file
load_dotenv()

# Access environment variables
db_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")

print(f"Loaded Database URL: {db_url}")

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("PySparkDotenvExample") \
    .getOrCreate()

# Example: Pass an environment variable into Spark configuration
spark.conf.set("spark.executor.extraJavaOptions", f"-Dapi.key={api_key}")

# Your PySpark logic here...
spark.stop()
Use code with caution.

Important Note on Distributed Execution (Clusters vs. Local)

• Driver vs. Workers: load_dotenv() loads the variables into the local OS environment of the driver node running the Python script.
• Passing to Executors: If your worker nodes (executors) on a multi-node cluster (like YARN, Kubernetes, or Databricks) need these environment variables, you must explicitly pass them via Spark configuration options (spark.executorEnv.*) or distribute the .env file / configuration values using sparkContext.addFile().
If you are running this PySpark code on a distributed cluster (like YARN or Kubernetes) rather than locally, let me know so I can show you how to propagate .env values to the worker nodes.