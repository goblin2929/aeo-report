/* Comments on the E-V2 phone of the copy review page (Eki, 27 Nov 2026: Zi En reviews E-V2 here).
   Click a heading, line, paragraph, button or photo in the E-V2 phone, or select a few words, type and press Send.
   Comments go to the internal Sheet through the Apps Script web app; status and our reply show under the phone. */
(() => {
const ENDPOINT = "https://script.google.com/macros/s/AKfycbwCWFYq54DoLL3dW8AXUdhpjaRVr-wW99wd915O7D-zZbWBV63QHj7li7j0jSv5joAn/exec";
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const store = {get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } },
               set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }};
const toast = t => { const x = $("#zcToast"); x.textContent = t; x.classList.add("show"); clearTimeout(toast._t); toast._t = setTimeout(() => x.classList.remove("show"), 2600); };
const post = body => fetch(ENDPOINT, {method: "POST", headers: {"Content-Type": "text/plain;charset=utf-8"}, body: JSON.stringify(body)}).then(r => r.json());
const API = {
  all: () => fetch(ENDPOINT + "?action=list&t=" + Date.now()).then(r => r.json()).then(j => j.comments || []),
  add: c => post({action: "add", comment: c}).then(j => { if (!j.ok) throw new Error(j.error); }),
  del: id => post({action: "delete", id}).then(j => { if (!j.ok) throw new Error(j.error); })};
const KIND = {heading: "Heading", paragraph: "Paragraph", item: "List item", button: "Button", image: "Photo",
              words: "Selected words", text: "Text", page: "Whole page"};

let all = [], loaded = false, mine = store.get("zc_mine", []), doc = null, frame = null, pending = null, selState = null;
const cur = () => { const slug = location.hash.slice(1).split(":")[0]; return D.pages.find(x => x.slug === slug) || D.pages[0]; };
const key = () => cur().slug;
const pageComments = () => all.filter(c => c.page === key() && !c.deleted).sort((a, b) => String(a.time).localeCompare(String(b.time)));

/* ---------- what can be commented on ---------- */
const BLOCK = "h1,h2,h3,h4,h5,h6,p,li,label,td,th,.qh,.r,a.btn,button,.mt";
const IMG_SEL = "img,[style*='background-image']";
const ownText = el => [...el.childNodes].some(n => n.nodeType === 3 && n.data.trim());
const isPhoto = el => el.matches(IMG_SEL) && !(el.textContent.trim() && el.tagName !== "SECTION" && !el.matches("[class*=hero]") && ownText(el));
const kindOf = el => isPhoto(el) ? "image" : /^H[1-6]$/.test(el.tagName) || el.matches(".qh") ? "heading" :
  el.tagName === "P" ? "paragraph" : el.tagName === "LI" || el.matches(".r") ? "item" : el.matches("a.btn,button") ? "button" : "text";
function pick(t) {
  if (!t || !doc || t === doc.body || t.closest(".zc-b")) return null;
  const chip = t.closest(".pk,.cpick > span,.mt > em"); if (chip) return chip;
  const blk = t.closest(BLOCK); if (blk && blk.textContent.trim()) return blk;
  if (ownText(t)) { let e = t; while (e.parentElement && e.parentElement !== doc.body && doc.defaultView.getComputedStyle(e).display.startsWith("inline")) e = e.parentElement; return e; }
  if (t.tagName === "IMG") return t;
  return t.closest(IMG_SEL);
}
const allEls = () => [...doc.body.querySelectorAll("*")];
const imgUrl = el => { const raw = el.tagName === "IMG" ? el.getAttribute("src") : ((el.style.backgroundImage || "").match(/url\(["']?([^"')]+)/) || [])[1] || ""; try { return new URL(raw, doc.baseURI).href; } catch (e) { return raw; } };
const textOf = el => (el.innerText || el.textContent).replace(/\s+/g, " ").replace(/^[−+]\s+/, "").trim();
const snip = el => kindOf(el) === "image" ? "photo:" + imgUrl(el).split("/").pop() : textOf(el).slice(0, 160);

/* ---------- the E-V2 phone ---------- */
function attach() {
  const col = document.getElementById("col-EV2");
  tabCounts();
  doc = null; frame = null; closeComposer(true); hideSel();
  if (!col) return;
  if (!document.getElementById("zcHint")) $("#cols").insertAdjacentHTML("beforebegin", `<p class="zc-hint" id="zcHint"><b>Your comments on E-V2:</b> click any heading, sentence, button or photo in the <b>E-V2 phone</b>, type your comment and press <b>Send</b>. To comment on a few words, select them first. Your comments show under the E-V2 phone.</p>`);
  col.insertAdjacentHTML("beforeend", `<div class="zc-box"><h3 id="zcTitle">Comments on E-V2</h3><button class="zc-whole zc-top" id="zcWhole" type="button">Comment on the whole page</button><div class="zc-list" id="zcList"></div></div>`);
  $("#zcWhole").onclick = () => openComposer(null, null);
  frame = col.querySelector("iframe");
  list();
  const t0 = Date.now(), poll = setInterval(() => {
    if (!frame || !frame.isConnected || Date.now() - t0 > 30000) return clearInterval(poll);
    const d = frame.contentDocument;
    if (d && d.body && d.querySelector("section[data-i]") && !d.getElementById("upd") && !d.__zc) { clearInterval(poll); prepare(d); }
  }, 250);
}
function tabCounts() {
  document.querySelectorAll(".tab").forEach(b => { const n = all.filter(c => c.page === b.dataset.s && !c.deleted).length;
    if (n && !b.querySelector(".zc-cnt")) b.insertAdjacentHTML("beforeend", `<span class="zc-cnt">${n}</span>`); });
}
function prepare(d) {
  d.__zc = true; doc = d;
  const st = d.createElement("style");
  st.textContent = `.zc-hov{outline:2px dashed #00788a!important;outline-offset:2px;cursor:pointer}
  .zc-mark{outline:2px solid #ffd54a!important;outline-offset:2px;background-color:rgba(255,213,74,.18)}
  .zc-mark.zc-on,.zc-on{outline:3px solid #c8102e!important;outline-offset:2px}
  mark.zc-w{background:#ffd54a;color:inherit;padding:0 1px}
  .zc-b{position:absolute;z-index:30;min-width:22px;height:22px;padding:0 6px;border-radius:11px;background:#ffd54a;color:#1f2328;
        font:700 12px/22px -apple-system,Segoe UI,sans-serif;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.3);cursor:pointer}
  .qa{display:block!important}`;
  d.head.appendChild(st);
  d.querySelectorAll(".qh em").forEach(m => m.textContent = "−");
  d.querySelectorAll(".q").forEach(q => q.classList.add("open"));
  let hov = null;
  d.addEventListener("mouseover", e => { const el = pick(e.target); if (hov) hov.classList.remove("zc-hov"); hov = el;
    if (el && !e.target.closest("[data-dd],[data-menu],[data-wsel]")) el.classList.add("zc-hov"); });
  d.addEventListener("click", e => {
    const b = e.target.closest(".zc-b"); if (b) { e.preventDefault(); e.stopImmediatePropagation(); viewComment(b.dataset.id); return; }
    if (e.target.closest("[data-dd],[data-menu],[data-wsel]")) return;  // menus and the week switch keep working
    e.preventDefault(); e.stopImmediatePropagation();
    const s = d.getSelection(); if (s && !s.isCollapsed && s.toString().trim()) return;
    const el = pick(e.target); if (el) openComposer(el, null);
  }, true);
  const onSel = () => { clearTimeout(onSel._t); onSel._t = setTimeout(() => {
    const s = d.getSelection();
    if (!s || s.isCollapsed || !s.toString().trim()) return hideSel();
    const node = s.anchorNode.nodeType === 3 ? s.anchorNode.parentElement : s.anchorNode;
    selState = {el: pick(node) || node, words: s.toString().replace(/\s+/g, " ").trim()}; const sb = $("#zcSel"); sb.hidden = false;
    const r = frame.closest(".phone").getBoundingClientRect(); sb.classList.add("anch"); sb.style.left = Math.max(16, r.left + r.width / 2 - sb.offsetWidth / 2) + "px";
  }, 200); };
  d.addEventListener("mouseup", onSel); d.addEventListener("touchend", onSel); d.addEventListener("selectionchange", onSel);
  paint();
}
function hideSel() { $("#zcSel").hidden = true; selState = null; }
$("#zcSelBtn").onmousedown = e => e.preventDefault();
$("#zcSelBtn").onclick = () => { if (!selState || !doc) return; const {el, words} = selState; hideSel(); doc.getSelection().removeAllRanges(); openComposer(el, words); };

/* ---------- comment box ---------- */
const unsent = () => !$("#zcCmp").hidden && $("#zcText").value.trim();
function openComposer(el, words) {
  const kind = words ? "words" : el ? kindOf(el) : "page";
  pending = {el, kind, words};
  $("#zcWhat").textContent = "Comment on E-V2: " + KIND[kind];
  const q = $("#zcQuote");
  if (kind === "image") q.innerHTML = `<img src="${esc(imgUrl(el))}" alt="The photo you clicked">`;
  else if (kind === "page") q.textContent = cur().title + " page";
  else q.textContent = words || textOf(el);
  const kept = unsent();
  $("#zcCmp").hidden = false; if (!kept) $("#zcText").value = ""; else toast("Your typed comment is kept. It now points here.");
  $("#zcName").value = $("#zcName").value || store.get("zc_name", "");
  hideSel();
  if (doc) doc.querySelectorAll(".zc-on").forEach(x => x.classList.remove("zc-on"));
  if (el) { el.classList.add("zc-on"); showTarget(el); }
  $("#zcView").hidden = true;
  setTimeout(() => $("#zcText").focus({preventScroll: true}), 30);
}
const narrow = () => window.innerWidth <= 700;
function showTarget(el) {  // the clicked part stays in sight, above the box on a phone
  const w = doc.defaultView, top = el.getBoundingClientRect().top + w.scrollY;
  w.scrollTo({top: Math.max(0, top - 16), behavior: "smooth"});
  if (narrow()) { const ph = frame.closest(".phone").getBoundingClientRect(), hd = document.querySelector(".bar").offsetHeight;
    window.scrollTo({top: window.scrollY + ph.top - (document.querySelector(".bar").style.position === "static" ? 0 : hd) - 4, behavior: "smooth"}); }
}
function closeComposer(silent) {
  $("#zcText").value = ""; $("#zcCmp").hidden = true; pending = null;
  if (doc) doc.querySelectorAll(".zc-on").forEach(x => x.classList.remove("zc-on"));
}
$("#zcCancel").onclick = () => { if (!$("#zcText").value.trim() || confirm("Discard the comment you typed?")) closeComposer(); };
$("#zcSend").onclick = async () => {
  const text = $("#zcText").value.trim(), name = $("#zcName").value.trim();
  if (!text) { $("#zcText").focus(); toast("Please type your comment first."); return; }
  if (!name) { $("#zcName").focus(); toast("Please add your name, so we know who wrote it."); return; }
  store.set("zc_name", name);
  const {el, kind, words} = pending, els = el && doc ? allEls() : [];
  const c = {id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), page: key(),
    pageTitle: cur().title + " (E-V2)", kind, label: KIND[kind], tag: el ? el.tagName : "", idx: el ? els.indexOf(el) : -1,
    snip: el ? snip(el) : "", words: words || "", image: kind === "image" ? imgUrl(el) : "",
    text, name, time: new Date().toISOString(), status: "Open", reply: ""};
  const b = $("#zcSend"); b.disabled = true; b.textContent = "Sending...";
  try { await API.add(c); all.push(c); mine.push(c.id); store.set("zc_mine", mine); closeComposer(); refreshTabs(); list(); paint(); toast("Thank you, your comment is saved.");
  } catch (err) { toast("Could not save. Please check your connection and press Send again."); }
  b.disabled = false; b.textContent = "Send comment";
};

/* ---------- markers in the phone ---------- */
function findEl(c) {
  if (!doc || c.idx < 0) return null;
  const t = allEls(); if (t[c.idx] && snip(t[c.idx]) === c.snip) return t[c.idx];
  return t.find(x => x.tagName === c.tag && snip(x) === c.snip) || t.find(x => snip(x) === c.snip) ||
    t.find(x => c.snip && !String(c.snip).startsWith("photo:") && snip(x).startsWith(String(c.snip).slice(0, 60))) || null;
}
function markWords(el, words) {
  const w = doc.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
  while ((n = w.nextNode())) { const i = n.data.indexOf(words); if (i >= 0) { const r = doc.createRange(); r.setStart(n, i); r.setEnd(n, i + words.length);
    const m = doc.createElement("mark"); m.className = "zc-w"; r.surroundContents(m); return m; } }
  return null;
}
function paint() {
  if (!doc || !doc.body) return;
  doc.querySelectorAll(".zc-b").forEach(x => x.remove());
  doc.querySelectorAll(".zc-mark").forEach(x => x.classList.remove("zc-mark"));
  doc.querySelectorAll("mark.zc-w").forEach(m => m.replaceWith(...m.childNodes));
  const w = doc.defaultView, placed = [];
  pageComments().forEach((c, i) => {
    const el = findEl(c); if (!el) return;
    const tgt = (c.words && markWords(el, c.words)) || el;
    const bgPhoto = c.kind === "image" && el.tagName !== "IMG" && textOf(el);
    if (!c.words && !bgPhoto) el.classList.add("zc-mark");
    const r = tgt.getBoundingClientRect(), b = doc.createElement("span");
    b.className = "zc-b"; b.dataset.id = c.id; b.textContent = bgPhoto ? `${i + 1} · photo` : i + 1; b.title = c.text;
    let x = bgPhoto ? r.right + w.scrollX - 80 : Math.max(2, r.left + w.scrollX - 8), y = bgPhoto ? r.top + w.scrollY + 10 : Math.max(2, r.top + w.scrollY - 12);
    while (placed.some(([px, py]) => Math.abs(px - x) < 28 && Math.abs(py - y) < 24)) x += 28;
    placed.push([x, y]); b.style.left = x + "px"; b.style.top = y + "px";
    doc.body.appendChild(b);
  });
}

/* ---------- list under the phone ---------- */
function list() {
  const box = $("#zcList"); if (!box) return;
  const cs = pageComments();
  $("#zcTitle").textContent = loaded ? `Comments on E-V2 (${cs.length})` : "Loading comments...";
  box.innerHTML = cs.length ? cs.map((c, i) => `<div class="zc-c" data-id="${c.id}">
    <div class="h"><span class="zc-num">${i + 1}</span><span>${esc(c.label)} · ${esc(c.name)} · ${new Date(c.time).toLocaleDateString("en-SG", {day: "numeric", month: "short"})}</span>
    ${mine.includes(c.id) && (c.status || "Open") === "Open" ? `<button class="del" data-del="${c.id}" type="button">Delete</button>` : ""}</div>
    ${c.kind === "page" ? "" : c.kind === "image" ? `<img class="thumb" src="${esc(c.image)}" alt="The photo this comment is about">` : `<div class="q">${esc(c.words || c.snip)}</div>`}
    <div class="t">${esc(c.text)}</div>
    ${c.status && c.status !== "Open" ? `<div class="st"><b>${esc(c.status)}</b>${c.reply ? ": " + esc(c.reply) : ""}</div>` : ""}</div>`).join("")
    : loaded ? `<p class="zc-empty">No comments yet. Click anything in the E-V2 phone to add one.</p>` : "";
  box.querySelectorAll(".zc-c").forEach(x => x.onclick = e => { if (!e.target.closest("[data-del]")) focusComment(x.dataset.id); });
  box.querySelectorAll("[data-del]").forEach(x => x.onclick = async () => {
    if (!confirm("Delete this comment?")) return;
    try { await API.del(x.dataset.del); all = all.filter(c => c.id !== x.dataset.del); refreshTabs(); list(); paint(); toast("Comment deleted."); }
    catch (e) { toast("Could not delete. Please try again."); } });
}
function refreshTabs() { document.querySelectorAll(".tab .zc-cnt").forEach(x => x.remove()); tabCounts(); }
$("#zcViewClose").onclick = () => { $("#zcView").hidden = true; if (doc) doc.querySelectorAll(".zc-on").forEach(x => x.classList.remove("zc-on")); };
function viewComment(id) {
  if (unsent()) return focusComment(id);
  const cs = pageComments(), i = cs.findIndex(x => x.id === id), c = cs[i]; if (!c) return;
  $("#zcViewH").innerHTML = `<span class="zc-num">${i + 1}</span><span>${esc(c.label)} · ${esc(c.name)}</span>`;
  $("#zcViewT").textContent = c.text;
  $("#zcViewS").innerHTML = c.status && c.status !== "Open" ? `<div class="st"><b>${esc(c.status)}</b>${c.reply ? ": " + esc(c.reply) : ""}</div>` : "";
  $("#zcView").hidden = false; focusComment(id, true);
}
function focusComment(id, fromMarker) {
  document.querySelectorAll(".zc-c").forEach(x => x.classList.toggle("on", x.dataset.id === id));
  const c = all.find(x => x.id === id), el = c && findEl(c); if (!el) return;
  doc.querySelectorAll(".zc-on").forEach(x => x.classList.remove("zc-on")); el.classList.add("zc-on");
  const w = doc.defaultView; w.scrollTo({top: el.getBoundingClientRect().top + w.scrollY - 80, behavior: "smooth"});
  if (!fromMarker) frame.closest(".col").querySelector(".phone").scrollIntoView({block: "nearest", behavior: "smooth"});
}

/* ---------- start: hook the page switch, then load comments ---------- */
const orig = window.render;
window.addEventListener("beforeunload", e => { if (unsent()) { e.preventDefault(); e.returnValue = ""; } });
let lastHash = location.hash;
window.render = h => {
  if (unsent() && !confirm("You have a comment you have not sent yet. Leave it and open another page?")) { history.replaceState(null, "", lastHash || "#"); return; }
  lastHash = location.hash; orig(h); attach();
};
attach();
API.all().then(got => { all = got; }).catch(() => toast("Could not load earlier comments. Please refresh the page."))
  .finally(() => { loaded = true; refreshTabs(); list(); paint(); });
})();
