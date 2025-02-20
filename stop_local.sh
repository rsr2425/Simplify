#!/bin/bash

echo "Stopping simplify container..."
docker stop simplify 2>/dev/null || true

echo "Removing simplify container..."
docker rm simplify 2>/dev/null || true

echo "Services stopped and cleaned up!" 