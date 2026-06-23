# Commit Conventions

This document outlines the standards and conventions for writing commit messages in this project. All commits must follow these guidelines to maintain a clear, consistent, and meaningful project history.

## Table of Contents

1. [General Principles](#general-principles)
2. [Commit Message Format](#commit-message-format)
3. [Commit Types](#commit-types)
4. [Scope](#scope)
5. [Subject Line](#subject-line)
6. [Multi-Type Commits](#multi-type-commits)
7. [Commit Body](#commit-body)
8. [Best Practices](#best-practices)
9. [Examples](#examples)
10. [Definition of Done](#definition-of-done)

---

## General Principles

### Purpose of Commit History

The commit history is the **technical documentation** of the project. Each commit should clearly communicate:
- **What** changed
- **Why** the change was made (context provided in PR description)
- **How** the change impacts the codebase

### Core Rule

> A commit message should explain the change without requiring the reader to examine the code.

### Language

All commit messages must be written in **English**.

---

## Commit Message Format

### Basic Format

```
<type>: <subject>
```

### With Scope

```
<type>(<scope>): <subject>
```

### Examples

```
feat: add user authentication module
fix(api): resolve null pointer exception in request handler
docs: update installation instructions for Ubuntu
test(core): add edge case tests for data validation
```

---

## Commit Types

| Type | Purpose | Examples |
|------|---------|----------|
| `feat` | New feature or functionality | `feat: add caching layer` |
| `fix` | Bug fix | `fix: correct memory leak in parser` |
| `docs` | Documentation changes | `docs: update API reference` |
| `test` | Test additions or modifications | `test: add boundary condition tests` |
| `refactor` | Code refactoring (no behavior change) | `refactor: simplify data processing logic` |
| `style` | Code style, formatting, linting | `style: apply code formatter` |
| `perf` | Performance improvements | `perf: optimize query execution time` |
| `ci` | CI/CD pipeline changes | `ci: add GitHub Actions workflow` |
| `config` | Configuration changes | `config: update CMake build settings` |
| `script` | Build, deployment, or developer scripts | `script: add deployment automation` |
| `chore` | Maintenance, dependencies, tooling | `chore: update dependencies` |
| `release` | Version release or tag | `release: version 2.1.0` |

### Type Guidelines

#### `feat` - New Feature

Use when adding new functionality that provides value to the user or system.

```
feat: implement priority queue for task scheduling
feat(database): add connection pooling support
```

#### `fix` - Bug Fix

Use when fixing an error or defect in existing code.

```
fix: prevent integer overflow in calculation
fix(parser): handle malformed JSON gracefully
```

#### `docs` - Documentation

Use for documentation-only changes (README, API docs, guides).

```
docs: add quickstart guide
docs(api): document authentication endpoints
```

#### `test` - Tests

Use when adding or modifying tests (unit, integration, etc.).

```
test: add validation edge cases
test(core): increase coverage for error handling
```

#### `refactor` - Refactoring

Use for code restructuring that doesn't change behavior.

```
refactor: extract common logic into utility functions
refactor(module): improve code clarity without behavior change
```

#### `style` - Style Changes

Use for non-functional changes like formatting, linting, naming.

```
style: apply code formatter
style: rename variables for clarity
style: remove unused imports
style: fix type annotations
```

#### `perf` - Performance

Use when improving speed, efficiency, or resource usage.

```
perf: reduce memory allocation in loops
perf: optimize sorting algorithm from O(n²) to O(n log n)
```

#### `ci` - CI/CD Changes

Use for continuous integration or deployment pipeline changes.

```
ci: add automated testing workflow
ci: configure code coverage reporting
```

#### `config` - Configuration

Use for build, tooling, or environment configuration changes.

```
config: update CMake C++ standard requirement
config: configure static analysis tools
```

#### `script` - Scripts

Use for build, deployment, or developer utility scripts.

```
script: add deployment automation script
script: create database migration tool
```

#### `chore` - Maintenance

Use for routine maintenance and dependency updates.

```
chore: update third-party libraries
chore: bump version in package files
```

#### `release` - Release

Use when creating a release or version tag.

```
release: version 1.0.0
release: prepare 2.5.0 release
```

---

## Scope

Scope is **optional** but **recommended** when changes affect a specific area.

### Scope Format

```
<type>(<scope>): <subject>
```

### Examples

```
feat(authentication): implement OAuth2 support
fix(database): resolve connection timeout issue
refactor(core): simplify algorithm implementation
docs(install): update setup instructions
```

### When to Use Scope

- Changes affect a specific module or component
- Changes are localized to one area
- Helps categorize commits for better navigation

### When Scope is Not Needed

- Small utility changes
- Global refactoring affecting multiple areas
- Changes that don't clearly fit one area

---

## Subject Line

The subject line is the first line of the commit message.

### Rules

1. **Use imperative mood** ("add", "fix", "update", "remove")
   - ✅ "add user authentication"
   - ❌ "added user authentication"
   - ❌ "adds user authentication"

2. **Be specific and concise**
   - ✅ "fix null pointer exception in parser"
   - ❌ "fix bug"
   - ❌ "update code"

3. **Maximum length: 110 characters** (preferably under 70)

4. **No period at the end**
   - ✅ "add error handling"
   - ❌ "add error handling."

5. **Lowercase (except proper nouns and acronyms)**
   - ✅ "implement HTTP request handler"
   - ❌ "Implement HTTP Request Handler"

6. **No imperative forms**
   - ✅ "apply code formatter"
   - ❌ "formatting code" or "code formatting"

### Subject Line Test

A good subject line completes this sentence:

> "If applied, this commit will **[subject line]**"

Examples:
- "If applied, this commit will **add user authentication**" ✅
- "If applied, this commit will **fix memory leak**" ✅
- "If applied, this commit will **update code**" ❌

### Subject Line Examples

**Good:**
```
feat: implement priority queue scheduling
fix: resolve race condition in thread pool
docs: add performance benchmarks
test: add validation error edge cases
refactor: simplify data transformation pipeline
perf: optimize query performance by 40%
```

**Bad:**
```
feat: User authentication stuff added
fix: Fixed a bug
docs: Updates and changes
test: Testing things
refactor: Code cleanup
chore: stuff
```

---

## Multi-Type Commits

When a commit affects multiple types (rare), separate types with a comma.

### Format

```
<type1>,<type2>: <subject>
```

### Examples

```
feat,test: implement validation with comprehensive tests
docs,refactor: improve documentation and simplify code
fix,perf: resolve bug and optimize performance
```

### When to Use Multi-Type

- Tightly related changes that form a single logical unit
- Test additions directly paired with feature implementation
- Documentation updates essential to understanding the code change

### When NOT to Use

- Changes should typically be separate commits
- Use multi-type sparingly; if commits feel disconnected, split them

---

## Commit Body

The commit body is **optional** but **recommended** for non-trivial changes.

### Format

```
<type>(<scope>): <subject>

<body>
```

### Body Guidelines

1. **Separate body from subject with a blank line**
2. **Explain what and why, not how** (code shows how)
3. **Wrap at 80 characters per line**
4. **Use bullet points for multiple reasons or changes**
5. **Reference related issues or PRs** (if applicable)

### Body Example

```
feat(cache): implement LRU cache eviction policy

Add Least Recently Used (LRU) eviction to cache manager.
This resolves memory issues when cache exceeds 1GB limit.

- Evict least accessed items when cache is full
- Maintain O(1) lookup and O(1) eviction time
- Compatible with existing cache interface

Closes #245
Related-To: #240
```

### When to Include Body

- Complex implementation requiring explanation
- Non-obvious why the change was necessary
- Breaking changes or API modifications
- Performance or security implications

---

## Best Practices

### 1. Atomic Commits

Each commit should represent **one logical change**.

**Good:**
```
feat: add user authentication
fix: resolve database connection leak
docs: update API documentation
```

**Bad:**
```
feat: add authentication, update docs, and fix database bug
```

### 2. Commit Frequency

- Commit **frequently** (multiple times per day)
- Keep commits **small and focused**
- Make commits **easy to review**
- Each commit should be independently testable

```
✅ Small, focused commits:
  - feat: add email validation
  - test: add email validation tests
  - fix: handle edge case in parser
  
❌ Large, multi-purpose commit:
  - feat: add email, refactor parser, update docs
```

### 3. No Generic Messages

Avoid:
```
❌ update
❌ changes
❌ fix stuff
❌ minor changes
❌ wip (work in progress)
❌ updates to files
❌ misc
```

### 4. Work in Progress (WIP)

If a commit is incomplete, mark it clearly:

```
chore: wip scheduler refactor
```

**Important:** WIP commits should **never be merged** to main branch.

### 5. No Merging Until Ready

Before merging:
- ✅ Commit messages are clear
- ✅ Commits are logically grouped
- ✅ CI/CD passes
- ✅ Code review approved
- ✅ No WIP commits

### 6. Meaningful Scope Usage

**Use scope for clarity:**
```
feat(authentication): implement JWT token refresh
fix(parser): handle escaped quotes in strings
refactor(cache): improve eviction policy
```

**Don't use scope for everything:**
```
feat(src): add authentication  # Too vague
fix(file.cc): fix bug          # Implementation detail
```

---

## Examples

### Good Commit Messages

```
feat: implement exponential backoff retry logic
fix: prevent division by zero in statistics module
docs: add deployment guide for Ubuntu 20.04
test: add edge case tests for empty input validation
refactor: extract database connection logic
style: apply code formatter to entire codebase
perf: reduce memory usage by 25% in data processor
ci: configure automated code coverage reporting
config: update CMake minimum version to 3.16
script: automate database migration process
chore: upgrade Catch2 to version 3.0
release: version 1.5.0
```

### With Scope

```
feat(auth): implement multi-factor authentication
fix(api): resolve timeout on large requests
docs(install): clarify Ubuntu-specific requirements
test(core): add comprehensive error handling tests
refactor(utils): simplify string utility functions
style(headers): fix include guard formatting
perf(cache): optimize key lookup time
ci(github): add GitHub Actions workflow
config(cmake): update compiler flags
script(deploy): create production deployment tool
```

### Multi-Type

```
feat,test: implement validation with full test coverage
docs,refactor: improve documentation and code clarity
fix,perf: resolve memory leak and improve performance
```

### With Body

```
feat(scheduler): implement priority queue for task execution

Previously, tasks were executed FIFO. Now implement priority queue
to handle urgent tasks first. This improves system responsiveness
for critical operations.

- Use std::priority_queue from STL
- O(log n) insertion and removal
- Maintains backward compatibility with existing interface

Closes #128
```

### Bad Examples

```
❌ Fixed bug
❌ Updated code
❌ Changes
❌ feat: added new stuff
❌ fix: fixing things
❌ feat(src): add authentication to system
❌ feat: Add Authentication.
❌ WIP - refactoring
❌ chore: stuff
```

---

## Definition of Done — Commit

A commit is correct and ready when:

- [ ] Message clearly describes **what** changed
- [ ] Message explains **why** (if non-obvious)
- [ ] Follows type convention (feat, fix, docs, etc.)
- [ ] Subject is imperative mood and lowercase
- [ ] Subject is under 110 characters
- [ ] No period at end of subject
- [ ] Scope is relevant and specific (if used)
- [ ] Commit is logically atomic
- [ ] Commit is not too broad or too narrow
- [ ] CI/CD pipeline passes
- [ ] Code review approved
- [ ] No WIP commits in main branch
- [ ] Commit history is clean and navigable

---

## Commit Message Checklist

Before committing, verify:

- [ ] Changes are logically related
- [ ] Subject line is in imperative mood
- [ ] Subject describes the change clearly
- [ ] Subject is concise (under 70 characters preferred)
- [ ] Type is appropriate (feat, fix, docs, etc.)
- [ ] Scope is used when helpful
- [ ] No generic messages ("update", "fix bug")
- [ ] No period at end of subject
- [ ] Body explains why (if needed)
- [ ] Body is wrapped at 80 characters
- [ ] Related issues are referenced
- [ ] CI passes before push
- [ ] Commit is not marked WIP unless appropriate

---

## Tools and Integration

### Commit Template

Create `.gitmessage` file in project root:

```
<type>(<scope>): <subject>

<body>

# Examples:
# feat(auth): implement two-factor authentication
# fix(api): resolve timeout on large requests
# docs: update installation guide

# <type> can be:
# feat, fix, docs, test, refactor, style, perf, ci, config, script, chore, release
```

Enable template in git config:

```bash
git config commit.template .gitmessage
```

### Pre-commit Hook

Create `.git/hooks/pre-commit` to validate commit messages:

```bash
#!/bin/bash
# Validate commit message format

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat $COMMIT_MSG_FILE)

# Check if message starts with valid type
if ! [[ $COMMIT_MSG =~ ^(feat|fix|docs|test|refactor|style|perf|ci|config|script|chore|release) ]]; then
  echo "Error: Commit message must start with a valid type"
  echo "Valid types: feat, fix, docs, test, refactor, style, perf, ci, config, script, chore, release"
  exit 1
fi

exit 0
```

Make executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

## Common Patterns

### Feature Development

```
feat(payment): add credit card processing
test(payment): add card validation tests
feat(payment): integrate payment gateway
docs(payment): document payment API
perf(payment): optimize payment processing
```

### Bug Fix with Testing

```
fix(parser): handle escaped characters correctly
test(parser): add escaped character edge cases
```

### Refactoring

```
refactor(core): extract common logic
test(core): ensure refactoring maintains behavior
```

### Documentation Update

```
docs: add architecture overview
docs: update API documentation
docs(install): clarify Ubuntu requirements
```

### Release Process

```
chore: bump version to 1.5.0
docs: update changelog for 1.5.0
release: version 1.5.0
```

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Git Best Practices](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

---

**Last Updated:** June 2026  
**Version:** 1.0
