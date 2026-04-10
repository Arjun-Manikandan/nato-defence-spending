"""
NATO Defence Spending Analyser
================================
Analyses defence spending trends (as % of GDP) across NATO member states
from 2014-2023, using publicly reported SIPRI/NATO figures.

The 2% GDP target is NATO's benchmark for member commitment.
This script explores who meets it, who doesn't, and how trends
have shifted — particularly since Russia's invasion of Ukraine in 2022.

Author: Arjun Manikandan
Data source: SIPRI Military Expenditure Database / NATO Defence Expenditure Reports
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
# Read the CSV file. Each row is a country, each column is a year.
# The values are defence spending as a % of GDP.

df = pd.read_csv("data/nato_spending.csv", index_col="country")

# Convert column names from strings ("2014") to integers (2014)
# so we can do maths on them later (e.g. sorting, arithmetic)
df.columns = df.columns.astype(int)
years = df.columns.tolist()  # [2014, 2015, 2016, ..., 2023]

print("=== NATO Defence Spending Analyser ===\n")
print(f"Dataset: {len(df)} countries, {len(years)} years ({years[0]}–{years[-1]})\n")


# ── 2. KEY STATISTICS ─────────────────────────────────────────────────────────
# Find which countries meet the NATO 2% GDP target in the most recent year

NATO_TARGET = 2.0
latest_year = years[-1]  # 2023

latest = df[latest_year].sort_values(ascending=False)

print(f"Defence spending as % of GDP in {latest_year}:")
print("-" * 40)
for country, value in latest.items():
    # Add a marker if they meet the 2% target
    marker = " ✓ meets NATO target" if value >= NATO_TARGET else ""
    print(f"  {country:<20} {value:.2f}%{marker}")

# Count how many countries meet the target
meeting_target = (latest >= NATO_TARGET).sum()
print(f"\n{meeting_target} of {len(df)} countries meet the 2% NATO target in {latest_year}\n")


# ── 3. UK TREND ANALYSIS ──────────────────────────────────────────────────────
# Look specifically at how UK spending has changed over time

uk_values = df.loc["United Kingdom"]
uk_change = uk_values[latest_year] - uk_values[years[0]]

print(f"UK spending change {years[0]}–{latest_year}: {uk_change:+.2f}% of GDP")
print(f"  From {uk_values[years[0]]:.2f}% → {uk_values[latest_year]:.2f}%\n")


# ── 4. POST-UKRAINE SHIFT ─────────────────────────────────────────────────────
# Russia invaded Ukraine in Feb 2022. Did NATO members increase spending?
# Compare average spending: 2014–2021 (pre-escalation) vs 2022–2023

pre_ukraine = df[[y for y in years if y <= 2021]].mean(axis=1)
post_ukraine = df[[y for y in years if y >= 2022]].mean(axis=1)
shift = (post_ukraine - pre_ukraine).sort_values(ascending=False)

print("Average spending shift after Ukraine invasion (2022–2023 vs 2014–2021):")
print("-" * 50)
for country, delta in shift.items():
    direction = "↑" if delta > 0 else "↓"
    print(f"  {country:<20} {direction} {abs(delta):.2f}% of GDP")
print()


# ── 5. VISUALISATIONS ─────────────────────────────────────────────────────────
# Create an output folder for the charts
os.makedirs("output", exist_ok=True)

# Set a clean, minimal style
plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#1f4e79", "#c00000", "#375623", "#7030a0", "#833c00",
          "#215868", "#843c0c", "#244185", "#4c2c69", "#2e4053"]


# ── Chart 1: UK spending over time with NATO target line ──────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(years, df.loc["United Kingdom"], color="#1f4e79", linewidth=2.5,
        marker="o", markersize=5, label="United Kingdom")

# Draw the 2% NATO target as a dashed red line
ax.axhline(y=NATO_TARGET, color="#c00000", linestyle="--",
           linewidth=1.5, label="NATO 2% target")

# Shade the area under the UK line
ax.fill_between(years, df.loc["United Kingdom"], alpha=0.1, color="#1f4e79")

# Mark the Ukraine invasion year
ax.axvline(x=2022, color="orange", linestyle=":", linewidth=1.5,
           label="Russia invades Ukraine (Feb 2022)")

ax.set_title("UK Defence Spending as % of GDP (2014–2023)", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("% of GDP", fontsize=11)
ax.set_ylim(0, 3.5)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
ax.legend(fontsize=10)
ax.set_xticks(years)

plt.tight_layout()
plt.savefig("output/uk_spending_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: output/uk_spending_trend.png")


# ── Chart 2: All NATO members — 2023 spending ranked, with target line ────────
fig, ax = plt.subplots(figsize=(11, 6))

sorted_2023 = df[latest_year].sort_values(ascending=True)
bar_colors = ["#c00000" if v >= NATO_TARGET else "#1f4e79" for v in sorted_2023]

bars = ax.barh(sorted_2023.index, sorted_2023.values, color=bar_colors, height=0.6)

# Add value labels to the right of each bar
for bar, val in zip(bars, sorted_2023.values):
    ax.text(val + 0.03, bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}%", va="center", fontsize=9)

ax.axvline(x=NATO_TARGET, color="#c00000", linestyle="--",
           linewidth=1.5, label="2% NATO target")

ax.set_title(f"NATO Member Defence Spending as % of GDP ({latest_year})",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("% of GDP", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
ax.legend(fontsize=10)

# Add a legend for bar colour meaning
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor="#c00000", label="Meets 2% target"),
                   Patch(facecolor="#1f4e79", label="Below 2% target")]
ax.legend(handles=legend_elements, fontsize=10)

plt.tight_layout()
plt.savefig("output/nato_2023_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: output/nato_2023_comparison.png")


# ── Chart 3: Multi-country trend lines 2014–2023 ─────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

for i, country in enumerate(df.index):
    # Make UK and US bolder so they stand out
    lw = 2.8 if country in ["United Kingdom", "United States"] else 1.5
    alpha = 1.0 if country in ["United Kingdom", "United States"] else 0.65
    ax.plot(years, df.loc[country], label=country, color=COLORS[i % len(COLORS)],
            linewidth=lw, alpha=alpha, marker="o", markersize=3)

ax.axhline(y=NATO_TARGET, color="black", linestyle="--",
           linewidth=1.2, alpha=0.5, label="2% NATO target")

ax.axvline(x=2022, color="orange", linestyle=":", linewidth=1.5,
           label="Ukraine invasion")

ax.set_title("NATO Defence Spending Trends (2014–2023)", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("% of GDP", fontsize=11)
ax.set_ylim(0, 4.5)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
ax.legend(fontsize=8.5, loc="upper left", ncol=2)
ax.set_xticks(years)

plt.tight_layout()
plt.savefig("output/all_countries_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: output/all_countries_trend.png")

print("\nAnalysis complete. All charts saved to /output/")
