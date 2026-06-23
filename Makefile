# Tworzy worktree dla podanej gałęzi, jeśli jeszcze nie istnieje.
worktree:
	@if [[ -z "$(BRANCH_NAME)" ]]; then \
		echo "Błąd: ustaw BRANCH_NAME, np. make worktree BRANCH_NAME=worktree/branch/name." >&2; \
		exit 1; \
	fi
	@WORKTREE_DIR="$(WORKTREE_ROOT)/$$(echo "$(BRANCH_NAME)" | tr '/' '-')"; \
	mkdir -p "$(WORKTREE_ROOT)"; \
	if git worktree list --porcelain | grep -Fxq "branch refs/heads/$(BRANCH_NAME)"; then \
		echo "Worktree dla gałęzi $(BRANCH_NAME) już istnieje."; \
		exit 0; \
	fi; \
	if git show-ref --verify --quiet "refs/heads/$(BRANCH_NAME)"; then \
		git worktree add "$$WORKTREE_DIR" "$(BRANCH_NAME)"; \
	else \
		git worktree add -b "$(BRANCH_NAME)" "$$WORKTREE_DIR" develop; \
	fi; \
	echo "Utworzono worktree: $$WORKTREE_DIR (gałąź: $(BRANCH_NAME))."

# Przechodzi do istniejącego worktree, jeśli nie jest zajęte przez inną instancję.
switch-to-worktree:
	@if [[ -z "$(BRANCH_NAME)" ]]; then \
		echo "Błąd: ustaw BRANCH_NAME, np. make switch-to-worktree BRANCH_NAME=worktree/branch/name." >&2; \
		exit 1; \
	fi
	@if ! git show-ref --verify --quiet "refs/heads/$(BRANCH_NAME)"; then \
		echo "Błąd: podana gałąź nie istnieje: $(BRANCH_NAME)." >&2; \
		exit 1; \
	fi
	@WORKTREE_DIR="$$(git worktree list --porcelain | awk -v target="refs/heads/$(BRANCH_NAME)" '\
		$$1=="worktree" { path=$$2 } \
		$$1=="branch" && $$2==target { print path; exit }')"; \
	if [[ -z "$$WORKTREE_DIR" ]]; then \
		echo "Błąd: worktree dla gałęzi $(BRANCH_NAME) nie istnieje. Najpierw uruchom make worktree BRANCH_NAME=$(BRANCH_NAME)." >&2; \
		exit 1; \
	fi; \
	LOCK_FILE="$(WORKTREE_LOCKS_DIR)/$$(echo "$(BRANCH_NAME)" | tr '/' '-').lock"; \
	mkdir -p "$(WORKTREE_LOCKS_DIR)"; \
	if [[ -f "$$LOCK_FILE" ]]; then \
		LOCK_PID="$$(cat "$$LOCK_FILE")"; \
		if [[ -n "$$LOCK_PID" ]] && kill -0 "$$LOCK_PID" 2>/dev/null; then \
			echo "Błąd: worktree jest już zajęte przez inną instancję (PID: $$LOCK_PID)." >&2; \
			echo "Jak to zwolnić: zakończ proces o PID $$LOCK_PID (np. zamknij powłokę, która utrzymuje lock)." >&2; \
			exit 1; \
		fi; \
		rm -f "$$LOCK_FILE"; \
	fi; \
	echo "$$BASHPID" > "$$LOCK_FILE"; \
	cleanup() { rm -f "$$LOCK_FILE"; }; \
	trap cleanup EXIT INT TERM; \
	echo "Przełączono do $$WORKTREE_DIR. Aby zwolnić blokadę, zakończ tę powłokę."; \
	cd "$$WORKTREE_DIR"; \
	"$${SHELL:-/bin/bash}" -i