FROM ubuntu:24.04

RUN apt-get update
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    software-properties-common

RUN add-apt-repository ppa:git-core/ppa
RUN apt-get update

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    ccache \
    zsh \
    curl \
    wget \
    lsb-release \
    wget \
    software-properties-common \
    ninja-build \
    gcc \
    python3-full \
    python3-pip \
    cmake \
    build-essential \
    git \
    gcc-11 \
    g++-11

RUN apt-get purge -y --auto-remove llvm clang python3-lldb-14
RUN wget https://apt.llvm.org/llvm.sh
RUN chmod +x llvm.sh
RUN ./llvm.sh 17 all

RUN update-alternatives --install /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-17 17

RUN python3 -m venv /venv
RUN /venv/bin/pip install conan
RUN /venv/bin/pip install cmake-format
RUN /venv/bin/pip install gcovr 
