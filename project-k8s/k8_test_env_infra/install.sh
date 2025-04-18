export K8S_VERSION="1.29"
sudo hostnamectl set-hostname "k8s-master"

sudo bash -c 'cat >> /etc/hosts << EOF
10.192.36.5  k8s-master1
10.192.36.6  k8s-master2
10.192.36.7  k8s-worker1
10.192.36.8  k8s-worker2
EOF'
sudo swapoff -a
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# sysctl params required by setup, params persist across reboots
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
# Apply sysctl params without reboot
sudo sysctl --system

sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip that package
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
curl -fsSL https://pkgs.k8s.io/core:/stable:/v$K8S_VERSION/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
# This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v$K8S_VERSION/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl


# sudo apt install runc
sudo apt-get download runc
sudo dpkg -i runc*
wget https://github.com/containerd/containerd/releases/download/v1.7.24/containerd-1.7.24-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local containerd-1.7.24-linux-amd64.tar.gz

sudo mkdir -p /usr/local/lib/systemd/system/
sudo bash -c 'cat > /usr/local/lib/systemd/system/containerd.service << EOF
# Copyright The containerd Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

[Unit]
Description=containerd container runtime
Documentation=https://containerd.io
After=network.target local-fs.target dbus.service

[Service]
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/containerd

Type=notify
Delegate=yes
KillMode=process
Restart=always
RestartSec=5

# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNPROC=infinity
LimitCORE=infinity

# Comment TasksMax if your systemd version does not supports it.
# Only systemd 226 and above support this version.
TasksMax=infinity
OOMScoreAdjust=-999

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload 
sudo systemctl enable --now containerd
sudo systemctl status containerd.service

sudo mkdir /etc/containerd
sudo sh -c "containerd config default > /etc/containerd/config.toml"
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml 
sudo systemctl restart containerd.service
sudo systemctl enable containerd
sudo systemctl restart kubelet.service
sudo systemctl status kubelet.service

sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --control-plane-endpoint=10.192.36.5:6443 --apiserver-advertise-address=10.192.36.5 --apiserver-cert-extra-sans=k8master.supportlab.infoblox.com

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

#Installing kubeneter networking

# curl https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/calico.yaml -O
curl https://raw.githubusercontent.com/projectcalico/calico/refs/heads/release-v3.29/manifests/calico.yaml -O
kubectl create -f calico.yaml



#  sudo kubeadm init phase kubeconfig admin
kubeadm init phase upload-certs --upload-certs
 kubeadm token create --print-join-command --certificate-key 995179030861bb03af133ac124ad7fd536ab2302169eb42be0a06109a26d8723
kubectl edit cm -n kube-system kubeadm-config
        controlPlaneEndpoint : "10.192.36.5:6443"