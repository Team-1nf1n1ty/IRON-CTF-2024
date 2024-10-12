# Use the official Ubuntu 18.04 image as the base
FROM ubuntu:18.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages: build-essential (for gcc, g++), and any other tools you might need
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    make \
    gdb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a directory for the source code
WORKDIR /src

# Copy the source code into the container
COPY blind.c .

# Compile the source code
RUN gcc blind.c -o blind -no-pie -Wl,-z,relro,-z,now

# Specify the default command to run
CMD ["./blind"]

