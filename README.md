# font-licenses

字体授权文件库，管理 Windfonts 字库中所有字体的授权协议和商用条款。

## 目录结构

```
licenses/
  {norm}/
    LICENSE            # 授权协议原文（有原文才有）
    license-info.json  # 结构化授权信息
schemas/
  license-info.schema.json   # 字段真源
```

目录名是历史 `normalizedName`：绝大多数是 CamelCase 旧值（`Ibmps`、`Xwbright`），2026-10-07 短码迁移后的新条目是店面短码小写（`851ckrdzyk`）。新条目直接用 canonical 小写 normalized 建目录。旧目录到 canonical 的对照在 `data/dir-aliases.json`（764 条：`case` 仅大小写差异、`rename` 是短码迁移改名；`unmatched` 54 条不在当前目录，按归档处理）。仓内没有 `index.json`；全量清单以各目录 `license-info.json` 为准。

## 与 vault 的同步约定

- 本仓是许可原文与结构化许可信息的归档真源；vault `fonts` 表的 license/spdx/cssAllowed 是运行时消费的投影，两边字段名不同不互相覆盖。
- vault 侧完成人工核实（license-index verified）后，把 `verified`/`verifiedAt`/`verifiedBy`/`spdx`/`licenseUrl` 回写本仓对应 `license-info.json`；回写以 vault 核实结果为准，本仓不反向改 vault。
- 目录名对照见 `data/dir-aliases.json`：查 vault `normalizedName` 时先按 canonical 小写找，没有再查 aliases 的 `canonical` 反查旧目录。
- 新字体入库顺序：先建 `licenses/{canonical小写}/`（LICENSE + license-info.json），再让 vault 收录；不要用旧 CamelCase 建新目录。

## license-info.json 字段

字段真源是 `schemas/license-info.schema.json`，实际键为 camelCase：

| 字段 | 类型 | 说明 |
|------|------|------|
| normalizedName | string | 字体唯一标识（目录名） |
| type | string | 授权类型（中文分类，见下） |
| licenseName | string | 授权协议名 |
| spdx | string\|null | SPDX 标识符（如 OFL-1.1、Apache-2.0） |
| licenseUrl | string\|null | 授权协议原文 URL |
| licenseFile | string\|null | 本仓库内授权文件路径 |
| commercial | boolean | 是否允许商用 |
| modification | boolean\|null | 是否允许修改 |
| distribution | boolean\|null | 是否允许再分发 |
| embedding | boolean\|null | 是否允许嵌入文档/应用 |
| webUse | boolean\|null | 是否允许 Web 字体使用（@font-face） |
| attribution | boolean\|null | 是否需要署名 |
| shareAlike | boolean\|null | 是否要求衍生作品同协议 |
| purchaseUrl | string\|null | 购买/授权链接（付费字体） |
| price | number\|null | 授权价格（人民币） |
| notes | string\|null | 补充说明 |
| verified | boolean | 是否人工核实（false = AI 生成待核实） |
| verifiedAt / verifiedBy | string\|null | 核实日期 / 核实人 |
| source | string\|null | 授权信息来源 |

## 授权类型（type）

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

- `fonts-vault` → 字体库 `fonts` 表（`normalizedName` 关联；vault 的 `license-*` 字段是分发侧结构化许可，回流同步约定见审计报告 #14）
- `font-foundries` → 厂商档案（`foundry` 字段关联）
- `fonts-front` → 店面目录（`normalized` 小写即 OSS 包目录）

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

## 2026-09-24 maoken 批（五款，均已核对 OFL 英文原文）

来源 github.com/maoken-fonts，五款全部 `spdx: OFL-1.1`、`verified: true`：

| 目录 | 字体 | 上游仓 |
|---|---|---|
| `Frexsans` | 械黑 Frex Sans GB | frex-sans（含 IBM Plex Sans 衍生版权行与保留名 Plex） |
| `Jnmy` | 荆南麦圆 | KNMaiyuan |
| `Mkybkjs` | 猫啃硬笔楷书 | MaokenYingBiKaiShuJ（随包取仓内 0.20 版 OFL） |
| `Mkkzh` | 猫啃扛重族黑 | maoken-heavy-labourer（LICENSE.txt 为英文原文，另有中译 LICENSE_ZHS） |
| `Mkkzs` | 猫啃扛重族宋 | 同上，两族共用一份上游许可 |

扛重族在 GitHub 接口上标 NOASSERTION，实际是 OFL 1.1：`LICENSE.txt` 是英文原文（版权头 Maoken/NightFurySL2001 + Adobe 保留名 Source），判断依据已写入两份 `license-info.json` 的 notes。

## 2026-09-24 GuiWonder 批（七款，授权三类）

来源 github.com/GuiWonder（尚古系列/合简/华英明朝/上元明朝作者），全部 `verified: true`：

| 目录 | 字体 | 授权 | 上游仓 |
|---|---|---|---|
| `Sght` `Sgyt` `Sgdk` | 尚古黑体/圆体/等宽 | OFL-1.1 | Shanggu（仓内文件名是 LICENSE.txt，不是 OFL.txt） |
| `Hjht` | 合简黑体 | OFL-1.1 | HeSimplFonts（同上） |
| `Hymc` | 华英明朝（传承体 Classic） | IPA Font License v1.0 | HuayingMincho（全文随仓） |
| `Syma` `Symb` | 上元明朝 A/B | GlyphWiki 协议 | LanternMing（README 授权节声明遵循 GlyphWiki 页面，与花园明朝同款） |

IPA 许可要点：允许嵌入、再分发与衍生（衍生须更名），分发必须附条款全文——本仓 `Hymc/LICENSE` 即条款原文。上元明朝 A/B 没有独立许可文件，协议原文在 GlyphWiki 站点，`LICENSE` 存声明与出处链接。


