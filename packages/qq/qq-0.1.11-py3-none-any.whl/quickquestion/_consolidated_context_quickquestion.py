
# ==================================================
# File: __init__.py
# ==================================================


# ==================================================
# File: cache.py
# ==================================================
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List


class ProviderCache:
    _instance = None

    def __new__(cls, debug=False):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, debug=False):
        if self._initialized:
            self.debug = debug
            return

        self.debug = debug
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self.cache_file = Path.home() / '.qq_cache.json'
        self.ttl_settings = {
            'providers': 3600,  # 1 hour for provider configuration
            'models': 3600,    # 1 hour for model lists
            'default': 30      # 30 seconds for everything else
        }
        self._initialized = True
        self._load_cache()

    def _provider_to_dict(self, provider: Any) -> dict:
        """Convert provider object to serializable dictionary with \
            complete model info"""
        # Get the models first if possible
        available_models = []
        try:
            if hasattr(provider, 'get_available_models'):
                models = provider.get_available_models()
                if models:
                    available_models = models
                    if self.debug:
                        print(f"DEBUG Cache: Captured {len(models)} \
                              models for {provider.__class__.__name__}")
        except Exception as e:
            if self.debug:
                print(f"DEBUG Cache: Error getting models for \
                      {provider.__class__.__name__}: {str(e)}")

        # Build the provider data
        provider_data = {
            'type': provider.__class__.__name__,
            'model': getattr(provider, 'current_model', None),
            'available_models': available_models,
            'api_url': getattr(provider, 'api_url', None),
            'status': {
                'last_check': time.time(),
                'available': bool(available_models),
                'error': None
            }
        }

        if self.debug:
            print(f"DEBUG Cache: Serialized provider {provider_data['type']} \
                  with model {provider_data['model']}")
            if provider_data['available_models']:
                print(f"DEBUG Cache: Available models: \
                      {provider_data['available_models']}")

        return provider_data

    def _dict_to_provider(self, data: dict) -> Any:
        """Convert dictionary back to provider object with enhanced \
            model handling"""
        from quickquestion.llm_provider import (
            LMStudioProvider,
            OllamaProvider,
            OpenAIProvider,
            AnthropicProvider,
            GroqProvider,
            GrokProvider
        )

        provider_map = {
            'LMStudioProvider': LMStudioProvider,
            'OllamaProvider': OllamaProvider,
            'OpenAIProvider': OpenAIProvider,
            'AnthropicProvider': AnthropicProvider,
            'GroqProvider': GroqProvider,
            'GrokProvider': GrokProvider
        }

        if self.debug:
            print(f"DEBUG Cache: Reconstructing provider {data['type']}")

        provider_class = provider_map.get(data['type'])
        if not provider_class:
            if self.debug:
                print(f"DEBUG Cache: Unknown provider type: {data['type']}")
            return None

        try:
            provider = provider_class()
            provider.current_model = data.get('model')
            provider.available_models = data.get('available_models', [])
            if 'api_url' in data and data['api_url']:
                provider.api_url = data['api_url']

            if self.debug:
                print(f"DEBUG Cache: Reconstructed {data['type']} with model \
                      {provider.current_model}")
                if provider.available_models:
                    print(f"DEBUG Cache: Restored \
                          {len(provider.available_models)} models")

            return provider

        except Exception as e:
            if self.debug:
                print(f"DEBUG Cache: Error reconstructing provider \
                      {data['type']}: {str(e)}")
            return None

    def _serialize_providers(self, providers: List[Any]) -> List[dict]:
        """Convert list of provider objects to serializable format"""
        return [self._provider_to_dict(p) for p in providers if p]

    def _deserialize_providers(self, data: List[dict]) -> List[Any]:
        """Convert list of dictionaries back to provider objects"""
        if self.debug:
            print(f"DEBUG Cache: Deserializing {len(data)} providers")

        providers = []
        for provider_data in data:
            try:
                provider = self._dict_to_provider(provider_data)
                if provider:
                    if self.debug:
                        print(f"DEBUG Cache: Successfully deserialized \
                              {provider_data['type']}")
                        if provider.current_model:
                            print(f"DEBUG Cache: Restored model: \
                                  {provider.current_model}")
                        if provider.available_models:
                            print(f"DEBUG Cache: Restored \
                                  {len(provider.available_models)} models")
                    providers.append(provider)
                else:
                    if self.debug:
                        print(f"DEBUG Cache: Failed to deserialize \
                              {provider_data['type']}")
            except Exception as e:
                if self.debug:
                    print(f"DEBUG Cache: Error deserializing provider \
                          {provider_data.get('type', 'unknown')}: {str(e)}")
                continue

        if self.debug:
            print(f"DEBUG Cache: Successfully deserialized \
                  {len(providers)} providers")

        return providers

    def _load_cache(self):
        """Load cache from disk with debug info"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    self._cache = data.get('cache', {})
                    self._timestamps = {k: float(v) for k, v
                                        in data.get('timestamps', {}).items()}

                    # Convert provider data back to objects
                    if 'available_providers' in self._cache:
                        self._cache['available_providers'] = self._deserialize_providers(
                            self._cache['available_providers'])

                if self.debug:
                    print(f"DEBUG Cache: Loaded cache from {self.cache_file}")
                    print("DEBUG Cache: Current cache contents:", self._cache.keys())
            except Exception as e:
                if self.debug:
                    print(f"DEBUG Cache: Error loading cache: {str(e)}")
                self._cache = {}
                self._timestamps = {}
        else:
            if self.debug:
                print("DEBUG Cache: No cache file found at", self.cache_file)

    def _save_cache(self):
        """Save cache to disk with enhanced error handling"""
        try:
            # Convert provider objects to serializable format
            cache_copy = self._cache.copy()
            if 'available_providers' in cache_copy:
                providers_data = []
                for provider in cache_copy['available_providers']:
                    try:
                        provider_data = self._provider_to_dict(provider)
                        if provider_data:
                            providers_data.append(provider_data)
                    except Exception as e:
                        if self.debug:
                            print(f"DEBUG Cache: Error serializing \
                                  provider: {str(e)}")
                            continue
                cache_copy['available_providers'] = providers_data

            with open(self.cache_file, 'w') as f:
                json.dump({
                    'cache': cache_copy,
                    'timestamps': self._timestamps
                }, f, indent=2)

            if self.debug:
                print(f"DEBUG Cache: Saved cache to {self.cache_file}")
                if 'available_providers' in cache_copy:
                    print("DEBUG Cache: Saved providers:", [p['type'] for p in providers_data])

        except Exception as e:
            if self.debug:
                print(f"DEBUG Cache: Error saving cache: {str(e)}")

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache with debug info"""
        if key in self._cache:
            ttl = self.ttl_settings.get(
                next((k for k in self.ttl_settings if k in key), 'default')
            )
            age = time.time() - self._timestamps[key]

            if self.debug:
                print(f"DEBUG Cache: Found key '{key}' (age: {age:.1f}s, ttl: {ttl}s)")

            if age < ttl:
                if self.debug:
                    print(f"DEBUG Cache: Returning cached value for '{key}'")
                return self._cache[key]
            else:
                if self.debug:
                    print(f"DEBUG Cache: Entry '{key}' has expired")
                del self._cache[key]
                del self._timestamps[key]
                self._save_cache()
        else:
            if self.debug:
                print(f"DEBUG Cache: Key '{key}' not found in cache")
        return None

    def set(self, key: str, value: Any):
        """Set value in cache with debug info"""
        self._cache[key] = value
        self._timestamps[key] = time.time()
        if self.debug:
            print(f"DEBUG Cache: Setting key '{key}' in cache")
        self._save_cache()

    def clear(self, key_prefix: Optional[str] = None):
        """Clear cache entries with debug info"""
        if key_prefix:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(key_prefix)]
            if self.debug:
                print(f"DEBUG Cache: Clearing entries with prefix '{key_prefix}':", keys_to_delete)
            for k in keys_to_delete:
                del self._cache[k]
                del self._timestamps[k]
        else:
            if self.debug:
                print("DEBUG Cache: Clearing entire cache")
            self._cache.clear()
            self._timestamps.clear()
        self._save_cache()

    def get_cache_info(self) -> Dict[str, Dict[str, float]]:
        """Get information about cache entries"""
        current_time = time.time()
        cache_info = {}

        for key in self._cache:
            ttl = self.ttl_settings.get(
                next((k for k in self.ttl_settings if k in key), 'default')
            )
            age = current_time - self._timestamps[key]

            cache_info[key] = {
                'age_seconds': age,
                'expires_in_seconds': ttl - age,
                'ttl': ttl
            }

        return cache_info


# Global cache instance - now with debug mode support
def get_provider_cache(debug=False) -> ProviderCache:
    """Get or create the provider cache instance with debug mode"""
    return ProviderCache(debug=debug)


# Initialize the global cache instance
provider_cache = ProviderCache()


# ==================================================
# File: dev_actions/__init__.py
# ==================================================
# dev_actions/__init__.py
from .base import DevAction
from .git_push import GitPushAction

# Register all available actions
available_actions = [
    GitPushAction
]


# ==================================================
# File: dev_actions/base.py
# ==================================================
# dev_actions/base.py
from abc import ABC, abstractmethod
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from functools import wraps
from contextlib import contextmanager
from quickquestion.utils import clear_screen, getch
import threading


class DevAction(ABC):
    """Base class for developer actions with execution lock prevention"""
    
    def __init__(self, provider, debug: bool = False):
        self.provider = provider
        self.debug = debug
        self.console = Console()
        self._execution_lock = threading.Lock()
        self._is_executing = False
        
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the action shown in the menu"""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """The description shown in the menu"""
        pass

    @contextmanager
    def show_loading(self, message: str = None):
        """Context manager for showing loading state"""
        default_message = f"Executing {self.name}..."
        with self.console.status(
            f"[bold blue]{message or default_message}[/bold blue]",
            spinner="dots",
            spinner_style="blue"
        ):
            yield

    def execute_with_loading(self, func):
        """Decorator to add loading message to any method"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.show_loading():
                return func(*args, **kwargs)
        return wrapper
        
    @abstractmethod
    def execute(self) -> bool:
        """Execute the action. Return True if successful."""
        pass

    def _wrapped_execute(self) -> bool:
        """Internal wrapper to add loading state and prevent multiple executions"""
        # Check if we're already executing
        if self._is_executing:
            if self.debug:
                self.console.print("[red]Action already executing, ignoring request[/red]")
            return False

        try:
            # Set executing flag
            with self._execution_lock:
                if self._is_executing:
                    return False
                self._is_executing = True

            # Execute with loading status
            with self.show_loading():
                return self.execute()

        finally:
            # Always reset the executing flag
            with self._execution_lock:
                self._is_executing = False

    def __call__(self) -> bool:
        """Make the action callable with default loading behavior and execution lock"""
        return self._wrapped_execute()

    def display_options(self, options: List[str], title: str = "Options") -> Optional[int]:
        """Display a list of options with consistent UI"""
        selected = 0

        # Show options
        for i, option in enumerate(options):
            style = "bold white on blue" if i == selected else "blue"
            self.console.print(Panel(str(option), border_style=style))

        while True:
            c = getch(debug=self.debug)
            
            if c == '\x1b[A':  # Up arrow
                if selected > 0:
                    selected -= 1
                    return self.display_options(options)  # Recursively redraw
            elif c == '\x1b[B':  # Down arrow
                if selected < len(options) - 1:
                    selected += 1
                    return self.display_options(options)  # Recursively redraw
            elif c == '\r':  # Enter
                return selected
            elif c == 'q':  # Quick exit
                return None

    def confirm_action(self, message: str) -> bool:
        """Display a confirmation dialog with consistent UI
        
        Args:
            message: Message to display
            
        Returns:
            True if confirmed, False if cancelled
        """
        options = ["Confirm", "Cancel"]
        selected = self.display_options(options, "Confirmation")
        return selected == 0


# ==================================================
# File: dev_actions/git_push.py
# ==================================================
# dev_actions/git_push.py

import subprocess
import os
from typing import List, Optional, Tuple
from rich.panel import Panel
from pathlib import Path
from quickquestion.ui_library import UIOptionDisplay
from quickquestion.utils import clear_screen
from contextlib import contextmanager
from .base import DevAction


class GitPushAction(DevAction):
    """Git push action with AI-generated commit messages"""
    
    def __init__(self, provider, debug: bool = False):
        super().__init__(provider, debug)
        self._is_loading = False

    @property
    def name(self) -> str:
        return "Push Code"
        
    @property
    def description(self) -> str:
        return "Stage, commit, and push changes with AI-generated commit message"

    def _is_git_repository(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            if self.debug:
                self.console.print(f"[blue]DEBUG: Git repository check result: {result.returncode}[/blue]")
                if result.stderr:
                    self.console.print(f"[blue]DEBUG: Git stderr: {result.stderr}[/blue]")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            if self.debug:
                self.console.print(f"[red]DEBUG: Git repository check error: {str(e)}[/red]")
            return False

    def _get_git_changes(self) -> Tuple[str, List[str]]:
        """Get the diff of changes and list of modified files"""
        if self.debug:
            self.console.print("[blue]DEBUG: Getting git changes[/blue]")
            
        # Get both staged and unstaged changes
        diff_process = subprocess.run(
            ["git", "diff", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # Get both modified and untracked files
        status_process = subprocess.run(
            ["git", "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        modified_files = [
            line[3:] for line in status_process.stdout.split('\n')
            if line.strip() and line[0] in ['M', 'A', 'D', '?', ' ']
        ]
        
        if self.debug:
            self.console.print(f"[blue]DEBUG: Found {len(modified_files)} modified files[/blue]")
            for file in modified_files:
                self.console.print(f"[blue]DEBUG: Modified file: {file}[/blue]")
        
        return diff_process.stdout, modified_files

    def _stage_changes(self) -> bool:
        """Stage all changes"""
        try:
            if self.debug:
                self.console.print("[blue]DEBUG: Staging changes[/blue]")
            result = subprocess.run(
                ["git", "add", "-A"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode != 0:
                if self.debug:
                    self.console.print(f"[red]DEBUG: Git add error: {result.stderr}[/red]")
                return False
            return True
        except subprocess.CalledProcessError as e:
            if self.debug:
                self.console.print(f"[red]DEBUG: Error staging changes: {str(e)}[/red]")
            return False

    def _commit_changes(self, message: str) -> bool:
        """Commit staged changes with the given message"""
        try:
            if self.debug:
                self.console.print("[blue]DEBUG: Committing changes[/blue]")
            result = subprocess.run(
                ["git", "commit", "-m", message],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode != 0:
                if self.debug:
                    self.console.print(f"[red]DEBUG: Git commit error: {result.stderr}[/red]")
                return False
            if self.debug and result.stdout:
                self.console.print(f"[blue]DEBUG: Git commit output: {result.stdout}[/blue]")
            return True
        except subprocess.CalledProcessError as e:
            if self.debug:
                self.console.print(f"[red]DEBUG: Error committing changes: {str(e)}[/red]")
            return False

    def _generate_commit_message(self, diff: str, files: List[str]) -> str:
        """Generate a commit message using the LLM"""
        prompt = f"""As a developer, analyze these git changes and generate a clear, concise commit message.
Modified files: {', '.join(files)}

Changes:
{diff}

Rules for the commit message:
1. Use present tense (e.g., "Add feature" not "Added feature")
2. Keep it under 50 characters
3. Be specific but concise
4. Focus on the "what" and "why", not the "how"
5. Don't include file names unless crucial

Return ONLY the commit message with no additional text or formatting."""

        try:
            if self.debug:
                self.console.print("[blue]DEBUG: Generating commit message using LLM[/blue]")
            response = self.provider.generate_response(prompt)
            return response[0].strip('"\'')
        except Exception as e:
            if self.debug:
                self.console.print(f"[red]Error generating commit message: {str(e)}[/red]")
            return ""

    def _display_commit_options(self, commit_message: str, modified_files: List[str]) -> Optional[str]:
        """Display commit options without additional status messages"""
        ui = UIOptionDisplay(self.console, debug=self.debug)
        
        # Prepare options data
        options = ["Commit", "Regenerate", "Cancel"]
        panel_titles = ["Commit Changes", "Generate New Message", "Exit"]
        
        # Prepare header panels
        header_panels = [
            {
                'title': 'Git Status',
                'content': f"[yellow]Modified Files:[/yellow]\n{', '.join(modified_files)}"
            },
            {
                'title': 'Current Commit Message',
                'content': f"[green]{commit_message}[/green]"
            }
        ]

        while True:
            selected, action = ui.display_options(
                options=options,
                panel_titles=panel_titles,
                extra_content=[
                    "Apply the selected commit message",
                    "Generate a new message",
                    "Cancel the operation"
                ],
                header_panels=header_panels,
                show_cancel=False,  # We have our own cancel option
                banner_params={
                    'title': "Git Commit Review",
                    'subtitle': ["Review and confirm commit message"],
                    'website': "https://southbrucke.com"
                }
            )

            if action in ('quit', 'cancel') or selected == 2:  # Exit
                return None
                
            if action == 'select':
                if selected == 0:  # Commit
                    return commit_message
                elif selected == 1:  # Regenerate
                    # Show loading only while generating
                    with self.show_loading("Generating new commit message..."):
                        diff, _ = self._get_git_changes()
                        new_message = self._generate_commit_message(diff, modified_files)
                    
                    if new_message:
                        commit_message = new_message
                        # Update the header panel with new message
                        header_panels[1]['content'] = f"[green]{commit_message}[/green]"
                    else:
                        ui.display_message(
                            "Failed to generate new commit message",
                            style="red",
                            title="Error",
                            pause=True
                        )
                    continue

        return None

    def execute(self) -> bool:
        """Execute the git push action with clean UI flow"""
        ui = UIOptionDisplay(self.console, debug=self.debug)
        
        if self.debug:
            self.console.print("[blue]DEBUG: Starting git push action[/blue]")
            
        if not self._is_git_repository():
            ui.display_message(
                "Not a git repository",
                style="red",
                title="Error"
            )
            return False

        # Get git changes silently
        diff, modified_files = self._get_git_changes()
        
        if not modified_files:
            ui.display_message(
                "No changes to commit",
                style="yellow",
                title="Status"
            )
            return False

        # Generate initial commit message with loading indicator
        with self.show_loading("Analyzing changes..."):
            commit_message = self._generate_commit_message(diff, modified_files)
        
        if not commit_message:
            ui.display_message(
                "Could not generate commit message",
                style="red",
                title="Error"
            )
            return False

        # Display options and get selected message
        # Note: No status message here as the UI is interactive
        selected_message = self._display_commit_options(commit_message, modified_files)
        
        if selected_message is None:
            ui.display_message(
                "Operation cancelled",
                style="yellow",
                title="Status"
            )
            return False
            
        # Show loading only during actual commit
        with self.show_loading("Committing changes..."):
            success = self._stage_changes() and self._commit_changes(selected_message)
        
        if success:
            ui.display_message(
                "Successfully committed changes!",
                style="green",
                title="Success"
            )
            return True
        
        ui.display_message(
            "Failed to commit changes",
            style="red",
            title="Error"
        )
        return False


# ==================================================
# File: dev_mode.py
# ==================================================
# dev_mode.py

import os
import sys
import json
import inspect
import importlib.util
from pathlib import Path
from typing import Optional, List, Type, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import threading

from quickquestion.llm_provider import LLMProvider
from quickquestion.utils import clear_screen, getch
from quickquestion.settings_manager import get_settings
from quickquestion.dev_actions import available_actions, DevAction
from quickquestion.ui_library import UIOptionDisplay


class DevMode:
    def __init__(self, debug: bool = False):
        self.console = Console()
        self.debug = debug
        self.settings = get_settings(debug=debug)
        self.ui = UIOptionDisplay(self.console, debug=debug)
        
        # Show loading if not in debug mode
        if not debug:
            with self.ui.display_loading("Initializing dev mode..."):
                self.provider = self._initialize_provider()
                self.custom_actions_dir = Path.home() / "QuickQuestion" / "CustomDevActions"
                self.actions = self._initialize_actions()
        else:
            self.provider = self._initialize_provider()
            self.custom_actions_dir = Path.home() / "QuickQuestion" / "CustomDevActions"
            self.actions = self._initialize_actions()
            
        self._execution_lock = threading.Lock()
        self._is_executing = False
        
    def debug_print(self, message: str, data: Any = None):
        """Print debug information if debug mode is enabled"""
        if self.debug:
            # Add timestamp to debug messages
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            msg = f"[{timestamp}] DEBUG DevMode: {message}"
            self.console.print(msg)
            
            if data is not None:
                if isinstance(data, (dict, list)):
                    self.console.print(Panel(
                        json.dumps(data, indent=2),
                        title="Debug Data",
                        border_style="cyan"
                    ))
                else:
                    self.console.print(Panel(
                        str(data),
                        title="Debug Data",
                        border_style="cyan"
                    ))

    def _ensure_custom_actions_dir(self):
        """Ensure custom actions directory exists and contains required files"""
        if not self.custom_actions_dir.exists():
            self.debug_print(f"Creating custom actions directory: {self.custom_actions_dir}")
            self.custom_actions_dir.mkdir(parents=True)
            
            # Create __init__.py file
            init_file = self.custom_actions_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")
                self.debug_print("Created __init__.py file")
            
            # Create sample action file
            sample_path = self.custom_actions_dir / "sample_action.py"
            if not sample_path.exists():
                self.debug_print("Creating sample action file")
                sample_content = '''"""Sample Developer Action for Quick Question"""
import time
from rich.progress import Progress, SpinnerColumn, TextColumn
from quickquestion.dev_actions.base import DevAction

class SampleStepAction(DevAction):
    @property
    def name(self) -> str:
        return "Sample Two-Step Action"
        
    @property
    def description(self) -> str:
        return "Demonstrates a two-step process with progress indicators"

    def show_countdown(self, seconds: int, message: str):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(message, total=seconds)
            for remaining in range(seconds, 0, -1):
                progress.update(task, description=f"{message} ({remaining}s)")
                time.sleep(1)
        
    def execute(self) -> bool:
        self.console.print("[bold blue]Starting sample two-step process...[/bold blue]")
        
        self.console.print("[green]Step 1:[/green] First waiting period")
        self.show_countdown(3, "Processing step 1")
        
        if not self.confirm_action("Continue to step 2?"):
            self.console.print("[yellow]Process cancelled[/yellow]")
            return False
            
        self.console.print("[green]Step 2:[/green] Second waiting period")
        self.show_countdown(3, "Processing step 2")
        
        self.console.print("[bold green]Process completed successfully![/bold green]")
        return True
    '''
                sample_path.write_text(sample_content)
                self.debug_print("Created sample action file")

    def _load_custom_actions(self) -> List[Type[DevAction]]:
        """Load custom actions from the CustomDevActions directory"""
        custom_actions = []
        
        self._ensure_custom_actions_dir()
        
        if not self.custom_actions_dir.exists():
            self.debug_print(f"Custom actions directory not found: {self.custom_actions_dir}")
            return []

        sys.path.append(str(self.custom_actions_dir.parent.parent))
        
        # Scan for .py files
        for file_path in self.custom_actions_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
                
            try:
                module_name = f"QuickQuestion.CustomDevActions.{file_path.stem}"
                self.debug_print(f"Loading module: {module_name}")
                
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None or spec.loader is None:
                    self.debug_print(f"Could not create spec for {file_path}")
                    continue
                    
                module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
                
                # Find DevAction subclasses
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and issubclass(obj, DevAction) and obj != DevAction):
                        self.debug_print(f"Found custom action: {name}")
                        custom_actions.append(obj)
                        
            except Exception as e:
                self.debug_print(f"Error loading {file_path}: {str(e)}")
                if self.debug:
                    import traceback
                    traceback.print_exc()
                continue
        
        return custom_actions

    def _initialize_actions(self) -> List[DevAction]:
        """Initialize both built-in and custom actions"""
        # Get built-in actions
        actions = [action(self.provider, self.debug) for action in available_actions]
        self.debug_print(f"Initialized {len(actions)} built-in actions")
        
        # Load custom actions
        custom_actions = self._load_custom_actions()
        actions.extend(action(self.provider, self.debug) for action in custom_actions)
        self.debug_print(f"Added {len(custom_actions)} custom actions")
        
        return actions

    def _initialize_provider(self) -> Optional[LLMProvider]:
        """Initialize the LLM provider based on current settings"""
        self.debug_print("Initializing provider")
        from quickquestion.qq import QuickQuestion
        qq = QuickQuestion(debug=self.debug, settings=self.settings)
        return qq.provider

    def display_menu(self):
        """Display the developer mode menu using the enhanced UI library"""
        try:
            self.debug_print("Starting dev mode display")
            
            # Display banner
            if not self.debug:
                clear_screen()
            
            # Prepare menu data
            options = self.actions + ["Exit"]
            panel_titles = []
            extra_content = []
            
            # Format action options
            for action in self.actions:
                panel_titles.append(action.name)
                extra_content.append(f"[dim]{action.description}[/dim]")
                
            # Add exit option
            panel_titles.append("Exit")
            extra_content.append("Exit developer mode")

            while True:
                try:
                    # Display menu and get selection
                    selected, action = self.ui.display_options(
                        options=[opt.name if isinstance(opt, DevAction) else opt for opt in options],
                        panel_titles=panel_titles,
                        extra_content=extra_content,
                        show_cancel=False,
                        banner_params={
                            'title': "Quick Question",
                            'subtitle': ["Select an action"],
                            'website': "https://southbrucke.com"
                        }
                    )
                    
                    # Log selection in debug mode
                    if self.debug:
                        self.debug_print("Menu selection", {
                            "selected": selected,
                            "action": action,
                            "selected_name": (options[selected].name
                                if selected < len(self.actions)
                                else "Exit")
                        })

                    # Handle selection
                    if action in ('quit', 'cancel') or selected == len(options) - 1:  # Exit
                        self.debug_print("Exiting dev mode")
                        clear_screen()
                        return
                        
                    elif action == 'select':
                        selected_action = self.actions[selected]
                        self.debug_print(f"Executing action: {selected_action.name}")
                        
                        # Execute selected action
                        self._execute_action(selected_action)
                        
                        # Refresh display after action completes
                        if not self.debug:
                            clear_screen()
                        self.ui.display_banner(
                            "Quick Question - Developer Mode - Line 259",
                            subtitle=["Select an action to execute"],
                            website="https://southbrucke.com"
                        )
                        
                except KeyboardInterrupt:
                    self.debug_print("Keyboard interrupt received")
                    clear_screen()
                    return
                    
                except Exception as e:
                    self.debug_print(f"Error in menu handling: {str(e)}")
                    if self.debug:
                        import traceback
                        self.debug_print("Full traceback", traceback.format_exc())
                    return
                    
        except Exception as e:
            self.debug_print(f"Fatal error in display_menu: {str(e)}")
            if self.debug:
                import traceback
                self.debug_print("Full traceback", traceback.format_exc())
            raise

    def _execute_action(self, action: DevAction):
        """Execute an action with proper locking and error handling"""
        if self._is_executing:
            self.ui.display_message(
                "An action is already running, please wait...",
                style="yellow",
                title="Warning"
            )
            return

        try:
            with self._execution_lock:
                if self._is_executing:
                    return
                
                self._is_executing = True
                self.debug_print(f"Executing action: {action.name}")
                
                # Execute without a persistent loading indicator
                success = action.execute()

                if not success:
                    self.debug_print("Action completed with errors")
                    self.ui.display_message(
                        "Action completed with errors. Check the output above.",
                        style="yellow",
                        title="Warning",
                        pause=True
                    )

        except Exception as e:
            self.debug_print(f"Error executing action: {str(e)}")
            self.ui.display_message(
                f"Error executing action: {str(e)}",
                style="red",
                title="Error",
                pause=True
            )
            if self.debug:
                import traceback
                traceback.print_exc()

        finally:
            with self._execution_lock:
                self._is_executing = False


def main():
    """Entry point for developer mode"""
    import argparse
    parser = argparse.ArgumentParser(description="Quick Question - Developer Mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    dev_mode = DevMode(debug=args.debug)
    dev_mode.display_menu()


if __name__ == "__main__":
    main()


# ==================================================
# File: llm_provider.py
# ==================================================
#!/usr/bin/env python3
# llm_provider.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import requests
import json
import os
import asyncio
import aiohttp
import sys
import ssl


class LLMProvider(ABC):
    """Base class for LLM providers"""

    PREFERRED_MODELS = [
        "mistral",
        "llama2",
        "codellama",
        "openhermes",
        "neural-chat",
        "stable-beluga",
        "qwen",
        "yi"
    ]

    def __init__(self, debug: bool = False):
        """Initialize the provider with debug mode"""
        self.debug = debug

    def _check_special_characters(self, content: str) -> dict:
        """Check content for special characters in a Python-version-compatible way"""
        null_byte = chr(0)  # Instead of using \x00
        newline = chr(10)   # Instead of using \n
        carriage_return = chr(13)  # Instead of using \r
        tab = chr(9)        # Instead of using \t

        return {
            "length": len(content),
            "first_chars": [ord(c) for c in content[:10]],
            "has_null_bytes": null_byte in content,
            "has_newlines": newline in content,
            "has_carriage_returns": carriage_return in content,
            "has_tabs": tab in content,
            "starts_with_markdown": content.startswith('```'),
            "ends_with_markdown": content.endswith('```'),
            "starts_with_bracket": content.startswith('['),
            "ends_with_bracket": content.endswith(']')
        }

    def _parse_llm_response(self, content: str) -> List[str]:
        """
        Enhanced response parser for LLM outputs that handles:
        - Nested array structures
        - Multiple JSON arrays on separate lines
        - Markdown code blocks
        - Escaped quotes and characters
        - Different JSON formatting styles
        - Truncated responses
        """
        def clean_command(cmd: str) -> str:
            """Clean up individual commands by removing extra quotes and escaping"""
            cmd = cmd.strip()
            # Remove wrapping quotes if present
            if (cmd.startswith('"') and cmd.endswith('"')) or \
               (cmd.startswith("'") and cmd.endswith("'")):
                cmd = cmd[1:-1]
            # Unescape escaped quotes
            cmd = cmd.replace('\\"', '"').replace("\\'", "'")
            # Remove any residual JSON escaping
            cmd = cmd.replace('\\\\', '\\')
            return cmd

        try:
            # Clean up markdown formatting if present
            if content.startswith('```'):
                first_newline = content.find('\n')
                if first_newline != -1:
                    content = content[first_newline + 1:]
                if content.endswith('```'):
                    content = content[:-3]
            
            content = content.strip()
            
            # Fix truncated responses by balancing brackets
            if content.count('[') > content.count(']'):
                content = content + ']' * (content.count('[') - content.count(']'))
            
            # Try parsing as single JSON array first
            try:
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    # Handle nested arrays and clean up commands
                    commands = []
                    for item in parsed:
                        if isinstance(item, list):
                            commands.extend(clean_command(str(x)) for x in item)
                        else:
                            cleaned = clean_command(str(item))
                            if cleaned:
                                commands.append(cleaned)
                    return commands
                else:
                    raise ValueError("Response is not a list")
                    
            except json.JSONDecodeError:
                # If JSON parsing fails, try line-by-line
                commands = []
                for line in content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('```'):
                        continue
                        
                    try:
                        # Try parsing line as JSON
                        line_parsed = json.loads(line)
                        if isinstance(line_parsed, list):
                            commands.extend(clean_command(cmd) for cmd in line_parsed)
                        else:
                            cleaned = clean_command(line)
                            if cleaned:
                                commands.append(cleaned)
                    except json.JSONDecodeError:
                        # If not valid JSON and looks like a command, add it
                        if not line.startswith('[') and not line.endswith(']'):
                            cleaned = clean_command(line)
                            if cleaned:
                                commands.append(cleaned)
                
                if commands:
                    return commands
                
                raise ValueError("No valid commands found in response")

        except Exception as e:
            if self.debug:
                print("DEBUG: Error parsing response:", str(e))
                print("DEBUG: Raw content:", content)
                print("DEBUG: Content type:", type(content))
                if content:
                    print("DEBUG: First few characters:", repr(content[:100]))
                    print("DEBUG: Content analysis:", self._check_special_characters(content))
            raise Exception(f"Error parsing response: {str(e)}\nRaw content: {content}")

    async def async_check_status(self, debug=False) -> bool:
        """Async version of status check with enhanced debugging"""
        if debug:
            print(f"\nDEBUG Provider: Starting async status check for {self.__class__.__name__}")

        try:
            # For SDK-based providers that don't use HTTP endpoints
            if not hasattr(self, 'api_url'):
                if debug:
                    print("DEBUG Provider: Using direct SDK connection")
                models = self.get_available_models()
                if models:
                    self.current_model = self.select_best_model(models)
                    if debug:
                        print(f"DEBUG Provider: Found models: {models}")
                        print(f"DEBUG Provider: Selected model: {self.current_model}")
                    return True
                if debug:
                    print("DEBUG Provider: No models found")
                return False

            # For HTTP API-based providers
            if debug:
                print(f"DEBUG Provider: API URL = {self.api_url}")

            try:
                async with aiohttp.ClientSession() as session:
                    if debug:
                        print("DEBUG Provider: Established aiohttp session")
                        print(f"DEBUG Provider: Attempting connection to {self.api_url}")

                    try:
                        async with session.get(self.api_url, timeout=2.0) as response:
                            if debug:
                                print(f"DEBUG Provider: Response status: {response.status}")
                                print(f"DEBUG Provider: Response headers: {dict(response.headers)}")
                            return response.status == 200
                    except asyncio.TimeoutError:
                        if debug:
                            print("DEBUG Provider: Connection timeout")
                        return False
                    except aiohttp.ClientError as e:
                        if debug:
                            print(f"DEBUG Provider: Connection error: {str(e)}")
                        return False
            except Exception as e:
                if debug:
                    print(f"DEBUG Provider: Connection error: {str(e)}")
                return False

        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Unexpected error: {str(e)}")
                import traceback
                print("DEBUG Provider: Full traceback:")
                traceback.print_exc()
            return False

    def check_status(self, debug=False) -> bool:
        """Sync wrapper for async status check with debugging"""
        try:
            if debug:
                print(f"\nDEBUG Provider: Setting up async loop for {self.__class__.__name__}")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            if debug:
                print("DEBUG Provider: Created new event loop")

            result = loop.run_until_complete(self.async_check_status(debug=debug))

            if debug:
                print(f"DEBUG Provider: Async check completed with result: {result}")

            loop.close()

            if debug:
                print("DEBUG Provider: Closed event loop")

            return result
        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Error in async wrapper: {str(e)}")
                import traceback
                print("DEBUG Provider: Full traceback:")
                traceback.print_exc()
            return False

    def select_best_model(self, available_models: List[str]) -> Optional[str]:
        """Select the best model from available ones based on preferences"""
        available_lower = [m.lower() for m in available_models]

        for preferred in self.PREFERRED_MODELS:
            for available in available_lower:
                if preferred in available:
                    return available_models[available_lower.index(available)]

        return available_models[0] if available_models else None

    @abstractmethod
    def get_model_info(self) -> Optional[str]:
        """Get information about the currently loaded model"""
        pass

    @abstractmethod
    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response from the model"""
        pass

    @abstractmethod
    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass


class LMStudioProvider(LLMProvider):
    """LM Studio implementation of LLM provider"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
        self.api_url = "http://localhost:1234/v1"
        self.current_model = None
        self.default_model = "model"

    def generate_response(self, prompt: str) -> List[str]:
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "model": self.current_model or self.default_model  # Use default if no model set
        }

        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._parse_llm_response(content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "model": self.current_model or self.default_model  # Use default if no model set
        }

        try:
            print("\nDEBUG: Making request to LM Studio API...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")
            print(f"DEBUG: Request headers: {json.dumps(headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")

            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            
            # Handle headers that might be Mock objects in tests
            try:
                response_headers = dict(response.headers)
            except (TypeError, AttributeError):
                response_headers = {"note": "Headers not available in test environment"}
                
            print(f"DEBUG: Response headers: {json.dumps(response_headers, indent=2)}")

            response.raise_for_status()
            response_json = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")

            content = response_json["choices"][0]["message"]["content"]
            print(f"\nDEBUG: Raw content before parsing: {content}")

            parsed = self._parse_llm_response(content)
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")

            return parsed

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"DEBUG: Full response text: {e.response.text if hasattr(e, 'response') else 'No response text'}")
            raise Exception(f"Error generating response: {str(e)}")

    def get_available_models(self) -> List[str]:
        try:
            response = requests.get(f"{self.api_url}/models")
            if response.status_code == 200:
                models = response.json()
                if models.get('data'):
                    return [model['id'] for model in models['data']]
            return []
        except requests.exceptions.RequestException:
            return []

    def check_status(self) -> bool:
        available_models = self.get_available_models()
        if available_models:
            self.current_model = self.select_best_model(available_models)
            return True
        return False

    def get_model_info(self) -> Optional[str]:
        return self.current_model


class OllamaProvider(LLMProvider):
    """Ollama implementation of LLM provider"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
        self.api_url = "http://localhost:11434/api"
        self.current_model = None

    def get_available_models(self) -> List[str]:
        """Get available models with better error handling"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=2.0)

            if response.status_code == 200:
                models = response.json()
                if models.get('models'):
                    return [model['name'] for model in models['models']]
            return []

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {str(e)}")
            return []

    def select_best_model(self, available_models: List[str]) -> Optional[str]:
        """Enhanced model selection for Ollama"""
        available_lower = [m.lower() for m in available_models]

        # First try exact matches with preferred models
        for preferred in self.PREFERRED_MODELS:
            for available in available_lower:
                if preferred == available:
                    return available_models[available_lower.index(available)]

        # Then try partial matches
        for preferred in self.PREFERRED_MODELS:
            for available in available_lower:
                if preferred in available:
                    return available_models[available_lower.index(available)]

        # If no matches, return first available
        return available_models[0] if available_models else None

    async def async_check_status(self, debug=False) -> bool:
        """Async version of status check with enhanced error handling"""
        if debug:
            print(f"\nDEBUG Provider: Starting async status check for {self.__class__.__name__}")
            print(f"DEBUG Provider: API URL = {self.api_url}")

        try:
            async with aiohttp.ClientSession() as session:
                if debug:
                    print("DEBUG Provider: Established aiohttp session")
                    print(f"DEBUG Provider: Attempting connection to {self.api_url}/tags")

                try:
                    # Ollama uses /api/tags to list models
                    async with session.get(f"{self.api_url}/tags", timeout=2.0) as response:
                        if debug:
                            print(f"DEBUG Provider: Response status: {response.status}")
                            print(f"DEBUG Provider: Response headers: {dict(response.headers)}")

                            if response.status != 200:
                                text = await response.text()
                                print(f"DEBUG Provider: Error response: {text}")

                        # Only consider 200 as success
                        if response.status == 200:
                            models_data = await response.json()
                            if models_data.get('models'):
                                available_models = [m['name'] for m in models_data['models']]
                                if debug:
                                    print(f"DEBUG Provider: Found models: {available_models}")
                                self.current_model = self.select_best_model(available_models)
                                if debug:
                                    print(f"DEBUG Provider: Selected model: {self.current_model}")
                                return True
                            else:
                                if debug:
                                    print("DEBUG Provider: No models found in response")
                                return False

                        if debug:
                            print("DEBUG Provider: Unsuccessful status code")
                        return False

                except asyncio.TimeoutError:
                    if debug:
                        print("DEBUG Provider: Connection timeout")
                    return False
                except aiohttp.ClientError as e:
                    if debug:
                        print(f"DEBUG Provider: Connection error: {str(e)}")
                        print(f"DEBUG Provider: Is Ollama running at {self.api_url}?")
                    return False

        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Unexpected error: {str(e)}")
                import traceback
                print("DEBUG Provider: Full traceback:")
                traceback.print_exc()
            return False

    def check_status(self, debug=False) -> bool:
        """Sync version of status check"""
        if debug:
            print("\nDEBUG Provider: Checking Ollama status")

        try:
            available_models = self.get_available_models()
            if available_models:
                self.current_model = self.select_best_model(available_models)
                if debug:
                    print(f"DEBUG Provider: Found models: {available_models}")
                    print(f"DEBUG Provider: Selected model: {self.current_model}")
                return True
            return False
        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Error checking status: {str(e)}")
            return False

    def get_model_info(self) -> Optional[str]:
        return self.current_model

    def generate_response(self, prompt: str) -> List[str]:
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7
        }

        try:
            response = requests.post(f"{self.api_url}/generate", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["response"]
            return self._parse_llm_response(content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7
        }

        try:
            print("\nDEBUG: Making request to Ollama API...")
            print(f"DEBUG: Request URL: {self.api_url}/generate")
            print(f"DEBUG: Request headers: {json.dumps(headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")

            response = requests.post(f"{self.api_url}/generate", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {json.dumps(dict(response.headers), indent=2)}")

            response.raise_for_status()
            response_json = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")

            content = response_json["response"]
            print(f"\nDEBUG: Raw content before parsing: {content}")

            parsed = self._parse_llm_response(content)
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")

            return parsed

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"DEBUG: Full response text: {e.response.text if hasattr(e, 'response') else 'No response text'}")
            raise Exception(f"Error generating response: {str(e)}")


class AnthropicProvider(LLMProvider):
    """Anthropic implementation of LLM provider using the official SDK"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.current_model = None
        self.client = None
        self.available_models = []

        if not self.api_key:
            if self.debug:
                print("DEBUG: No Anthropic API key found in environment")
            return

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)

            # Define default models - these will be used if we can't get them from the SDK
            self.available_models = [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
                "claude-2.1",
                "claude-2.0",
                "claude-instant-1.2"
            ]

            # Try to get models from the SDK if possible
            try:
                from anthropic.types import Model
                if hasattr(Model, '__args__'):
                    union_args = Model.__args__
                    if len(union_args) > 1:
                        literal_type = union_args[1]
                        sdk_models = list(literal_type.__args__)
                        if sdk_models:
                            self.available_models = sdk_models
            except (ImportError, AttributeError, IndexError) as e:
                if self.debug:
                    print(f"DEBUG: Using default models list due to error: {str(e)}")

        except ImportError as e:
            if "anthropic" in str(e):
                print("Anthropic SDK not installed. Please install with: pip install anthropic")
            else:
                print(f"Error importing Anthropic SDK: {str(e)}")
            self.client = None
            self.available_models = []
        except Exception as e:
            print(f"Error initializing Anthropic client: {str(e)}")
            self.client = None
            self.available_models = []

    def get_available_models(self) -> List[str]:
        if not self.api_key or not self.client:
            return []
        return self.available_models

    async def async_get_available_models(self, debug=False) -> List[str]:
        """Async version of get_available_models"""
        if debug:
            print("DEBUG Anthropic: Checking available models")
        return self.get_available_models()

    def check_status(self) -> bool:
        if not self.api_key or not self.client:
            return False

        try:
            if self.available_models:
                self.current_model = self.select_best_model(self.available_models)
                return True
            return False
        except Exception as e:
            if self.debug:
                print(f"DEBUG: Error checking Anthropic status: {str(e)}")
            return False

    def get_model_info(self) -> Optional[str]:
        return self.current_model

    def generate_response(self, prompt: str) -> List[str]:
        if not self.current_model:
            raise Exception("No model selected")

        try:
            message = self.client.messages.create(
                model=self.current_model,
                max_tokens=1000,  # Increased from 200 to 1000
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return self._parse_llm_response(message.content[0].text)
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")

        try:
            print("\nDEBUG: Making request to Anthropic API...")
            print(f"DEBUG: Using model: {self.current_model}")
            print("DEBUG: Request data:", {
                "model": self.current_model,
                "max_tokens": 1000,  # Increased from 200 to 1000
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}]
            })

            message = self.client.messages.create(
                model=self.current_model,
                max_tokens=1000,  # Increased from 200 to 1000
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            print("\nDEBUG: Response received")
            print(f"DEBUG: Raw response: {message}")
            print(f"\nDEBUG: Raw content before parsing: {message.content[0].text}")

            parsed = self._parse_llm_response(message.content[0].text)
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")

            return parsed

        except Exception as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            import traceback
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            raise Exception(f"Error generating response: {str(e)}")


class OpenAIProvider(LLMProvider):
    """OpenAI implementation of LLM provider"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.api_url = "https://api.openai.com/v1"
        self.current_model = None
        self.ssl_context = self._create_ssl_context()

        self.available_models = [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo"
        ]

    def _create_ssl_context(self) -> Optional[ssl.SSLContext]:
        """Create SSL context with proper certificate handling"""
        if sys.platform == 'darwin':
            # Try to find the certificates
            cert_paths = [
                '/usr/local/etc/openssl/cert.pem',  # Homebrew OpenSSL
                '/usr/local/etc/openssl@3/cert.pem',  # Homebrew OpenSSL 3
                '/etc/ssl/cert.pem',  # System SSL
                '/Library/Developer/CommandLineTools/usr/lib/python3/cert.pem'  # Python SSL
            ]

            for cert_path in cert_paths:
                if os.path.exists(cert_path):
                    ctx = ssl.create_default_context()
                    ctx.load_verify_locations(cert_path)
                    return ctx

        # For non-macOS or if no cert found, use default
        return None

    async def async_check_status(self, debug=False) -> bool:
        """Enhanced async status check with proper SSL handling"""
        if debug:
            print("\nDEBUG OpenAI: Starting async status check")
            print(f"DEBUG OpenAI: Using API URL: {self.api_url}")
            print(f"DEBUG OpenAI: API key status: {'Present' if self.api_key else 'Missing'}")
            if self.ssl_context:
                print("DEBUG OpenAI: Using custom SSL context")
            else:
                print("DEBUG OpenAI: Using default SSL context")

        if not self.api_key:
            if debug:
                print("DEBUG OpenAI: Cannot proceed without API key")
            return False

        try:
            connector = None
            if self.ssl_context:
                connector = aiohttp.TCPConnector(ssl=self.ssl_context)

            timeout = aiohttp.ClientTimeout(total=10)  # Increased timeout
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                if debug:
                    print("DEBUG OpenAI: Testing API key validity with models endpoint")

                async with session.get(f"{self.api_url}/models", headers=headers) as response:
                    if debug:
                        print(f"DEBUG OpenAI: Models endpoint response status: {response.status}")
                        if response.status != 200:
                            text = await response.text()
                            print(f"DEBUG OpenAI: Error response: {text}")

                    return response.status == 200

        except aiohttp.ClientError as e:
            if debug:
                print(f"DEBUG OpenAI: Connection error: {str(e)}")
            return False
        except asyncio.TimeoutError:
            if debug:
                print("DEBUG OpenAI: Request timed out")
            return False
        except Exception as e:
            if debug:
                print(f"DEBUG OpenAI: Unexpected error: {str(e)}")
                import traceback
                print("DEBUG OpenAI: Full traceback:")
                traceback.print_exc()
            return False

    def get_available_models(self) -> List[str]:
        """Get list of available models with enhanced error handling"""
        if not self.api_key:
            return self.available_models

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.get(
                f"{self.api_url}/models",
                headers=headers,
                timeout=5.0
            )

            if response.status_code == 200:
                models = response.json()
                chat_models = [
                    model['id'] for model in models['data']
                    if any(preferred in model['id'] for preferred in ['gpt-4', 'gpt-3.5'])
                ]
                return chat_models if chat_models else self.available_models
            elif response.status_code == 401:
                print("OpenAI API key is invalid or expired")
                return self.available_models
            else:
                return self.available_models

        except requests.exceptions.RequestException:
            return self.available_models

    def check_status(self) -> bool:
        if not self.api_key:
            return False

        available_models = self.get_available_models()
        if available_models:
            self.current_model = self.select_best_model(available_models)
            return True
        return False

    def get_model_info(self) -> Optional[str]:
        return self.current_model

    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response with proper SSL handling"""
        if not self.current_model:
            raise Exception("No model selected")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=10,
                verify=True if not self.ssl_context else False
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._parse_llm_response(content)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            print("\nDEBUG: Making request to OpenAI API...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")

            # Mask the API key in debug output
            debug_headers = headers.copy()
            debug_headers["Authorization"] = "Bearer ***"
            print(f"DEBUG: Request headers: {json.dumps(debug_headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")

            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")

            response.raise_for_status()
            response_json = response.json()

            # Only log essential parts of the response
            debug_response = {
                'choices': [{
                    'message': response_json['choices'][0]['message']
                }],
                'usage': response_json['usage']
            }
            print(f"DEBUG: Response (truncated): {json.dumps(debug_response, indent=2)}")

            content = response_json["choices"][0]["message"]["content"]
            print(f"\nDEBUG: Raw content before parsing: {content}")

            # Check for special characters using the base class method
            char_analysis = self._check_special_characters(content)
            print("\nDEBUG: Content analysis:")
            for key, value in char_analysis.items():
                print(f"DEBUG: {key}: {value}")

            # Handle markdown code blocks
            if char_analysis["starts_with_markdown"] and char_analysis["ends_with_markdown"]:
                print("DEBUG: Detected markdown code block, cleaning...")
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
                content = content.strip()
                print("DEBUG: Content after markdown cleanup:", content)

            try:
                # Try parsing as JSON first
                print("\nDEBUG: Attempting JSON parse...")
                json_data = json.loads(content)
                if isinstance(json_data, list):
                    print("DEBUG: Successfully parsed as JSON array")
                    parsed = [str(cmd) for cmd in json_data]
                else:
                    raise ValueError("JSON data is not an array")
            except json.JSONDecodeError as e:
                print("DEBUG: JSON parse failed:", str(e))
                print("DEBUG: Falling back to manual parsing...")
                # Manual parsing as fallback
                if content.startswith('[') and content.endswith(']'):
                    content = content[1:-1]
                    import re
                    parsed = re.findall(r'"([^"]*)"', content)
                else:
                    raise Exception("Content is not in expected format")

            print("\nDEBUG: Final parsed commands:", json.dumps(parsed, indent=2))
            return parsed

        except Exception as e:
            print("\nDEBUG: Error occurred:", str(e))
            if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response'):
                print("DEBUG: Full response text:", e.response.text)
            import traceback
            print("DEBUG: Full traceback:", traceback.print_exc())
            raise Exception(f"Error generating response: {str(e)}")


class GroqProvider(LLMProvider):
    """Groq implementation of LLM provider using their OpenAI-compatible API"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
        self.api_key = os.environ.get('GROQ_API_KEY')
        self.api_url = "https://api.groq.com/openai/v1"
        self.current_model = None

    def get_available_models(self) -> List[str]:
        """Fetch available models from Groq API"""
        if not self.api_key:
            return []

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.get(f"{self.api_url}/models", headers=headers)
            response.raise_for_status()

            models_data = response.json()
            # Filter to get only text models (exclude whisper and vision models)
            text_models = [
                model["id"] for model in models_data["data"]
                if not any(x in model["id"].lower() for x in ["whisper", "vision"]) and model["active"]
            ]

            # Sort to ensure newer models appear first
            text_models.sort(reverse=True)
            return text_models

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Groq models: {str(e)}")
            return []
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Groq models response: {str(e)}")
            return []

    def check_status(self) -> bool:
        """Check if the provider is available and ready"""
        if not self.api_key:
            return False

        try:
            models = self.get_available_models()
            if models:
                self.current_model = self.select_best_model(models)
                return True
            return False
        except Exception:
            return False

    def get_model_info(self) -> Optional[str]:
        """Get information about the currently loaded model"""
        return self.current_model

    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response from the model"""
        if not self.current_model:
            raise Exception("No model selected")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]

            # Handle markdown code blocks
            if content.startswith('```') and content.endswith('```'):
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
            content = content.strip()

            return self._parse_llm_response(content)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to Groq API: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Error parsing Groq response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            print("\nDEBUG: Making request to Groq API...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")

            # Mask the API key in debug output
            debug_headers = headers.copy()
            debug_headers["Authorization"] = "Bearer ***"
            print(f"DEBUG: Request headers: {json.dumps(debug_headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")

            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {json.dumps(dict(response.headers), indent=2)}")

            response.raise_for_status()
            response_json = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")

            content = response_json["choices"][0]["message"]["content"]
            print("\nDEBUG: Raw content before parsing:", content)

            # Check for special characters using the base class method
            char_analysis = self._check_special_characters(content)
            print("\nDEBUG: Content analysis:")
            for key, value in char_analysis.items():
                print(f"DEBUG: {key}: {value}")

            # Handle markdown code blocks
            if char_analysis["starts_with_markdown"] and char_analysis["ends_with_markdown"]:
                print("DEBUG: Detected markdown code block, cleaning...")
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
                content = content.strip()
                print("DEBUG: Content after markdown cleanup:", content)

            try:
                # Try parsing as JSON first
                print("\nDEBUG: Attempting JSON parse...")
                json_data = json.loads(content)
                if isinstance(json_data, list):
                    print("DEBUG: Successfully parsed as JSON array")
                    parsed = [str(cmd) for cmd in json_data]
                else:
                    raise ValueError("JSON data is not an array")
            except json.JSONDecodeError as e:
                print("DEBUG: JSON parse failed:", str(e))
                print("DEBUG: Falling back to manual parsing...")
                # Manual parsing as fallback
                if content.startswith('[') and content.endswith(']'):
                    content = content[1:-1]
                    import re
                    parsed = re.findall(r'"([^"]*)"', content)
                else:
                    raise Exception("Content is not in expected format")

            print("\nDEBUG: Final parsed commands:", json.dumps(parsed, indent=2))
            return parsed

        except Exception as e:
            print("\nDEBUG: Error occurred:", str(e))
            if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response'):
                print("DEBUG: Full response text:", e.response.text)
            import traceback
            print("DEBUG: Full traceback:", traceback.format_exc())
            raise Exception(f"Error generating response: {str(e)}")


class GrokProvider(LLMProvider):
    """Grok implementation of LLM provider using their API"""

    def __init__(self, debug: bool = False):
        super().__init__(debug=debug)
        self.api_key = os.environ.get('GROK_API_KEY')
        self.api_url = "https://api.x.ai/v1"
        self.current_model = None

    def get_available_models(self) -> List[str]:
        """Fetch available models from Grok API"""
        if not self.api_key:
            return []

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # Use the correct endpoint for fetching models
            response = requests.get(f"{self.api_url}/language-models", headers=headers)
            response.raise_for_status()

            models_data = response.json()
            # Extract only the model IDs
            return [model['id'] for model in models_data['models']]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Grok models: {str(e)}")
            return []
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Grok models response: {str(e)}")
            return []

    def check_status(self) -> bool:
        """Check if the provider is available and ready"""
        if not self.api_key:
            return False

        try:
            models = self.get_available_models()
            if models:
                self.current_model = self.select_best_model(models)
                return True
            return False
        except Exception:
            return False

    def get_model_info(self) -> Optional[str]:
        """Get information about the currently loaded model"""
        return self.current_model

    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response with proper SSL handling"""
        if not self.current_model:
            raise Exception("No model selected")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._parse_llm_response(content)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            print("\nDEBUG: Making request to Grok (using OpenAI API standard)...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")

            # Mask the API key in debug output
            debug_headers = headers.copy()
            debug_headers["Authorization"] = "Bearer ***"
            print(f"DEBUG: Request headers: {json.dumps(debug_headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")

            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")

            response.raise_for_status()
            response_json = response.json()

            # Only log essential parts of the response
            debug_response = {
                'choices': [{
                    'message': response_json['choices'][0]['message']
                }],
                'usage': response_json['usage']
            }
            print(f"DEBUG: Response (truncated): {json.dumps(debug_response, indent=2)}")

            content = response_json["choices"][0]["message"]["content"]
            print(f"\nDEBUG: Raw content before parsing: {content}")

            # Check for special characters using the base class method
            char_analysis = self._check_special_characters(content)
            print("\nDEBUG: Content analysis:")
            for key, value in char_analysis.items():
                print(f"DEBUG: {key}: {value}")

            # Handle markdown code blocks
            if char_analysis["starts_with_markdown"] and char_analysis["ends_with_markdown"]:
                print("DEBUG: Detected markdown code block, cleaning...")
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
                content = content.strip()
                print("DEBUG: Content after markdown cleanup:", content)

            try:
                # Try parsing as JSON first
                print("\nDEBUG: Attempting JSON parse...")
                json_data = json.loads(content)
                if isinstance(json_data, list):
                    print("DEBUG: Successfully parsed as JSON array")
                    parsed = [str(cmd) for cmd in json_data]
                else:
                    raise ValueError("JSON data is not an array")
            except json.JSONDecodeError as e:
                print("DEBUG: JSON parse failed:", str(e))
                print("DEBUG: Falling back to manual parsing...")
                # Manual parsing as fallback
                if content.startswith('[') and content.endswith(']'):
                    content = content[1:-1]
                    import re
                    parsed = re.findall(r'"([^"]*)"', content)
                else:
                    raise Exception("Content is not in expected format")

            print("\nDEBUG: Final parsed commands:", json.dumps(parsed, indent=2))
            return parsed

        except Exception as e:
            print("\nDEBUG: Error occurred:", str(e))
            if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response'):
                print("DEBUG: Full response text:", e.response.text)
            import traceback
            print("DEBUG: Full traceback:", traceback.print_exc())
            raise Exception(f"Error generating response: {str(e)}")


# ==================================================
# File: qq.py
# ==================================================
#!/usr/bin/env python3
# qq.py

import sys
import argparse
import json
import os
from rich.console import Console
from rich.panel import Panel
import time
import asyncio
if sys.platform != 'win32':
    import termios
    import tty

import subprocess
from rich import box
from rich.text import Text
from rich.terminal_theme import TerminalTheme
from typing import List, Type
from pathlib import Path
from datetime import datetime
from quickquestion.llm_provider import (
    LLMProvider,
    LMStudioProvider,
    OllamaProvider,
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider,
    GrokProvider
)
from quickquestion.settings_manager import SettingsManager, get_settings
from quickquestion.utils import getch
from quickquestion.utils import clear_screen
from quickquestion.cache import provider_cache
from quickquestion.utils import enable_debug_printing, disable_debug_printing
from quickquestion.ui_library import UIOptionDisplay


class QuickQuestion:
    # In QuickQuestion.__init__
    def __init__(self, debug=False, settings=None):
        self.console = Console()
        self.debug = debug
        self.history_file = Path.home() / '.qq_history.json'
        self.settings = settings or get_settings(debug=debug)

        # Show loading only if needed
        if not debug:
            with self.console.status("[bold blue]Initializing...[/bold blue]", spinner="dots"):
                self.providers = self._get_cached_or_new_providers()
        else:
            self.providers = self._get_cached_or_new_providers()

        if not self.providers:
            self.console.print("[red]Error: No LLM providers available")
            self.console.print("[yellow]Please make sure either LM Studio or Ollama is running")
            sys.exit(1)

        # Set the provider based on settings
        default_provider = self.settings["default_provider"]
        self.provider = next(
            (p for p in self.providers
            if self.get_provider_name(p) == default_provider),
            self.providers[0]
        )

    def _get_cached_or_new_providers(self) -> List[LLMProvider]:
        """Get providers from cache or initialize new ones"""
        # First check the cache
        cached_providers = provider_cache.get('available_providers')
        if cached_providers is not None:
            if self.debug:
                cache_info = provider_cache.get_cache_info()
                print("\nDEBUG: Using cached providers")
                print(f"DEBUG: Cache age: {cache_info['available_providers']['age_seconds']:.1f} seconds")
                print(f"DEBUG: Cache expires in: {cache_info['available_providers']['expires_in_seconds']:.1f} seconds")
                for p in cached_providers:
                    print(f"DEBUG: Cached provider: {self.get_provider_name(p)}")
                    if hasattr(p, 'current_model'):
                        print(f"DEBUG: Provider model: {p.current_model}")
            return cached_providers

        if self.debug:
            print("\nDEBUG: No valid cache found, checking providers")

        # If no cache, do the full provider check
        providers = self._get_available_providers()

        # Cache the results if we found any providers
        if providers:
            if self.debug:
                print("\nDEBUG: Caching newly found providers:")
                for p in providers:
                    print(f"DEBUG: Caching provider: {self.get_provider_name(p)}")
                    if hasattr(p, 'current_model'):
                        print(f"DEBUG: Provider model: {p.current_model}")
            provider_cache.set('available_providers', providers)

        return providers

    def debug_print(self, message: str, data: any = None):
        """Print debug information if debug mode is enabled"""
        if self.debug:
            self.console.print(f"[cyan]DEBUG: {message}[/cyan]")
            if data is not None:
                if isinstance(data, (dict, list)):
                    self.console.print(Panel(
                        json.dumps(data, indent=2),
                        title="Debug Data",
                        border_style="cyan"
                    ))
                else:
                    self.console.print(Panel(
                        str(data),
                        title="Debug Data",
                        border_style="cyan"
                    ))

    def is_cloud_provider(self, provider: LLMProvider) -> bool:
        """Check if the provider is cloud-based"""
        return isinstance(provider, (OpenAIProvider, AnthropicProvider))

    def get_provider_name(self, provider=None) -> str:
        """Get the friendly name of the provider"""
        provider = provider or self.provider
        if isinstance(provider, OpenAIProvider):
            return "OpenAI"
        elif isinstance(provider, LMStudioProvider):
            return "LM Studio"
        elif isinstance(provider, OllamaProvider):
            return "Ollama"
        elif isinstance(provider, AnthropicProvider):
            return "Anthropic"
        elif isinstance(provider, GroqProvider):
            return "Groq"
        elif isinstance(provider, GrokProvider):
            return "Grok"
        return "Unknown Provider"

    def get_provider_type_message(self) -> str:
        """Get the provider type message with appropriate color"""
        return "[red]Cloud Based Provider[/red]" if self.is_cloud_provider(self.provider) else "[green]Local Provider[/green]"

    def print_banner(self):
        """Print the banner using UI library"""
        ui = UIOptionDisplay(self.console, debug=self.debug)
        
        # Check configured provider
        default_provider = self.settings['default_provider']
        provider_available = any(self.get_provider_name(p) == default_provider for p in self.providers)
        
        # Create subtitle lines
        subtitle = []
        
        if provider_available:
            subtitle.append(f"[yellow]Provider: {default_provider}[/yellow]")
        else:
            fallback_provider = self.get_provider_name()
            subtitle.append(f"[red]Provider: {default_provider} (Not Available) → Using: {fallback_provider}[/red]")
        
        subtitle.append(self.get_provider_type_message())
        subtitle.append(f"[yellow]Command Action: {self.settings.get('command_action', 'Run Command')}[/yellow]")
        
        ui.display_banner(
            "Quick Question",
            subtitle=subtitle,
            website="https://southbrucke.com"
        )

    def load_history(self) -> List[dict]:
        """Load command history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_to_history(self, command: str, question: str):
        """Save command to history with timestamp and question"""
        history = self.load_history()
        history.append({
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'question': question
        })
        # Keep only last 100 commands
        history = history[-100:]

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def display_history(self):
        """Display command history with interactive selection"""
        history = self.load_history()
        if not history:
            self.console.print("[yellow]No command history found[/yellow]")
            return

        selected = 0
        # Get last 10 entries in reverse order
        entries = list(reversed(history[-10:]))

        def render_screen():
            if not self.debug:  # Only clear screen if not in debug mode
                clear_screen()
            self.print_banner()
            self.console.print("[bold]Command History:[/bold]\n")

            # Show instructions
            self.console.print("\n[dim]↑/↓ to select, Enter to execute, [/dim][red]q[/red][dim] to cancel[/dim]\n")

            # Display each history entry
            for i, entry in enumerate(entries):
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
                style = "bold white on blue" if i == selected else "blue"
                self.console.print(
                    Panel(
                        f"[dim]{timestamp}[/dim]\nQ: {entry['question']}\n[green]$ {entry['command']}[/green]",
                        title=f"Entry {i + 1}",
                        border_style=style
                    )
                )

            # Add cancel option
            cancel_style = "bold white on red" if selected == len(entries) else "red"
            self.console.print(Panel("Cancel", title="Exit", border_style=cancel_style))

        while True:
            render_screen()
            c = self.getch()
            if self.debug:
                print(f"\nDEBUG UI - Received key: {repr(c)}")

            # Simple arrow key handling
            if c == '\x1b[A':  # Up arrow
                if self.debug:
                    print(f"DEBUG UI - Up arrow - Current selection: {selected}")
                if selected > 0:
                    selected -= 1
                    if self.debug:
                        print(f"DEBUG UI - New selection: {selected}")

            elif c == '\x1b[B':  # Down arrow
                if self.debug:
                    print(f"DEBUG UI - Down arrow - Current selection: {selected}")
                if selected < len(entries):
                    selected += 1
                    if self.debug:
                        print(f"DEBUG UI - New selection: {selected}")

            elif c == '\r':  # Enter key
                if selected == len(entries):  # If cancel is selected
                    clear_screen()
                    sys.exit(0)
                else:
                    clear_screen()
                    self.print_banner()
                    selected_entry = entries[selected]
                    command = selected_entry['command']
                    self.console.print(f"\n[green]Executing command:[/green] {command}")
                    # Don't add to history again since it's already there
                    subprocess.run(command, shell=True)
                    break

            elif c == 'q':  # Quick exit
                clear_screen()
                sys.exit(0)

    def display_help(self):
        """Display help information"""
        clear_screen()
        self.print_banner()

        help_text = """[bold white]Usage:[/bold white]
        qq "your question here"    Ask for command suggestions
        qq --history              Show command history
        qq --settings            Configure application settings
        qq --debug               Enable debug mode

    [bold white]Examples:[/bold white]
        qq "how to find files containing text"
        qq "show running processes"
        qq "check disk space"

    [bold white]Navigation:[/bold white]
        ↑/↓ arrows               Select options
        Enter                    Execute/Select
        q                        Quit/Cancel

    [bold white]Current Configuration:[/bold white]
        Provider: [green]{provider}[/green]
        Action: [green]{action}[/green]
        Model: [green]{model}[/green]

    For more information, visit: [blue]https://southbrucke.com[/blue]
    """.format(
            provider=self.get_provider_name(),
            action=self.settings.get('command_action', 'Run Command'),
            model=self.provider.get_model_info() or 'Not Set'
        )

        self.console.print(Panel(
            help_text,
            title="Quick Question Help",
            border_style="blue",
            expand=False
        ))

    def generate_prompt(self, question: str) -> str:
        os_type = "Windows" if sys.platform == "win32" else "macOS"
        return f"""You are a helpful command-line expert. Provide exactly 3 different command-line solutions for the following question: {question}

    Rules:
    1. Provide exactly 3 command options
    2. Each command must be a single line
    3. Do not provide explanations
    4. Format the response as a JSON array with 3 strings
    5. Focus on {os_type} terminal commands
    6. Keep commands concise and practical

    Example response format:
    ["command1", "command2", "command3"]"""

    def get_command_suggestions(self, question: str) -> List[str]:
        clear_screen()
        self.print_banner()

        current_model = self.provider.get_model_info()
        if current_model:
            self.console.print(f"[green]Using model: {current_model}")

        try:
            prompt = self.generate_prompt(question)
            self.debug_print("Generated prompt:", prompt)

            # Create and start the spinner
            with self.console.status(
                "[bold blue]Thinking...[/bold blue]",
                spinner="dots",
                spinner_style="blue"
            ):
                raw_response = self.provider.generate_response_with_debug(prompt) if self.debug else self.provider.generate_response(prompt)

                if self.debug:
                    self.debug_print("Raw LLM response:", raw_response)

                return raw_response

        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}")
            if self.debug:
                import traceback
                self.debug_print("Full traceback:", traceback.format_exc())
            self.console.print("[yellow]Please make sure your LLM provider is running and configured correctly.")
            sys.exit(1)

    def getch(self):
        return getch(debug=self.debug)

    async def _check_providers_async(self) -> List[LLMProvider]:
        """Async provider checking with enhanced debugging"""
        available_providers = []
        default_model = self.settings.get('default_model')

        if self.debug:
            print("\nDEBUG: Starting async provider checks")
            print(f"DEBUG: Default model from settings: {default_model}")

        # Check cache first
        cached_providers = provider_cache.get('available_providers')
        if cached_providers is not None:
            if self.debug:
                print("DEBUG: Using cached providers")
                for p in cached_providers:
                    print(f"DEBUG: Cached provider: {self.get_provider_name(p)}")
            return cached_providers

        # Create all provider instances
        providers = [
            LMStudioProvider(),
            OllamaProvider(),
            OpenAIProvider(),
            AnthropicProvider(),
            GroqProvider(),
            GrokProvider()
        ]

        if self.debug:
            print("\nDEBUG: Created provider instances")
            for p in providers:
                print(f"DEBUG: Initialized {p.__class__.__name__}")

        # Check all providers concurrently
        async def check_provider(provider):
            if self.debug:
                print(f"\nDEBUG: Checking {provider.__class__.__name__}")

            if await provider.async_check_status(debug=self.debug):
                if self.debug:
                    print(f"DEBUG: {provider.__class__.__name__} is available")

                if default_model and self.get_provider_name(provider) == self.settings['default_provider']:
                    provider.current_model = default_model
                    if self.debug:
                        print(f"DEBUG: Set default model to {default_model}")
                return provider

            if self.debug:
                print(f"DEBUG: {provider.__class__.__name__} is not available")
            return None

        if self.debug:
            print("\nDEBUG: Starting concurrent provider checks")

        # Run all checks concurrently
        tasks = [check_provider(p) for p in providers]
        results = await asyncio.gather(*tasks)

        if self.debug:
            print("\nDEBUG: Completed concurrent provider checks")

        # Filter out None results
        available_providers = [p for p in results if p is not None]

        if self.debug:
            print(f"\nDEBUG: Found {len(available_providers)} available providers:")
            for p in available_providers:
                print(f"DEBUG: - {self.get_provider_name(p)}")

        # Cache the results
        provider_cache.set('available_providers', available_providers)

        if self.debug:
            print("\nDEBUG: Cached available providers")
            if not available_providers:
                print("\nDEBUG: No providers available")
                print("DEBUG: Please ensure either LM Studio or Ollama is running")
                print("DEBUG: LM Studio should be running on http://localhost:1234")
                print("DEBUG: Ollama should be running on http://localhost:11434")

        return available_providers

    def _get_available_providers(self) -> List[LLMProvider]:
        """Get available providers with enhanced caching"""
        if self.debug:
            print("\nDEBUG: Starting provider initialization")

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            providers = loop.run_until_complete(self._check_providers_async())
            loop.close()

            # Cache the results if we found any providers
            if providers:
                provider_cache.set('available_providers', providers)
                if self.debug:
                    print("\nDEBUG: Cached new provider configuration")
                    cache_info = provider_cache.get_cache_info()
                    print(f"DEBUG: Cache will expire in: {cache_info['available_providers']['expires_in_seconds']} seconds")

            return providers

        except Exception as e:
            if self.debug:
                print(f"\nDEBUG: Error checking providers: {str(e)}")
                import traceback
                print("DEBUG: Full traceback:")
                traceback.print_exc()
            return []

    def display_suggestions(self, suggestions: List[str], question: str):
        """Display command suggestions using the enhanced UI library"""
        ui = UIOptionDisplay(self.console, debug=self.debug)

        # Format header panels with provider info
        provider_type = "Cloud Based Provider" if self.is_cloud_provider(self.provider) else "Local Provider"
        provider_info = self.get_provider_name()
        current_model = self.provider.get_model_info()
        
        header_panels = [
            {
                'title': 'Provider Info',
                'content':
                    f"Type: [{'red' if self.is_cloud_provider(self.provider) else 'green'}]{provider_type}[/]\n"
                    f"Provider: [yellow]{provider_info}[/yellow]\n"
                    f"Model: [blue]{current_model or 'Not Set'}[/blue]"
            },
            {
                'title': 'Question',
                'content': f"[italic]{question}[/italic]"
            }
        ]

        # Prepare options data
        options = [f"Option {i + 1}" for i in range(len(suggestions))]
        panel_titles = [f"Command {i + 1}" for i in range(len(suggestions))]
        
        # Format the command display with syntax highlighting
        def format_command(cmd: str) -> str:
            return f"[green]$ {cmd}[/green]"
        
        extra_content = [format_command(cmd) for cmd in suggestions]

        while True:
            selected, action = ui.display_options(
                options=options,
                panel_titles=panel_titles,
                extra_content=extra_content,
                header_panels=header_panels,
                show_cancel=True,
                formatter=lambda x: x  # Simple pass-through formatter
            )

            if action in ('quit', 'cancel'):
                clear_screen()
                sys.exit(0)

            if action == 'select':
                clear_screen()
                ui.display_banner("Quick Question",
                    ["Command execution"],
                    website="https://southbrucke.com")

                selected_command = suggestions[selected]

                # Check command action setting
                if self.settings.get('command_action') == 'Copy Command':
                    try:
                        copy_to_clipboard(selected_command)
                        ui.display_message(
                            f"Command copied to clipboard:\n[green]{selected_command}[/green]",
                            style="blue",
                            title="Success",
                            pause=True
                        )
                        # Save to history before exiting
                        self.save_to_history(selected_command, question)
                        sys.exit(0)
                    except Exception as e:
                        ui.display_message(
                            f"Error copying to clipboard: {str(e)}",
                            style="red",
                            title="Error",
                            pause=True
                        )
                        sys.exit(1)
                else:
                    self.console.print(f"\n[green]Executing command:[/green] {selected_command}")
                    # Save to history before executing
                    self.save_to_history(selected_command, question)
                    subprocess.run(selected_command, shell=True)
                    break


def copy_to_clipboard(text: str):
    """Cross-platform clipboard copy"""
    try:
        import pyperclip
        pyperclip.copy(text)
    except ImportError:
        if sys.platform == 'darwin':
            subprocess.run('pbcopy', input=text.encode(), env={'LANG': 'en_US.UTF-8'})
        elif sys.platform == 'win32':
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
            win32clipboard.CloseClipboard()


def main():
    """Entry point for Quick Question"""
    parser = argparse.ArgumentParser(description="Quick Question - Command Line Suggestions")
    parser.add_argument("question", nargs="*", help="Your command-line question")
    parser.add_argument("--settings", action="store_true", help="Open settings menu")
    parser.add_argument("--history", action="store_true", help="Show command history")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the provider cache")
    parser.add_argument("--dev", action="store_true", help="Enter developer mode")

    args = parser.parse_args()

    if args.debug:
        enable_debug_printing()

    if args.clear_cache:
        provider_cache.clear()
        print("Cache cleared successfully")
        return

    # Only show loading message if not in debug mode and not in dev mode
    if not args.debug and not args.dev:
        print("Loading Quick Question...")

    if args.settings:
        SettingsManager(debug=args.debug, clear_cache=True).display_settings_ui()
        return
    
    if args.dev:
        from quickquestion.dev_mode import DevMode
        DevMode(debug=args.debug).display_menu()
        return

    # Pass clear_cache=False for normal operation
    settings_manager = SettingsManager(debug=args.debug, clear_cache=False)
    settings = settings_manager.load_settings()

    qq = QuickQuestion(debug=args.debug, settings=settings)

    try:
        if args.history:
            qq.display_history()
            return

        if not args.question:
            # Show help if no arguments provided
            qq.display_help()
        else:
            question = " ".join(args.question)
            suggestions = qq.get_command_suggestions(question)
            qq.display_suggestions(suggestions, question)
    finally:
        if args.debug:
            disable_debug_printing()


if __name__ == "__main__":
    main()


# ==================================================
# File: settings_manager.py
# ==================================================
# settings_manager.py

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from quickquestion.ui_library import UIOptionDisplay
from quickquestion.llm_provider import (
    LLMProvider,
    LMStudioProvider,
    OllamaProvider,
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider,
    GrokProvider
)
from quickquestion.utils import clear_screen
from quickquestion.cache import get_provider_cache


class SettingsManager:
    def __init__(self, debug=False, clear_cache=False):
        self.console = Console()
        self.settings_file = Path.home() / '.qq_settings.json'
        self.debug = debug
        self.ui = UIOptionDisplay(self.console, debug=debug)

        # Define default settings
        self.default_settings = {
            "default_provider": "LM Studio",
            "provider_options": ["LM Studio", "Ollama", "OpenAI", "Anthropic", "Groq", "Grok"],
            "command_action": "Run Command",
            "command_action_options": ["Run Command", "Copy Command"],
            "default_model": None,
            "available_models": []
        }

        # Get cache with debug mode
        self.provider_cache = get_provider_cache(debug=debug)

        # Only clear cache if explicitly requested
        if clear_cache:
            if self.debug:
                print("DEBUG Settings: Clearing provider cache")
            self.provider_cache.clear('available_providers')

    def debug_print(self, message: str, data: Any = None):
        """Print debug information if debug mode is enabled"""
        if self.debug:
            print(f"DEBUG Settings: {message}")
            if data is not None:
                if isinstance(data, (dict, list)):
                    print(f"DEBUG Settings: Data = {json.dumps(data, indent=2)}")
                else:
                    print(f"DEBUG Settings: Data = {str(data)}")

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults if no file exists"""
        settings = self.default_settings.copy()
        self.debug_print("Loading settings")

        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)

                # Check if there are new provider options to add
                if "provider_options" in saved_settings:
                    new_providers = [p for p in self.default_settings["provider_options"]
                                   if p not in saved_settings["provider_options"]]
                    if new_providers:
                        self.debug_print(f"Adding new providers: {new_providers}")
                        saved_settings["provider_options"].extend(new_providers)
                        # Save the updated settings back to file
                        with open(self.settings_file, 'w') as f:
                            json.dump(saved_settings, f, indent=2)

                settings.update(saved_settings)
                self.debug_print("Loaded settings", settings)

            except json.JSONDecodeError as e:
                self.debug_print(f"Error loading settings: {str(e)}")
                return self.default_settings

        return settings

    def get_provider_instance(self, provider_name: str) -> Optional[LLMProvider]:
        """Create a provider instance based on name"""
        self.debug_print(f"Creating provider instance for {provider_name}")
        provider_map = {
            "LM Studio": LMStudioProvider,
            "Ollama": OllamaProvider,
            "OpenAI": OpenAIProvider,
            "Anthropic": AnthropicProvider,
            "Groq": GroqProvider,
            "Grok": GrokProvider
        }
        provider_class = provider_map.get(provider_name)
        if provider_class:
            return provider_class(debug=self.debug)
        return None

    def update_available_models(self, settings: dict, provider_name: str):
        """Update available models list for the selected provider"""
        self.debug_print(f"Updating available models for {provider_name}")
        
        with self.ui.display_loading(f"Checking available models for {provider_name}..."):
            provider = self.get_provider_instance(provider_name)
            if provider and provider.check_status():
                models = provider.get_available_models()
                self.debug_print("Found models", models)
                settings["available_models"] = models
                if not settings["default_model"] or settings["default_model"] not in models:
                    settings["default_model"] = provider.select_best_model(models)
                    self.debug_print(f"Selected default model: {settings['default_model']}")
            else:
                self.debug_print("No models available")
                settings["available_models"] = []
                settings["default_model"] = None

    def display_settings_ui(self):
        """Display interactive settings UI using the enhanced UI library"""
        settings = self.load_settings()
        editing_mode = False
        
        self.debug_print("Starting settings UI display")
        
        # Display banner
        self.ui.display_banner(
            "Quick Question Settings",
            ["Configure your Quick Question preferences"],
            website="https://southbrucke.com"
        )

        while True:
            # Prepare settings data for display
            settings_data = [
                {
                    'title': "Default LLM Provider",
                    'content': {
                        'current': settings['default_provider'],
                        'options': settings['provider_options'],
                        'selected_index': settings['provider_options'].index(settings['default_provider'])
                    }
                },
                {
                    'title': "Default Model",
                    'content': {
                        'current': settings.get('default_model', 'Not Set'),
                        'options': settings['available_models'],
                        'selected_index': (
                            settings['available_models'].index(settings['default_model'])
                            if settings.get('default_model') in settings.get('available_models', [])
                            else 0
                        ),
                        'error': 'No models available for selected provider' if not settings['available_models'] else None
                    }
                },
                {
                    'title': "Command Action",
                    'content': {
                        'current': settings['command_action'],
                        'options': settings['command_action_options'],
                        'selected_index': settings['command_action_options'].index(settings['command_action'])
                    }
                }
            ]

            # Prepare UI elements
            options = ['Edit Provider', 'Edit Model', 'Edit Action', 'Save Changes', 'Cancel']
            panel_titles = ["Provider Settings", "Model Settings", "Action Settings", "Save", "Cancel"]
            
            # Format panel content
            extra_content = []
            current_editing = self.ui.state.selected_index if editing_mode else None
            
            for i, setting in enumerate(settings_data[:3]):
                is_editing = editing_mode and current_editing == i
                if self.debug:
                    self.debug_print(f"Formatting panel {i}", {
                        "setting": setting['title'],
                        "editing": is_editing,
                        "current_editing": current_editing
                    })
                
                content = self.ui.format_panel_content(
                    content=setting['content'],
                    editing_mode=is_editing,
                    error=setting['content'].get('error')
                )
                
                if i == current_editing:
                    # When editing, show the available options
                    options_list = setting['content']['options']
                    selected_idx = self.ui.state.selected_value_index
                    content = self.ui.format_panel_content(
                        content=f"Edit {setting['title']}",
                        options=options_list,
                        selected_index=selected_idx,
                        current_value=setting['content']['current'],
                        editing_mode=True,
                        error=setting['content'].get('error')
                    )
                extra_content.append(content)
            
            # Add content for Save and Cancel options
            extra_content.extend([
                "Save and apply all changes",
                "Exit without saving"
            ])

            # Display options
            selected, action = self.ui.display_options(
                options=options,
                panel_titles=panel_titles,
                extra_content=extra_content,
                show_cancel=False,
                editing_mode=editing_mode
            )

            self.debug_print("UI action", {"selected": selected, "action": action})

            if action == 'quit':
                if editing_mode:
                    self.debug_print("Exiting edit mode")
                    editing_mode = False
                    continue
                self.debug_print("Exiting settings")
                clear_screen()
                return

            if editing_mode:
                current_setting = settings_data[selected]
                options_list = current_setting['content']['options']
                
                if action == 'left' and self.ui.state.selected_value_index > 0:
                    self.ui.state.set_value_selection(self.ui.state.selected_value_index - 1)
                elif action == 'right' and self.ui.state.selected_value_index < len(options_list) - 1:
                    self.ui.state.set_value_selection(self.ui.state.selected_value_index + 1)
                elif action == 'select':
                    self.debug_print("Applying setting change", {
                        "setting": current_setting['title'],
                        "value_index": self.ui.state.selected_value_index
                    })
                    
                    if selected == 0:  # Provider
                        new_provider = settings['provider_options'][self.ui.state.selected_value_index]
                        if new_provider != settings['default_provider']:
                            settings['default_provider'] = new_provider
                            self.update_available_models(settings, new_provider)
                    elif selected == 1 and settings['available_models']:  # Model
                        settings['default_model'] = settings['available_models'][self.ui.state.selected_value_index]
                    elif selected == 2:  # Action
                        settings['command_action'] = settings['command_action_options'][self.ui.state.selected_value_index]
                    
                    editing_mode = False
                    self.ui.state.reset()

            else:  # Not editing
                if action == 'select':
                    if selected < 3:  # Editable options
                        self.debug_print(f"Entering edit mode for option {selected}")
                        editing_mode = True
                        current_setting = settings_data[selected]
                        self.ui.state.set_selection(selected)
                        self.ui.state.set_value_selection(current_setting['content']['selected_index'])
                    elif selected == 3:  # Save
                        self.debug_print("Saving settings")
                        self.save_settings(settings)
                        clear_screen()
                        self.ui.display_message(
                            "Settings saved successfully!",
                            style="green",
                            title="Success"
                        )
                        return
                    else:  # Cancel
                        self.debug_print("Canceling settings")
                        clear_screen()
                        return

    def save_settings(self, settings: Dict[str, Any]):
        """Save settings and update cache"""
        self.debug_print("Starting settings save")
        
        try:
            with self.ui.display_loading("Saving settings..."):
                # Save settings to file
                with open(self.settings_file, 'w') as f:
                    json.dump(settings, f, indent=2)
                self.debug_print("Saved settings to file", settings)

                # Initialize provider with new settings
                provider = self.get_provider_instance(settings["default_provider"])
                if provider and provider.check_status():
                    self.debug_print(f"Initializing new provider: {settings['default_provider']}")

                    # Update available models
                    models = provider.get_available_models()
                    if models:
                        settings["available_models"] = models
                        if not settings["default_model"] or settings["default_model"] not in models:
                            settings["default_model"] = provider.select_best_model(models)
                            provider.current_model = settings["default_model"]
                        
                        self.debug_print("Updated models", {
                            "provider": settings['default_provider'],
                            "model": settings['default_model'],
                            "available_models": models
                        })

                    # Update provider cache
                    providers = []
                    for provider_name in settings["provider_options"]:
                        try:
                            provider_instance = self.get_provider_instance(provider_name)
                            if provider_instance and provider_instance.check_status():
                                if provider_name == settings["default_provider"]:
                                    provider_instance.current_model = settings["default_model"]
                                providers.append(provider_instance)
                                self.debug_print(f"Added provider {provider_name} to cache")
                        except Exception as e:
                            self.debug_print(f"Error initializing provider {provider_name}: {str(e)}")

                    if providers:
                        self.debug_print(f"Caching {len(providers)} providers")
                        self.provider_cache.set('available_providers', providers)

        except Exception as e:
            self.debug_print(f"Error in save_settings: {str(e)}")
            self.ui.display_message(
                f"Error saving settings: {str(e)}",
                style="red",
                title="Error"
            )
            if self.debug:
                import traceback
                traceback.print_exc()


def get_settings(debug=False):
    """Helper function to get current settings"""
    return SettingsManager(debug=debug).load_settings()


# ==================================================
# File: ui_library.py
# ==================================================
# ui_library.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from typing import List, Optional, Tuple, Any, Dict, Union
import json
from .utils import getch, clear_screen


class UIStateManager:
    """Manages UI state and transitions"""
    def __init__(self):
        self.editing_mode = False
        self.selected_index = 0
        self.selected_value_index = 0
        
    def reset(self):
        self.editing_mode = False
        self.selected_index = 0
        self.selected_value_index = 0
        
    @property
    def is_editing(self) -> bool:
        return self.editing_mode
        
    def toggle_editing(self):
        self.editing_mode = not self.editing_mode
        
    def set_selection(self, index: int):
        self.selected_index = index
        
    def set_value_selection(self, index: int):
        self.selected_value_index = index


class UIOptionDisplay:
    """Enhanced UI component for displaying and managing interactive menus"""
    
    def __init__(self, console: Console, debug: bool = False):
        self.console = console
        self.debug = debug
        self.state = UIStateManager()
        
    def debug_print(self, message: str, data: Any = None):
        """Print debug information if debug mode is enabled"""
        if self.debug:
            if data is not None:
                if isinstance(data, (dict, list)):
                    print(f"DEBUG UI: {message}")
                    print(f"DEBUG UI: Data = {json.dumps(data, indent=2)}")
                else:
                    print(f"DEBUG UI: {message} - {str(data)}")
            else:
                print(f"DEBUG UI: {message}")

    def display_banner(self,
        title: str,
        subtitle: List[str] = None,
        website: str = None
    ):
        """Display a consistent banner across UI components"""
        self.debug_print("Displaying banner", {
            'title': title,
            'subtitle': subtitle,
            'website': website
        })
        
        website_text = Text.assemble(
            "",
            (f"({website})", "dim")
        ) if website else ""
        
        title_text = f"[purple]{title}[/purple]"
        if subtitle:
            title_text += "\n" + "\n".join(subtitle)
        if website:
            title_text += f"\n{website_text}"
            
        self.console.print(Panel(
            title_text,
            box=box.ROUNDED,
            style="white",
            expand=False
        ), end="")

    def display_loading(self, message: str = "Loading..."):
        """Display a loading spinner with message"""
        self.debug_print(f"Displaying loading spinner: {message}")
        return self.console.status(
            f"[bold blue]{message}[/bold blue]",
            spinner="dots",
            spinner_style="blue"
        )

    def format_panel_content(
        self,
        content: Union[str, Dict[str, Any]],
        current_value: Optional[str] = None,
        options: Optional[List[str]] = None,
        selected_index: Optional[int] = None,
        editing_mode: bool = False,
        error: Optional[str] = None
    ) -> str:
        """Format content for display in a panel"""
        self.debug_print("Formatting panel content", {
            'content_type': type(content).__name__,
            'editing_mode': editing_mode,
            'has_error': error is not None
        })
        
        formatted = []
        
        # Handle dictionary-style content
        if isinstance(content, dict):
            current = content.get('current', 'Not Set')
            current_options = content.get('options', [])
            current_index = content.get('selected_index', 0)
            
            formatted.append(f"Current: [green]{current}[/green]")
            
            if current_options and editing_mode:
                options_str = ", ".join(
                    f"[{'white on cyan' if i == current_index else 'white'}]{opt}[/]"
                    for i, opt in enumerate(current_options)
                )
                formatted.append(f"Available: {options_str}")
                
        # Handle direct content
        else:
            if current_value:
                formatted.append(f"Current: [green]{current_value}[/green]")
            
            formatted.append(str(content))
            
            if options and editing_mode:
                options_str = ", ".join(
                    f"[{'white on cyan' if i == selected_index else 'white'}]{opt}[/]"
                    for i, opt in enumerate(options)
                )
                formatted.append(f"Available: {options_str}")
        
        # Add error message if present
        if error:
            formatted.append(f"[red]{error}[/red]")
            
        return "\n".join(formatted)

    def display_message(
        self,
        message: str,
        style: str = "green",
        title: str = None,
        pause: bool = True
    ):
        """Display a message with optional pause"""
        self.debug_print("Displaying message", {
            'message': message,
            'style': style,
            'title': title,
            'pause': pause
        })
        
        self.console.print(Panel(
            message,
            title=title,
            border_style=style
        ))
        
        if pause:
            self.console.print("\nPress Enter to continue...")
            while True:
                c = getch(debug=self.debug)
                if c == '\r':
                    break

    def display_header_panels(
        self,
        panels: List[Dict[str, str]],
        title: str = "Summary",
        style: str = "blue"
    ):
        """Display header panels with structured content"""
        self.debug_print("Displaying header panels", {
            'num_panels': len(panels),
            'title': title
        })
        
        if not panels:
            return
            
        content = []
        for panel in panels:
            panel_title = panel.get('title', '')
            panel_content = panel.get('content', '')
            content.append(f"[bold]{panel_title}[/bold]\n{panel_content}")
            
        self.console.print(Panel(
            "\n\n".join(content),
            title=title,
            border_style=style,
            box=box.ROUNDED
        ))

    def display_options(
        self,
        options: List[Any],
        title: str = "Options",
        panel_titles: Optional[List[str]] = None,
        extra_content: Optional[List[str]] = None,
        header_panels: Optional[List[Dict[str, str]]] = None,
        show_cancel: bool = True,
        editing_mode: bool = False,
        selected: Optional[int] = None,
        formatter: Optional[callable] = None,
        banner_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, str]:
        """Display an interactive option menu with optional banner"""
        self.debug_print("Starting display_options", {
            'num_options': len(options),
            'editing_mode': editing_mode,
            'selected': selected,
            'has_banner': banner_params is not None
        })
        
        if selected is not None:
            self.state.set_selection(selected)
        
        def render_screen():
            # Always clear screen before rendering
            clear_screen(caller="UIOptionDisplay.display_options")
            
            # Display banner if parameters provided
            if banner_params:
                self.debug_print("Rendering banner", banner_params)
                self.display_banner(
                    title=banner_params.get('title', ''),
                    subtitle=banner_params.get('subtitle', []),
                    website=banner_params.get('website')
                )
                
            if header_panels:
                self.debug_print("Rendering header panels", {
                    'num_panels': len(header_panels)
                })
                self.display_header_panels(header_panels)
            
            # Show appropriate navigation instructions
            instructions = (
                "[dim]←/→ to select, Enter to confirm, q to cancel[/dim]"
                if editing_mode else
                "[dim]↑/↓ to select, Enter to edit, q to exit[/dim]"
            )
            self.console.print(instructions)
            
            # Display options
            self.debug_print("Rendering options", {
                'current_selection': self.state.selected_index,
                'editing_mode': editing_mode
            })
            
            for i, option in enumerate(options):
                style = "bold white on blue" if i == self.state.selected_index else "blue"
                content = formatter(option) if formatter else str(option)
                
                panel_content = content
                if extra_content and i < len(extra_content):
                    panel_content = f"{content}\n{extra_content[i]}"
                
                panel_title = (
                    panel_titles[i] if panel_titles and i < len(panel_titles)
                    else f"Option {i + 1}"
                )
                
                self.console.print(Panel(
                    panel_content,
                    title=panel_title,
                    border_style=style
                ))
            
            if show_cancel:
                cancel_style = "bold white on red" if self.state.selected_index == len(options) else "red"
                self.console.print(Panel(
                    "Cancel",
                    title="Exit",
                    border_style=cancel_style
                ))

        while True:
            render_screen()
            c = getch(debug=self.debug)
            
            self.debug_print("Key pressed", repr(c))
            
            if not editing_mode:
                if c == '\x1b[A':  # Up arrow
                    self.debug_print("Up arrow pressed", {
                        'current_index': self.state.selected_index
                    })
                    if self.state.selected_index > 0:
                        self.state.set_selection(self.state.selected_index - 1)
                        continue
                        
                elif c == '\x1b[B':  # Down arrow
                    self.debug_print("Down arrow pressed", {
                        'current_index': self.state.selected_index
                    })
                    max_index = len(options) - 1 if not show_cancel else len(options)
                    if self.state.selected_index < max_index:
                        self.state.set_selection(self.state.selected_index + 1)
                        continue
                        
            else:  # Editing mode
                if c == '\x1b[D':  # Left arrow
                    self.debug_print("Left arrow pressed (editing mode)")
                    return self.state.selected_index, 'left'
                    
                elif c == '\x1b[C':  # Right arrow
                    self.debug_print("Right arrow pressed (editing mode)")
                    return self.state.selected_index, 'right'
            
            if c == '\r':  # Enter
                self.debug_print("Enter pressed", {
                    'selected_index': self.state.selected_index,
                    'is_cancel': show_cancel and self.state.selected_index == len(options)
                })
                if show_cancel and self.state.selected_index == len(options):
                    return self.state.selected_index, 'cancel'
                return self.state.selected_index, 'select'
                
            elif c == 'q':  # Quick exit
                self.debug_print("Quick exit requested")
                return self.state.selected_index, 'quit'


# ==================================================
# File: utils.py
# ==================================================
import sys
import os
import inspect
import builtins
import datetime
from typing import Any
if sys.platform != 'win32':
    import termios
    import tty


def getch(debug=False):
    """Cross-platform character input with cleaner debug output"""
    if sys.platform == 'win32':
        import msvcrt
        first = msvcrt.getch()
        if debug:
            print("\nDEBUG getch() - First byte:", first)

        if first in [b'\xe0', b'\x00']:  # Special keys
            second = msvcrt.getch()
            if debug:
                print("DEBUG getch() - Second byte:", second)

            # Windows arrow keys mapping
            if second == b'H':    # Up arrow
                result = '\x1b[A'
            elif second == b'P':  # Down arrow
                result = '\x1b[B'
            elif second == b'K':  # Left arrow
                result = '\x1b[D'
            elif second == b'M':  # Right arrow
                result = '\x1b[C'
            else:
                result = 'x'  # Default for unmapped special keys

            if debug:
                print(f"DEBUG getch() - Mapped to: {repr(result)}")

            return result

        return first.decode('utf-8', errors='replace')
    else:
        # Unix systems (macOS, Linux)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            first = sys.stdin.read(1)
            if debug:
                print(f"\nDEBUG getch() - First byte: {repr(first)}")

            if first == '\x1b':  # Escape sequence
                # Read potential escape sequence
                second = sys.stdin.read(1)
                if debug:
                    print(f"DEBUG getch() - Second byte: {repr(second)}")

                if second == '[':
                    third = sys.stdin.read(1)
                    if debug:
                        print(f"DEBUG getch() - Third byte: {repr(third)}")

                    # Map arrow keys
                    result = '\x1b[' + third

                    if debug:
                        print(f"DEBUG getch() - Mapped to: {repr(result)}")

                    return result

                # Handle non-arrow escape sequences
                return first + second

            return first

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear_screen(caller: str = None):
    """Fast cross-platform screen clearing with caller tracking

    Args:
        caller: Optional string to identify the caller. If not provided,
               will attempt to automatically detect the caller.
    """
    # Get caller info if not provided
    if caller is None:
        # Get the caller's frame
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        
        if caller_frame:
            # Get the module name and calling function name
            module_name = caller_frame.f_globals.get('__name__', '')
            function_name = caller_frame.f_code.co_name
            
            # Format caller string
            caller = f"{module_name}.{function_name}"
        else:
            caller = "unknown"
            
    debug_str = f"Clearing screen (called from: {caller})"
    
    # If debug mode is enabled (checking if print has been replaced with debug_print)
    if hasattr(print, '__wrapped__'):
        print(debug_str)
    
    # Perform the actual screen clearing
    if sys.platform == 'win32':
        # Use ANSI escape sequences if available, fallback to cls
        try:
            import colorama
            colorama.init()
            print('\033[2J\033[H', end='')
        except ImportError:
            os.system('cls')
    else:
        print('\033[2J\033[H', end='')


original_print = builtins.print


def debug_print(*args: Any, **kwargs: Any):
    """Enhanced print function that adds timestamps to debug messages"""
    if args and isinstance(args[0], str) and args[0].strip().startswith("DEBUG"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        new_args = (f"[{timestamp}] {args[0]}",) + args[1:]
        original_print(*new_args, **kwargs)
    else:
        original_print(*args, **kwargs)


def enable_debug_printing():
    """Enable timestamped debug printing"""
    builtins.print = debug_print


def disable_debug_printing():
    """Restore original print function"""
    builtins.print = original_print
