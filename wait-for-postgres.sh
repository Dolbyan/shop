#!/bin/sh


until nc -z $1 $2; do
  echo "Czekam na PostgreSQL pod $1:$2..."
  sleep 1
done

echo "PostgreSQL jest gotowy! Uruchamiam aplikację..."