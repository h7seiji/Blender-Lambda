FROM public.ecr.aws/amazonlinux/amazonlinux:2023

ARG BLENDER_DOWNLOAD_URL = "https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz"
ARG FUNCTION_DIR="/var/task"
ARG BLENDER_DIR="${FUNCTION_DIR}/blender"
RUN mkdir -p ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

# Basic dependencies
RUN dnf update -y
RUN dnf install -y openssl-devel bzip2-devel libffi-devel zlib-devel python3-pip

# Lambda Python dependencies
RUN pip install setuptools boto3
RUN pip install --target ${FUNCTION_DIR} awslambdaric

# Blender dependencies
RUN dnf install -y \
    glibc \
    libX11 \
    libXxf86vm \
    libXcursor \
    libXi \
    libXrandr \
    libXinerama \
    mesa-libGL \
    libwayland-client \
    wayland-protocols-devel \
    libxkbcommon \
    dbus \
    libSM
RUN curl -SL {BLENDER_DOWNLOAD_URL} | tar -Jx -C ${BLENDER_DIR} --strip-components=1
ENV PATH="${PATH}:${BLENDER_DIR}"

COPY src ${FUNCTION_DIR}/src

COPY requirements.txt ${FUNCTION_DIR}

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "-m", "awslambdaric" ]

CMD [ "src/blender.handler" ]
