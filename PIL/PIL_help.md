## 1. 基础使用

`OpenSSH` 是 SSH协议的流行的免费开源实现。`OpenSSH`提供了服务端程序(`openssh-server`)和客户端工具(`openssh-client`)。

UNIX 平台系统（Linux/MacOS）等一般都默认安装了 SSH 客户端，直接在终端中使用SSH命令即可，Windows 等其它平台则需要手动安装 SSH 客户端，较常用的Windows SSH客户端有`Putty`和`XShell`等。

```bash
# 安装服务端/客户端(Ubuntu/Debian)
$ sudo apt install openssh-server/openssh-client

# 查看ssh服务是否开启
$ netstat -tlp | grep ssh

# 启动/停止/重启 ssh服务
$ sudo /etc/init.d/ssh start/stop/restart
```

SSH服务端配置文件默认为`/etc/ssh/sshd_config`，可以按需修改默认`22`端口等配置。



```bash
# 命令格式
$ ssh [-options] [user@hostname]
```

| options | 含义                               |
| ------- | ---------------------------------- |
| `-p`    | 指定ssh端口号,默认端口为`22`       |
| `-i`    | 使用指定私钥文件连接服务器免密登录 |

- `user`远程服务器登录的用户名，默认为当前用户
- `hostname`远程服务器地址。可以是IP/域名/别名
- `exit`或`logout`命令均可退出当前登录



```bash
# 以colin用户登录192.168.1.196的到ssh服务器
$ ssh colin@192.168.1.196

# 以colin用户登录到192.168.1.198的ssh服务器，使用2222端口
$ ssh -p 2222 colin@192.168.1.198
```

## 2. SSH高级配置

SSH配置信息一般保存在`~/.ssh` 目录下。

| 配置文件          | 作用                                                         |
| ----------------- | ------------------------------------------------------------ |
| `known_hosts`     | 作为客户端。记录曾连接服务器授权。SSH第一次连接一台服务器会有一个授权提示，确认授权后会记录在此文件中，下次连接记录中的服务器时则不再需要进行授权确认提示 |
| `authorized_keys` | 作为服务端。客户端的免密连接公钥文件                         |
| `config`          | 作为客户端。记录连接服务器配置的别名                         |

### 2.1 服务器别名

远程管理命令(如`ssh`,`scp`等)连接一台服务器时一般都需要提供 服务器地址、端口、用户名 ，每次输入比较繁琐，我们可以把经常使用的服务器连接参数打包记录到配置文件中并为其设置一个简单易记的别名。这样我们就可以通过别名方便的访问服务器，而不需要提供地址、端口、用户名等信息了。

配置方法如下：

- 创建或打开 `~/.ssh/config`，在文件追加服务器配置信息

- 一台服务器配置格式如下

  

  ```json
  Host ColinMac
    HostName 192.168.1.196
    User colin
    Port 22
  ```

  以上配置中只有`HostName`是必选项，其他都可按需省略。

配置完成后远程管理命令中就可以直接使用别名访问了。



```sh
$ ssh ColinMac
$ scp abc.txt ColinMac:Desktop
```

### 2.2 免密登录



```
# 命令格式
$ ssh-keygen [-options]
```

| options | 含义                                                         |
| ------- | ------------------------------------------------------------ |
| `-t`    | 指定加密类型,默认为非对称加密(`rsa`), 所有可选项`[dsa,ecdsa,ed25519,rsa]` |
| `-f`    | 密钥文件名。                                                 |
| `-C`    | 注释，将附加在密钥文件尾部                                   |

- 远程管理命令(如`ssh`,`scp`等)每次都需要提供用户密码保证安全。除此之外，我们也可配置使指定加密算法验证密钥文件的方式，避免每次输入密码
- 配置免密登录后，`ssh`连接和`scp`等远程管理命令都不需要再输密码
- 生成密钥时若指定了文件名，连接服务器时需要通过`-i`指定要验证的密钥文件,形如：`ssh -i file user@host`。默认文件名则可省略
- 默认配置只需以下两步：



```sh
# 客户端生成密钥对
$ ssh-keygen

# 上传公钥到服务器
$ ssh-copy-id user@hostname   # 文件会自动上传为服务器特定文件 ～/.ssh/authorized_keys
```

完成以上步骤后直接使用`ssh ColinUbuntu`即可登录，服务器地址和密码均不用录入。

### 2.3 免密钥文件登录

出于安全考虑，大部分服务器提供商如要求使用密钥文件进行远程登录，如`GCP`和`AWS`。下面我们以`GCP`为例来看如何简化连接操作,这搞起来吧...

#### 2.3.1 生成密钥对



```sh
$ ssh-keygen -t rsa -f ~/.ssh/[KEY_FILENAME] -C [USERNAME]
$ chmod 400 ~/.ssh/[KEY_FILENAME]
```

[cloud.google.com/compute/docs/instances/add..](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#createsshkeys)

#### 2.3.2 上传公钥

在`Compute Engine`页面左侧菜单找到`元数据`,将上一步生成的公钥文件(`KEY_FILENAME_pub`)内容添加到SSH密钥中即可。

![GCP上传密钥](https://cdn.hashnode.com/res/hashnode/image/upload/v1658765499770/lKWhgchbf.jpg?auto=compress,format&format=webp)

#### 2.3.3 连接GCP

使用以下命令登录即可



```sh
$ ssh -i ~/.ssh/KEY_FILENAME [USERNAME]@[IP_ADDRESS]
```

#### 2.3.4 简化登录

以上是`GCP`官方步骤，使用`IdentityFile`方式进行登录，每次登录都要通过`-i`选项指定私钥路径比较繁琐，我们可以将密钥文件添加到`ssh`客户端`config`中以简化连接命令。



```json
Host *
 AddKeysToAgent yes
 UseKeychain yes  # only for mac

Host tu
   HostName IP_ADDRESS
   Port 22
   User USERNAME
   IdentityFile ~/.ssh/gcp
```

按照以上配置添加到`～/.ssh/config`中



```sh
# 后台运行ssh-agent
$ eval "$(ssh-agent -s)"
# 添加密钥到ssh-agent
$ ssh-add -K ~/.ssh/gcp
```

完成以上配置后，连接服务器只需使用 `ssh tu`即可。

> 除了连接云服务器，`GitHub`等服务也可是通过以上方式连接

## 3. SCP命令

`scp`是`secure copy`缩写，它基于SSH实现远程文件拷贝。`scp`命令只能在UNIX内核系统(如Linux/mac OS) 中运行。在Windows中文件传输推荐使用FTP工具，如`FileZilla`等。



```sh
# 命令格式
$ scp [-options] [[user@]host1:]file1 [[user@]host2:]file2
```

| options | 含义                                     |
| ------- | ---------------------------------------- |
| `-r`    | 远程拷贝文件或递归拷贝目录               |
| `-P`    | 指定远程服务器端口号，默认22端口可以省略 |



```sh
# 将本地123.txt远程拷贝到192.168.1.196服务器的colin用户的Desktop目录并重命名为test.txt
$ scp 123.txt colin@192.168.1.196:Desktop/test.txt

# 将192.168.1.196服务器的colin用户的Desktop/test.txt远程拷贝到本地当前目录并重命名为123.txt
$ scp conlin@192.168.1.196:Desktop/test.txt 123.txt

# 将本地~/Desktop/Python拷贝到192.168.1.196服务器的colin用户的Desktop目录下
$ scp -r ~/Desktop/Python colin@192.168.1.196:Desktop
```









