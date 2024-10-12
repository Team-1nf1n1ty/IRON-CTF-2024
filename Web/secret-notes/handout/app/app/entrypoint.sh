#!/bin/sh
python3 -m flask run --host=0.0.0.0 &
sleep 5  # Adjust sleep as necessary to ensure the server is up
wait