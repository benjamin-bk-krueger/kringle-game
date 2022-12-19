# Python venv
export PATH=~/venv/bin:$PATH

# Default credentials, need to be changed on production stage
export POSTGRES_HOST=kringle_database
export POSTGRES_PORT=5432
export POSTGRES_USER=kringle
export POSTGRES_PW=kringle
export POSTGRES_DB=kringle
export S3_FOLDER=http://minio:9000/kringle-public
