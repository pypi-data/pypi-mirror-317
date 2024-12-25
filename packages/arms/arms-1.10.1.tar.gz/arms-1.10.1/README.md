## 一、如何使用arms？

使用`--help`命令熟悉arms:

```
(venv311) ➜  ~ arms --help
usage: arms [-h] {version,init,patch,config,search,update,design} ...

armstrong

positional arguments:
  {version,init,patch,config,search,update,design}
    version             显示版本
    init                项目初始化工具
    patch               项目补丁工具
    config              arms配置工具
    search              项目搜索工具
    update              arms更新配置
    design              生成文本并复制

options:
  -h, --help            show this help message and exit
```

### 第一步：配置arms

```
arms config ${PARSEC_GITLAB}/arms-tpl/source
```

### 第二步：搜索项目

对于kotlin项目，可以尝试：

```
(venv311) ➜  ~ arms search kotlin
spring-kotlin - kotlin on springboot with CI
kotlin-user - kotlin, 带用户体系
```

### 第三步：生成初始化代码

根据上一步的搜索接口，先cd到新创建的项目目录，执行：

```
git init  # 如果目录下已经用.git目录则忽略
arms init kotlin-user
```

## 二、如何创建模版项目

以kotlin-user项目为例，在其项目根目录创建一个`.arms.json`文件，内容为：

```json
{
  "__name__": [
    {"word": "grpn", "hint": "组名称"}
  ],
  ".env": {
    "ARMS_PROJECT_NAME": "demo"
  }
}
```

然后在`arms init ...`的时候arms就会要求用户输入「组名称」和「服务名称」，用于“智能地”替换"grpn"和"demo"。

arms也支持多级配置，例如下面这个前端CI模版的`.arms.json`文件：

```json
{
    "管理端": {
        "__name__": [{"word": "grpn", "hint": "组名称"}],
        "__only__": ["docker", ".gitlab-ci.yml"]
    },
    "H5端": {
        "__name__": [{"word": "grpn", "hint": "组名称"}],
        "__only__": ["docker", ".gitlab-ci.yml:.gitlab-ci.mobile.yml"]
    },
    ".env": {
        "ARMS_PROJECT_NAME": "demo"
    }
}
```

### 关键字列表

```
__name__: [{}]  //依次提示用户输入
__only__: [""]  //只包含的文件，支持改名
__except__: [""]  //排除的文件
```

## 三、如何使用patch功能

patch功能可以把生成的内容打印到标准输入，用户可以把内容作为上下文，跟prompt一起提交给LLM，从而提升LLM结果的质量。

## 四、友情项目

- inky-flow-cli: ${PARSEC_GITLAB}/inky/flow_cli ，用于后端项目启动阶段，目标是生成openapi.json。