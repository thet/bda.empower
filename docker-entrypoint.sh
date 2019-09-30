#!/bin/bash
set -e

COMMANDS="debug help logtail show stop adduser fg kill quit run wait console foreground logreopen reload shell status"
START="start restart"
CMD="su-exec plone /plone/bin/instance"

echo "Plone Control Script"

if [[ $START == *"$1"* ]]; then
  _stop() {
    $CMD stop
    kill -TERM $child 2>/dev/null
  }

  trap _stop SIGTERM SIGINT
  $CMD console &

  child=$!
  wait "$child"
else
  if [[ $COMMANDS == *"$1"* ]]; then
    exec bin/instance "$@"
  fi
  exec "$@"
fi
