# Run Celery worker in a new terminal
osascript -e 'tell app "Terminal"
    do script "cd /Users/indra/Programming/Library_Management_System/backend && source myenv/bin/activate && celery -A tasks worker"
end tell'

# Run Celery beat in a new terminal
osascript -e 'tell app "Terminal"
    do script "cd /Users/indra/Programming/Library_Management_System/backend && source myenv/bin/activate && celery -A tasks beat"
end tell'