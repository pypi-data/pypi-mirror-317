# 卡谷电商工具集

**卡谷电商工具集** 是一个用 Python 开发的工具包，旨在为电商开发者提供便捷的数据导入、配置管理和日常任务处理功能。

---

## 功能特点

- **交互式配置管理**：支持创建、查看、列表和删除配置，配置文件存储于用户主目录下。
- **Excel 数据导入数据库**：支持将 Excel 表格数据高效导入指定的数据库中。
- **命令行工具**：提供易用的 CLI 界面，用户可快速完成配置和数据导入任务。

---

## 安装

```shell
  pip install cagu-toolkit
```

## 快速开始

### 配置管理

通过命令行管理工具运行以下操作：

#### 1. 添加配置

```shell
  cagu-toolkit config add
```

#### 2. 查看配置

```shell
  cagu-toolkit config list
```

列出所有配置。

#### 3. 获取某个配置

```shell
  cagu-toolkit config get <配置名称>
```

#### 4. 删除配置

```shell
  cagu-toolkit config delete <配置名称>
```

### 数据导入

将 Excel 数据导入数据库：

1. 准备好 Excel 文件。
2. 运行以下命令：

```shell
  cagu-toolkit import -p <配置名称> <导入模块> -f <Excel文件路径>
```

`导入模块` 可以通过以下命令查看

```shell
  cagu-toolkit import --help
```

### 配置文件存储路径

工具会将配置文件存储于用户主目录下：

```shell
  ~/.cagu-toolkit/config.json
```

配置文件以 JSON 格式保存，支持手动编辑或通过命令行管理。

### 自动更新

脚本在执行时会自动检查最新版本以更新

### CHANGELOGS

#### 1.2.0 - 2024-12-22

##### Features
- 添加了支持 YAML 配置文件的功能 (#45)
- 增加了交互式 CLI 数据导入模块 (#32)

##### Bug Fixes
- 修复了在 Python 3.11 环境下的兼容性问题 (#67)
- 修正了导入 Excel 数据时因特殊字符导致的崩溃问题 (#89)

##### Improvements
- 优化了数据库连接的性能，提高了导入速度
- 更新了日志输出，增加调试信息 (#22)

##### Breaking Changes
- 移除了对 Python 3.6 的支持，请升级到 Python >= 3.7
- 配置文件结构变更：将 `database` 下的 `url` 改为 `connection_string` (#78)

##### Documentation
- 更新了使用说明文档，增加了快速入门指南
- 添加了常见问题的解答 (FAQ) 部分

---