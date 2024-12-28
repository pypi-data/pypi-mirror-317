# 配置页面生成助手

只需一个JSON/YAML配置文件，就可以生成一个配置页面并实现配置功能，支持多种表单控件，包括文本输入框、下拉框、单选框、复选框、开关、日期选择器、范围选择器等。

---

## 使用方法

> 支持直接调用，也可以生成项目模板

使用前需要 `pip install -U xiaoqiangclub` 安装 `xiaoqiangclub` 模块

### 直接调用接口

参考下面的调用示例：

```python
from xiaoqiangclub import generate_config_ui

# 用户可以在现有应用中调用 generate_config_ui 函数
# default_config_file = r"D:\001_MyArea\002_MyCode\001_PythonProjects\2024\xiaoqiangclub\xiaoqiangclub\templates\html\config_template\config_ui.json"
config_file = r"D:\001_MyArea\002_MyCode\001_PythonProjects\2024\xiaoqiangclub\xiaoqiangclub\templates\html\config_template\config_ui.yml"
data_dir = r"D:\001_MyArea\002_MyCode\001_PythonProjects\2024\xiaoqiangclub\tests"
# 将配置功能集成到现有应用中
app = generate_config_ui(default_config_file=config_file, user_config_dir_or_file=data_dir, route_path="/config")


# 其他路由或功能保持不变
@app.get("/")
async def root():
    return "Hello XiaoqiangClub!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

```

### 生成模板

安装 `xiaoqiangclub` 模块后，终端执行 `xiaoqiangclub config_ui_template` 生成项目模板。修改 [config_ui.py](./config_ui.py)
中的 `config_file = "config_ui.json"` 指向你的配置文件，然后运行
`config_ui.py` 即可启动配置页面服务器。用户配置后，会自动生成一个 `"data/user_config.json"` 文件，用户可以通过访问
`127.0.0.1:8000` 或手动修改该文件，以实现动态配置。后端的其他应用直接调用该文件即可。

注意：配置文件中需要使用 `双引号""`

## 顶级字段说明

### **title**: 页面标题（必需）

- **描述**: 页面标题显示在浏览器标签栏。
- **类型**: 字符串
- **示例**:
  ```json
  "title": "设置界面"
  ```

### **title_link**: 页面标题链接（可选）

- **描述**: 标题下方的链接，点击后会跳转到该链接
- **类型**: 字符串
- **示例**:
  ```json
  "title": "设置界面"
  ```

### **help**: 帮助文档

- **描述**: 当鼠标悬浮在标题上时，会显示该字段中的内容
- **类型**: 字符串
- **示例**:
  ```json
  "help": "这是一个帮助文档"
  ```

### **logo**: 网站或应用的 logo 图片地址（可选）

- **描述**: 设置网站 logo 图片地址，默认为：http://217.142.251.127/h/img/xiaoqiangclub_logo.png
- **类型**: 字符串（URL 地址）
- **示例**:
  ```json
  "logo": "https://example.com/logo.png"
  ```

### **footer**: 页脚说明（可选）

- **描述**: 页脚说明，显示在页面底部，默认值为 `XiaoqiangClub`。可以设置 `footer_link` 进行跳转。
- **类型**: 字符串
- **示例**:
  ```json
  "footer": "All rights reserved."
  ```

### **footer_link**: 页脚链接（可选）

- **描述**: footer的链接，点击后会跳转到该链接，默认为：https://xiaoqiangclub.us.kg/
- **类型**: 字符串
- **示例**:
  ```json
  "footer_link": "https://xiaoqiangclub.us.kg/"
  ```

### **max_width**: 页面最大宽度（可选）

- **描述**: 页面最大宽度，默认为 `3xl`，TailwindCSS风格，[参考文档](https://tailwindcss.com/docs/max-width) 。
- **类型**: 字符串
- **示例**:
  ```json
  "max_width": "5xl"
  ```

### **items**: 配置项的分组（必需）

- **描述**: 配置项分组，每个分组表示一个表单的标题，包含该表单下的所有配置项。
- **类型**: 对象
- **示例**:
  ```json
  {
      "个人信息": { ... },
      "账户设置": { ... }
  }
  ```

---

## 配置项字段说明

每个配置项包含以下字段：

### **order**: 表单项顺序（必需）

- **描述**: 控制每一个表单项在页面中的显示顺序。
- **类型**: 整数
- **示例**:
  ```json
  "order": 1
  ```

### **label**: 表单项标签（必需）

- **描述**: 表单项的名称或标签，显示在用户界面上。
- **类型**: 字符串
- **示例**:
  ```json
  "label": "用户名"
  ```

### **help**: 表单项帮助说明（可选）

- **描述**: 设置该项后会在 `label` 后面显示一个 `?`，悬停时会显示帮助说明。
- **类型**: 字符串
- **示例**:
  ```json
  "help": "请输入用户名"
  ```

### **help_link**: 表单项帮助链接（可选）

- **描述**: 设置该项后，help 会变成一个链接，点击后会跳转到该链接。
- **类型**: 字符串
- **示例**:
  ```json
  "help_link": "https://example.com"
  ```

### **type**: 表单项类型（必需）

- **描述**: 表单项的类型，决定表单项的显示方式。
- **类型**: 字符串
- **可选值**:
    - `text`：文本输入框
    - `list` ：添加多个项并展示，支持删除
    - `select`：下拉框
    - `radio`：单选框
    - `checkbox`：复选框
    - `switch`：开关
    - `date`：日期选择器
    - `range`：范围选择器
- **示例**:
  ```json
  "type": "input"
  ```

### **value**: 默认值（必需）

- **描述**: 表单项的初始值，用户提交时将会返回该字段的值。
- **类型**: 根据 `type` 类型不同而不同：
    - 对于 `input`、`select`、`radio`、`date` 等类型，`value` 为字符串。
    - 对于 `checkbox` 和 `list` 类型，`value` 为字符串数组，表示选中的选项。
    - 对于 `switch` 类型，`value` 为布尔值。
- **示例**:
  ```json
  "value": "xiaoqiangclub"
  ```

### **options**: 可选项（适用于 `select`、`radio`、`checkbox` 类型）

- **描述**: 提供的选项列表，用户可以选择其中一个或多个。
- **类型**: 数组（字符串）
- **示例**:
  ```json
  "options": ["男", "女"]
  ```

### **placeholder**: 占位符文本（适用于 `input` 类型）

- **描述**: 输入框未输入内容时显示的提示文本。
- **类型**: 字符串
- **示例**:
  ```json
  "placeholder": "请输入用户名"
  ```

### **min**: 最小值（适用于 `range` 类型）

- **描述**: 范围选择器的最小值。
- **类型**: 数字
- **示例**:
  ```json
  "min": 0
  ```

### **max**: 最大值（适用于 `range` 类型）

- **描述**: 范围选择器的最大值。
- **类型**: 数字
- **示例**:
  ```json
  "max": 100
  ```

---

## 各种表单控件类型及示例

### 1. **input** （文本输入框）

文本框用于输入单行文本。

```json
"username":{
"label": "用户名",
"type": "input",
"value": "user123"
}
```

### 2. **list** （列表输入框）

添加多个项并展示，支持删除。

```json
"douban": {
"label": "豆瓣",
"order": 2,
"placeholder": "请输入豆瓣用户ID",
"help": "请输入豆瓣用户ID",
"help_link": "https://www.douban.com/people/fsf/",
"type": "list",
"value": ["56548956"]
}
```

### 3. **password** （密码输入框）

文本框用于输入密码。

```json
"password":{
"order": 1,
"label": "用户名",
"type": "password",
"value": "password123"
}
```

### 4. **select** （下拉框）

下拉框用于提供多个选项供用户选择。

```json
"language":{
"order": 2,
"label": "语言选择",
"type": "select",
"options": [
"简体中文",
"English",
"日本語"
],
"value": "简体中文"
}
```

### 5. **radio** （单选框）

单选框允许用户从多个选项中选择一个。

```json
"gender":{
"order": 3,
"label": "性别",
"type": "radio",
"options": [
"男",
"女"
],
"value": "男"
}
```

### 6. **checkbox** （复选框）

复选框允许用户从多个选项中选择多个，`value` 为字符串数组。

```json
"hobby":{
"order": 4,
"label": "兴趣爱好",
"type": "checkbox",
"options": [
"阅读",
"旅行",
"运动",
"电影"
],
"value": [
"运动",
"旅行"
]
}
```

注意：`checkbox`不能单独放在一个 `item`，否则当全部没选中的情况下会无法保存数据。

### 7. **switch** （开关）

开关用于切换布尔值（例如启用/禁用）。

```json
"enable_notification":{
"order": 5,
"label": "启用通知",
"type": "switch",
"value": true
}
```

注意：`switch`不能单独放在一个 `switch`，否则当全部没选中的情况下会无法保存数据。

### 8. **date** （日期选择器）

日期选择器用于选择日期，`value` 为日期字符串。

```json
"birthday":{
"order": 6,
"label": "选择生日",
"type": "date",
"value": "2000-01-01"
}
```

### 9. **range** （范围选择器）

范围选择器通常用于选择一个数字范围。

```json
"brightness":{
"order": 7,
"label": "设置亮度",
"type": "range",
"min": 0,
"max": 100,
"value": 50
}
```

下面是修改后完成的 **分隔线**（line）的说明，包含了参数说明和 `JSON` 示例：

---

### 10. **line** （分隔线）

分隔线用于分隔不同部分的配置，参数说明：

- **"type"**: `"line"`。指定分隔线类型，必须为 `line`。
- **"thickness"**: 分隔线的粗细值 `border-t`，默认为 `1`
  。该值可以参考 [Tailwind CSS 文档](https://tailwindcss.com/docs/border-width)，可以设置为 `1`、`2`、`3` 等，表示不同的粗细程度。
- **"color"**: 分隔线的颜色 `border-`，默认为 `"gray-600"`。你可以选择 Tailwind CSS 预定义的颜色（如 `red-300`、`blue-500`
  等），也可以自定义颜色值，参考 [Tailwind CSS 自定义颜色文档](https://tailwindcss.com/docs/customizing-colors)。
- **"length"**: 分隔线的长度 `w-`，默认为 `"full"`。该值决定了分隔线的宽度。你可以选择像 `full`（100%宽度）、`1/2`（50%宽度）、
  `1/3`（33%宽度）等，或者使用具体的像素宽度如 `w-32` 等，参考 [Tailwind CSS 宽度文档](https://tailwindcss.com/docs/width)。
- **"spacing"**: 上下间距 `my-`，默认为 `6`，表示 `1.5rem`
  。可以根据需要调整分隔线与其他元素的垂直间距，参考 [Tailwind CSS 间距文档](https://tailwindcss.com/docs/margin)。

### 示例：

```json
"separator": {
"order": 8,
"type": "line",
"thickness": 2,
"color": "red-300",
"length": "2/3",
"spacing": 8
}
```

---

## 完整配置文件示例

```json
{
  "title": "设置界面",
  "logo": "http://217.142.251.127/h/img/xiaoqiangclub_logo.png",
  "footer": "XiaoqiangClub",
  "max_width": "3xl",
  "个人信息": {
    "gender": {
      "order": 1,
      "label": "性别",
      "type": "radio",
      "options": [
        "男",
        "女"
      ],
      "value": "男"
    },
    "douban": {
      "label": "豆瓣",
      "order": 2,
      "placeholder": "请输入豆瓣用户ID",
      "help": "请输入豆瓣用户ID",
      "help_link": "https://www.douban.com/people/fsf/",
      "type": "list",
      "value": [
        "56548956"
      ]
    }
  },
  "账户设置": {
    "username": {
      "order": 3,
      "label": "用户名",
      "type": "input",
      "placeholder": "请输入用户名",
      "value": ""
    },
    "password": {
      "order": 4,
      "label": "密码",
      "type": "password",
      "placeholder": "请输入密码",
      "value": ""
    },
    "separator": {
      "order": 5,
      "type": "line",
      "thickness": 3,
      "color": "red-300",
      "length": "2/3"
    },
    "hobbies": {
      "order": 6,
      "label": "选择兴趣爱好",
      "type": "checkbox",
      "options": [
        "阅读",
        "旅行",
        "运动",
        "电影"
      ],
      "value": [
        "旅行",
        "运动",
        "电影"
      ]
    }
  },
  "系统设置": {
    "language": {
      "order": 7,
      "label": "语言选择",
      "type": "select",
      "options": [
        "简体中文",
        "English",
        "日本語"
      ],
      "value": "简体中文"
    },
    "theme": {
      "order": 8,
      "label": "启用暗黑模式",
      "type": "switch",
      "value": "on"
    },
    "birthday": {
      "order": 9,
      "label": "选择生日",
      "type": "date",
      "value": "2000-01-01"
    },
    "brightness": {
      "order": 10,
      "label": "设置亮度",
      "type": "range",
      "min": 0,
      "max": 100,
      "value": "15"
    }
  }
}
```

## 提交与保存数据

- 用户修改表单项后，通过表单提交按钮提交数据，后端会接收到更新后的 JSON 数据。
- 后端根据提交的 JSON 数据更新配置文件，只修改对应 `value` 参数的值，保持数据结构不变。
