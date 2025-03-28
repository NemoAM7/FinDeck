#!/bin/bash
echo "Monitoring data exploration server logs (press Ctrl+C to exit)"
echo "====================================================="
echo ""

if [ -f server/logs/data_exploration.log ]; then
    tail -f server/logs/data_exploration.log
else
    echo "Log file not found. Make sure the server has been started."
    exit 1
fi 