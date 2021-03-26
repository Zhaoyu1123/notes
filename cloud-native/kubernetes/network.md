### 容器网络模型

#### bridge模式

bridge模式是Docker默认的网络设置，此模式会为每一个容器分配Network Namespace、设置IP等，并将一个主机上的Docker容器连接到一个虚拟网桥上。

#### host模式

Docker使用的网络实际上和宿主机一样，在容器内看到的网卡ip是宿主机上的ip。容器的时候使用host模式，那么这个容器将不会获得一个独立的Network Namespace，而是和宿主机共用一个Network Namespace。容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口。

#### container模式

多个容器使用共同的网络看到的ip是一样的，这个模式指定新创建的容器和已经存在的一个容器共享一个Network Namespace，而不是和宿主机共享。新创建的容器不会创建自己的网卡，配置自己的IP，而是和一个指定的容器共享IP、端口范围等。
#### none模式

这种模式下不会配置任何网络。这个模式和前两个不同。在这种模式下，Docker容器拥有自己的Network Namespace，但是，并不为Docker容器进行任何网络配置。也就是说，这个Docker容器没有网卡、IP、路由等信息。需要我们自己为Docker容器添加网卡、配置IP等。

### Kubernetes 集群网络

分为四种不同的网络问题需要解决：

1. 高度耦合 容器-容器 通信 (同一个 Pod 内的不同容器)
2. Pod 间通信 (同一个节点和不同节点)
3. Pod 和 Service 间通信
4. 外部 和 Service 间通信

#### 同节点 POD 间通信

同一节点两个 POD 信息展示

    [root@k8s-master ~]# kubectl --namespace=hyjx--hyjx-group3 get pods -o wide
    NAME                READY     STATUS    RESTARTS   AGE       IP            NODE
    mysql-demo-e81sy    1/1       Running   0          23h       10.20.92.11   k8s-node2
    wp-frontend-0rlk4   1/1       Running   0          1d        10.20.92.3    k8s-node2
    
分别查看pod内的路由表：

    [root@k8s-node2 ~]# docker exec -it `docker ps |grep -v POD |grep mysql-demo-e81sy |awk '{print $1}'` ip route list
    default via 10.20.92.1 dev eth0
    10.20.92.0/24 dev eth0 proto kernel scope link src 10.20.92.11
     
    [root@k8s-node2 ~]# docker exec -it `docker ps |grep -v POD |grep wp-frontend-0rlk4 |awk '{print $1}'` ip route list
    default via 10.20.92.1 dev eth0
    10.20.92.0/24 dev eth0 proto kernel scope link src 10.20.92.3

对应路由，目的地址为 10.20.92.0/24（本机docker0网桥的地址）的数据包都会通过容器内的 eth0（veth设备）直接转给 Kernel，因为 veth 设备都是成对存在的，另一端连在 docker0 网桥上，所以会由 Kernel 直接转发给 docker0 网桥上的另一个veth设备。

    10.20.92.0/24 dev eth0  proto kernel  scope link  src 10.20.92.3

宿主机上的路由表：

    [root@k8s-node2 ~]# ip route list
    default via 192.168.128.1 dev eth0  proto static  metric 100
    10.20.0.0/16 dev flannel0  proto kernel  scope link  src 10.20.92.0
    10.20.92.0/24 dev docker0  proto kernel  scope link  src 10.20.92.1
    192.168.122.0/24 dev virbr0  proto kernel  scope link  src 192.168.122.1
    192.168.128.0/20 dev eth0  proto kernel  scope link  src 192.168.138.222  metric 100
     
    [root@k8s-node2 ~]# netstat -rn
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
    0.0.0.0         192.168.128.1   0.0.0.0         UG        0 0          0 eth0
    10.20.0.0       0.0.0.0         255.255.0.0     U         0 0          0 flannel0
    10.20.92.0      0.0.0.0         255.255.255.0   U         0 0          0 docker0
    192.168.122.0   0.0.0.0         255.255.255.0   U         0 0          0 virbr0
    192.168.128.0   0.0.0.0         255.255.240.0   U         0 0          0 eth0

#### veth pair

Virtual Ethernet Pair简称 veth pair,是一个成对的端口,所有从这对端口一 端进入的数据包都将从另一端出来,反之也是一样.

    #创建veth pair
    [root@centos ~]# ip link add tap1 type veth peer name tap2
    #创建namespace：ns1和ns2
    [root@centos ~]# ip netns add ns1
    [root@centos ~]# ip netns add ns2
    #把两个tap分别迁移到对应的namespace中去
    [root@centos ~]# ip link set tap1 netns ns1
    [root@centos ~]# ip link set tap2 netns ns2
    #分别给两个tap绑定IP
    [root@centos ~]# ip netns exec ns1 ip addr add local 192.168.50.1/24 dev tap1
    [root@centos ~]# ip netns exec ns2 ip addr add local 192.168.50.2/24 dev tap2
    #将两个tap设置为up
    [root@centos ~]# ip netns exec ns1 ifconfig tap1 up
    [root@centos ~]# ip netns exec ns2 ifconfig tap2 up
    #ping测试
    [root@centos ~]# ip netns exec ns2 ping 192.168.50.1
    PING 192.168.50.1 (192.168.50.1) 56(84) bytes of data.
    64 bytes from 192.168.50.1: icmp_seq=1 ttl=64 time=0.051 ms
    64 bytes from 192.168.50.1: icmp_seq=2 ttl=64 time=0.025 ms
    64 bytes from 192.168.50.1: icmp_seq=3 ttl=64 time=0.027 ms
    
   
#### 不同Node上的pod之间的通信

1. 整个kubernetes集群中对每个POD分配一个唯一的IP：在部署Kubernetes时，对每个Node节点的docker0网桥的网段重新划分，用户设定一个大的网段（eg：10.20.0.0/16），存在etcd中，每个节点的flanneld会去etcd中查找这个值，然后，flanneld随机生成一个属于大网段的，且不冲突的子网（eg: 10.20.37.0/24; 10.20.92.0/24; 10.20.0.53/24）并将该值写回etcd中，这样就保证了每个pod的IP都会在10.20.0.0/16这个网段内；
2. Node节点之间需要架设一个overlay网络（一般通过flannel实现），保证pod可以互相访问。
   
POD 信息展示

    [root@k8s-master ~]# kubectl --namespace=hyjx--hyjx-group3 get pods -o wide
    NAME                READY     STATUS    RESTARTS   AGE       IP            NODE
    wp-mysql-t5w0m      1/1       Running   0          2d        10.20.37.5    k8s-node1
    mysql-demo-e81sy    1/1       Running   0          1d        10.20.92.11   k8s-node2
   
例如，k8s-node1（192.168.138.221/20）上的pod（src=10.20.37.5/24）要发送目的地址为dest=10.20.92.11/24的数据包。

Node1 的路由表:

    [root@k8s-node1 ~]# netstat -rn
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
    0.0.0.0         192.168.128.1   0.0.0.0         UG        0 0          0 eth0
    10.20.0.0       0.0.0.0         255.255.0.0     U         0 0          0 flannel0
    10.20.37.0      0.0.0.0         255.255.255.0   U         0 0          0 docker0
    192.168.122.0   0.0.0.0         255.255.255.0   U         0 0          0 virbr0
    192.168.128.0   0.0.0.0         255.255.240.0   U         0 0          0 eth0

dest=10.20.92.11/24匹配第二条路由表，目的地址为10.20.0.0/16的数据包要交给flannel0网桥处理，flanneld会到etcd中查找10.20.92.11/24所在的node节点的IP（192.168.139.222/20）：

    
    [root@k8s-master ~]# etcdctl get /awcloud.com/network/config
    {"NetWork":"10.20.0.0/16"}
    [root@k8s-master ~]# etcdctl ls /awcloud.com/network/subnets
    /awcloud.com/network/subnets/10.20.92.0-24
    /awcloud.com/network/subnets/10.20.100.0-24
    /awcloud.com/network/subnets/10.20.53.0-24
    /awcloud.com/network/subnets/10.20.37.0-24
     
    [root@k8s-master ~]# etcdctl get /awcloud.com/network/subnets/10.20.92.0-24
    {"PublicIP":"192.168.138.222"}

在目的Node节点，flanneld收到数据包后，去除flanneld加上的头部，将原始的数据包发送到宿主机的网络栈里面，这时的数据包src=10.20.37.5/24，dest=10.20.92.11/24；
然后flanneld在原来的数据包的基础上，重新封装成UDP数据包，加上UDP的头部（src=192.168.138.221/20:8285, dest=192.168.138.222/20:8285，flannel 默认使用 8285 端口作为 UDP 封装报文的端口，VxLan 的话使用 8472 端口）直接发送给192.168.138.222:8285（8285是flanneld监听的端口）。

Node2 路由表：

    [root@k8s-node2 ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.128.1   0.0.0.0         UG    100    0        0 eth0
    10.20.0.0       0.0.0.0         255.255.0.0     U     0      0        0 flannel0
    10.20.92.0      0.0.0.0         255.255.255.0   U     0      0        0 docker0
    192.168.122.0   0.0.0.0         255.255.255.0   U     0      0        0 virbr0
    192.168.128.0   0.0.0.0         255.255.240.0   U     100    0        0 eth0

dest=10.20.92.11/24优先匹配第三条路由规则，将数据包转发给docker0网桥上，docker0网桥再将数据包转给IP为10.20.92.11/24的POD中，响应数据包反之。