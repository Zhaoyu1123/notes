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
