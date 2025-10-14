Domain 		: supportlab.local
ip			: 10.0.0.1
DNS			: 10.192.36.99
ocp cluster : ocp413

api vip		: api.ocp413.supportlab.local
ingress vip : *.apps.supportlab.local


disk.EnableUUID TRUE


systemctl stop firewalld
systemctl disable firewalld 
vim /etc/sellinu/conf 
	disbale

dnf install https -y
systemctl enable httpd
systemctl start httpd
systemctl status httpd
mkdir /var/www/html/ocp4/
chown -R apache: /var/www/html/ocp4/
chmod 755 /var/www/html/ocp4/
chcon -R -t httpd_sys_content_t /var/www/html/ocp4/

dnf insatll haproxy -y
setsebool -P haproxy_connect_any 1


dnf install nftables
systemctl enable nftables
systemctl start nftables
iptables -t nat -A POSTROUTING -o ens160 -j MASQUERADE ; ens160 external adapter
iptables -t nat -L -v -n
iptables -t nat -F


vim /etc/sysctl.conf 
	net.ipv4.ip_forward = 1


sudo coreos-installer install /dev/sda -u http://10.0.0.1:8080/ocp4/rhcos.raw.gz -I http://10.0.0.1:8080/ocp4/bootstrap.ign --insecure --insecure-ignition

sudo coreos-installer install /dev/sda -u http://10.0.0.1:8080/ocp4/rhcos.raw.gz -I http://10.0.0.1:8080/ocp4/master.ign --insecure --insecure-ignition

sudo coreos-installer install /dev/sda -u http://10.0.0.1:8080/ocp4/rhcos.raw.gz -I http://10.0.0.1:8080/ocp4/worker.ign --insecure --insecure-ignition