"""
Judge0 Client - Interface to judge0 code execution platform
"""
import requests
import time
from typing import Dict, Any, Optional
from pathlib import Path


class Judge0Client:
    """Client for interacting with judge0 API"""

    # Python language ID in judge0
    PYTHON_LANGUAGE_ID = 71

    def __init__(self, base_url: str = "http://localhost:2358"):
        """
        Initialize judge0 client.

        Args:
            base_url: Base URL for judge0 API (default: localhost:2358)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def execute_code(
        self,
        source_code: str,
        stdin: str = "",
        language_id: int = PYTHON_LANGUAGE_ID,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute code via judge0.

        Args:
            source_code: The code to execute
            stdin: Standard input for the program
            language_id: Judge0 language ID (default: Python 71)
            timeout: Maximum execution time in seconds

        Returns:
            Dict with execution results
        """
        # Create submission
        submission_data = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": stdin,
        }

        try:
            # Submit code
            response = self.session.post(
                f"{self.base_url}/submissions?wait=true",
                json=submission_data
            )
            response.raise_for_status()

            result = response.json()

            return {
                'success': result.get('status', {}).get('id') == 3,  # Status 3 = Accepted
                'output': result.get('stdout', ''),
                'error': result.get('stderr') or result.get('compile_output'),
                'status': result.get('status', {}).get('description'),
                'time': result.get('time'),
                'memory': result.get('memory'),
                'token': result.get('token')
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'output': '',
                'error': f'Judge0 API error: {str(e)}',
                'status': 'API Error'
            }

    def execute_file(self, file_path: Path, stdin: str = "") -> Dict[str, Any]:
        """
        Execute a Python file via judge0.

        Args:
            file_path: Path to the Python file
            stdin: Standard input for the program

        Returns:
            Dict with execution results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()

            return self.execute_code(source_code, stdin=stdin)

        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Error reading file: {str(e)}',
                'status': 'File Error'
            }

    def get_languages(self) -> list[Dict[str, Any]]:
        """Get list of supported languages from judge0"""
        try:
            response = self.session.get(f"{self.base_url}/languages")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return [{'error': str(e)}]

    def health_check(self) -> bool:
        """Check if judge0 is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/about")
            return response.status_code == 200
        except:
            return False


def main():
    """Test judge0 client"""
    client = Judge0Client()

    print("=" * 60)
    print("Judge0 Client Test")
    print("=" * 60)
    print()

    # Health check
    print("Health check...")
    is_healthy = client.health_check()
    print(f"  Judge0 accessible: {is_healthy}")
    print()

    if is_healthy:
        # Test simple code execution
        print("Testing code execution...")
        result = client.execute_code('print("Hello from Judge0!")')
        print(f"  Success: {result['success']}")
        print(f"  Output: {result['output']}")
        print(f"  Status: {result['status']}")
    else:
        print("  Skipping execution test (judge0 not accessible)")
        print("  Note: Start judge0 with: docker-compose up -d")


if __name__ == "__main__":
    main()
