# 1. 环境准备（如已安装可跳过）
# pip install pandas numpy matplotlib seaborn scipy adjustText

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import adjustText  # 仅用于自动避让文字，可删

# 图区整体美化
sns.set_theme(style="ticks", font="Times New Roman", font_scale=1.2)

# -------------------------------------------------
# 图① 双 y 轴折线
# -------------------------------------------------
x = np.linspace(0, 10, 101)
y1 = np.sin(x) + 0.1 * np.random.randn(101)          # 温度
y2 = np.cos(x) - 0.2 * x + 0.1 * np.random.randn(101) # 应变

fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=300)
ax2 = ax1.twinx()

l1 = ax1.plot(x, y1, lw=1.6, color="#1f77b4", label="Temperature")
l2 = ax2.plot(x, y2, lw=1.6, color="#ff7f0e", label="Strain")

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Temperature (°C)", color="#1f77b4")
ax2.set_ylabel("Strain (%)", color="#ff7f0e")
ax1.tick_params(axis='y', labelcolor="#1f77b4")
ax2.tick_params(axis='y', labelcolor="#ff7f0e")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
fig1.tight_layout()
fig1.savefig("fig1_dual_axis.pdf", bbox_inches="tight")
plt.close(fig1)

# -------------------------------------------------
# 图② 带显著性标记的箱线图
# -------------------------------------------------
np.random.seed(42)
ctrl = stats.norm.rvs(loc=10, scale=1.5, size=30)
trtA = stats.norm.rvs(loc=12, scale=1.8, size=30)
trtB = stats.norm.rvs(loc=13, scale=2.0, size=30)

df = pd.DataFrame({
    "value": np.hstack([ctrl, trtA, trtB]),
    "group": np.repeat(["ctrl", "trtA", "trtB"], 30)
})

# 计算 p 值
# 计算 p 值
_, p_ctrl_trtA = stats.ttest_ind(ctrl, trtA)
_, p_ctrl_trtB = stats.ttest_ind(ctrl, trtB)
_, p_trtA_trtB = stats.ttest_ind(trtA, trtB)

fig2, ax = plt.subplots(figsize=(4, 3), dpi=300)
sns.boxplot(x="group", y="value", data=df, palette="Set2", width=0.5, ax=ax)

# 画显著性横线
def bar(x1, x2, y, p):
    lw = 1.2
    ax.plot([x1, x1, x2, x2], [y, y+0.3, y+0.3, y], lw=lw, color="k")
    ax.text((x1+x2)/2, y+0.4, f"p={p:.3f}", ha="center", va="bottom", fontsize=10)

y_max = df["value"].max() + 0.5
bar(0, 1, y_max, p_ctrl_trtA)
bar(0, 2, y_max+1, p_ctrl_trtB)
bar(1, 2, y_max+2, p_trtA_trtB)

ax.set_xlabel("Group")
ax.set_ylabel("Response (a.u.)")
sns.despine()
fig2.tight_layout()
fig2.savefig("fig2_boxplot.pdf", bbox_inches="tight")
plt.close(fig2)

print("两张图已生成：fig1_dual_axis.pdf 和 fig2_boxplot.pdf")