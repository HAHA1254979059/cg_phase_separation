# README — NVT 预热与回归流程（PVCN/PTB7-T 共混）

本文档记录本次 **NVT 成功收敛** 的标准流程与命令，按实际使用的 4 个 MDP 依次执行：

1. `nvt_initial.mdp`（SD，无约束，低温小步长预热）  
2. `nvt_transi.mdp`（MD，无约束，过渡 50–100 ps）  
3. `nvt_transi2.mdp`（**带约束的 EM**，将几何投影到约束流形）  
4. `nvt_normal.mdp`（MD，启用 H-bond 约束的常规 NVT）

> 目标：避免在第 0 步启用约束时 LINCS 爆炸；通过“SD 预热 → 无约束 MD → 带约束 EM → 常规 NVT”的序列，安全回归到标准 NVT。

---

## 0) 前置与输入
- 起点：软排斥预处理 + **能量最小化（Fmax 达标）**的坐标，例如 `em.gro`。  
- 拓扑：`box.top`（包含 MOLA/MOLB）。  
- 建议坐标为 **whole 分子**（如需可先执行 `trjconv -pbc mol`）。

```bash
# (Optional) ensure molecules are whole and centered
gmx trjconv -s em.tpr -f em.gro -o em_whole.gro -pbc mol -ur compact -center
