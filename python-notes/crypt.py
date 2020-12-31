1.分类

加密算法首先分为两种：单向加密、双向加密。
单向加密是不可逆的，也就是只能加密，不能解密。通常用来传输类似用户名和密码，直接将加密后的数据提交到后台，因为后台不需要知道用户名和密码，可以直接将收到的加密后的数据存储到数据库。
双向加密算法通常分为对称性加密算法和非对称性加密算法，对于对称性加密算法，信息接收双方都需事先知道密匙和加解密算法且其密匙是相同的，之后便是对数据进行 加解密了。非对称算法与之不同，发送双方A,B事先均生成一堆密匙，然后A将自己的公有密匙发送给B，B将自己的公有密匙发送给A，如果A要给B发送消 息，则先需要用B的公有密匙进行消息加密，然后发送给B端，此时B端再用自己的私有密匙进行消息解密，B向A发送消息时为同样的道理。
2.常用算法

几种对称性加密算法：AES,DES,3DES

DES是一种分组数据加密技术（先将数据分成固定长度的小数据块，之后进行加密），速度较快，适用于大量数据加密，而3DES是一种基于DES的加密算法，使用3个不同密匙对同一个分组数据块进行3次加密，如此以使得密文强度更高。

相较于DES和3DES算法而言，AES算法有着更高的速度和资源使用效率，安全级别也较之更高了，被称为下一代加密标准。

几种非对称性加密算法：RSA,DSA,ECC

RSA和DSA的安全性及其它各方面性能都差不多，而ECC较之则有着很多的性能优越，包括处理速度，带宽要求，存储空间等等。

几种线性散列算法（签名算法）：MD5,SHA1,HMAC

这几种算法只生成一串不可逆的密文，经常用其效验数据传输过程中是否经过修改，因为相同的生成算法对于同一明文只会生成唯一的密文，若相同算法生成的密文不同，则证明传输数据进行过了修改。通常在数据传说过程前，使用MD5和SHA1算法均需要发送和接收数据双方在数据传送之前就知道密匙生成算法，而HMAC与之不同的是需要生成一个密匙，发送方用此密匙对数据进行摘要处理（生成密文），接收方再利用此密匙对接收到的数据进行摘要处理，再判断生成的密文是否相同。

3.加密算法选用

对于各种加密算法的选用：

由于对称加密算法的密钥管理是一个复杂的过程，密钥的管理直接决定着他的安全性，因此当数据量很小时，我们可以考虑采用非对称加密算法。

在实际的操作过程中，我们通常采用的方式是：采用非对称加密算法管理对称算法的密钥，然后用对称加密算法加密数据，这样我们就集成了两类加密算法的优点，既实现了加密速度快的优点，又实现了安全方便管理密钥的优点。

如果在选定了加密算法后，那采用多少位的密钥呢？一般来说，密钥越长，运行的速度就越慢，应该根据的我们实际需要的安全级别来选择，一般来说，RSA建议采用1024位的数字，ECC建议采用160位，AES采用128为即可。

对于几种加密算法的内部实现原理，有兴趣的可以细细研究。而对于其实现而言，网上有很多开源版本，比较经典的是PorlaSSL（官网：http://en.wikipedia.org/wiki/PolarSSL ）。其它语言如JAVA,OBJC也都有相应的类库可以使用。


交互流程：

客户端上传数据加密 A

客户端随机产生一个16位的字符串，用以之后AES加密的秘钥，AESKey。
使用RSA对AESKey进行公钥加密，RSAKey
我们一般取其中的关键字段(别人可能修改的字段)，比如此时step，和time及memberId，都比较敏感。获取step，time，memberId，拼接成一个字符串(顺序和服务器约定好)，然后使用md5加密，采用base64编码(编码格式和服务约定)。得到signData,然后将获取到的signData以key-value的形式保存到原来明文的数据包中，
将明文的要上传的数据包(字典/Map)转为Json字符串，使用AESKey加密，得到JsonAESEncryptedData。
封装为{key : RSAKey, value : JsonAESEncryptedData}的字典上传服务器，服务器只需要通过key和value，然后解析，获取数据即可。

服务器获取数据解密 B

获取到RSAKey后用服务器私钥解密，获取到AESKey
获取到JsonAESEncriptedData，使用AESKey解密，得到明文的客户端上传上来的数据。
按照喝客户端约定的字段拼接，将得到的step，time，memberId拼接后，使用同样的md5_base64处理，然后比较数据包中的签名sign是否和客户端当时的签名一致。如果一致，接受数据。不一致，抛弃数据，终止本次操作

