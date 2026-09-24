# font-licenses

字体授权文件库，管理 Windfonts 字库中所有字体的授权协议和商用条款。

## 目录结构

```
licenses/
  {NormalizedName}/
    LICENSE            # 授权协议原文
    license-info.json  # 结构化授权信息
schemas/
  license-info.schema.json
index.json             # 所有字体授权索引
```

## license-info.json 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| normalized_name | string | 字体唯一标识 |
| license_type | string | 授权类型（见下） |
| license_spdx | string | SPDX 标识符（如 OFL-1.1、Apache-2.0） |
| license_url | string | 授权协议原文 URL |
| commercial_use | boolean | 是否允许商用 |
| modification | boolean | 是否允许修改 |
| distribution | boolean | 是否允许分发 |
| attribution_required | boolean | 是否需要署名 |
| purchase_url | string | 购买/授权链接（付费字体） |
| notes | string | 补充说明 |
| verified | boolean | 是否人工核实 |
| verified_at | string | 核实日期 |

## 授权类型（license_type）

| 类型 | 说明 |
|------|------|
| 免费商用 | 可免费用于商业用途 |
| 个人免费 | 仅限个人非商业使用 |
| 试用版 | 功能受限的试用授权 |
| 付费授权 | 需购买商业授权 |
| 联系授权 | 需联系厂商获取授权 |

## 常见开源字体协议

- **OFL-1.1**（SIL Open Font License）：可商用、可修改、不可单独售卖字体文件
- **Apache-2.0**：可商用、可修改、需保留版权声明
- **MIT**：最宽松，可商用可修改
- **CC BY 4.0**：需署名，可商用

## 关联仓库

- `font-metadata` → 字体基本信息（通过 normalized_name 关联）
- `font-foundries` → 厂商授权政策

## 2026-09-24 OSS 核对

桶 `wenfeng-fonts`（CDN `cn.windfonts.com`）当时 271312 个对象。字体许可原文只有两份，已抄进本仓 `972b5ab`：

| 目录 | OSS 对象 | 本仓文件 |
|---|---|---|
| `Dlzht` 鼎猎珠海体 | `wenfeng/fonts/dlzht/license.pdf` | `LICENSE` 是排版断行接上后的摘录；`license.pdf` 是带签名的原件 |
| `Opsa` OPPO Sans | `wenfeng/fonts/opsa/license.0 License Notice` | `LICENSE` 与对象字节对应（入库时换行被规范成 LF） |

鼎猎珠海体授权说明（2024-09-03，登记号陕作登字-2024-F-00013790）允许把字体当画面用于设计和广告，并写明电子文件嵌入网站、计算机程序或带显示的电子产品不在授权范围内。原文没有写能否修改或再分发字体文件。`license-info.json` 的 `webUse`、`embedding` 为 false，`modification`、`distribution` 为 null。`verified` 仍是 false。

OPPO Sans 协议（Copyright 2024 Guangdong OPPO）允许不修改地嵌入，并随非字体软件再分发。必须标明使用了 OPPO Sans。禁止修改，禁止单独再分发或出售字体文件。

没有入库的同名对象：

- `wenfeng/fonts/cszt/`：入户申请、Vue 笔记、Mantine README。
- `wenfeng/fonts/test/`：心理健康报告、教学资源申请表。
- 184 个 `wenfeng/fonts/<家族>/<字重>/*.zip`：只有 woff2、css、`reporter.json`。
- `fonts-packages/`：网页字体包旁边没有 LICENSE / OFL.txt。

128 个家族目录里，有 `LICENSE` 的是 10 个：上述 2 个，加上 `6a1b7f2` 的 8 份上游 OFL（Dyh、Btot、Hclcks、Yzklct、Ibmps、Ljmc、Xwmh、Zkklt）。其余 118 个目录仍只有 `license-info.json`。没有原文就不要写许可正文，也不要把 AI 句子当成原文。

## 2026-09-24 淘宝买菜体

`Tbmct`：发行包内无许可文件，`LICENSE` 存官方页面声明原文摘录（fonts.alibabadesign.com / www.alibabafonts.com，「现这款字体向所有个人和组织开放，永久免费商用」），出处与核实链见 `license-info.json` 与 `LICENSE` 尾注。
