# Builds Docker image after some modifications to current directory

cp -r ../../../lib .
docker build -t base-infer -f Dockerfile .
rm -rf lib/
