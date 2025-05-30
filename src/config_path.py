# input information
import os
import sys
import yaml

# Function to load configuration from HIT.yaml
def load_config(file_path):
    global config
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Define paths
Src_PATH = os.path.dirname(os.path.abspath(__file__))
Base_PATH = os.path.dirname(Src_PATH)
Run_PATH = f'{Base_PATH}/run'  # Modify to the actual path
Database_PATH = f'{Base_PATH}/database'
Case_PATH = ''
Para_PATH = ''
Specific_Case_PATH = ''
Case_PATHs = []
next_case = 0
tasks = 0
config_file_path = os.getenv('CONFIG_FILE_PATH', '')

print("config_file_path",config_file_path)

config = load_config(config_file_path)

# Set variables from config
usr_requirment = config.get('usr_requirment', '')
max_loop = config.get('max_loop', 20)
temperature = config.get('temperature', 0.01)
batchsize = config.get('batchsize', 10)
searchdocs = config.get('searchdocs', 2)
run_times = config.get('run_times', 1)
MetaGPT_PATH = config.get('MetaGPT_PATH', '')
model = config.get('model', '')
should_stop = False
If_RAG = True
If_all_files = True
If_reviewer = False
First_time_of_case = False
# Set environment variables from config
if model.lower().startswith("deepseek"):
    os.environ["DEEPSEEK_API_KEY"] = config.get("DEEPSEEK_API_KEY", "")
    os.environ["DEEPSEEK_BASE_URL"] = config.get("DEEPSEEK_BASE_URL", "")
elif model.lower().startswith("gpt"):
    os.environ["OPENAI_API_KEY"] = config.get("OPENAI_API_KEY", "")
    os.environ["OPENAI_PROXY"] = config.get("OPENAI_PROXY", "")
    os.environ["OPENAI_BASE_URL"] = config.get("OPENAI_BASE_URL", "")
else:
    print('the chat model is not identified, only the model start with deepseek and gpt can be identified.')
    sys.exit()


# Add MetaGPT_PATH to sys.path
sys.path.append(MetaGPT_PATH)
sys.path.append(Src_PATH)


print("Configuration loaded successfully:")
print(f"usr_requirment: {usr_requirment}")

# Extract MetaGPT_PATH

config2_yaml_path = os.path.join(MetaGPT_PATH, "config/config2.yaml")

# Check if config2.yaml exists
if not os.path.exists(config2_yaml_path):
    raise FileNotFoundError(f"{config2_yaml_path} does not exist")

with open(config2_yaml_path, 'r') as file:
    config2_data = yaml.safe_load(file)
if model.lower().startswith("deepseek"):
    new_config2_data = {
        "llm": {
            "api_type": "openai",
            "model": model,
            "base_url": os.environ.get('DEEPSEEK_BASE_URL'),
            "api_key": os.environ.get('DEEPSEEK_API_KEY')
        }
    }
elif model.lower().startswith("gpt"):
    new_config2_data = {
        "llm": {
            "api_type": "openai",
            "model": model,
            "proxy": os.environ.get('OPENAI_PROXY'),
            "base_url": os.environ.get('OPENAI_BASE_URL'),
            "api_key": os.environ.get('OPENAI_API_KEY')
        }
    }
else:
    print('the chat model is not identified, only the model start with deepseek and gpt can be identified.')
    sys.exit()
# Write the modified config back to config2.yaml
with open(config2_yaml_path, 'w') as file:
    yaml.dump(new_config2_data, file, default_flow_style=False)

print(f"{config2_yaml_path} has been updated successfully.")