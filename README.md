## Deployment
Run on server:
* Local
```
sh run_dev.sh
```
* Test
```
sh deploy.sh
```
* Prod
```
sh deploy_prod.sh
```

### Install requirements:
1. Python 3.9+
2. Pip 22+
3. virtualenv

Kiểm tra môi trường:
```shell
### Check version
$ python --version
$ python3.9 --version
$ pip --version
$ virtualenv --version

### Check installation path
$ which pip
$ which python
$ which virtualenv
...
```

Cài đặt các packages còn thiếu sau:
```shell
### Install Python 3.9 in CentOS 7
$ sudo add-apt-repository ppa:jonathonf/python-3.9
$ sudo yum update
$ sudo apt install python3.9

### Install pip
$ sudo apt install python-pip
$ pip install -U pip            # Update pip to last version

### VirtualEnv
$ sudo apt install virtualenv virtualenvwrapper
```

### Setup VirtualEnv
việc setup virtualenv giúp cô lập (isolate) môi trường của ứng dụng với môi trường của hệ điều hành.
```shell
$ virtualenv -p python3.9 .venv
$ source .venv/bin/activate
```

### Install Other services
```shell
### MySQL
$ sudo apt install mysql-server mysql-client

### Redis
$ sudo apt install redis-server redis-tools
```

### Run & test :gear:
#### Run
```shell
$ sh run_dev.sh
```

#### Test
```shell
### Unit test
$ pytest
### Pytest with coverage
$ pytest --cov=locore --cov-report=term
```

#### Lint: Check coding conventions
```shell
$ pip install pylint
$ pylint src
```


#### Folder Structure
```
├── deploy # Script deploy trên server
├── instance # Config env
├── migrations # Update db
│   └── versions
├── source
│   ├── commands # Tất cả các cmd viết thêm flask <cmd>
│   ├── core
│   │   ├── admin # Trang admin
│   │   ├── api # Code api
│   │   │   ├── health
│   │   │   │   └── core
│   │   │   └── v1 # Api v1
│   │   │       ├── core # Source code chính 
│   │   │       ├── exception
│   │   │       ├── request # Validate input api
│   │   │       └── response # Response api
│   │   └── common
│   ├── exts
│   │   ├── authz # Xử lý token
│   │   ├── marshmallow
│   │   └── signals
│   ├── helpers # Các hàm hỗ trợ, chứa ít hoặc không can thiệp vào db
│   ├── languages # Quản lý ngôn ngữ cho api
│   ├── models # Chứa cấu trúc database 
│   ├── templates # Admin template
│   └── utils # Luồng xử lý toàn bộ api, can thiệp database
├── tests # Các tests unit cho hệ thống
```