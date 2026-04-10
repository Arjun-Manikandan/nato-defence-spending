# nato-defence-spending
A Python data analysis project examining defence spending trends (as % of GDP) across NATO member states from 2014–2023, using publicly reported SIPRI and NATO figures.
What this project does
Loads and cleans real NATO spending data
Identifies which member states meet the 2% GDP commitment — and which don't
Analyses the post-Ukraine-invasion spending shift across member states
Produces three publication-quality charts saved to `/output/`
Why I built this
Reading Peter Thiel's Zero to One and Marc Andreessen's Techno-Optimist Manifesto got me thinking seriously about the relationship between technology, state capability, and national security. Palantir's work — building data infrastructure for defence and government — sits directly at that intersection. I wanted to understand the data behind the funding commitments that underpin it.
The question that motivated this: after decades of underspending, are NATO members actually changing behaviour in response to a genuine security threat, or is the rhetoric outpacing the numbers?
The data gives a mixed answer. Poland is a standout — spending nearly 4% of GDP by 2023, the highest in the dataset. Germany finally broke 2% in 2023 after years of political resistance. The UK has held roughly flat just above the target. The US, despite spending nearly 3.5% of GDP, frequently lectures allies who spend far less.
Charts produced
Chart	Description
`uk_spending_trend.png`	UK spending over time with NATO target line and Ukraine invasion marker
`nato_2023_comparison.png`	All countries ranked by 2023 spending, colour-coded by whether they meet the 2% target
`all_countries_trend.png`	Multi-country trend lines 2014–2023
How to run it
```bash
# Install dependencies
pip install pandas matplotlib

# Run the analysis
python analyse.py
```
Charts will be saved to the `/output/` folder.
Data source
SIPRI Military Expenditure Database
NATO Defence Expenditure Reports
Values are defence expenditure as a percentage of GDP, as reported by NATO.
Project structure
```
defence_spending/
├── analyse.py          # Main analysis script
├── data/
│   └── nato_spending.csv   # Dataset (SIPRI/NATO figures, 2014–2023)
└── output/             # Generated charts (created on first run)
```
