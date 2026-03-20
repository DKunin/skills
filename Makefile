SHELL := /bin/bash

.PHONY: validate
validate:
	./scripts/validate-skills.sh

.PHONY: new-skill
new-skill:
	@test -n "$(NAME)" || (echo "NAME is required" && exit 1)
	@test -n "$(DESCRIPTION)" || (echo "DESCRIPTION is required" && exit 1)
	./scripts/new-skill.sh "$(NAME)" "$(DESCRIPTION)"
