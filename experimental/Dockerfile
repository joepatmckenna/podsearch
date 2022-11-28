FROM --platform=linux/x86_64 python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
  curl \
  git \
  subversion \
  unzip

# clang \
# g++ \
# gnupg2 \
# wget

# RUN wget -nv -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
# RUN echo "deb http://apt.llvm.org/buster/ llvm-toolchain-buster-11 main" >> /etc/apt/sources.list
# RUN echo "deb-src http://apt.llvm.org/buster/ llvm-toolchain-buster-11 main" >> /etc/apt/sources.list
# RUN apt-get update
# RUN apt-get install clang-11

# clang \
# software-properties-common \

RUN python3 -m pip install --upgrade pip
RUN pip3 install tensorflow-io

ARG BAZEL_VERSION=5.3.2
ARG BAZEL_INSTALLER=bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh

RUN curl -OLsS https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/${BAZEL_INSTALLER} \
  && chmod +x ${BAZEL_INSTALLER} \
  && ./${BAZEL_INSTALLER} \
  && rm ${BAZEL_INSTALLER}

# ARG SCANN_COMMIT_ID=06604970e69f9f79a2ff32e07742890bcfc6c268

# PYTHON_BIN_PATH=$(which python3) \
#    CC=clang \

RUN svn checkout https://github.com/google-research/google-research/trunk/scann

RUN cd scann \
  && python3 configure.py \
  && bazel build \
       -c opt \
       --features=thin_lto \
       --copt=-mavx \
       --copt=-mfma \
       --cxxopt="-std=c++17" \
       --copt=-fsized-deallocation \
       --copt=-w \
       :build_pip_pkg


# RUN apt-get install -y software-properties-common curl gnupg rsync
# RUN apt install apt-transport-https curl gnupg

# RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg \
#     && sudo mv bazel-archive-keyring.gpg /usr/share/keyrings \
#     && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

# FROM ubuntu:18.04

# RUN apt-get update
# RUN apt-get install python3@3.9
#-y python3-numpy python3-scipy python3-pip build-essential git
# RUN pip3 install -U pip

# WORKDIR /home/app
# # COPY requirements.txt run_algorithm.py ./
# COPY requirements.txt ./
# RUN pip3 install -r requirements.txt

# # ENTRYPOINT ["python3", "-u", "run_algorithm.py"]

# # FROM ann-benchmarks

# RUN pip3 install --upgrade pip
# RUN pip3 install scann
# RUN python3 -c 'import scann'