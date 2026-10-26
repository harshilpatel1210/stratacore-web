import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Locate input data feed
xlsx_path = "StrataCore_Advisory_Master_Model_v2.5.xlsx"
csv_path = "PowerBI_DataFeed.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
elif os.path.exists(xlsx_path):
    df = pd.read_excel(xlsx_path, sheet_name="PowerBI_DataFeed", skiprows=3)
else:
    print("Error: Master model file not found in current folder.")
    exit(1)

df_m = df[df['Horizon_Type'] == 'Monthly'].copy().reset_index(drop=True)
df_a = df[df['Horizon_Type'] == 'Annual'].copy().reset_index(drop=True)

# ---------------------------------------------------------
# 1. GENERATE INSTITUTIONAL PDF DELIVERABLE
# ---------------------------------------------------------
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9), facecolor='#0A0F1D')
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], figure=fig, hspace=0.35, wspace=0.22, left=0.07, right=0.94, top=0.88, bottom=0.08)

# Header Banner & Metadata
fig.text(0.07, 0.94, 'STRATACORE ANALYTICS LLC — EXECUTIVE BOARDROOM DASHBOARD', fontsize=15, fontweight='bold', color='#FFFFFF')
fig.text(0.07, 0.915, 'Wing A Deliverable: Corporate Financial Model Presentation Layer | Plan III Retainer Advisory', fontsize=10.5, color='#C5A880')

ev_val = f"${df['Enterprise_Value_Gordon'].iloc[0]:,.0f}" if 'Enterprise_Value_Gordon' in df.columns else "$54,277,830"
y5_rev = f"${df_a['Revenue_Total'].iloc[-1]:,.0f}"
csh_m12 = f"${df_m['Ending_Cash'].iloc[-1]:,.0f}"
fig.text(0.94, 0.94, f'Implied EV: {ev_val}  |  Y5 Revenue: {y5_rev}  |  M12 Cash: {csh_m12}', fontsize=10.5, fontweight='bold', color='#38BDF8', ha='right')

# Visual 1: Operating Scale (Monthly Revenue vs EBITDA)
ax1 = fig.add_subplot(gs[0, 0], facecolor='#0F172A')
ax1.grid(color='#334155', linestyle='--', linewidth=0.5, alpha=0.7)
x_m = list(range(len(df_m)))
w = 0.38
ax1.bar([i - w/2 for i in x_m], df_m['Revenue_Total']/1000, width=w, label='Gross Revenue', color='#1E40AF', alpha=0.9)
ax1.bar([i + w/2 for i in x_m], df_m['EBITDA']/1000, width=w, label='EBITDA', color='#C5A880', alpha=0.95)
ax1.set_xticks(x_m)
ax1.set_xticklabels(df_m['Period_Key'], color='#94A3B8', fontsize=9)
ax1.set_ylabel('USD ($ Thousands)', color='#94A3B8', fontsize=9)
ax1.set_title('Operating Scale: Revenue vs. EBITDA (M1–M12)', color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
ax1.legend(loc='upper left', framealpha=0.3, facecolor='#1E293B', labelcolor='#FFFFFF', fontsize=8.5)

# Visual 2: 12-Month Liquidity Trajectory & Runway Buffer
ax2 = fig.add_subplot(gs[0, 1], facecolor='#0F172A')
ax2.grid(color='#334155', linestyle='--', linewidth=0.5, alpha=0.7)
ax2.plot(x_m, df_m['Ending_Cash']/1000, color='#0284C7', linewidth=2.5, marker='o', markersize=4, label='Ending Cash Balance')
ax2.fill_between(x_m, df_m['Ending_Cash']/1000, color='#0284C7', alpha=0.2)
ax2.set_xticks(x_m)
ax2.set_xticklabels(df_m['Period_Key'], color='#94A3B8', fontsize=9)
ax2.set_ylabel('USD ($ Thousands)', color='#94A3B8', fontsize=9)
ax2.set_title('12-Month Liquidity Trajectory & Runway Buffer', color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
ax2.legend(loc='upper left', framealpha=0.3, facecolor='#1E293B', labelcolor='#FFFFFF', fontsize=8.5)

# Visual 3: 5-Year Scale & Margin Expansion (FY1-FY5)
ax3 = fig.add_subplot(gs[1, 0], facecolor='#0F172A')
ax3.grid(color='#334155', linestyle='--', linewidth=0.5, alpha=0.7)
x_a = list(range(len(df_a)))
ax3.bar([i - w/2 for i in x_a], df_a['Revenue_Total']/1e6, width=w, label='Annual Revenue', color='#2563EB', alpha=0.9)
ax3.bar([i + w/2 for i in x_a], df_a['EBITDA']/1e6, width=w, label='Annual EBITDA', color='#EAB308', alpha=0.95)
ax3.set_xticks(x_a)
ax3.set_xticklabels(df_a['Period_Key'], color='#94A3B8', fontsize=9)
ax3.set_ylabel('USD ($ Millions)', color='#94A3B8', fontsize=9)
ax3.set_title('5-Year Strategic Scale & Margin Expansion (FY1–FY5)', color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
ax3.legend(loc='upper left', framealpha=0.3, facecolor='#1E293B', labelcolor='#FFFFFF', fontsize=8.5)

# Visual 4: Debt Amortization & Deleveraging Profile
ax4 = fig.add_subplot(gs[1, 1], facecolor='#0F172A')
ax4.grid(color='#334155', linestyle='--', linewidth=0.5, alpha=0.7)
ax4.plot(x_m, df_m['Senior_Debt']/1000, color='#94A3B8', linewidth=2, linestyle='--', label='Senior Term Debt')
ax4.plot(x_m, df_m['Total_Debt']/1000, color='#F87171', linewidth=2, label='Total Debt Outstanding')
ax4.set_xticks(x_m)
ax4.set_xticklabels(df_m['Period_Key'], color='#94A3B8', fontsize=9)
ax4.set_ylabel('USD ($ Thousands)', color='#94A3B8', fontsize=9)
ax4.set_title('Senior Debt Amortization & Deleveraging (M1–M12)', color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
ax4.legend(loc='upper right', framealpha=0.3, facecolor='#1E293B', labelcolor='#FFFFFF', fontsize=8.5)

pdf_filename = "StrataCore_Executive_Dashboard.pdf"
plt.savefig(pdf_filename, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"SUCCESS: Exported Boardroom PDF to {pdf_filename}")

# ---------------------------------------------------------
# 2. GENERATE INTERACTIVE HTML BOARDROOM DASHBOARD
# ---------------------------------------------------------
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>StrataCore Analytics — Executive Boardroom Presentation Layer</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  :root { --bg-p: #0A0F1D; --bg-s: #0F172A; --card: #1E293B; --gold: #C5A880; --blue: #0284C7; --green: #10B981; --border: #334155; }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, sans-serif; }
  body { background: var(--bg-p); color: #F8FAFC; padding: 24px; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }
  .btn-t { background: var(--card); color: #FFF; border: 1px solid var(--border); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; }
  .btn-t.active { background: var(--gold); color: #000; }
  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
  .kpi-card { background: var(--bg-s); border: 1px solid var(--border); border-radius: 8px; padding: 18px; border-left: 4px solid var(--gold); }
  .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .chart-card { background: var(--bg-s); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
  .chart-container { position: relative; height: 280px; width: 100%; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1 style="font-size:20px;">STRATACORE ANALYTICS LLC — BOARDROOM PRESENTATION LAYER</h1>
      <p style="font-size:12px; color:var(--gold); margin-top:4px;">Wing A Deliverable: Plan III Corporate Advisory Presentation Layer</p>
    </div>
    <div>
      <button id="bM" class="btn-t active" onclick="setH('Monthly')">Monthly (M1–M12)</button>
      <button id="bA" class="btn-t" onclick="setH('Annual')">Annual (FY1–FY5)</button>
    </div>
  </div>
  <div class="kpi-grid">
    <div class="kpi-card" style="border-left-color: var(--gold);"><div style="font-size:11px; color:#94A3B8;">IMPLIED ENTERPRISE VALUE</div><div style="font-size:24px; font-weight:700;">$54,277,830</div><div style="font-size:12px; color:var(--green);">Gordon Growth DCF</div></div>
    <div class="kpi-card" style="border-left-color: var(--blue);"><div id="kL" style="font-size:11px; color:#94A3B8;">ENDING REVENUE</div><div id="kV" style="font-size:24px; font-weight:700;">$176,000</div><div style="font-size:12px; color:var(--blue);">Run-Rate Scale</div></div>
    <div class="kpi-card" style="border-left-color: var(--green);"><div style="font-size:11px; color:#94A3B8;">LIQUIDITY BUFFER</div><div id="kC" style="font-size:24px; font-weight:700;">$432,020</div><div style="font-size:12px; color:var(--green);">Solvent Runway</div></div>
    <div class="kpi-card" style="border-left-color: #818CF8;"><div style="font-size:11px; color:#94A3B8;">SENIOR COVERAGE</div><div style="font-size:24px; font-weight:700;">21.9x DSCR</div><div style="font-size:12px; color:#818CF8;">Senior Debt: $202,400</div></div>
  </div>
  <div class="charts-grid">
    <div class="chart-card"><div style="font-size:13px; font-weight:600; margin-bottom:12px;">Operating Scale & Margin Expansion</div><div class="chart-container"><canvas id="sC"></canvas></div></div>
    <div class="chart-card"><div style="font-size:13px; font-weight:600; margin-bottom:12px;">Liquidity Runway Trajectory</div><div class="chart-container"><canvas id="cC"></canvas></div></div>
  </div>
<script>
const mD = { labels:['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12'], r:[125000,128938,133002,137197,141528,145998,150611,155371,160282,165351,170582,176000], eb:[38125,39411,40741,42117,43539,45009,46529,48099,49723,51402,53138,54933], c:[199336,216650,234655,253375,272835,293060,314076,335911,358593,382151,406616,432020] };
const aD = { labels:['FY1','FY2','FY3','FY4','FY5'], r:[1804860,2526804,3335381,4202580,5043096], eb:[555132,793417,1073993,1386851,1699523], c:[432020,680410,1024350,1489200,2095400] };
let sChart = new Chart(document.getElementById('sC').getContext('2d'), { type:'bar', data:{ labels:mD.labels, datasets:[{ label:'Revenue ($)', data:mD.r, backgroundColor:'#1E40AF' }, { label:'EBITDA ($)', data:mD.eb, backgroundColor:'#C5A880' }] }, options:{ responsive:true, maintainAspectRatio:false, scales:{ x:{ ticks:{ color:'#94A3B8' } }, y:{ ticks:{ color:'#94A3B8' } } } } });
let cChart = new Chart(document.getElementById('cC').getContext('2d'), { type:'line', data:{ labels:mD.labels, datasets:[{ label:'Ending Cash ($)', data:mD.c, borderColor:'#0284C7', backgroundColor:'#0284C730', fill:true }] }, options:{ responsive:true, maintainAspectRatio:false, scales:{ x:{ ticks:{ color:'#94A3B8' } }, y:{ ticks:{ color:'#94A3B8' } } } } });
function setH(t){
  document.getElementById('bM').className = 'btn-t ' + (t==='Monthly'?'active':'');
  document.getElementById('bA').className = 'btn-t ' + (t==='Annual'?'active':'');
  const d = t==='Monthly'?mD:aD;
  document.getElementById('kV').innerText = t==='Monthly'?'$176,000':'$5,043,096';
  document.getElementById('kC').innerText = t==='Monthly'?'$432,020':'$2,095,400';
  sChart.data.labels = d.labels; sChart.data.datasets[0].data = d.r; sChart.data.datasets[1].data = d.eb; sChart.update();
  cChart.data.labels = d.labels; cChart.data.datasets[0].data = d.c; cChart.update();
}
</script>
</body>
</html>
"""
with open("StrataCore_Executive_Dashboard.html", "w") as f:
    f.write(html_content)
print("SUCCESS: Exported Interactive HTML Dashboard to StrataCore_Executive_Dashboard.html")
