# Bash Scripting Conventions

This document outlines the coding standards and conventions for bash scripts in this project. All bash scripts must conform to these guidelines.

## Table of Contents

1. [Script Header](#script-header)
2. [Formatting and Style](#formatting-and-style)
3. [Naming Conventions](#naming-conventions)
4. [Script Structure](#script-structure)
5. [Functions](#functions)
6. [Variables](#variables)
7. [Error Handling](#error-handling)
8. [Testing and Conditions](#testing-and-conditions)
9. [Arguments and Parameters](#arguments-and-parameters)
10. [Best Practices](#best-practices)
11. [Security Considerations](#security-considerations)
12. [Performance Optimization](#performance-optimization)
13. [Tools and Analysis](#tools-and-analysis)

---

## Script Header

Every bash script must start with a standardized header:

```bash
#!/bin/bash
# FILE: script_name.sh
#
# ABOUT: Brief description of what this script does and its purpose.
#        Can span multiple lines if necessary.
#
# ARGUMENTS:
#   --input-file : Path to the input file (required)
#   --output-dir : Directory for output files (optional, default: ./output)
#   --verbose    : Enable verbose output (flag)
#
# USAGE:
#   bash script_name.sh --input-file data.txt --output-dir ./results
#   bash script_name.sh --input-file data.txt --verbose
```

### Header Components

- **FILE**: Name of the script file
- **ABOUT**: Clear description of script purpose and functionality
- **ARGUMENTS**: List of all expected arguments with descriptions
- **USAGE**: Examples of how to run the script with different argument combinations

---

## Formatting and Style

### Indentation

- Use **2 spaces** per indentation level.
- Never mix tabs and spaces.

```bash
if [[ condition ]]; then
  # 2 spaces indentation
  if [[ nested_condition ]]; then
    # 4 spaces for nested
    echo "Nested block"
  fi
fi
```

### Line Length

- **Maximum line length: 100 characters**.
- Break long lines logically:

```bash
# Good: Breaking long lines
if [[ -f "${INPUT_FILE}" ]] && [[ -r "${INPUT_FILE}" ]]; then
  process_file "${INPUT_FILE}"
fi

# Bad: Exceeds 100 characters
if [[ -f "${INPUT_FILE}" ]] && [[ -r "${INPUT_FILE}" ]] && [[ -s "${INPUT_FILE}" ]]; then

# Good: Use intermediate variables for clarity
CONDITION1=$([[ -f "${INPUT_FILE}" ]] && echo 1 || echo 0)
CONDITION2=$([[ -r "${INPUT_FILE}" ]] && echo 1 || echo 0)
if [[ "${CONDITION1}" -eq 1 ]] && [[ "${CONDITION2}" -eq 1 ]]; then
  process_file "${INPUT_FILE}"
fi
```

### Spacing

- One space after control flow keywords:

```bash
if [[ condition ]]; then
  # body
fi

for item in "${ARRAY[@]}"; do
  # body
done

while [[ condition ]]; do
  # body
done
```

### Braces and Parentheses

- Always use double brackets `[[ ]]` for conditionals (not `[ ]`).
- Use proper quoting with `"${var}"` instead of `$var`:

```bash
# Good
if [[ "${STATUS}" == "success" ]]; then
  echo "Success"
fi

# Bad
if [ $STATUS = "success" ]; then
  echo "Success"
fi
```

---

## Naming Conventions

### Script Files

- Use **`snake_case`** for script filenames:
  ```bash
  process_data.sh
  backup_database.sh
  deploy_application.sh
  ```

### Functions

- Use **`snake_case`** for function names:
  ```bash
  function validate_input() { }
  function process_data() { }
  function log_message() { }
  ```

### Global Variables

- Use **UPPERCASE with underscores** for global variables:
  ```bash
  CONFIG_FILE="/etc/app/config.conf"
  MAX_RETRIES=5
  DEBUG_MODE=true
  ```

### Exported Variables

- Use **UPPERCASE** for variables that are exported (available to child processes):
  ```bash
  export DATABASE_URL="postgresql://localhost/mydb"
  export API_KEY="secret_key"
  ```

### Local Variables in Functions

- Use **UPPERCASE with `PARAM_` prefix** for function parameters and local variables:
  ```bash
  function process_file() {
    local PARAM_FILE_PATH=$1
    local PARAM_VERBOSE=$2
    local TEMP_RESULT=""
    
    # function body
  }
  ```

---

## Script Structure

A typical bash script structure:

```bash
#!/bin/bash
# FILE: process_data.sh
#
# ABOUT: Processes input data and generates reports.
#
# ARGUMENTS:
#   --input : Path to input file
#   --format : Output format (json, csv)
#
# USAGE:
#   bash process_data.sh --input data.txt --format json

# Error handling - ALWAYS include this
set -euo pipefail

# Global configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${SCRIPT_DIR}/script.log"
VERBOSE=false

# Function definitions
function log_info() {
  echo "[INFO] $*" | tee -a "${LOG_FILE}"
}

function validate_input() {
  # implementation
}

# Main script logic
function main() {
  # Main functionality
  validate_input "$@"
  process_data
}

# Execute main function
main "$@"
```

---

## Functions

### Function Definition

Use `function` keyword with parentheses:

```bash
function my_function() {
  # function body
}
```

### Function Documentation

Every function must have documentation:

```bash
# Validates the input file format and checks if it's readable.
# Parameters:
#   @PARAM_FILE_PATH : Path to the file to validate
#   @PARAM_STRICT    : Enable strict validation (optional)
# Returns:
#   0 if valid, 1 if invalid, 2 if file doesn't exist
function validate_file() {
  local PARAM_FILE_PATH=$1
  local PARAM_STRICT=${2:-false}
  
  if [[ ! -f "${PARAM_FILE_PATH}" ]]; then
    echo "Error: File not found" >&2
    return 2
  fi
  
  if [[ ! -r "${PARAM_FILE_PATH}" ]]; then
    echo "Error: File is not readable" >&2
    return 1
  fi
  
  # Validation logic
  if validate_format "${PARAM_FILE_PATH}"; then
    return 0
  else
    return 1
  fi
}
```

### Return Values

#### For Integer/Status Returns

Use `return` statement with exit codes:

```bash
# Returns status code
function check_database_connection() {
  local PARAM_HOST=$1
  local PARAM_PORT=$2
  
  if nc -z "${PARAM_HOST}" "${PARAM_PORT}" > /dev/null 2>&1; then
    return 0  # Success
  else
    return 1  # Connection failed
  fi
}

# Usage
if check_database_connection "localhost" 5432; then
  echo "Database is reachable"
else
  echo "Database is not reachable"
fi
```

#### For String/Data Returns

Use `echo` to return values and capture with command substitution:

```bash
# Returns string value via echo
function get_config_value() {
  local PARAM_KEY=$1
  
  local VALUE=$(grep "^${PARAM_KEY}=" "${CONFIG_FILE}" | cut -d= -f2)
  echo "${VALUE}"
}

# Usage
DATABASE_URL=$(get_config_value "database.url")
echo "Database URL: ${DATABASE_URL}"
```

#### Combined Return (Status and Value)

```bash
# Returns both status and value
function process_and_return() {
  local PARAM_DATA=$1
  
  if [[ -z "${PARAM_DATA}" ]]; then
    return 1  # Error case
  fi
  
  local RESULT=$(echo "${PARAM_DATA}" | tr '[:lower:]' '[:upper:]')
  echo "${RESULT}"
  return 0
}

# Usage
if RESULT=$(process_and_return "hello"); then
  echo "Result: ${RESULT}"
else
  echo "Processing failed"
fi
```

### Function Best Practices

```bash
# Good: Clear parameters with local scope
function calculate_total() {
  local PARAM_ITEMS=("$@")
  local TOTAL=0
  
  for item in "${PARAM_ITEMS[@]}"; do
    ((TOTAL += item))
  done
  
  echo "${TOTAL}"
  return 0
}

# Bad: Using global variables
TOTAL=0
function calculate_total_bad() {
  for item in "$@"; do
    ((TOTAL += item))
  done
}
```

---

## Variables

### Variable Declaration

Always declare variables explicitly:

```bash
# Good: Explicit declaration
readonly CONFIG_FILE="/etc/app/config.conf"
local PARAM_NAME=$1
export DATABASE_URL="postgresql://localhost/db"

# Bad: Implicit declaration
NAME=$1
RESULT=5
```

### Variable Quoting

Always use double quotes around variable references:

```bash
# Good
echo "${USER_INPUT}"
if [[ "${STATUS}" == "ok" ]]; then
  process "${DATA}"
fi

# Bad
echo $USER_INPUT
if [ $STATUS = ok ]; then
  process $DATA
fi
```

### Variable Scope

```bash
# Global variable - accessible everywhere
GLOBAL_CONFIG="config.txt"

function my_function() {
  # Local variable - only in this function
  local PARAM_FILE=$1
  
  # Modify global (not recommended, use return values instead)
  GLOBAL_RESULT="processed"
}
```

### Global vs Local Variables

```bash
# Script level - UPPERCASE
DATABASE_HOST="localhost"
DATABASE_PORT=5432
DEBUG_MODE=false

function main() {
  # Local with PARAM_ prefix
  local PARAM_INPUT_FILE=$1
  local PARAM_VERBOSE=$2
  
  # Process input
  process_file "${PARAM_INPUT_FILE}"
}

main "$@"
```

---

## Error Handling

### Script-Level Error Handling

Every bash script must start with:

```bash
#!/bin/bash
set -euo pipefail
```

**What each option does:**

- `set -e` : Exit immediately if any command exits with non-zero status
- `set -u` : Exit if undefined variable is used
- `set -o pipefail` : Return exit code of last non-zero command in pipe

### Exit Codes

Standardized exit codes for the entire script:

- **0**: Successful execution
- **1**: Invalid arguments or invalid input
- **2**: Runtime error during execution

```bash
#!/bin/bash
set -euo pipefail

function validate_arguments() {
  if [[ $# -lt 1 ]]; then
    echo "Error: Missing required argument --input" >&2
    return 1
  fi
}

function main() {
  if ! validate_arguments "$@"; then
    exit 1  # Invalid arguments
  fi
  
  if ! process_data; then
    exit 2  # Runtime error
  fi
  
  exit 0  # Success
}

main "$@"
```

### Error Messages

Always write error messages to stderr:

```bash
# Good
echo "Error: Invalid file format" >&2
return 1

# Bad
echo "Error: Invalid file format"
return 1
```

### Error Traps

Use traps for cleanup:

```bash
#!/bin/bash
set -euo pipefail

TEMP_FILE="/tmp/script_temp_$$"

# Cleanup function
function cleanup() {
  local EXIT_CODE=$?
  
  if [[ -f "${TEMP_FILE}" ]]; then
    rm -f "${TEMP_FILE}"
  fi
  
  return "${EXIT_CODE}"
}

trap cleanup EXIT

# Script logic
echo "Processing..." > "${TEMP_FILE}"
process_file "${TEMP_FILE}"
```

---

## Testing and Conditions

### Double Brackets vs Single Brackets

Always use `[[ ]]` (not `[ ]`):

```bash
# Good: Double brackets (bash built-in)
if [[ "${VALUE}" == "success" ]]; then
  echo "Success"
fi

if [[ -f "${FILE}" && -r "${FILE}" ]]; then
  echo "File exists and is readable"
fi

# Bad: Single brackets (POSIX, limited)
if [ "$VALUE" = "success" ]; then
  echo "Success"
fi

if [ -f "$FILE" ] && [ -r "$FILE" ]; then
  echo "File exists and is readable"
fi
```

### String Comparisons

```bash
# Good
if [[ "${STRING}" == "value" ]]; then
  echo "Match"
fi

if [[ "${STRING}" != "value" ]]; then
  echo "No match"
fi

# Pattern matching (double brackets only)
if [[ "${STRING}" == "prefix"* ]]; then
  echo "Starts with prefix"
fi

# Regex matching (double brackets only)
if [[ "${STRING}" =~ ^[0-9]+$ ]]; then
  echo "All digits"
fi
```

### Numeric Comparisons

```bash
# Good
if [[ "${COUNT}" -eq 0 ]]; then
  echo "Zero"
fi

if [[ "${COUNT}" -gt 10 ]]; then
  echo "Greater than 10"
fi

if [[ "${COUNT}" -le 100 ]]; then
  echo "Less than or equal to 100"
fi
```

### File Tests

```bash
# Good
if [[ -f "${FILE}" ]]; then
  echo "Regular file"
fi

if [[ -d "${DIR}" ]]; then
  echo "Directory"
fi

if [[ -r "${FILE}" ]]; then
  echo "File is readable"
fi

if [[ -x "${SCRIPT}" ]]; then
  echo "File is executable"
fi

if [[ -s "${FILE}" ]]; then
  echo "File exists and is not empty"
fi
```

### Logical Operators

```bash
# Good: Logical AND
if [[ -f "${FILE}" && -r "${FILE}" ]]; then
  echo "File exists and is readable"
fi

# Good: Logical OR
if [[ "${STATUS}" == "done" || "${STATUS}" == "complete" ]]; then
  echo "Process finished"
fi

# Good: Negation
if [[ ! -f "${FILE}" ]]; then
  echo "File does not exist"
fi

# Good: Combining conditions
if [[ (-f "${FILE}" && -r "${FILE}") || -d "${DIR}" ]]; then
  echo "Valid input"
fi
```

---

## Arguments and Parameters

### Single Unnamed Argument

Scripts with a single argument can use unnamed (positional) arguments:

```bash
#!/bin/bash
# FILE: process.sh
# ABOUT: Processes a single input file.
# ARGUMENTS:
#   input_file : Path to the file to process
# USAGE:
#   bash process.sh data.txt

set -euo pipefail

INPUT_FILE=$1

function validate_input() {
  if [[ -z "${INPUT_FILE}" ]]; then
    echo "Error: Input file not provided" >&2
    exit 1
  fi
  
  if [[ ! -f "${INPUT_FILE}" ]]; then
    echo "Error: File not found: ${INPUT_FILE}" >&2
    exit 1
  fi
}

validate_input
# Process INPUT_FILE
```

### Multiple Named Arguments

Scripts with multiple arguments MUST use named arguments:

```bash
#!/bin/bash
# FILE: deploy.sh
# ABOUT: Deploys application with configuration.
# ARGUMENTS:
#   --environment : Target environment (required)
#   --version     : Application version (required)
#   --config-file : Path to config file (optional)
#   --dry-run     : Perform dry run without changes (optional)
# USAGE:
#   bash deploy.sh --environment prod --version 1.0.0
#   bash deploy.sh --env prod --ver 1.0.0 --config-file custom.conf --dry-run

set -euo pipefail

ENVIRONMENT=""
VERSION=""
CONFIG_FILE="config.conf"
DRY_RUN=false

function parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --environment | --env)
        ENVIRONMENT="$2"
        shift 2
        ;;
      --version | --ver)
        VERSION="$2"
        shift 2
        ;;
      --config-file)
        CONFIG_FILE="$2"
        shift 2
        ;;
      --dry-run)
        DRY_RUN=true
        shift
        ;;
      *)
        echo "Error: Unknown argument: $1" >&2
        exit 1
        ;;
    esac
  done
}

function validate_arguments() {
  if [[ -z "${ENVIRONMENT}" ]]; then
    echo "Error: --environment is required" >&2
    exit 1
  fi
  
  if [[ -z "${VERSION}" ]]; then
    echo "Error: --version is required" >&2
    exit 1
  fi
  
  if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo "Error: Config file not found: ${CONFIG_FILE}" >&2
    exit 1
  fi
}

function main() {
  parse_arguments "$@"
  validate_arguments
  
  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "[DRY-RUN] Deploying to ${ENVIRONMENT} version ${VERSION}"
  else
    deploy_application
  fi
}

main "$@"
```

---

## Best Practices

### Use readonly for Constants

```bash
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CONFIG_FILE="${SCRIPT_DIR}/config.conf"
readonly MAX_RETRIES=5
```

### Avoid Subshells in Loops

```bash
# Bad: Subshell loses variable changes
while IFS= read -r line; do
  COUNTER=$((COUNTER + 1))
done < "${FILE}"
echo "${COUNTER}"  # May be wrong

# Good: Use process substitution or mapfile
mapfile -t LINES < "${FILE}"
COUNTER=${#LINES[@]}
echo "${COUNTER}"
```

### Use Local Variables in Functions

```bash
# Good
function calculate() {
  local PARAM_A=$1
  local PARAM_B=$2
  local RESULT=$((PARAM_A + PARAM_B))
  echo "${RESULT}"
}

# Bad: Pollutes global namespace
function calculate_bad() {
  RESULT=$((A + B))
  echo "${RESULT}"
}
```

### Proper Array Handling

```bash
# Good: Proper array expansion
for item in "${ARRAY[@]}"; do
  process_item "${item}"
done

# Bad: Doesn't handle spaces in items
for item in ${ARRAY[@]}; do
  process_item "${item}"
done

# Good: Using mapfile for reading files
mapfile -t LINES < "${FILE}"
for line in "${LINES[@]}"; do
  process_line "${line}"
done
```

### Command Substitution

```bash
# Good: Modern syntax
RESULT=$(command)
FILES=$(find . -name "*.txt")

# Old syntax (avoid)
RESULT=`command`
```

### Process Substitution

```bash
# Good: For feeding data to functions
while IFS= read -r line; do
  process_line "${line}"
done < <(grep "pattern" "${FILE}")

# Good: For piping to functions that need variables
process_data < <(generate_data)
```

---

## Security Considerations

### Quote Variables

Always quote variables to prevent word splitting and glob expansion:

```bash
# Good
rm -f "${FILE}"
process_file "${INPUT}"

# Dangerous: Unquoted variables can lead to unexpected behavior
rm -f ${FILE}
process_file ${INPUT}
```

### Avoid eval

Never use `eval`:

```bash
# Bad: Security risk
eval "command ${USER_INPUT}"

# Good: Use direct assignment or safe alternatives
COMMAND="${USER_INPUT}"
${COMMAND}  # Still risky, but safer than eval
```

### Input Validation

Always validate user input:

```bash
# Good: Validate input format
function validate_email() {
  local PARAM_EMAIL=$1
  
  if [[ ! "${PARAM_EMAIL}" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "Error: Invalid email format" >&2
    return 1
  fi
  
  return 0
}

# Good: Sanitize file paths
function safe_file_operation() {
  local PARAM_FILE=$1
  
  # Prevent directory traversal
  if [[ "${PARAM_FILE}" == *".."* ]] || [[ "${PARAM_FILE}" == /* ]]; then
    echo "Error: Invalid file path" >&2
    return 1
  fi
  
  process_file "${PARAM_FILE}"
}
```

### Use Temporary Files Safely

```bash
# Good: Using mktemp
TEMP_FILE=$(mktemp)
trap "rm -f ${TEMP_FILE}" EXIT

echo "data" > "${TEMP_FILE}"
process_file "${TEMP_FILE}"

# Good: For temporary directories
TEMP_DIR=$(mktemp -d)
trap "rm -rf ${TEMP_DIR}" EXIT
```

### Restrict File Permissions

```bash
# Good: Create files with restricted permissions
touch "${CONFIG_FILE}"
chmod 600 "${CONFIG_FILE}"

# Good: Create secure temporary files
mktemp -t secure_file.XXXXXX
```

---

## Performance Optimization

### Use Built-in Commands

```bash
# Good: Built-in parameter expansion
FILENAME="${PATH##*/}"  # Get basename
DIRECTORY="${PATH%/*}"  # Get dirname

# Avoid: External commands for simple tasks
FILENAME=$(basename "${PATH}")
DIRECTORY=$(dirname "${PATH}")
```

### Avoid Unnecessary Subshells

```bash
# Good: Avoid subshells
if [[ -d "${DIR}" ]]; then
  cd "${DIR}"
  # Do work
  cd -
fi

# Better: Use subshell when necessary
(
  cd "${DIR}"
  process_files
)

# Bad: Multiple subshells
find . -name "*.txt" | while read file; do
  # Each line creates a subshell
done
```

### Use Efficient Searching

```bash
# Good: grep is efficient for pattern matching
grep "pattern" "${FILE}"

# Good: Use grep with appropriate flags
grep -c "pattern" "${FILE}"  # Count matches
grep -l "pattern" *.txt      # List files with matches

# Avoid: Multiple greps
grep "pattern1" "${FILE}" | grep "pattern2"
# Better:
grep "pattern1.*pattern2" "${FILE}"
```

### Array Operations

```bash
# Good: Direct array operations
ARRAY+=("new_element")
echo "${#ARRAY[@]}"  # Get array length

# Avoid: Recalculating repeatedly
for i in "${!ARRAY[@]}"; do
  # Avoid accessing ${#ARRAY[@]} multiple times in loop
done
```

---

## Tools and Analysis

### ShellCheck

Use **ShellCheck** for static analysis:

```bash
# Install
# Ubuntu/Debian: sudo apt-get install shellcheck
# macOS: brew install shellcheck

# Run analysis
shellcheck script.sh
shellcheck *.sh

# Ignore specific warnings
# Add this comment to script:
# shellcheck disable=SC2086  # Ignore word splitting warning
```

### Common ShellCheck Warnings

- **SC2086**: Double quote to prevent word splitting
- **SC2181**: Check exit code with `if $(...); then`
- **SC2230**: `which` is not portable, use `command -v`
- **SC1091**: Cannot follow non-constant source

### Code Review Checklist

Before submitting a script, verify:

- [ ] Shebang is `#!/bin/bash`
- [ ] Header includes FILE, ABOUT, ARGUMENTS, USAGE
- [ ] Script starts with `set -euo pipefail`
- [ ] All variables are quoted as `"${var}"`
- [ ] Functions use `[[ ]]` not `[ ]`
- [ ] Naming follows conventions (snake_case for functions/variables)
- [ ] Global variables are UPPERCASE
- [ ] Local parameters use PARAM_ prefix
- [ ] Function parameters documented in comments
- [ ] Return values clearly documented
- [ ] Error messages written to stderr (>&2)
- [ ] Exit codes follow standard (0=success, 1=invalid args, 2=runtime error)
- [ ] No hardcoded paths (use variables)
- [ ] Input validation performed on all user input
- [ ] Temporary files created with mktemp
- [ ] ShellCheck reports no warnings
- [ ] Lines do not exceed 100 characters
- [ ] Scripts with multiple args use named arguments
- [ ] No use of eval or other dangerous constructs

---

## Example Scripts

### Example 1: Data Processing Script (Single Argument)

```bash
#!/bin/bash
# FILE: process_log.sh
#
# ABOUT: Processes log file and generates statistics.
#
# ARGUMENTS:
#   log_file : Path to the log file to process
#
# USAGE:
#   bash process_log.sh /var/log/app.log

set -euo pipefail

readonly LOG_FILE=$1

function validate_input() {
  if [[ -z "${LOG_FILE}" ]]; then
    echo "Error: Log file path required" >&2
    exit 1
  fi
  
  if [[ ! -f "${LOG_FILE}" ]]; then
    echo "Error: File not found: ${LOG_FILE}" >&2
    exit 1
  fi
  
  if [[ ! -r "${LOG_FILE}" ]]; then
    echo "Error: File not readable: ${LOG_FILE}" >&2
    exit 1
  fi
}

# Counts lines matching a pattern.
# Parameters:
#   @PARAM_FILE : Log file to search
#   @PARAM_PATTERN : Pattern to search for
# Returns:
#   Count of matching lines
function count_pattern() {
  local PARAM_FILE=$1
  local PARAM_PATTERN=$2
  
  local COUNT=$(grep -c "${PARAM_PATTERN}" "${PARAM_FILE}" || echo 0)
  echo "${COUNT}"
}

function main() {
  validate_input
  
  local ERROR_COUNT=$(count_pattern "${LOG_FILE}" "ERROR")
  local WARNING_COUNT=$(count_pattern "${LOG_FILE}" "WARNING")
  local INFO_COUNT=$(count_pattern "${LOG_FILE}" "INFO")
  
  echo "Log Statistics:"
  echo "  Errors:   ${ERROR_COUNT}"
  echo "  Warnings: ${WARNING_COUNT}"
  echo "  Info:     ${INFO_COUNT}"
}

main
```

### Example 2: Deployment Script (Multiple Arguments)

```bash
#!/bin/bash
# FILE: deploy.sh
#
# ABOUT: Deploys application to specified environment.
#
# ARGUMENTS:
#   --environment : Target environment (dev, staging, prod)
#   --version     : Application version to deploy
#   --skip-tests  : Skip running tests (optional)
#
# USAGE:
#   bash deploy.sh --environment prod --version 2.1.0
#   bash deploy.sh --environment staging --version 2.1.0 --skip-tests

set -euo pipefail

ENVIRONMENT=""
VERSION=""
SKIP_TESTS=false

function parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --environment)
        ENVIRONMENT="$2"
        shift 2
        ;;
      --version)
        VERSION="$2"
        shift 2
        ;;
      --skip-tests)
        SKIP_TESTS=true
        shift
        ;;
      *)
        echo "Error: Unknown argument: $1" >&2
        exit 1
        ;;
    esac
  done
}

function validate_arguments() {
  if [[ -z "${ENVIRONMENT}" ]]; then
    echo "Error: --environment is required" >&2
    exit 1
  fi
  
  if [[ ! "${ENVIRONMENT}" =~ ^(dev|staging|prod)$ ]]; then
    echo "Error: Invalid environment: ${ENVIRONMENT}" >&2
    exit 1
  fi
  
  if [[ -z "${VERSION}" ]]; then
    echo "Error: --version is required" >&2
    exit 1
  fi
  
  if [[ ! "${VERSION}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid version format: ${VERSION}" >&2
    exit 1
  fi
}

# Runs unit tests.
# Returns:
#   0 if all tests pass, 1 if any test fails
function run_tests() {
  echo "Running tests..."
  
  if ./run_tests.sh; then
    echo "All tests passed"
    return 0
  else
    echo "Tests failed" >&2
    return 1
  fi
}

# Deploys application to specified environment.
# Parameters:
#   @PARAM_ENV : Target environment
#   @PARAM_VER : Version to deploy
# Returns:
#   0 on success, 2 on failure
function deploy_application() {
  local PARAM_ENV=$1
  local PARAM_VER=$2
  
  echo "Deploying to ${PARAM_ENV}..."
  echo "Version: ${PARAM_VER}"
  
  # Deployment logic here
  if ./scripts/deploy.sh "${PARAM_ENV}" "${PARAM_VER}"; then
    echo "Deployment successful"
    return 0
  else
    echo "Deployment failed" >&2
    return 2
  fi
}

function main() {
  parse_arguments "$@"
  validate_arguments
  
  if [[ "${SKIP_TESTS}" != "true" ]]; then
    if ! run_tests; then
      echo "Cannot deploy: tests failed" >&2
      exit 2
    fi
  fi
  
  if ! deploy_application "${ENVIRONMENT}" "${VERSION}"; then
    exit 2
  fi
  
  echo "Deployment complete"
}

main "$@"
```

---

## References

- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellstyle.html)
- [Defensive BASH Programming](https://www.kfirlavi.com/blog/2012/11/14/defensive-bash-programming/)

---

**Last Updated:** June 2026  
**Version:** 1.0
