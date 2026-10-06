vis_hook=f"AI visibility rose from <strong>{VIS_N:.1f}% to {VIS_J:.1f}%</strong> and AI citations of GoFreight pages grew <strong>{cit_p:+.1f}% ({f(ac_n)} to {f(ac_j)})</strong>."
vis_read=(f"Non brand visibility rose to <b>{VIS_J:.1f}% for September</b> (from {VIS_N:.1f}% in August), the highest month in the series. "
  "<b>ChatGPT held in the 31% to 36% band every week of September</b>, up from 16% to 26% in early August, and Perplexity stayed in the high 30s. "
  "Google AI Overview was more volatile week to week (28% to 36%).")
aeo_box=f'''<div class="takeaway-box win"><b>AEO performance: visibility, citations and sessions all grew.</b>
      <ul>
        <li><b>Non brand AI visibility rose {VIS_J-VIS_N:+.1f} pts</b> ({VIS_N:.1f}% to {VIS_J:.1f}%), the strongest month so far, with the largest step up on ChatGPT.</li>
        <li><b>AI citations grew {cit_p:+.1f}%</b> ({f(ac_n)} to {f(ac_j)}) on a wider page set ({TOT['jun_pages']} to {TOT['jul_pages']} pages). The comparison and buying guide blogs carry most of the load.</li>
        <li><b>AI Platform Sessions grew {ais_p:+.1f}%</b> ({f(AIS_N)} to {f(AIS_J)}, GA4 direct), led by ChatGPT.</li>
      </ul>
    </div>
    <div class="takeaway-box watch"><b>Being cited is not the same as being recommended.</b> Visibility counts answers that name GoFreight; citations count answers that use a GoFreight page as a source. Many answers still quote a GoFreight blog post and then recommend another vendor, which is why the October work focuses on the solution and product pages that assistants use for vendor claims.</div>'''
top15_read=('<div class="takeaway-box"><b>Read: SEO winners and AEO winners are still different pages.</b> Google clicks flow to glossary and educational content; AI engines answering buying intent prompts cite the <b>commercial pages</b>: best TMS software, platform overview, the FMS listicle, cargowise vs gofreight and the reviews page. '
  'Note that the <a href="https://gofreight.com/blog/best-freight-management-software" target="_blank">FMS listicle</a> gained AI citations in September (373 to 507) even while it lost its Google position, so its value to AI answers is intact. '
  'Newer comparison pages such as <a href="https://gofreight.com/blog/transparent-freight-software-pricing" target="_blank">transparent freight software pricing</a> (62 to 190) and <a href="https://gofreight.com/blog/best-freight-customer-portal-software" target="_blank">best freight customer portal software</a> (53 to 189) entered the top 15.</div>')
