"""Generate publication figures for IEEE submission.

Sets pdf.fonttype = 42 and ps.fonttype = 42 to ensure TrueType fonts (no Type 3).
Fixes Fig 4 x-tick label collision and legend position.
Fixes Fig 5 legend overlap with Transparency bar and uses '×' in axis label.
"""

from __future__ import annotations

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
matplotlib.rcParams['font.family'] = 'sans-serif'

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
SUB_FIG_DIR = ROOT / "submission/final/figures"

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"
GRAY = "#7f7f7f"


def make_fig1():
    # Fig 1: Outcome prediction baselines (n=1503)
    # 244.8 x 172.8 pts -> (3.4, 2.4) in
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    
    models = ['Majority', 'E1 TF-IDF+LR', 'E2 mean-logit', 'E2 maj-vote']
    acc = [0.5017, 0.61344, 0.596806, 0.6015]
    f1 = [0.3341, 0.612342, 0.592358, 0.5937]
    
    x = np.arange(len(models))
    w = 0.35
    
    rects1 = ax.bar(x - w/2, acc, w, label='Accuracy', color=BLUE)
    rects2 = ax.bar(x + w/2, f1, w, label='Macro-F1', color=ORANGE)
    
    ax.set_title("Outcome baselines, ILDC test (n=1,503)", fontsize=8.5, pad=6)
    ax.set_ylim(0, 0.72)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6])
    ax.set_yticklabels(["0.0", "0.2", "0.4", "0.6"], fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=7, rotation=18, ha='right')
    
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig1_outcome.pdf")
    plt.close(fig)


def make_fig2():
    # Fig 2: Authority recovery funnel (combined-37)
    # 244.8 x 158.4 pts -> (3.4, 2.2) in
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    
    cats = ['Top-5\nselected', 'Retrieved\nonly (6-100)', 'Absent\nat k=100']
    base = np.array([12, 3, 15])
    ext = np.array([0, 5, 2])
    total = base + ext
    
    x = np.arange(len(cats))
    w = 0.55
    
    p1 = ax.bar(x, base, w, label='Base-30', color=BLUE)
    p2 = ax.bar(x, ext, w, bottom=base, label='Extension-7', color=ORANGE)
    
    for i, t in enumerate(total):
        ax.text(x[i], t + 0.6, str(t), ha='center', va='bottom', fontsize=8)
    
    ax.set_title("Authority recovery funnel, combined-37", fontsize=8.5, pad=6)
    ax.set_ylabel("Cases (combined n=37)", fontsize=7.5)
    ax.set_ylim(0, 22)
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_yticklabels(["0", "5", "10", "15", "20"], fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=7.5)
    
    # Legend in upper left where bars are short (bar 1 is at 12); leaves "Absent at k=100" (bar 3, 17) completely clear
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig2_funnel.pdf")
    plt.close(fig)


def make_fig3():
    # Fig 3: Displayed-evidence integrity (combined-37)
    # 244.8 x 158.4 pts -> (3.4, 2.2) in
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    
    cats = ['Grounded\n37/37', 'Provenance\n185/185', 'Temporal\nviol. 0/185', 'Unsupported\n0/37']
    vals = [1.00, 1.00, 0.00, 0.00]
    colors = [GREEN, GREEN, GRAY, GRAY]
    
    x = np.arange(len(cats))
    w = 0.55
    
    rects = ax.bar(x, vals, w, color=colors)
    
    for i, v in enumerate(vals):
        ax.text(x[i], v + 0.04, f"{v:.2f}", ha='center', va='bottom', fontsize=7.5)
    
    ax.set_title("Displayed-evidence integrity, combined-37", fontsize=8.5, pad=6)
    ax.set_ylim(0, 1.30)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
    ax.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0", "1.2"], fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=7)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig3_integrity.pdf")
    plt.close(fig)


def make_fig4():
    # Fig 4: Retrieval investigation pathway (historical)
    # 244.8 x 158.4 pts -> (3.4, 2.2) in
    # Requirement: stop x-tick labels colliding, move legend so it doesn't cover data points.
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    
    dev_x = [0, 1, 2, 3]
    dev_y = [0/9, 3/9, 6/9, 7/9]
    
    b30_r5_x = [4.4, 4.4]
    b30_r5_y = [5/30, 12/30]
    
    b30_r100_x = [5.5, 5.5]
    b30_r100_y = [12/30, 15/30]
    
    ax.plot(dev_x, dev_y, 's-', color=BLUE, label='Dev R@100 (n=9)', markersize=5, linewidth=1.2)
    ax.plot(b30_r5_x, b30_r5_y, 'o-', color=ORANGE, label='Base-30 R@5 pre/post', markersize=5, linewidth=1.2)
    ax.plot(b30_r100_x, b30_r100_y, '^-', color=GREEN, label='Base-30 R@100 pre/post', markersize=5, linewidth=1.2)
    
    ax.set_title("Retrieval investigation pathway (historical)", fontsize=8.5, pad=6)
    ax.set_ylim(-0.05, 1.40)
    ax.set_yticks([0.00, 0.25, 0.50, 0.75, 1.00])
    ax.set_yticklabels(["0.00", "0.25", "0.50", "0.75", "1.00"], fontsize=7.5)
    
    tick_pos = [0, 1, 2, 3, 4.4, 5.5]
    tick_labels = ['Legacy (dev)', 'Salient (dev)', 'Self-match (dev)', 'Pre-rank (dev)', 'Base-30 R@5', 'Base-30 R@100']
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(tick_labels, fontsize=6.5, rotation=25, ha='right')
    
    # Legend placed in headroom (upper left), completely clear of all data points and lines
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98), fontsize=6.2, framealpha=0.9, handletextpad=0.3, borderpad=0.25)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_bounds(0, 1)
    
    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig4_investigation.pdf")
    plt.close(fig)


def make_fig5():
    # Fig 5: RQ3 exploratory LLM ratings (not human)
    # 244.8 x 172.8 pts -> (3.4, 2.4) in
    # Requirement: move legend so it doesn't overlap Transparency bar; use "×" instead of "x" in axis label.
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    
    dims = ['Linkage', 'Verifiability', 'Traceability', 'Clarity', 'Transparency']
    structured = [4.589286, 4.696429, 4.642857, 4.732143, 4.642857]
    unstructured = [2.839286, 3.696429, 2.160714, 2.214286, 2.660714]
    
    y = np.arange(len(dims))
    h = 0.35
    
    rects1 = ax.barh(y + h/2, structured, h, label='Structured', color=BLUE)
    rects2 = ax.barh(y - h/2, unstructured, h, label='Unstructured', color=ORANGE)
    
    ax.set_title("RQ3 exploratory LLM ratings (not human)", fontsize=8.5, pad=6)
    # Axis label using '×' instead of 'x'
    ax.set_xlabel("Mean rating (1–5; 4 LLM raters × 14 cases)", fontsize=7.5)
    ax.set_xlim(0, 5.2)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xticklabels(["0", "1", "2", "3", "4", "5"], fontsize=7.5)
    ax.set_yticks(y)
    ax.set_yticklabels(dims, fontsize=7.5)
    
    # Transparency bar top edge is around y=4.2. Setting ylim=(-0.5, 5.3)
    # creates ample clear space above the Transparency bar for the legend!
    ax.set_ylim(-0.5, 5.3)
    ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.99), ncol=2, fontsize=7, framealpha=0.9, handletextpad=0.3, borderpad=0.25)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig5_explanation.pdf")
    plt.close(fig)


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    SUB_FIG_DIR.mkdir(parents=True, exist_ok=True)
    
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    make_fig5()
    
    import shutil
    for fig_name in ["fig1_outcome.pdf", "fig2_funnel.pdf", "fig3_integrity.pdf", "fig4_investigation.pdf", "fig5_explanation.pdf"]:
        shutil.copy2(FIG_DIR / fig_name, SUB_FIG_DIR / fig_name)
    print("All 5 figure PDFs generated and copied successfully.")


if __name__ == "__main__":
    main()
