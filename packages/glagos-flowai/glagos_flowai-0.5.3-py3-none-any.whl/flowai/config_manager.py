import os
import configparser
from pathlib import Path
import configparser
from typing import Tuple, Optional

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "flowai"
        self.config_file = self.config_dir / "config.ini"
        self.system_prompt_file = self.config_dir / "system_prompt"

    def config_exists(self):
        return self.config_file.exists()

    def create_default_config(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'default_provider': 'openai',
            'default_model': 'gpt-3.5-turbo',
            'openai_api_key': '',
            'anthropic_api_key': '',
            'groq_api_key': '',
            'google_api_key': '',
            'ollama_base_url': 'http://localhost:11434',
            'quiet_mode': 'true',
            'stream_mode': 'true'
        }
        self.save_config(config)
        self.create_default_system_prompt()

    def create_default_system_prompt(self):
        default_prompt = ("You are a helpful assistant that responds to all questions as accurately as possible. "
                            "If you dont know the answer to a question to will be honest and say so. "
                            "Answer the question concisely - no explanations, no greetings, no unneccesary white space or formatting. "
                            "Just the response")
        with open(self.system_prompt_file, 'w') as f:
            f.write(default_prompt)

    def get_system_prompt(self):
        if not self.system_prompt_file.exists():
            self.create_default_system_prompt()
        with open(self.system_prompt_file, 'r') as f:
            return f.read().strip()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def save_config(self, config):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        

        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def validate_config(self) -> Tuple[bool, Optional[str]]:
        config = self.load_config()
        default_model = config.get('DEFAULT', 'default_model', fallback=None)

        if not default_model:
            return False, "Missing model in configuration."

        parts = default_model.split(':', 1)
        if len(parts) < 2:
            return False, f"Invalid model format '{default_model}'. It should be in the format 'provider:model'."

        provider, model = parts

        if provider == 'openai' and not model.startswith('gpt'):
            return False, f"Invalid model '{model}' for OpenAI provider. OpenAI models should start with 'gpt'."
        elif provider == 'anthropic' and not model.startswith('claude'):
            return False, f"Invalid model '{model}' for Anthropic provider. Anthropic models should start with 'claude'."
        elif provider == 'ollama':
            # Ollama models can have additional colons, so we don't need to validate the model name structure
            pass
        elif provider == 'groq' and not (model.startswith('llama') or model.startswith('mixtral') or model.startswith('gemma')):
            return False, f"Invalid model '{model}' for Groq provider. Groq models should start with 'llama', 'mixtral', or 'gemma'."
        elif provider == 'google' and not ('gemini' in model):
            return False, f"Invalid model '{model}' for Google provider. Google models should contain 'gemini'."
        elif provider not in ['openai', 'anthropic', 'ollama', 'groq', 'google']:
            return False, f"Unknown provider '{provider}'."
        
        return True, None