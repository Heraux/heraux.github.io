#!/bin/bash
# Minimal HTTP server using bash and netcat
PORT=8765
FILE="/c/Users/thefi/OneDrive/Desktop/CARD BLOCK/blockbrawl_dnb.html"
echo "Server running on port $PORT"
while true; do
  CONTENT=$(cat "$FILE")
  LEN=${#CONTENT}
  echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: $LEN\r\nConnection: close\r\n\r\n$CONTENT" | nc -l -p $PORT -q 1 2>/dev/null
done
