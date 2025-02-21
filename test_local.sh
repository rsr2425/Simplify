#!/bin/bash

# Colors and formatting
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'
DIVIDER="=================================================================="

echo -e "\n${BLUE}${DIVIDER}"
echo -e "${BOLD}🔨 BUILD PHASE"
echo -e "${BLUE}${DIVIDER}${NC}"

# Build test image
echo -e "${YELLOW}Building test image...${NC}"
docker build -t simplify-test -f Dockerfile.test .

echo -e "\n${BLUE}${DIVIDER}"
echo -e "${BOLD}🧪 FRONTEND TESTS"
echo -e "${BLUE}${DIVIDER}${NC}"

# Run frontend tests
echo -e "${YELLOW}Running frontend tests...${NC}"
docker run simplify-test npm test --prefix frontend

echo -e "\n${BLUE}${DIVIDER}"
echo -e "${BOLD}🐍 BACKEND TESTS"
echo -e "${BLUE}${DIVIDER}${NC}"

# Run backend tests
echo -e "${YELLOW}Running backend tests...${NC}"
docker run --env-file .env simplify-test pytest backend/tests

echo -e "\n${GREEN}✨ Testing complete!${NC}\n" 