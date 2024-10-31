# Hash Checker

This tool performs various actions on a file to test which actions result in a change in the file's hash value. By analyzing the effects of different operations, this tool helps identify actions that modify a file's integrity.

## Feature
- Hash Calculation: Calculates and records the hash of a file before and after each action.
- File Modification Tracking: Identifies which operations result in hash changes, such as file edits or metadata adjustments.
- Hash Types: MD5 or SHA512

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
python3 check_hash.py <file_name> <hash_type>
```
