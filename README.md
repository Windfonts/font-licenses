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
