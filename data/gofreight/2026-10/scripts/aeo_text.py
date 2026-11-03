_RC=json.load(open('/Users/ekiriandra/tmp/oct/wd_oct.json'))['monthly_response_counts']
rc_n,rc_j=_RC['2026-09'],_RC['2026-10']; cpr_n,cpr_j=ac_n/rc_n,ac_j/rc_j
_W=json.load(open('/Users/ekiriandra/tmp/oct/wd_oct.json'))
_hp=_W['subfolder_rollup']['Homepage']; hp_n,hp_j=_hp['jun_cit'],_hp['jul_cit']
vis_hook=f"Non brand AI visibility rose from <strong>{VIS_N:.1f}% to {VIS_J:.1f}%</strong>, a new high."
vis_read=(f"Non brand visibility reached <b>{VIS_J:.1f}% for October</b> (from {VIS_N:.1f}% in September), the highest completed month in the series. "
  "<b>ChatGPT rose from 34% to 36% in early October to 37% to 41%</b> in the last three weeks and <b>Perplexity reached 45%</b> in the week of Oct 26. "
  "Google AI Overview moved between 31% and 40% week to week.")
aeo_box=f'''<div class="takeaway-box win"><b>AEO performance: GoFreight is named in more AI answers.</b>
      <ul>
        <li><b>Non brand AI visibility rose {VIS_J-VIS_N:+.1f} pts</b> ({VIS_N:.1f}% to {VIS_J:.1f}%), the strongest month so far, with gains on ChatGPT and Perplexity.</li>
        <li><b>AI citations grew {cit_p:+.1f}%</b> ({f(ac_n)} to {f(ac_j)}) and the number of GoFreight pages cited grew from {TOT['jun_pages']} to {TOT['jul_pages']}. WorkDuo collected more answers in October ({f(rc_n)} to {f(rc_j)}), so per answer the rate eased from {cpr_n:.2f} to {cpr_j:.2f} citations; visibility is a rate and is not affected by the extra answers.</li>
        <li><b>AI Platform Sessions {ais_p:+.1f}%</b> ({f(AIS_N)} to {f(AIS_J)}, GA4 direct): the ChatGPT tracking bug of 8 to 15 October explains part of the ChatGPT decline, and Gemini nearly doubled.</li>
      </ul>
    </div>
    <div class="takeaway-box watch"><b>Watch: homepage citations.</b> AI answers cited the homepage {f(hp_n)} times in September and {f(hp_j)} in October, while the commercial blog posts gained. The homepage was redesigned at the end of October; we track its citations in November together with its keyword positions.</div>'''
top15_read=('<div class="takeaway-box"><b>Read: the commercial pages keep winning AI citations, and the October refreshes are among the gainers.</b> '
  'The two refreshed comparison listicles lead: <a href="https://gofreight.com/blog/best-tms-software" target="_blank">best TMS software</a> (572 to 655) and <a href="https://gofreight.com/blog/best-freight-management-software" target="_blank">best freight management software</a> (507 to 618). '
  '<a href="https://gofreight.com/blog/freight-forwarder-tech-stack" target="_blank">Freight forwarder tech stack</a>, refreshed on 14 Oct, more than doubled (92 to 205), and <a href="https://gofreight.com/blog/why-freight-forwarders-need-specialized-software" target="_blank">why freight forwarders need specialized software</a> entered the top 15 (36 to 186). '
  'Most of these pages get few Google clicks, which is why the click winners and the AI citation winners remain two different lists.</div>')
lp_read=('<div class="takeaway-box" style="margin-top:10px;"><b>Where ChatGPT visits landed:</b> the homepage stayed the main ChatGPT landing page (126 to 92 recorded sessions), and the declines are spread across many pages rather than one topic, which fits a tracking gap more than a content problem. '
  'New ChatGPT visits also reached help center articles in the knowledge base (for example user permissions and e-AWB air export shipments), a sign that people use ChatGPT to find GoFreight how to answers.</div>')
