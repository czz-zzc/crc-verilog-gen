该脚本可以生成任意CRC verilog代码，CRC多项式和并行度可配置

CRC并行电路实现原理参考：
https://github.com/czz-zzc/parallel-crc16/blob/master/%E5%B9%B6%E8%A1%8CCRC%E6%8E%A8%E5%AF%BC%E8%BF%87%E7%A8%8B.pdf

要运行 `crc_verilog_gen.py` 脚本并生成 Verilog 模块，请按照以下步骤操作：

### 1. 准备环境
确保你的系统上安装了 Python 3.x。如果没有安装，可以从 [Python 官方网站](https://www.python.org/) 下载并安装。

### 2. 下载脚本
将 `crc_verilog_gen.py` 脚本保存到你的工作目录中。

### 3. 运行脚本
打开命令行或终端，导航到保存脚本的目录，然后运行以下命令：

```sh
python crc_verilog_gen.py -p <多项式系数> -n <CRC位数> -w <数据输入宽度>
```

#### 参数说明：
- `-p`：多项式系数，用逗号分隔的整数列表。例如，`1,1,0,1,0` 表示多项式 `x^5 + x^4 + x^2 + 1`。
- `-n`：CRC 位数，整数。例如，`5` 表示 CRC-5。
- `-w`：数据输入宽度，整数。例如，`8` 表示数据输入宽度为 8 位。

#### 示例命令：
python crc_verilog_gen.py -p 1,1,0,1,0 -n 5 -w 8

### 4. 查看生成的 Verilog 文件
脚本运行后，会在当前目录下生成一个 Verilog 文件，文件名格式为 `crc<n>_d<data_width>.v`，例如 `crc5_d8.v`。

### 5. 检查生成的 Verilog 代码
打开生成的 Verilog 文件，检查生成的代码是否符合预期。代码应包含模块定义、输入输出声明以及 CRC 计算逻辑。

### 注意事项
- 确保多项式系数的数量与 CRC 位数一致。
- 数据输入宽度应为正整数。
- 如果参数输入有误，脚本会抛出相应的错误信息。

通过以上步骤，可以轻松生成所需的 CRC 计算 Verilog 模块。
