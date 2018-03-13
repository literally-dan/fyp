FROM frolvlad/alpine-python3:latest

RUN apk -U add bash openssh curl nmap tcpdump netcat-openbsd && \
  for key in rsa dsa ecdsa ed25519; do \
    ssh-keygen -f /etc/ssh/ssh_host_${key}_key -N '' -t ${key}; \
  done && \
  echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
  echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
  echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
  passwd -d root

COPY . .
RUN pip3 install -r src/requirements.txt
