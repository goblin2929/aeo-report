set -e
cd /Users/ekiriandra/tmp/oct
python3 build_oct_report.py | tail -1
python3 write_oct_report.py | tail -1
cp /Users/ekiriandra/seo-projects/novastacks/clients/gofreight/output/reports/gofreight_october_2026_report.html /Users/ekiriandra/seo-projects/aeo-report/
python3 apply_core17_oct.py | tail -1
python3 postfix_oct.py
