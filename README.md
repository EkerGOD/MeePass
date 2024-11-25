# 项目介绍
本项目是一个基于个人的密码管理系统，在确保安全性的同时尽可能做到方便快捷，本人不是专业的计算机专业学生或行业人员，只是对于这方面较为感兴趣所以开展此项目，本项目可能无法与很多优秀的密码管理系统相比较，但是我希望可以有更多热爱喜欢编程的人可以参与其中，也算是磨练自己熟悉一下真正项目开发是如何的

# 环境依赖
详见requirements.txt

# 目录结构描述
    MeePass/                // 项目主目录
    ├── database            // 存放密码数据库 
    ├── favicon             // 项目图标
    ├── MeePass_Backend/    // 后台OTP及未来密码备份服务后台文件
    │   ├── config.py       // 后台配置文件
    │   ├── response.py     // response类及相关枚举类
    │   └── TOTP.py         // 后端主代码，目前主要用作TOTP一次性密码验证
    ├── tests               // 测试文件存放
    ├── ui/                 // PyQt界面文件
    │   ├── dynamic         // 针对ui界面生成代码添加功能
    │   ├── static          // ui文件生成代码，不作任何修改
    │   ├── controller.py   // 用于各个页面之间交互
    │   └── main_ui.py      // ui主入口
    ├── utils/              // 工具文件夹
    │   ├── file.py         // 文件相关工具
    │   └── password.py     // 密码相关工具
    ├── .gitignore          // git忽略文件
    ├── auth.py             // 验证代码
    ├── config.py           // 配置文件
    ├── crypt.py            // 加解密代码
    ├── db.py               // 数据库代码
    ├── gui.py              // gui.py文件
    ├── gui.ui              // gui.ui文件
    ├── main.py             // 主入口
    ├── README.md           // 帮助文档
    ├── requirements.txt    // 依赖库文件
    └── sql.py              // 存放sql语句


# 使用说明

# 版本内容更新
##### v0.1.0:
    1. 实现基本密码存储功能
    
    2. 固定密码加密流程

    3. 实现TOTP一次性密码加密

##### v0.1.1:
    1. 编写基本gui页面

    2. 完成密码熵检测

## 流程
1. 打开gui
2. 创建密码库
3. 选择加密项目（主密码必选，OTP可选，选之前需要配置，加密文件可选）
4. 输入master password和OTP
5. 验证OTP
6. 进入系统
7. 查询密码账户
8. 用master password解密密码

## 数据表
passwords

| columns  | descriptions |
|----------|--------------|
| id       | 唯一标识符        |
| account  | 账户名          |
| password | 加密密码         |
| group_id | 对应的group_id  | 
| notes    | 备注           |

groups

| columns   | descriptions |
|-----------|--------------|
| id        | 唯一标识符        |
| name      | group名称      |
| parent_id | 父节点id        |

## 更新路径
- [ ] 完成gui页面
  - [ ] 完成打开数据库页面
  - [ ] 完成操作数据库页面
  - [ ] 完成创建主密码页面
- [ ] 云同步数据库
- [ ] 文件密码
- [ ] 自动填充
- [ ] 多端共享
- [x] 规范数据加密流程 //2024.11.23
- [x] 规范测试代码 // 2024.11.23
- [ ] 规范化版本管理
- [ ] 可以选择加密方式(主密码，otp，文件密码)
- [x] 文件配置规范 //2024.11.23
- [x] 规范README结构 // 2024.11.23
- [ ] otp密钥更改
- [x] 检测密码熵