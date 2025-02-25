#!/bin/bash

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'
DIVIDER="=================================================================="

echo -e "\n${BLUE}${DIVIDER}"
echo -e "${BOLD}🧹 DOCKER CLEANUP"
echo -e "${BLUE}${DIVIDER}${NC}"

# Stop all running containers
echo -e "\n${YELLOW}Stopping all running containers...${NC}"
docker stop $(docker ps -q) 2>/dev/null || echo -e "${RED}No running containers found${NC}"

# Remove all stopped containers
echo -e "\n${YELLOW}Removing stopped containers...${NC}"
docker container prune -f

# Remove unused images
echo -e "\n${YELLOW}Removing unused images...${NC}"
docker image prune -f

# Remove unused networks
echo -e "\n${YELLOW}Removing unused networks...${NC}"
docker network prune -f

# Remove unused volumes
echo -e "\n${YELLOW}Removing unused volumes...${NC}"
docker volume prune -f

echo -e "\n${GREEN}✨ Cleanup complete!${NC}"
echo -e "${YELLOW}Summary of available Docker resources:${NC}"
echo -e "\n${BOLD}Containers:${NC}"
docker ps -a
echo -e "\n${BOLD}Images:${NC}"
docker images
echo -e "\n" 