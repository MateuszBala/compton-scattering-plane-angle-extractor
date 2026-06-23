# Contributing Guide

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for making contributions to the codebase.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Branching Strategy](#branching-strategy)
5. [Making Changes](#making-changes)
6. [Commit Guidelines](#commit-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Code Review](#code-review)
9. [Testing Requirements](#testing-requirements)
10. [Documentation](#documentation)
11. [Reporting Issues](#reporting-issues)
12. [FAQ](#faq)

---

## Code of Conduct

### Our Commitment

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background, experience level, or identity.

### Expected Behavior

- Be respectful and professional in all communications
- Provide constructive feedback and criticism
- Respect differing opinions and approaches
- Focus on what is best for the project and community
- Accept responsibility and apologize when mistakes are made

### Unacceptable Behavior

- Harassment, discrimination, or exclusion based on any characteristics
- Insulting or derogatory comments
- Unwelcome sexual attention or advances
- Trolling, deliberately provocative behavior, or personal attacks
- Publishing private information without consent

### Enforcement

Project maintainers are responsible for enforcing this code of conduct. Violations may result in temporary or permanent removal from the project.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Git**: Version 2.0 or later
- **Compiler**: GCC 9.0+ or Clang 10.0+ (C++17 support required)
- **Build Tools**: CMake 3.16 or later
- **Development Tools**:
  - Cppcheck for static analysis
  - ClangFormat for code formatting
  - ShellCheck for bash script validation

### Required Knowledge

Familiarity with:
- C++17 programming language
- Bash scripting
- Git version control
- Our coding conventions (see CODING_CONVENTIONS.md)
- Our testing conventions (see TESTING_CONVENTIONS.md)

### Licensing

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

## Development Setup

### 1. Fork the Repository

If you don't have write access, fork the repository on GitHub:

```bash
# Navigate to the project repository
# Click "Fork" button on GitHub
```

### 2. Clone the Repository

```bash
# Clone your fork (or the original if you have write access)
git clone https://github.com/your-username/project.git
cd project
```

### 3. Add Upstream Remote

If you forked the repository, add the upstream remote:

```bash
git remote add upstream https://github.com/original-owner/project.git
git remote -v  # Verify remotes
```

### 4. Install Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  cmake \
  libcatch2-dev \
  cppcheck \
  clang-format \
  shellcheck
```

### 5. Build the Project

```bash
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
```

### 6. Run Tests

```bash
# In build directory
ctest --verbose

# Or use make
make test
```

### 7. Set Up Pre-commit Hooks (Optional)

```bash
# Copy provided pre-commit hooks
cp .git-hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

---

## Branching Strategy

We use a Git Flow branching strategy with the following main branches:

### Main Branches

- **`main`**: Production-ready code. Direct commits are **NOT ALLOWED**.
- **`develop`**: Integration branch for features. Direct commits are **NOT ALLOWED**.

### Feature Branches

Always create new branches from `develop` for your work.

### Naming Convention

Branch names must follow this convention:

```
<type>/<description>
```

To create empty new branch:

```bash
git checkout develop
git checkout -b <type>/<description>
git push -u origin <type>/<description>
```

#### Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature` | New feature development | `feature/user-authentication` |
| `bugfix` | Bug fix | `bugfix/memory-leak-in-parser` |
| `docs` | Documentation changes | `docs/api-reference-guide` |
| `refactor` | Code refactoring | `refactor/simplify-data-processing` |
| `test` | Test additions | `test/edge-case-validation` |
| `chore` | Maintenance tasks | `chore/update-dependencies` |
| `perf` | Performance improvements | `perf/optimize-query-execution` |

### Naming Rules

- Use lowercase letters and hyphens only
- Be descriptive but concise
- Maximum 50 characters (excluding type prefix)
- Use present tense: "add" not "adding" or "added"

**Examples:**
```
✅ feature/add-user-authentication
✅ bugfix/fix-memory-leak
✅ docs/update-api-documentation
✅ refactor/simplify-parser
✅ perf/optimize-cache-lookup

❌ Feature/UserAuthentication
❌ bugfix/fix-stuff
❌ docs/documentation-updates
❌ feature/adding-auth
❌ my-new-feature
```

### Branch Lifecycle

```
develop (current state)
    ↓
Create feature branch: feature/my-feature
    ↓
Make commits and push
    ↓
Create Pull Request
    ↓
Code review and feedback
    ↓
Merge to develop
    ↓
Delete feature branch
```

---

## Making Changes

### Before You Start

1. **Check for Existing Issues**: Ensure no one is already working on this
2. **Open an Issue** (if not already open): Describe the feature or bug
3. **Get Agreement**: Discuss approach with maintainers before major work
4. **Create Branch**: Use naming convention above

### During Development

1. **Keep Changes Focused**: Address one concern per branch
2. **Follow Conventions**: Use coding conventions from CODING_CONVENTIONS.md
3. **Write Tests**: Add tests alongside your code
4. **Commit Regularly**: Make small, logical commits
5. **Stay Updated**: Sync with `develop` regularly

```bash
# Update your branch with latest develop changes
git fetch upstream
git rebase upstream/develop
```

### Code Quality Standards

Your code must meet these standards:

- **Compilation**: Compiles with `-Wall -Wextra -Wpedantic` with no warnings
- **Static Analysis**: Passes Cppcheck with no issues
- **Formatting**: Passes ClangFormat check
- **Tests**: All existing and new tests pass
- **Documentation**: Code is documented per DOCUMENTATION_CONVENTIONS.md
- **Performance**: No significant performance degradation

---

## Commit Guidelines

Refer to **COMMIT_CONVENTIONS.md** for detailed commit message guidelines.

### Quick Summary

- Use format: `<type>(<scope>): <subject>`
- Use imperative mood ("add", "fix", "update")
- Lowercase, no period at end
- Maximum 110 characters
- Reference related issues: `Closes #123`

**Examples:**
```
feat(auth): implement OAuth2 authentication
fix(parser): resolve null pointer exception
docs: add quickstart guide
test(core): add edge case validation tests
```

### Commit Hygiene

```bash
# Make focused commits
git add src/module.cc
git commit -m "feat(core): add caching layer"

# Don't commit unrelated changes together
git add .
git commit -m "feat,fix,docs: multiple changes"  # Bad!

# Use interactive rebase to clean up history before PR
git rebase -i upstream/develop
```

---

## Pull Request Process

### 1. Create a Pull Request

When ready for review:

```bash
# Push your branch
git push origin feature/your-feature

# Create PR on GitHub
# - Use PR template
# - Link related issues
# - Describe changes clearly
```

### 2. PR Title Format

```
<type>(<scope>): <description>
```

Same format as commits.

**Examples:**
```
feat(auth): implement two-factor authentication
fix(api): resolve timeout on large requests
docs: update installation guide
test(core): add comprehensive error handling tests
```

### 3. PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Related Issues
Closes #123
Related to #456

## Changes
- Change 1
- Change 2
- Change 3

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe tests added or how changes were tested.

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
```

### 4. PR Checklist

Before submitting a PR, verify:

- [ ] Branch created from `develop` (not `main`)
- [ ] Branch name follows convention
- [ ] All commits follow COMMIT_CONVENTIONS.md
- [ ] Code compiles without warnings
- [ ] Cppcheck passes with no issues
- [ ] ClangFormat approved
- [ ] ShellCheck approved (for bash scripts)
- [ ] All tests pass (existing and new)
- [ ] New tests added for new functionality
- [ ] Documentation updated (if needed)
- [ ] No unrelated changes included
- [ ] PR title and description are clear
- [ ] Related issues are linked

### 5. Responding to Feedback

- Respond to all comments
- Make requested changes in new commits
- Don't force push after review starts (unless asked)
- Re-request review after addressing feedback

```bash
# Make changes based on feedback
git add .
git commit -m "review: address code review feedback"
git push origin feature/your-feature
```

---

## Code Review

### What Reviewers Look For

Reviewers will check:

1. **Correctness**: Does the code work correctly?
2. **Design**: Is the design sound and consistent?
3. **Style**: Does it follow coding conventions?
4. **Tests**: Are there adequate tests?
5. **Documentation**: Is it clearly documented?
6. **Performance**: Any performance issues?
7. **Security**: Any security concerns?

### Review Expectations

- **Maintainers**: Will review within 2-3 business days
- **Contributors**: Please address feedback promptly
- **Discussion**: Technical discussion is encouraged
- **Civility**: Keep all discussions professional and constructive

### Approval Requirements

A PR requires:
- At least **2 approvals** from maintainers
- **All CI checks** passing
- **All conversations** resolved
- **No merge conflicts**

### Merging

Only maintainers can merge PRs. Merging requirements:

```
✅ Approved by 2+ maintainers
✅ All CI checks passing
✅ No merge conflicts
✅ All conversations resolved
✅ Branch is up to date with develop
```

---

## Testing Requirements

### Unit Tests

All new code must have unit tests.

**Test Requirements:**
- Tests in `tests/` directory
- One test file per source file
- Follow TESTING_CONVENTIONS.md
- Use Catch2 for C++
- Use BATS for bash scripts

**Test Naming:**
```
test_<module>_<expected_behavior>
test_all_variables_initialised
test_zero_argument_raises_error
```

### Integration Tests

Add integration tests for:
- Multi-component interactions
- End-to-end workflows
- Critical system paths

### Test Execution

Before submitting PR:

```bash
# Build with tests
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make -j$(nproc)

# Run all tests
ctest --verbose

# Or run specific tests
./tests/test_module_name

# Run bash tests
bats tests/test_script.bats
```

### Code Coverage

While code coverage metrics are not enforced, aim for:
- **Unit test coverage**: 80%+ for new code
- **Critical paths**: 100% coverage
- **Edge cases**: Comprehensive testing

---

## Documentation

### Code Documentation

Per DOCUMENTATION_CONVENTIONS.md:

- **Functions/Methods**: Document with Google C++ style
- **Classes**: Document purpose and usage
- **Complex Logic**: Explain "why" not just "what"
- **Private Members**: Document to understand implementation

**Example:**
```cpp
/**
 * Validates the input data format and checks readability.
 *
 * @param input Input string to validate
 * @return 0 if valid, 1 if invalid format, 2 if unreadable
 *
 * Example:
 * @code
 *   int status = validate_input("data");
 * @endcode
 */
int validate_input(const std::string& input);
```

### Project Documentation

Update relevant documentation:

- **README.md**: If changing user-facing behavior
- **BUILD.md**: If changing build process
- **API.md**: If modifying public interfaces
- **ARCHITECTURE.md**: If changing system design
- **MODULE.md**: If modifying module functionality

### Commit Message as Documentation

Remember: commit messages are documentation. Write clear, descriptive messages that explain:
- What changed
- Why it changed
- Impact of the change

---

## Reporting Issues

### Before Reporting

1. **Search existing issues**: Your issue might already be reported
2. **Check documentation**: Solution might be in docs
3. **Update software**: Issue might be fixed in latest version

### Creating an Issue

Use the issue template:

```markdown
## Description
Clear description of the issue or request.

## Steps to Reproduce (for bugs)
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- OS: Ubuntu 20.04
- Compiler: GCC 9.4
- Version: 1.0.0

## Additional Context
Any other information helpful for understanding the issue.
```

### Issue Labels

Issues may be labeled:

- `bug`: Something isn't working
- `enhancement`: Feature request
- `documentation`: Documentation issue
- `good-first-issue`: Good for new contributors
- `help-wanted`: Need community input
- `question`: Support question

---

## Development Workflow Example

### Complete Example Workflow

```bash
# 1. Ensure you have latest develop
git checkout develop
git pull upstream develop

# 2. Create feature branch
git checkout -b feature/add-caching

# 3. Make changes
vim src/cache.cc
vim tests/test_cache.cc

# 4. Stage and commit
git add src/cache.cc
git commit -m "feat(core): implement caching layer"

git add tests/test_cache.cc
git commit -m "test(core): add caching functionality tests"

# 5. Run tests locally
cd build
ctest --verbose

# 6. Push to your fork
git push origin feature/add-caching

# 7. Create PR on GitHub
# - Fill out PR template
# - Link related issues
# - Request review

# 8. Address feedback (if any)
# - Make requested changes
# - Commit: git commit -m "review: address code review feedback"
# - Push: git push origin feature/add-caching

# 9. Maintainer merges PR

# 10. Update local repository
git fetch upstream
git checkout develop
git pull upstream develop

# 11. Clean up local branch
git branch -d feature/add-caching
```

---

## FAQ

### Q: Can I commit directly to `main` or `develop`?

**A:** No. All changes must go through pull requests with code review.

### Q: Do I need to fork the repository?

**A:** Only if you don't have write access. If you do, you can create branches directly.

### Q: How do I update my branch with latest `develop` changes?

**A:** 
```bash
git fetch upstream
git rebase upstream/develop
```

### Q: What if my PR has merge conflicts?

**A:** Resolve conflicts locally:
```bash
git fetch upstream
git rebase upstream/develop
# Resolve conflicts in files
git add .
git rebase --continue
git push --force-with-lease origin feature/your-feature
```

### Q: How long does code review take?

**A:** Typically 2-3 business days. Complex changes may take longer.

### Q: Can I make changes while under review?

**A:** Yes. Make changes in new commits, don't force push. Force push is only acceptable if requested by reviewers.

### Q: What if my tests fail?

**A:** 
1. Understand why they failed
2. Fix the issue
3. Commit: `git commit -m "fix: resolve failing tests"`
4. Push and request re-review

### Q: Can I rebase my PR?

**A:** You can rebase before first review. After review starts, avoid rebasing unless:
- Explicitly asked by reviewers
- Resolving merge conflicts
- Use `--force-with-lease` to be safe

### Q: How do I run specific tests?

**A:**
```bash
# Run specific test file
./build/tests/test_module_name

# Run specific test case
./build/tests/test_module_name "test_case_name"

# Run bash tests
bats tests/test_script.bats
```

### Q: What if I disagree with a review comment?

**A:** Technical discussion is welcome and encouraged. Explain your reasoning respectfully. If unresolved, maintainers will make final decision.

### Q: Can I contribute documentation only?

**A:** Yes! Documentation contributions are very welcome and follow the same process.

### Q: How do I suggest improvements to this contributing guide?

**A:** Create an issue or PR with your suggestions. Feedback is appreciated!

---

## Getting Help

### Where to Ask Questions

1. **GitHub Issues**: For bug reports and feature requests
2. **GitHub Discussions**: For general questions
3. **Documentation**: Check DOCUMENTATION_CONVENTIONS.md, BUILD.md, etc.
4. **Code Comments**: Look at existing code for examples

### Useful Resources

- **Coding Standards**: See CODING_CONVENTIONS.md
- **Bash Scripts**: See SCRIPTING_CONVENTIONS.md
- **Testing**: See TESTING_CONVENTIONS.md
- **Documentation**: See DOCUMENTATION_CONVENTIONS.md
- **Commits**: See COMMIT_CONVENTIONS.md
- **Build Instructions**: See BUILD.md

---

## Acknowledgments

Thank you for contributing to this project! Contributors are the backbone of open source, and we appreciate your effort to improve the codebase.

---

**Last Updated:** June 2026  
**Version:** 1.0
