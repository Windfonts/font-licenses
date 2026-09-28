# 上游镜像运维 SOP（wenfeng.org 源档案 · feicode 按组织镜像）

> 镜像总表：`data/source-mirrors.json`（norm → 上游 → feicode 镜像，本表是唯一索引，新款入库必须更新）。
> 机制：Forgejo 原生 pull mirror，8h 自动同步；组织名 = GitHub 上游组织名，URL 一一对应。

## 1. 新款入库时的镜像联动（必做）

1. 查上游是否有公开 GitHub 仓（license-info.json 的 licenseUrl/sourceUrl 已记则直接用）。
2. 有仓 → 建同名组织（若无）：`POST /api/v1/orgs`；迁移：`POST /api/v1/repos/migrate`，
   `clone_addr` 按代理回退顺序：`https://gh-proxy.com/https://github.com/<org>/<repo>.git` → `https://ghproxy.net/...` → `https://ghfast.top/...`；
   参数 `mirror=true, mirror_interval=8h, service="", repo_owner=<组织名字符串>`。
3. 更新 `data/source-mirrors.json`（mirror_state=pending → mirrored）。
4. 提交推送 font-licenses。

## 2. 迁移失败的处置

- migrate 失败会留**同名空壳仓**：重试前必须 `DELETE /api/v1/repos/<org>/<repo>`。
- Forgejo 15 的 `repo_owner` 是 **string**（组织名）。
- 大 pack 断连（curl 56）：换下一家代理重试（gh-proxy.com 实测最优，2G 仓可过）。
- 单仓 >3GB（如扛重族 3.3G 裸二进制历史）：标记 `skipped-too-heavy`，等 devops 出网方案，勿硬重试。

## 3. 镜像健康巡检

```bash
# mirror_updated 超过 25h 的仓即异常（同步失败或上游代理断连）
for org in $(ls 数据来源见 source-mirrors.json 的组织集合); do :; done
# 或直接用 API：GET /api/v1/repos/{org}/{repo} 看 mirror_updated
```
同步失败的手动补法：管理面板该仓 → 立即同步；仍失败换代理删壳重建（见 §1/§2）。

## 4. 验证口径

- 勿信 API 的 `size` 字段（mirror 仓统计任务不跑，恒 0/极小）。
- 验仓内容：归档下载 `/{org}/{repo}/archive/<默认分支>.zip` 返回 200 且体积合理；
  或 clone 后对拍 HEAD sha 与上游 `gh api repos/<org>/<repo>/commits/<分支> --jq .sha`。
- LFS：本批上游仓基本不用 LFS（字体源直接进 git）；迁移时 `lfs` 未启用，
  遇真 LFS 仓须初始迁移勾选 LFS + 定期 CI `git lfs fetch --all`（pull mirror 不增量同步 LFS，gitea#18369）。

## 5. 收录线（无公开仓的 373 款）

方正系等官网 zip/厂商声明款：私有仓 `Windfonts/font-sources-collected`（未建，等 schema 拍板），
manifest 记来源/版本/sha256/许可，可见级别 public/private 逐款定。

## 6. 收录线（2026-09-28 落地）

两仓已建，收录无 GitHub 上游的款（镜像线之外）：

| 仓 | 可见 | 内容 | 当前 |
|---|---|---|---|
| `Windfonts/font-sources` | public | 开源许可款源文件 | 252 款 |
| `Windfonts/font-sources-collected` | private | 免费商用/个人免费/待核实款 | 72 款（pending_review=true）|

- 每款一目录：源文件 + `manifest.json`（norm/许可/visibility/pending_review/collected_at/license_source/license_verified/upstream_hint/逐文件 sha256）。
- 转公开流程：核对 license-info.json 的 distribution 声明 → 该款目录迁至 font-sources + 两仓 manifest 的 visibility/pending_review 同步改。
- 缺源 39 款（开源 37 + 免商 2）待向厂商/官网收集后补录。
- 新款入库联动：MIRROR-SOP §1 判「有上游仓走镜像」，无仓走本节收录（按许可定仓），更新 manifest。
