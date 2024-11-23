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
- [ ] 云同步数据库
- [ ] 文件密码
- [ ] 自动填充
- [ ] 多端共享
- [ ] 规范数据加密流程
- [ ] 规范测试代码