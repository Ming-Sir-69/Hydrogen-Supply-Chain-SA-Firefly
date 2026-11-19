<picture>
  <source media="(prefers-color-scheme: dark)" srcset="readme-assets/cover-zh-dark.png">
  <img src="readme-assets/cover-zh-light.png" alt="氢能供应链的四种成本模型、十二种初始组合与随机退火候选搜索" width="100%">
</picture>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="实验数据.zip">实验归档</a> ·
  <a href="文件夹结构.txt">结构说明</a> ·
  <a href="https://github.com/Ming-Sir-69">作者主页</a>
</p>

<p align="center">
  <img alt="Source license not specified" src="https://img.shields.io/badge/source%20license-not%20specified-F6C555?style=flat-square&labelColor=2E2A26">
  <a href="readme-assets/PERSONAL-DOCUMENTATION-LICENSE.md"><img alt="Documentation license MIT" src="https://img.shields.io/badge/documentation%20license-MIT-F6C555?style=flat-square&labelColor=2E2A26"></a>
  <img alt="Python 3" src="https://img.shields.io/badge/python-3-6B655C?style=flat-square&labelColor=2E2A26">
  <img alt="NumPy required" src="https://img.shields.io/badge/dependency-NumPy-6B655C?style=flat-square&labelColor=2E2A26">
  <img alt="4 models" src="https://img.shields.io/badge/models-4-A8A196?style=flat-square&labelColor=2E2A26">
</p>

<p align="center">
  <b>简体中文</b> · <a href="README.en.md">English</a>
</p>

# 氢能供应链成本模型：模拟退火萤火虫搜索

本项目用离散模拟退火萤火虫算法搜索氢能生产与运输的低成本组合。四种制氢方式与三种运输方式组成 12 种候选，在四种成本与补贴模型中使用同一个搜索内核。仓库另附历史 Excel 实验归档；归档未由混合算法重新生成，不能用于推断政策效果。

## 主要功能

- **四种目标函数**：无补贴成本、直接资金补贴、比例成本分担、环境成本与绿色补贴。
- **离散候选搜索**：在 Green、SMR、ATR、CCS 与 Pipeline、Truck、LiquefiedTruck 之间改选，主搜索固定生产量和运输量。
- **温度与停止控制**：按典型上坡代价和目标接受率估计初始温度，逐轮降温，最多 1000 轮；连续 200 轮没有改进时提前停止。
- **两类运行入口**：Python 入口直接打印搜索过程；MATLAB 入口通过 `py.*` 调用对应目录的 Python 模块<sup>[[2]](#参考文献)</sup>。
- **历史实验归档**：压缩包含 209 个 XLSX 文件，按 model0 至 model3 分组；归档内容尚未由当前代码独立重建核对。

| 模型 | 目标函数 | 初始生产量（kg） | 管道距离（km） |
|---|---|---:|---:|
| [model0](model0/) | 生产成本 + 运输成本 | 1350 | 2500 |
| [model1](model1/) | model0 − 直接资金补贴 | 450 | 2500 |
| [model2](model2/) | model0 ×（1 − 成本分担比例） | 2250 | 2500 |
| [model3](model3/) | model0 + 环境成本 − 绿色补贴 | 1350 | 2400 |

## 快速开始

准备 Python 3 和 NumPy<sup>[[1]](#参考文献)</sup>。仓库没有依赖锁文件，也没有自动化测试套件或持续集成配置。在仓库根目录运行四个 Python 入口：

```sh
python3 -c 'import numpy'
for model in 0 1 2 3; do
  (cd "model${model}" && python3 -B "simulated_annealing_firefly_model${model}.py" --seed 7)
done
```

四个 Python 入口均已实跑。可用 `--seed` 固定随机序列；不传时每次运行的搜索轨迹可能不同。

只运行一个模型时，进入对应目录后执行，例如：

```sh
cd model0
python3 -B simulated_annealing_firefly_model0.py --seed 7
```

## 用法

### 修改模型输入

各模型目录的 `initialize_parameters.py` 保存生产量、运输距离、单位成本、环境成本与补贴参数。运输量固定为生产量的 `3/5`；卡车与液氢车距离分别为管道距离的 `3/5` 和 `2.6/5`。这些数值是代码内置输入，仓库未附其数据来源或校准记录。

`calculate_fitness_model*.py` 定义目标函数，`simulated_annealing_firefly_model*.py` 执行搜索。修改输入后应从对应模型目录运行，避免同名模块从其他目录载入。

### MATLAB 入口

每个模型都有 `matlab_script_model*.m` 与 `matlab_script_model*_modified.m`。两类脚本都写死了 Windows Python 3.11 可执行文件路径；运行前需用 `pyenv` 改为本机解释器，并确认当前目录与 Python 模块搜索路径<sup>[[2]](#参考文献)</sup>。

修改版还写入 Excel、生成统计图，并假定 `../实验数据/<模型>/` 及 `optimal_solutions/` 输出目录已经存在。仓库只提供压缩归档，没有展开这些目录；MATLAB 版本、工具箱依赖和修改版输出流程均未在本次核查中验证。

## 设计与原理

1. 每个候选由制氢方式、运输方式及固定数量组成。成本越低，视为越亮。
2. 每个候选从上一轮的同数量种群中随机选一只更亮的萤火虫；两个方式字段中不同的比例记为距离 `d`，按 `β₀ exp(−γd²)` 的概率向其复制不同字段。没有更亮同伴时跳过吸引。
3. 两个方式字段分别以一定概率变异；生产量和运输量不变。
4. 成本不升的提案直接接受；成本增加 `Δ` 时，以 `exp(−Δ/T)` 的概率接受。初温用单字段变更的正代价差中位数估算，然后每轮乘以小于 1 的因子。独立保存找到的最佳方案，不随种群变化。

萤火虫吸引与模拟退火的出处见参考文献<sup>[[3]](#参考文献)[[4]](#参考文献)</sup>。这里是对类别变量的离散改写，不是连续位置更新公式的原样复现。

## 局限

- 默认初始种群已覆盖 12 种组合，穷举即可得到精确最小值。四个模型从排除所有最优方案的初始种群出发，各用 10 个随机种子均找回穷举最优；这不是与穷举的性能对比，也不保证更大问题的收敛表现。
- model3 的运输环境成本只乘运输量，未乘距离，与参数注释中的“元/千克/公里”不一致。
- 成本、环境成本与补贴参数没有来源说明；Excel 归档尚未独立重建，不能当作已验证研究结果。
- MATLAB 脚本包含特定机器路径和输出目录假设，当前环境未验证其兼容性。脚本在调用 Python 后的旧汇报循环只是重复最终适应度，不是真实搜索轨迹。

## 开发

四个模型共用 `annealing_firefly.py`，保留各自的成本函数和 Python/MATLAB 入口。本仓库没有发布包或持续集成；已提交的 `__pycache__/` 是历史缓存，不是源码。

[结构说明](文件夹结构.txt)列出各目录用途，[实验归档](实验数据.zip)保留历史 XLSX 文件。文档授权范围见[个人文档许可](readme-assets/PERSONAL-DOCUMENTATION-LICENSE.md)。

## 致谢

- NumPy 提供随机候选生成与数值计算接口<sup>[[1]](#参考文献)</sup>。
- MathWorks 文档说明 MATLAB 的 Python 环境配置方式<sup>[[2]](#参考文献)</sup>。
- 封面插画由图像生成模型生成，经本项目处理。

## 参考文献

1. Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362. <https://doi.org/10.1038/s41586-020-2649-2>
2. MathWorks. *pyenv — Change default environment of Python interpreter*, R2026b. <https://www.mathworks.com/help/matlab/ref/pyenv.html>

3. Yang, X.-S. (2009). Firefly Algorithms for Multimodal Optimization. *Stochastic Algorithms: Foundations and Applications*, 169–178. Springer. <https://doi.org/10.1007/978-3-642-04944-6_14>
4. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by Simulated Annealing. *Science*, 220(4598), 671–680. <https://doi.org/10.1126/science.220.4598.671>

## 仓库结构

| 位置 | 内容 |
|---|---|
| `annealing_firefly.py` | 共享离散搜索内核 |
| `model0/` | 无补贴的生产与运输成本模型及运行入口 |
| `model1/` | 直接资金补贴模型及运行入口 |
| `model2/` | 比例成本分担模型及运行入口 |
| `model3/` | 环境成本与绿色补贴模型及运行入口 |
| `实验数据.zip` | 209 个历史 XLSX 文件及目录项 |
| `文件夹结构.txt` | 原目录说明 |
| `readme-assets/` | 封面、主题页眉、署名资源与文档许可 |

---

文档维护：<picture><source media="(prefers-color-scheme: dark)" srcset="readme-assets/em-logo-dark.svg"><img src="readme-assets/em-logo-light.svg" alt="EM" height="13"></picture> <b>EricMingle69</b> · <a href="https://github.com/Ming-Sir-69">Ming-Sir-69</a><br>
根目录未提供源码、既有数据或第三方材料的统一许可证，复用与再分发权限需另行确认；本轮文档原创表达的既有授权范围见[个人文档许可](readme-assets/PERSONAL-DOCUMENTATION-LICENSE.md)。
