#!/bin/bash

echo "🚀 Running unit tests with coverage..."
pytest tests \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=html \
  -v || exit 1

echo "✅ Running flake8 linter..."
flake8 app tests || exit 1

echo "✅ Running black formatting check..."
black --check app tests || exit 1

echo "🎉 All tests and lint checks passed!"
