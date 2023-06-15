# Roll Dice

扔骰子小工具。

## 使用

```python
# load your driver, set adapter, builtin plugin etc.
nonebot.load_plugin("nonebot_plugin_7s_roll")
nonebot.run()
```

其中 .env 文件除了 nonebot 的常规配置项外，还有可添加以下配置属性（示例中的是默认值）：

```env
# 命令名（在 at 机器人时使用， `@bot /roll 1d10`）
I7S_ROLL_COMMAND="roll"
# 关键字（直接使用，无需 at, `roll 1d10`）
I7S_ROLL_TRIGGER="roll"
```

## 命令

`roll <expr>[[ ]<operator>[ ]<target>]`

其中：

- `<expr>` 计算表达式，格式为
  - `<roll>[[ ][+|-][ ]<roll>]...`，其中 `roll` 不超过 20 项，其格式为：
    - `<times>[d|D]<faces>[ ][<policy>]`，其中
      - `<times>` 为投掷次数，不超过 20 次
      - `<faces>` 为骰子面数，不超过 1000 面
      - `<policy>` 为投掷方式，默认为 `sum`，可选方式有：
        - `sum` 求和
        - `min` 取最小值
        - `max` 取最大值
        - `avg` 取平均值
- `operator` 为比较运算，可以为
  - `>`、`大于`
  - `<`、`小于`
  - `>=`、`大于等于`
  - `<=`、`小于等于`
- `target` 为期望目标

## 举例

`roll 3d6`（在只有一个 `roll` 时，会显示的比较详细）:

```text
3d6 投掷结果

第 1 颗：5
第 2 颗：5
第 3 颗：6

总和为 16
```

`roll 3d10+2d6+1 >20`:

```text
3d10+2d6+1 投掷结果(目标 > 20)：
(5 + 1 + 9) + (4 + 5) + 1 = 25，通过
```

`roll 3d100max+4d10`

```text
3d100max+4d10 投掷结果
(max[35, 60, 29] = 60) + (1 + 1 + 5 + 8) = 75
```

## 截图

![screenshot-dice]

## LICENSE

MIT.

[screenshot-dice]: https://rikka.7sdre.am/files/8c6c5b15-0343-4d14-a203-422c7d6c634e.png
