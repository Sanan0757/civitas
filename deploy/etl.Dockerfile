FROM ubuntu:latest
LABEL authors="petrokvartsianyi"

ENTRYPOINT ["top", "-b"]
