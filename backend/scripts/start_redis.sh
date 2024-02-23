#!/bin/bash
# first run chmod +x start_redis.sh to make the file executable
# Run redis-server in a new terminal
osascript -e 'tell app "Terminal"
    do script "redis-server --port 6379"
end tell'

# Wait for a moment to ensure that redis-server has started
sleep 1

# Run redis-cli in a new terminal
osascript -e 'tell app "Terminal"
    do script "redis-cli"
end tell'
