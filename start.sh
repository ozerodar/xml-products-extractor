#!/bin/bash

uvicorn --host 0.0.0.0 --port 8000 app.api.main:app
