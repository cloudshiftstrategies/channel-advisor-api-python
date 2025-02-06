.PHONY: run-dev, docker-shell, docker-build, docker-run, test, test-functions, test-watch-functions, cdk-deploy, cdk-synth, test, test-snapshot-update, lint, fix, lint-fix

DIRS = channel_advisor_api
IMAGE = channel-advisor-catalog
BASE_DIR = channel_advisor_api

test:
	pytest --cov --cov-branch --cov-report=xml --cov-report=term-missing:skip-covered 

lint:
	flake8 --statistics

fix:
	black --line-length 120 .
	autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports --remove-duplicate-keys .

lint-fix: fix lint

version-noop:
	# Checks to see if the version will change
	semantic-release --noop version

version:
	# Checks to see if the version will change
	semantic-release version