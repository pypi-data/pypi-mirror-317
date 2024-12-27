from bidict import bidict

NODE = "node"
PYTHON = "python"
CSHARP = "csharp"
RUBY = "ruby"
PYTHON_TENSORFLOW = "python-tensorflow"
PYTHON_PYTORCH = "python-pytorch"
LANGUAGE_OPTIONS = [NODE, PYTHON, CSHARP, RUBY, PYTHON_TENSORFLOW, PYTHON_PYTORCH]
LANGUAGE_OPTIONS_STR = f"{NODE}, {PYTHON}, {CSHARP}, {RUBY}, {PYTHON_TENSORFLOW}, {PYTHON_PYTORCH}"
MEMORY_CHOICES = [128, 256, 512, 1024]

RUNTIME_LANGUAGE_MAPPING = bidict({
    "node18": NODE,
    "python3-http-debian": PYTHON,
    "python3-tensorflow": PYTHON_TENSORFLOW,
    "python3-http-cuda": PYTHON_PYTORCH, 
    "dotnet8-csharp": CSHARP,
    "ruby": RUBY
})

LANGUAGE_REQUIREMENT_MAPPING = {
    NODE: "package.json",
    PYTHON: "requirements.txt",
    CSHARP: "Function.csproj",
    RUBY: "Gemfile",
    PYTHON_TENSORFLOW: "requirements.txt",
    PYTHON_PYTORCH: "requirements.txt"
}

SOURCE_CODE_FILE_NAME = {
    NODE: "handler.js",
    PYTHON: "handler.py",
    CSHARP: "Handler.cs",
    RUBY: "handler.rb",
    PYTHON_TENSORFLOW: "handler.py",
    PYTHON_PYTORCH: "handler.py",
}

SETUP = "setup"
CREATE = "create"
UPDATE = "update"
DELETE = "delete"

VALIDATE_NAME_REGEX = r"^(?!-)(?!\\d+$)[a-z0-9-]{0,50}[a-z0-9](?<!-)$"
NAME_VALIDATION_MESSAGE = "Name can contain lowercase letters, digits, and hyphens, but hyphens are only allowed between characters, not at the start or end, with a maximum length of 50 characters."

RUNTIME_API_ENDPOINT = "api/v1/faas/runtimes/"
DEPLOY_API_ENDPOINT = "api/v1/faas/functions/"
GET_ALL_FUNCTION_API_ENDPOINT = "api/v1/faas/functions/"
DELETE_FUNCTION_API_ENDPOINT = "api/v1/faas/function/{function_name}/"
GET_SINGLE_FUNCTION_API_ENDPOINT = "api/v1/faas/function/{function_name}/"
UPDATE_FUNCTION_API_ENDPOINT = "api/v1/faas/handler_file/{function_name}/"

DEFAULT_FUNCTION_CONFIG = {
    'function': {
        'name': 'test',
        'runtime': 'python',
        'compute_type': 'cpu',
        'limits': {
            'memory': '512',
            'timeout': '15'
        },
    }
}

DEFAULT_FUNCTION_CONFIG_NAME = "function_config.yaml"
COMPUTE_TYPE_CHOICES=['cpu', 'gpu']

# function states
RUNNING = 'running'