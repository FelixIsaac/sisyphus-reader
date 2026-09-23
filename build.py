import os
import json
import zipfile
import shutil
import html

BASE_DIR = "/Users/felix/Projects/Myth-of-Sisyphus-Modern-Translation"
TRANS_DIR = os.path.join(BASE_DIR, "translations")
DIST_DIR = os.path.join(BASE_DIR, "dist")
os.makedirs(DIST_DIR, exist_ok=True)
DIST_HTML = os.path.join(DIST_DIR, "index.html")
ROOT_HTML = os.path.join(BASE_DIR, "index.html")
ICLOUD_DIR = "/Users/felix/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents"

SECTION_ORDER = [
    ("c0_preface", "Introduction", "Author's Preface & Epigraph"),
    ("c1_absurdity_and_suicide", "Part I: An Absurd Reasoning", "1. Absurdity and Suicide"),
    ("c2_absurd_walls", "Part I: An Absurd Reasoning", "2. Absurd Walls"),
    ("c3_philosophical_suicide", "Part I: An Absurd Reasoning", "3. Philosophical Suicide"),
    ("c4_absurd_freedom", "Part I: An Absurd Reasoning", "4. Absurd Freedom"),
    ("c5_don_juanism", "Part II: The Absurd Man", "5. Don Juanism"),
    ("c6_drama", "Part II: The Absurd Man", "6. Drama"),
    ("c7_conquest", "Part II: The Absurd Man", "7. Conquest"),
    ("c8_philosophy_and_fiction", "Part III: Absurd Creation", "8. Philosophy and Fiction"),
    ("c9_kirilov", "Part III: Absurd Creation", "9. Kirilov"),
    ("c10_ephemeral_creation", "Part III: Absurd Creation", "10. Ephemeral Creation"),
    ("c11_myth_of_sisyphus", "Part IV: The Myth of Sisyphus", "11. The Myth of Sisyphus"),
    ("c12_kafka_appendix", "Appendix", "Hope and the Absurd in Franz Kafka")
]

# Canonical Print Pagination (Vintage International Standard Edition)
CHAPTER_PAGE_STARTS = {
    "c0_preface": 1,
    "c1_absurdity_and_suicide": 3,
    "c2_absurd_walls": 10,
    "c3_philosophical_suicide": 28,
    "c4_absurd_freedom": 51,
    "c5_don_juanism": 65,
    "c6_drama": 77,
    "c7_conquest": 85,
    "c8_philosophy_and_fiction": 93,
    "c9_kirilov": 102,
    "c10_ephemeral_creation": 113,
    "c11_myth_of_sisyphus": 119,
    "c12_kafka_appendix": 124
}
TOTAL_BOOK_PAGES = 138

def load_all_sections():
    sections = []
    for slug, default_part, default_title in SECTION_ORDER:
        json_path = os.path.join(TRANS_DIR, f"{slug}.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sections.append(data)
        else:
            print(f"Warning: {slug}.json not found yet.")
    return sections

def build_web_app(sections):
    print(f"Building Web App with {len(sections)} sections...")
    
    # Generate Table of Contents Links
    toc_html = ""
    for sec in sections:
        sec_id = sec.get("section_id", "")
        title = sec.get("title", "")
        start_p = CHAPTER_PAGE_STARTS.get(sec_id, 1)
        toc_html += f'<li><a href="#{sec_id}" onclick="toggleTOC(false)">{title} <span style="font-family:monospace; font-size:0.75rem; color:var(--text-muted); float:right;">p. {start_p}</span></a></li>\n'
    
    # Calculate book-wide stats
    total_book_blocks = sum(len(s.get("pairs", [])) for s in sections)
    total_book_words = sum(sum(len(" ".join(p.get("mod_sentences", [])).split()) for p in s.get("pairs", [])) for s in sections)
    
    # Generate Sections HTML
    sections_html = ""
    global_idx = 0
    sec_keys = [s.get("section_id", "") for s in sections]
    for s_i, sec in enumerate(sections):
        sec_id = sec.get("section_id", "")
        part = sec.get("part", "")
        title = sec.get("title", "")
        pairs = sec.get("pairs", [])
        total_sec_paras = len(pairs)
        sec_words = sum(len(" ".join(p.get("mod_sentences", [])).split()) for p in pairs)
        est_sec_mins = max(1, round(sec_words / 240))

        start_p = CHAPTER_PAGE_STARTS.get(sec_id, 1)
        next_p = CHAPTER_PAGE_STARTS.get(sec_keys[s_i + 1], 138) if s_i + 1 < len(sec_keys) else 138
        pages_span = max(1, next_p - start_p)
        end_p = max(start_p, next_p - 1 if pages_span > 1 else start_p)
        page_range_str = f"pp. {start_p}–{end_p}" if end_p > start_p else f"p. {start_p}"
        
        sections_html += f"""
        <section class="book-section" id="{sec_id}" data-sec-id="{sec_id}" data-sec-title="{html.escape(title)}" data-sec-paras="{total_sec_paras}" data-sec-pages="{page_range_str}">
          <div class="section-badge">{part}</div>
          <h2 class="section-title">{title}</h2>
          <div class="section-meta-row">
            <span class="sec-meta-pill">📖 <strong>{page_range_str}</strong> (Vintage)</span>
            <span class="sec-meta-pill"><strong>{total_sec_paras}</strong> Paragraphs</span>
            <span class="sec-meta-pill"><strong>{sec_words:,}</strong> Words</span>
            <span class="sec-meta-pill">Est. <strong>~{est_sec_mins} min</strong></span>
            <span class="sec-meta-pill target-pill">🎯 Target: 15–20 min</span>
          </div>
          <div class="pairs-wrapper">
        """
        cum_sec_words = 0
        for p_idx, pair in enumerate(pairs, 1):
            global_idx += 1
            pid = pair.get("id", f"{sec_id}-p{p_idx}")
            orig_sents = pair.get("orig_sentences", [])
            mod_sents = pair.get("mod_sentences", [])
            move = pair.get("move", "")
            
            para_words = len(" ".join(mod_sents).split())
            est_para_secs = max(5, round(para_words / 4))
            pct_ch = round((p_idx / total_sec_paras) * 100)
            pct_book = round((global_idx / total_book_blocks) * 100)

            # Assign canonical book page based on word flow
            para_page = start_p + int((cum_sec_words / max(1, sec_words)) * pages_span)
            para_page = min(end_p, max(start_p, para_page))
            cum_sec_words += para_words
            
            sections_html += f"""
            <div class="pair-card" id="{pid}" data-pair="{pid}" data-words="{para_words}" data-sec-id="{sec_id}" data-page="{para_page}" data-p-idx="{p_idx}" data-p-total="{total_sec_paras}" data-global-idx="{global_idx}" data-global-total="{total_book_blocks}">
              <div class="col col-orig">
                <div class="col-header">
                  <span class="col-tag orig-tag">Original 1955 Translation</span>
                  <span class="para-tracker-orig">Page {para_page} • §{p_idx} of {total_sec_paras}</span>
                </div>
                <p class="para-text">
            """
            for s_idx, sent in enumerate(orig_sents):
                sid = f"{pid}-s{s_idx}"
                sections_html += f"""<span class="sent sent-orig" data-s="{sid}" onclick="handleSentClick('{sid}')">{sent} </span>"""
            
            sections_html += f"""
                </p>
              </div>
              <div class="col col-mod">
                <div class="col-header">
                  <div class="col-header-left">
                    <span class="col-tag mod-tag">Dignified Modern Translation</span>
                    <span class="para-pos-tag"><span class="badge-page">Page {para_page}</span><span class="para-sep">•</span>§{p_idx} of {total_sec_paras} <span class="para-pos-pct">({pct_ch}%)</span></span>
                  </div>
                  <div class="col-header-right">
                    <span class="para-meta-words">{para_words}w • ~{est_para_secs}s</span>
                    <button class="btn-check" id="chk-{pid}" onclick="toggleMarkRead('{pid}', {para_words}, event)" title="Toggle consumed">
                      <span class="check-icon">○</span> <span class="check-txt">Mark Read</span>
                    </button>
                  </div>
                </div>
                <p class="para-text">
            """
            for s_idx, sent in enumerate(mod_sents):
                sid = f"{pid}-s{s_idx}"
                sections_html += f"""<span class="sent sent-mod" data-s="{sid}" onclick="handleSentClick('{sid}')">{sent} </span>"""
            
            sections_html += f"""
                </p>
                <div class="move-box">
                  <div class="move-label">The Philosophical Move</div>
                  <p class="move-content">{move}</p>
                </div>
              </div>
            </div>
            """
        sections_html += """
          </div>
        </section>
        """
    
    app_template = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-view="parallel">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Camus Reader">
  <title>The Myth of Sisyphus — Complete Critical Edition</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <style>
    :root {{
      --bg: #0d0f12;
      --surface: #14171d;
      --surface-hover: #1c2028;
      --surface-orig: #121419;
      --border: #232731;
      --border-highlight: #3b4252;
      --text: #eaecee;
      --text-muted: #8b92a0;
      --text-dim: #5c6370;
      --crimson: #e05347;
      --crimson-dim: rgba(224, 83, 71, 0.15);
      --crimson-border: rgba(224, 83, 71, 0.35);
      --gold: #d19a66;
      --gold-bg: rgba(209, 154, 102, 0.22);
      --blue: #61afef;
      --blue-bg: rgba(97, 175, 239, 0.1);
      --font-serif: "Newsreader", "Charter", "Georgia", serif;
      --font-sans: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
      --font-mono: "SF Mono", Menlo, monospace;
    }}

    [data-theme="light"] {{
      --bg: #f8f6f0;
      --surface: #ffffff;
      --surface-hover: #f1ede4;
      --surface-orig: #faf8f5;
      --border: #e2ddd3;
      --border-highlight: #c8c2b5;
      --text: #1a1a1c;
      --text-muted: #5e626e;
      --text-dim: #9aa0a6;
      --crimson: #a8201a;
      --crimson-dim: rgba(168, 32, 26, 0.08);
      --crimson-border: rgba(168, 32, 26, 0.25);
      --gold: #b07226;
      --gold-bg: rgba(176, 114, 38, 0.18);
      --blue: #145374;
      --blue-bg: rgba(20, 83, 116, 0.08);
    }}

    [data-theme="sepia"] {{
      --bg: #eee4cc;
      --surface: #f7eed8;
      --surface-hover: #efe4ca;
      --surface-orig: #f4ebd5;
      --border: #dfd2b5;
      --border-highlight: #c5b694;
      --text: #2f271d;
      --text-muted: #6b5c49;
      --text-dim: #9e8e79;
      --crimson: #8f2d22;
      --crimson-dim: rgba(143, 45, 34, 0.1);
      --crimson-border: rgba(143, 45, 34, 0.3);
      --gold: #8c5b1b;
      --gold-bg: rgba(140, 91, 27, 0.2);
      --blue: #234b6e;
      --blue-bg: rgba(35, 75, 110, 0.1);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    html, body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-serif);
      font-size: 17px;
      line-height: 1.78;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* Fixed Glass Top Bar */
    header.app-bar {{
      position: sticky;
      top: 0;
      z-index: 200;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      background: rgba(13, 15, 18, 0.85);
      border-bottom: 1px solid var(--border);
      padding: 0.65rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-sans);
    }}
    [data-theme="light"] header.app-bar {{ background: rgba(248, 246, 240, 0.85); }}
    [data-theme="sepia"] header.app-bar {{ background: rgba(238, 228, 204, 0.88); }}

    .app-brand {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .brand-title {{
      font-weight: 700;
      font-size: 0.98rem;
      letter-spacing: -0.01em;
      color: var(--text);
    }}
    .brand-pill {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      background: var(--crimson-dim);
      color: var(--crimson);
      border: 1px solid var(--crimson-border);
    }}

    .app-controls {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    /* Control Buttons */
    .btn {{
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-family: var(--font-sans);
      font-size: 0.8rem;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: var(--surface-hover);
      border-color: var(--border-highlight);
    }}
    .btn.active {{
      background: var(--crimson);
      border-color: var(--crimson);
      color: #fff;
    }}

    /* Reading Progress Track & Bar */
    .reading-progress-track {{
      position: sticky;
      top: 48px;
      left: 0;
      width: 100%;
      height: 3px;
      background: rgba(255, 255, 255, 0.05);
      z-index: 199;
    }}
    .reading-progress-fill {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--crimson), var(--gold));
      transition: width 0.1s linear;
    }}

    /* Telemetry Bar */
    .telemetry-bar {{
      position: sticky;
      top: 51px;
      z-index: 198;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 0.35rem 1.4rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-sans);
      font-size: 0.76rem;
      color: var(--text-muted);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      white-space: nowrap;
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .telemetry-bar::-webkit-scrollbar {{
      display: none;
    }}
    .tele-stats {{
      display: flex;
      align-items: center;
      gap: 0.8rem;
      flex-shrink: 0;
    }}
    .tele-divider {{
      color: var(--border-highlight);
      font-size: 0.72rem;
      user-select: none;
      opacity: 0.5;
    }}
    .tele-item {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }}
    .tele-item strong {{
      color: var(--text);
      font-weight: 600;
    }}
    .tele-sub {{
      color: var(--text-dim);
      font-size: 0.72rem;
      font-family: var(--font-mono);
    }}
    .tele-timer-btn {{
      background: var(--surface-hover);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 4px;
      padding: 0.1rem 0.35rem;
      font-size: 0.68rem;
      cursor: pointer;
      line-height: 1;
      margin-left: 0.2rem;
    }}
    .pace-chip {{
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      font-family: var(--font-mono);
    }}
    .pace-chip.on-track {{
      background: rgba(39, 174, 96, 0.15);
      color: #2ecc71;
      border: 1px solid rgba(46, 204, 113, 0.3);
    }}
    .pace-chip.fast {{
      background: rgba(97, 175, 239, 0.15);
      color: #61afef;
      border: 1px solid rgba(97, 175, 239, 0.3);
    }}
    .tele-right {{
      display: flex;
      align-items: center;
      gap: 0.45rem;
      flex-shrink: 0;
      margin-left: 0.8rem;
    }}
    .tele-sync-btn {{
      background: var(--surface-orig);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 0.18rem 0.55rem;
      border-radius: 5px;
      font-size: 0.72rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      font-family: var(--font-sans);
      transition: all 0.15s ease;
    }}
    .tele-sync-btn:hover {{
      background: var(--surface-hover);
      color: var(--text);
      border-color: var(--border-highlight);
    }}

    /* Main Container */
    main.reader-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem 6rem 1.5rem;
    }}

    .book-section {{
      margin-bottom: 5rem;
      scroll-margin-top: 6rem;
    }}

    .section-badge {{
      font-family: var(--font-sans);
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--text-dim);
      margin-bottom: 0.4rem;
    }}
    .section-title {{
      font-size: 2.2rem;
      font-weight: 700;
      color: var(--crimson);
      margin-bottom: 0.8rem;
      letter-spacing: -0.01em;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.6rem;
    }}

    /* Section Metadata Row */
    .section-meta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 2rem;
      font-family: var(--font-sans);
    }}
    .sec-meta-pill {{
      font-size: 0.75rem;
      padding: 0.22rem 0.6rem;
      border-radius: 6px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }}
    .sec-meta-pill strong {{
      color: var(--text);
    }}
    .sec-meta-pill.target-pill {{
      background: var(--crimson-dim);
      color: var(--crimson);
      border-color: var(--crimson-border);
      font-weight: 600;
    }}

    /* Parallel Layout */
    .pairs-wrapper {{
      display: flex;
      flex-direction: column;
      gap: 2.2rem;
    }}

    .pair-card {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.8rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.8rem;
      transition: border-color 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
      scroll-margin-top: 7rem;
    }}
    .pair-card:hover {{
      border-color: var(--border-highlight);
    }}
    .pair-card.is-read {{
      border-color: rgba(46, 204, 113, 0.4);
      box-shadow: inset 0 0 0 1px rgba(46, 204, 113, 0.2);
    }}

    .col {{
      display: flex;
      flex-direction: column;
    }}
    .col-orig {{
      padding-right: 1.2rem;
      border-right: 1px solid var(--border);
    }}
    .col-mod {{
      padding-left: 0.6rem;
    }}

    .col-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      font-family: var(--font-sans);
      flex-wrap: wrap;
      gap: 0.4rem;
    }}
    .col-header-left {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .col-header-right {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .col-tag {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
    }}
    .orig-tag {{
      background: var(--surface-orig);
      color: var(--text-muted);
      border: 1px solid var(--border);
    }}
    .mod-tag {{
      background: var(--crimson-dim);
      color: var(--crimson);
      border: 1px solid var(--crimson-border);
    }}
    .para-tracker-orig {{
      font-size: 0.75rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
      font-weight: 500;
    }}
    .para-pos-tag {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text);
      font-family: var(--font-mono);
      display: inline-flex;
      align-items: center;
      flex-wrap: wrap;
    }}
    .badge-page {{
      color: var(--gold);
      font-weight: 700;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      background: var(--gold-bg);
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
      border: 1px solid rgba(209, 154, 102, 0.3);
      display: inline-block;
      margin-right: 0.35rem;
    }}
    .para-sep {{
      color: var(--text-dim);
      margin: 0 0.25rem;
      font-weight: 400;
    }}
    .tele-page-badge {{
      color: var(--gold);
      font-weight: 700;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      background: var(--gold-bg);
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
      border: 1px solid rgba(209, 154, 102, 0.35);
      margin-right: 0.2rem;
    }}
    .para-pos-pct {{
      color: var(--gold);
      font-size: 0.72rem;
      margin-left: 0.3rem;
    }}
    .para-meta-words {{
      font-size: 0.72rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }}

    /* Mark As Read Button */
    .btn-check {{
      background: var(--surface-orig);
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-family: var(--font-sans);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.2rem 0.55rem;
      border-radius: 5px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      transition: all 0.15s ease;
    }}
    .btn-check:hover {{
      background: var(--surface-hover);
      border-color: var(--border-highlight);
      color: var(--text);
    }}
    .pair-card.is-read .btn-check {{
      background: rgba(46, 204, 113, 0.15);
      border-color: rgba(46, 204, 113, 0.4);
      color: #2ecc71;
    }}

    .para-text {{
      font-size: 1.06rem;
      line-height: 1.8;
      color: var(--text);
      text-align: justify;
      flex-grow: 1;
    }}

    /* Interactive Sentence Highlighting */
    .sent {{
      cursor: pointer;
      border-radius: 3px;
      padding: 0 2px;
      transition: background-color 0.15s ease, color 0.15s ease;
    }}
    .sent:hover {{
      background-color: var(--gold-bg);
    }}
    .sent.active-highlight {{
      background-color: var(--gold-bg);
      color: var(--gold);
      font-weight: 500;
    }}

    /* The Philosophical Move Box */
    .move-box {{
      margin-top: 1.2rem;
      background: var(--blue-bg);
      border-left: 3px solid var(--blue);
      border-radius: 0 6px 6px 0;
      padding: 0.85rem 1.1rem;
      font-family: var(--font-sans);
      font-size: 0.88rem;
      line-height: 1.5;
    }}
    .move-label {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--blue);
      margin-bottom: 0.25rem;
    }}
    .move-content {{
      color: var(--text);
    }}

    /* Modern-First Mode (Single Column) */
    [data-view="modern"] .pair-card {{
      grid-template-columns: 1fr;
      max-width: 800px;
      margin: 0 auto;
    }}
    [data-view="modern"] .col-orig {{
      display: none;
    }}
    [data-view="modern"] .col-mod {{
      padding-left: 0;
    }}

    /* TOC Drawer Modal */
    .toc-drawer {{
      display: none;
      position: fixed;
      top: 0; left: 0; bottom: 0;
      width: 320px;
      background: var(--surface);
      border-right: 1px solid var(--border-highlight);
      z-index: 600;
      padding: 1.5rem;
      overflow-y: auto;
      box-shadow: 10px 0 30px rgba(0,0,0,0.5);
      font-family: var(--font-sans);
    }}
    .toc-drawer.open {{ display: block; }}
    .toc-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.6rem;
    }}
    .toc-title {{ font-size: 1.1rem; font-weight: 700; color: var(--crimson); }}
    .toc-list {{ list-style: none; }}
    .toc-list li {{ margin-bottom: 0.8rem; }}
    .toc-list a {{
      color: var(--text);
      text-decoration: none;
      font-size: 0.88rem;
      transition: color 0.15s ease;
    }}
    .toc-list a:hover {{ color: var(--crimson); }}

    /* Mobile Responsive View */
    @media (max-width: 900px) {{
      .pair-card {{
        grid-template-columns: 1fr;
        gap: 1.2rem;
        padding: 1.2rem;
      }}
      .col-orig {{
        padding-right: 0;
        border-right: none;
        border-bottom: 1px solid var(--border);
        padding-bottom: 1.2rem;
      }}
      .col-mod {{
        padding-left: 0;
      }}
      header.app-bar {{
        padding: 0.45rem 0.8rem;
      }}
      .brand-title {{
        font-size: 0.88rem;
        white-space: nowrap;
      }}
      .brand-pill {{
        display: none;
      }}
      .app-controls {{
        gap: 0.35rem;
      }}
      .btn {{
        padding: 0.25rem 0.5rem;
        font-size: 0.72rem;
      }}
      .telemetry-bar {{
        padding: 0.35rem 0.8rem;
        font-size: 0.72rem;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.35rem;
      }}
      .tele-stats {{
        gap: 0.5rem 0.9rem;
        width: 100%;
        justify-content: space-between;
      }}
      .tele-item {{
        font-size: 0.72rem;
      }}
      .tele-pace-item {{
        display: none;
      }}
    }}

    /* Key Concepts & Accountability Modals */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      z-index: 500;
      background: rgba(0,0,0,0.75);
      backdrop-filter: blur(8px);
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}
    .modal-overlay.open {{ display: flex; }}
    .modal-card {{
      background: var(--surface);
      border: 1px solid var(--border-highlight);
      border-radius: 12px;
      max-width: 640px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 1.8rem;
      font-family: var(--font-sans);
    }}
    .modal-accountability {{
      max-width: 700px;
    }}
    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1.2rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.6rem;
    }}
    .modal-title {{ font-size: 1.2rem; font-weight: 700; color: var(--crimson); }}
    .close-btn {{ background: transparent; border: none; font-size: 1.4rem; color: var(--text-muted); cursor: pointer; }}
    .concept-item {{ margin-bottom: 1.2rem; }}
    .concept-name {{ font-weight: 700; font-size: 0.95rem; color: var(--gold); }}
    .concept-desc {{ font-size: 0.88rem; color: var(--text); margin-top: 0.2rem; line-height: 1.5; }}

    /* Accountability KPI Grid */
    .acc-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 0.75rem;
      margin-bottom: 1.2rem;
    }}
    .acc-card {{
      background: var(--surface-orig);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.85rem;
      text-align: center;
    }}
    .acc-val {{
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--crimson);
      font-family: var(--font-mono);
    }}
    .acc-label {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-top: 0.25rem;
    }}
    .acc-sub {{
      font-size: 0.68rem;
      color: var(--text-dim);
      margin-top: 0.15rem;
    }}

    /* Pacing Box */
    .pacing-box {{
      background: var(--gold-bg);
      border: 1px solid rgba(209, 154, 102, 0.4);
      border-radius: 8px;
      padding: 0.85rem 1.1rem;
      margin-bottom: 1.3rem;
    }}
    .pacing-title {{
      font-weight: 700;
      font-size: 0.88rem;
      color: var(--gold);
      margin-bottom: 0.25rem;
    }}
    .pacing-desc {{
      font-size: 0.82rem;
      line-height: 1.5;
      color: var(--text);
    }}

    /* Chapter Progress Rows */
    .acc-section-title {{
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      margin-bottom: 0.5rem;
    }}
    .chapter-progress-list {{
      max-height: 220px;
      overflow-y: auto;
      margin-bottom: 1.2rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface-orig);
    }}
    .chapter-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.45rem 0.8rem;
      border-bottom: 1px solid var(--border);
      font-size: 0.8rem;
    }}
    .chapter-row:last-child {{
      border-bottom: none;
    }}
    .ch-name {{
      flex-grow: 1;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 280px;
    }}
    .ch-ratio {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-left: 0.6rem;
      white-space: nowrap;
    }}
    .ch-bar {{
      width: 70px;
      height: 6px;
      background: var(--border);
      border-radius: 3px;
      overflow: hidden;
      margin-left: 0.6rem;
      flex-shrink: 0;
    }}
    .ch-bar-fill {{
      height: 100%;
      background: #2ecc71;
      transition: width 0.3s ease;
    }}

    /* Modal Footer Actions */
    .modal-footer-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.8rem;
      margin-top: 1.2rem;
      border-top: 1px solid var(--border);
      padding-top: 0.8rem;
    }}
    .btn-danger {{
      background: rgba(224, 83, 71, 0.1);
      border: 1px solid var(--crimson-border);
      color: var(--crimson);
    }}
    .btn-danger:hover {{
      background: var(--crimson);
      color: #fff;
    }}
    .btn-primary {{
      background: var(--crimson);
      color: #fff;
      border-color: var(--crimson);
    }}
    .btn-secondary {{
      background: var(--surface-hover);
      border: 1px solid var(--border-highlight);
      color: var(--text);
    }}
    .btn-secondary:hover {{
      border-color: var(--gold);
      color: var(--gold);
    }}

    /* Cloudflare Sync Modal & Toast */
    .modal-sync {{
      max-width: 620px;
    }}
    .sync-box {{
      background: var(--surface-orig);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.9rem 1.1rem;
      margin-bottom: 1.1rem;
    }}
    .sync-box-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }}
    .sync-box-label {{
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      text-transform: uppercase;
      font-family: var(--font-mono);
    }}
    .sync-kv-badge {{
      font-size: 0.68rem;
      color: #2ecc71;
      font-weight: 600;
      background: rgba(46, 204, 113, 0.1);
      border: 1px solid rgba(46, 204, 113, 0.3);
      padding: 0.15rem 0.5rem;
      border-radius: 12px;
    }}
    .sync-key-row {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      flex-wrap: wrap;
    }}
    .sync-key-display {{
      font-family: var(--font-mono);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--gold);
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 0.35rem 0.8rem;
      border-radius: 6px;
      letter-spacing: 0.05em;
      user-select: all;
    }}
    .sync-qr-card {{
      display: flex;
      align-items: center;
      gap: 1.4rem;
      background: var(--surface-orig);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.1rem;
      margin-bottom: 1.1rem;
    }}
    #qrcode-wrap {{
      flex-shrink: 0;
      background: #fff;
      padding: 8px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    #qrcode img, #qrcode canvas {{
      display: block;
    }}
    .sync-qr-info h4 {{
      font-size: 0.95rem;
      color: var(--text);
      margin-bottom: 0.3rem;
    }}
    .sync-qr-info p {{
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 0.6rem;
    }}
    .sync-direct-url {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--crimson);
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 0.25rem 0.6rem;
      border-radius: 4px;
      word-break: break-all;
    }}
    .sync-pair-box {{
      background: var(--surface-orig);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.9rem 1.1rem;
      margin-bottom: 1.1rem;
    }}
    .sync-pair-title {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 0.5rem;
    }}
    .sync-input-row {{
      display: flex;
      gap: 0.6rem;
    }}
    .sync-input-row input {{
      flex-grow: 1;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 0.85rem;
      padding: 0.45rem 0.8rem;
      border-radius: 6px;
      outline: none;
    }}
    .sync-input-row input:focus {{
      border-color: var(--crimson);
    }}
    .app-toast {{
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border-highlight);
      border-left: 4px solid var(--crimson);
      box-shadow: 0 8px 24px rgba(0,0,0,0.35);
      padding: 0.75rem 1.2rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 500;
      z-index: 1000;
      opacity: 0;
      transform: translateY(12px);
      transition: opacity 0.25s ease, transform 0.25s ease;
      pointer-events: none;
      max-width: 380px;
    }}
    .app-toast.visible {{
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }}
    @media (max-width: 600px) {{
      .sync-qr-card {{
        flex-direction: column;
        text-align: center;
      }}
      .sync-key-row {{
        flex-direction: column;
        align-items: stretch;
      }}
      .sync-input-row {{
        flex-direction: column;
      }}
      .app-toast {{
        bottom: 1rem;
        right: 1rem;
        left: 1rem;
        max-width: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- TOC Drawer -->
  <div class="toc-drawer" id="toc-drawer">
    <div class="toc-header">
      <div class="toc-title">Table of Contents</div>
      <button class="close-btn" onclick="toggleTOC(false)">&times;</button>
    </div>
    <ul class="toc-list">
      {toc_html}
    </ul>
  </div>

  <!-- App Bar -->
  <header class="app-bar">
    <div class="app-brand">
      <button class="btn" onclick="toggleTOC(true)" title="Table of Contents">☰ Chapters</button>
      <span class="brand-title">The Myth of Sisyphus</span>
      <span class="brand-pill">Complete Edition</span>
    </div>

    <div class="app-controls">
      <button class="btn active" id="view-parallel-btn" onclick="setView('parallel')">Parallel</button>
      <button class="btn" id="view-modern-btn" onclick="setView('modern')">Modern Stream</button>

      <button class="btn" onclick="cycleTheme()" id="theme-btn" title="Toggle Theme">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button class="btn" onclick="toggleSyncModal(true)" id="sync-modal-btn" title="Cloudflare Cross-Device Sync">☁️ Sync</button>
      <button class="btn" onclick="toggleAccountabilityModal(true)" title="Reading Velocity & Accountability">📊 Stats</button>
      <button class="btn" onclick="toggleModal(true)">Concepts</button>
    </div>
  </header>

  <!-- Reading Progress Track Bar -->
  <div class="reading-progress-track">
    <div class="reading-progress-fill" id="reading-progress-bar"></div>
  </div>

  <!-- Reading Telemetry & Accountability Bar -->
  <div class="telemetry-bar">
    <div class="tele-stats">
      <span class="tele-item" id="tele-loc-item">
        📍 <span class="tele-page-badge" id="tele-page-badge">Page 1</span> <span class="tele-sub" id="tele-book-p">(p. 1 of 138)</span> • <span id="tele-loc"><strong>§1 of 2</strong></span> <span class="tele-loc-ch" id="tele-ch-title" style="color: var(--crimson); font-weight:600;">Introduction</span> <span class="tele-sub" id="tele-loc-pct">(50%)</span>
      </span>
      <span class="tele-divider">|</span>
      <span class="tele-item">
        📚 Read: <strong id="tele-consumed-count">0</strong> / {total_book_blocks} <span class="tele-sub" id="tele-consumed-pct">(0%)</span>
      </span>
      <span class="tele-divider">|</span>
      <span class="tele-item">
        ⏱ <strong id="timer-val">00:00</strong>
        <button class="tele-timer-btn" id="timer-toggle-btn" onclick="toggleTimer()" title="Pause / Resume">⏸</button>
      </span>
      <span class="tele-divider">|</span>
      <span class="tele-item">
        ⚡ <strong id="tele-speed">240</strong> wpm
      </span>
      <span class="tele-divider">|</span>
      <span class="tele-item tele-pace-item">
        <span class="pace-chip on-track" id="pace-chip">🎯 16m/ch</span>
      </span>
    </div>
    <div class="tele-right">
      <button class="tele-sync-btn" id="tele-sync-item" onclick="toggleSyncModal(true)" title="Cloudflare Cross-Device Sync">
        ☁️ <span id="tele-sync-dot">🟢</span> <span id="tele-sync-text">Synced</span>
      </button>
    </div>
  </div>

  <!-- Main Content Area -->
  <main class="reader-container">
    {sections_html}
  </main>

  <!-- Key Concepts Modal -->
  <div class="modal-overlay" id="concepts-modal" onclick="if(event.target===this) toggleModal(false)">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">Camus's Core Philosophical Moves</h3>
        <button class="close-btn" onclick="toggleModal(false)">&times;</button>
      </div>
      <div class="concept-item">
        <div class="concept-name">1. The Absurd (L'Absurde)</div>
        <div class="concept-desc">Not "wackiness" or "goofiness." It is strictly relational: the violent collision between humanity's desperate hunger for meaning and the universe's total, stubborn silence. The Absurd exists in the collision itself.</div>
      </div>
      <div class="concept-item">
        <div class="concept-name">2. Eluding / Evasion (L'Esquive)</div>
        <div class="concept-desc">Coping with the void through false grand narratives: religion, utopian political ideologies, or living strictly for "tomorrow." Camus calls hope the greatest evasion because it steals our only real possession: the present moment.</div>
      </div>
      <div class="concept-item">
        <div class="concept-name">3. Philosophical Suicide</div>
        <div class="concept-desc">Forcing an artificial leap of faith (intellectual surrender) to make reality feel safe and explained again. Camus refuses this—he demands we keep our critical intellect 100% awake without numbing ourselves.</div>
      </div>
      <div class="concept-item">
        <div class="concept-name">4. Lucidity (La Lucidité)</div>
        <div class="concept-desc">Staring directly into reality without illusions, without cosmic guarantees, and without flinching. Radical mental honesty.</div>
      </div>
      <div class="concept-item">
        <div class="concept-name">5. Revolt (La Révolte)</div>
        <div class="concept-desc">Camus's ultimate conclusion: Knowing life has no cosmic meaning does not justify dying—it demands living with maximum defiance, creativity, and mortal intensity.</div>
      </div>
    </div>
  </div>

  <!-- Accountability & Reading Pacing Modal -->
  <div class="modal-overlay" id="accountability-modal" onclick="if(event.target===this) toggleAccountabilityModal(false)">
    <div class="modal-card modal-accountability">
      <div class="modal-header">
        <div>
          <h3 class="modal-title">📊 Reading Velocity & Accountability</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">Track consumption speed, chapter pacing, and active completion.</p>
        </div>
        <button class="close-btn" onclick="toggleAccountabilityModal(false)">&times;</button>
      </div>
      <div class="acc-grid">
        <div class="acc-card">
          <div class="acc-val" id="stat-consumed-paras">0 / {total_book_blocks}</div>
          <div class="acc-label">Paragraphs Read</div>
          <div class="acc-sub" id="stat-consumed-pct">0% of entire book</div>
        </div>
        <div class="acc-card">
          <div class="acc-val" id="stat-words-read">0</div>
          <div class="acc-label">Words Consumed</div>
          <div class="acc-sub">out of {total_book_words:,} total</div>
        </div>
        <div class="acc-card">
          <div class="acc-val" id="stat-session-time">00:00</div>
          <div class="acc-label">Active Time</div>
          <div class="acc-sub">current reading session</div>
        </div>
        <div class="acc-card">
          <div class="acc-val" id="stat-avg-wpm">240</div>
          <div class="acc-label">Reading Speed</div>
          <div class="acc-sub">words per minute (WPM)</div>
        </div>
      </div>

      <div class="pacing-box">
        <div class="pacing-title">🎯 College Pacing Benchmark: 15–20 Min / Chapter</div>
        <div class="pacing-desc" id="pacing-feedback">
          At your current reading pace, each chapter takes approximately <strong>~16 minutes</strong>. You are maintaining comfortable comprehension speed without getting bogged down in 60-minute slogs!
        </div>
      </div>

      <div class="acc-section-title">Chapter Completion Breakdown</div>
      <div class="chapter-progress-list" id="chapter-progress-rows"></div>

      <div class="modal-footer-actions">
        <button class="btn btn-secondary" id="btn-mark-upto" onclick="markAllUpToCurrent()">✓ Mark Read Up To Current Page</button>
        <div style="display:flex; gap:0.5rem;">
          <button class="btn btn-danger" onclick="resetAllReadingProgress()">Reset</button>
          <button class="btn btn-primary" onclick="toggleAccountabilityModal(false)">Back to Reading</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Cloudflare Cross-Device Sync Modal -->
  <div class="modal-overlay" id="sync-modal" onclick="if(event.target===this) toggleSyncModal(false)">
    <div class="modal-card modal-sync">
      <div class="modal-header">
        <div>
          <h3 class="modal-title">☁️ Cloudflare Cross-Device Sync</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
            Read seamlessly across your Mac, iPhone, iPad, and e-reader. Zero login, zero passwords.
          </p>
        </div>
        <button class="close-btn" onclick="toggleSyncModal(false)">&times;</button>
      </div>

      <!-- Sync Key Display -->
      <div class="sync-box">
        <div class="sync-box-header">
          <span class="sync-box-label">YOUR DEVICE PAIRING KEY</span>
          <span class="sync-kv-badge">Cloudflare KV Active</span>
        </div>
        <div class="sync-key-row">
          <div class="sync-key-display" id="sync-token-display">sisy-••••••</div>
          <button class="btn btn-sm" onclick="copySyncLink()" id="btn-copy-sync">📋 Copy Link</button>
          <button class="btn btn-sm" onclick="generateNewSyncToken()" title="Generate a fresh sync token">🔄 New Key</button>
        </div>
      </div>

      <!-- QR Code Hand-Off -->
      <div class="sync-qr-card">
        <div id="qrcode-wrap">
          <div id="qrcode"></div>
        </div>
        <div class="sync-qr-info">
          <h4>📱 Scan with your iPhone Camera</h4>
          <p>
            Point your iPhone or iPad camera at this QR code. It instantly opens the reader, pairs the devices, and restores your marked paragraphs, speed, and chapter location.
          </p>
          <div class="sync-direct-url">
            <span id="sync-url-preview">https://sisyphus-reader.pages.dev/?sync=...</span>
          </div>
        </div>
      </div>

      <!-- Pair another device -->
      <div class="sync-pair-box">
        <div class="sync-pair-title">Have a key from another device?</div>
        <div class="sync-input-row">
          <input type="text" id="sync-input-token" placeholder="Paste device key (e.g. sisy-9x2m4k)..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
          <button class="btn btn-primary" onclick="pairRemoteDeviceToken()">Link & Merge</button>
        </div>
      </div>

      <div class="modal-footer-actions">
        <div style="font-size: 0.72rem; color: var(--text-dim);" id="sync-status-footer">
          Last Synced: Just now • Global Edge
        </div>
        <button class="btn btn-primary" onclick="toggleSyncModal(false)">Done</button>
      </div>
    </div>
  </div>

  <script>
    // Theme Management
    const themes = ['dark', 'light', 'sepia'];
    let currentThemeIdx = 0;
    function cycleTheme() {{
      currentThemeIdx = (currentThemeIdx + 1) % themes.length;
      document.documentElement.setAttribute('data-theme', themes[currentThemeIdx]);
      localStorage.setItem('camus-theme', themes[currentThemeIdx]);
    }}
    const savedTheme = localStorage.getItem('camus-theme');
    if (savedTheme) {{
      document.documentElement.setAttribute('data-theme', savedTheme);
      currentThemeIdx = themes.indexOf(savedTheme);
    }}

    // View Management
    function setView(view) {{
      document.documentElement.setAttribute('data-view', view);
      document.getElementById('view-parallel-btn').classList.toggle('active', view === 'parallel');
      document.getElementById('view-modern-btn').classList.toggle('active', view === 'modern');
      setTimeout(updateActiveLocationOnScroll, 40);
    }}

    // Interactive Sentence Lighting
    function handleSentClick(sid) {{
      document.querySelectorAll('.sent').forEach(el => el.classList.remove('active-highlight'));
      const matches = document.querySelectorAll(`[data-s="${{sid}}"]`);
      matches.forEach(el => {{
        el.classList.add('active-highlight');
      }});
      if (matches.length > 1) {{
        const target = matches[1];
        const rect = target.getBoundingClientRect();
        if (rect.top < 80 || rect.bottom > window.innerHeight) {{
          target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }}
      }}
    }}

    document.querySelectorAll('.sent').forEach(el => {{
      el.addEventListener('mouseenter', () => {{
        const sid = el.getAttribute('data-s');
        document.querySelectorAll(`[data-s="${{sid}}"]`).forEach(m => m.classList.add('active-highlight'));
      }});
      el.addEventListener('mouseleave', () => {{
        const sid = el.getAttribute('data-s');
        document.querySelectorAll(`[data-s="${{sid}}"]`).forEach(m => m.classList.remove('active-highlight'));
      }});
    }});

    // Modals & Drawers
    function toggleModal(open) {{
      document.getElementById('concepts-modal').classList.toggle('open', open);
    }}
    function toggleTOC(open) {{
      document.getElementById('toc-drawer').classList.toggle('open', open);
    }}
    function toggleAccountabilityModal(open) {{
      if (open) {{
        renderChapterBreakdown();
        const btnMarkUpto = document.getElementById('btn-mark-upto');
        if (btnMarkUpto) {{
          if (lastActiveCard) {{
            const pageNum = lastActiveCard.getAttribute('data-page') || '1';
            const pIdx = lastActiveCard.getAttribute('data-p-idx') || '1';
            btnMarkUpto.textContent = `✓ Mark Read Up To Page ${{pageNum}} (§${{pIdx}})`;
          }} else {{
            btnMarkUpto.textContent = `✓ Mark Read Up To Current Page`;
          }}
        }}
      }}
      document.getElementById('accountability-modal').classList.toggle('open', open);
    }}

    // Active Session Stopwatch & Pacing
    let sessionSeconds = 0;
    let timerRunning = true;
    const timerValEl = document.getElementById('timer-val');
    const timerToggleBtn = document.getElementById('timer-toggle-btn');
    
    function toggleTimer() {{
      timerRunning = !timerRunning;
      if (timerToggleBtn) timerToggleBtn.textContent = timerRunning ? '⏸' : '▶';
    }}

    setInterval(() => {{
      if (timerRunning && !document.hidden) {{
        sessionSeconds++;
        const mins = Math.floor(sessionSeconds / 60);
        const secs = sessionSeconds % 60;
        const timeStr = String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
        if (timerValEl) timerValEl.textContent = timeStr;
        const statTimeEl = document.getElementById('stat-session-time');
        if (statTimeEl) statTimeEl.textContent = timeStr;
        updatePacingCalculations();
      }}
    }}, 1000);

    // Reading Accountability & Progress Store
    const TOTAL_BOOK_BLOCKS = {total_book_blocks};
    const TOTAL_BOOK_WORDS = {total_book_words};
    let readCards = {{}};
    try {{
      readCards = JSON.parse(localStorage.getItem('sisyphus-consumed-cards') || '{{}}');
    }} catch(e) {{ readCards = {{}}; }}

    let unmarkedCards = {{}};
    try {{
      unmarkedCards = JSON.parse(localStorage.getItem('sisyphus-unmarked-cards') || '{{}}');
    }} catch(e) {{ unmarkedCards = {{}}; }}

    let allCardsCached = null;
    function getAllCards() {{
      if (!allCardsCached || allCardsCached.length === 0) {{
        allCardsCached = Array.from(document.querySelectorAll('.pair-card'));
      }}
      return allCardsCached;
    }}

    function syncReadCardsUI() {{
      const cardIds = Object.keys(readCards);
      let totalWordsRead = 0;
      cardIds.forEach(cid => {{
        const card = document.getElementById(cid);
        if (card) {{
          card.classList.add('is-read');
          const btn = document.getElementById(`chk-${{cid}}`);
          if (btn) {{
            btn.innerHTML = '<span class="check-icon">✓</span> <span class="check-txt">Read</span>';
          }}
          totalWordsRead += (readCards[cid].words || parseInt(card.getAttribute('data-words') || '150'));
        }}
      }});

      const count = cardIds.length;
      const pct = Math.round((count / TOTAL_BOOK_BLOCKS) * 100);

      const countEl = document.getElementById('tele-consumed-count');
      const pctEl = document.getElementById('tele-consumed-pct');
      if (countEl) countEl.textContent = count;
      if (pctEl) pctEl.textContent = `(${{pct}}%)`;

      const statParasEl = document.getElementById('stat-consumed-paras');
      const statPctEl = document.getElementById('stat-consumed-pct');
      const statWordsEl = document.getElementById('stat-words-read');
      if (statParasEl) statParasEl.textContent = `${{count}} / ${{TOTAL_BOOK_BLOCKS}}`;
      if (statPctEl) statPctEl.textContent = `${{pct}}% of entire book`;
      if (statWordsEl) statWordsEl.textContent = totalWordsRead.toLocaleString();

      updatePacingCalculations(totalWordsRead);
    }}

    function toggleMarkRead(pid, words, event) {{
      if (event) event.stopPropagation();
      const card = document.getElementById(pid);
      if (!card) return;

      if (readCards[pid]) {{
        delete readCards[pid];
        unmarkedCards[pid] = true;
        card.classList.remove('is-read');
        const btn = document.getElementById(`chk-${{pid}}`);
        if (btn) btn.innerHTML = '<span class="check-icon">○</span> <span class="check-txt">Mark Read</span>';
      }} else {{
        readCards[pid] = {{ words: words, time: Date.now() }};
        delete unmarkedCards[pid];
        card.classList.add('is-read');
        const btn = document.getElementById(`chk-${{pid}}`);
        if (btn) btn.innerHTML = '<span class="check-icon">✓</span> <span class="check-txt">Read</span>';
      }}

      localStorage.setItem('sisyphus-consumed-cards', JSON.stringify(readCards));
      localStorage.setItem('sisyphus-unmarked-cards', JSON.stringify(unmarkedCards));
      syncReadCardsUI();
      renderChapterBreakdown();
      scheduleCloudPush();
    }}

    function markAllUpToCurrent() {{
      const allCards = getAllCards();
      if (!allCards.length) return;

      let targetIdx = 0;
      if (lastActiveCard) {{
        targetIdx = parseInt(lastActiveCard.getAttribute('data-global-idx') || '1');
      }} else {{
        targetIdx = 1;
      }}

      for (let i = 0; i < targetIdx && i < allCards.length; i++) {{
        const c = allCards[i];
        if (c) {{
          const cid = c.id;
          const words = parseInt(c.getAttribute('data-words') || '150');
          readCards[cid] = {{ words: words, time: Date.now() }};
          delete unmarkedCards[cid];
        }}
      }}

      localStorage.setItem('sisyphus-consumed-cards', JSON.stringify(readCards));
      localStorage.setItem('sisyphus-unmarked-cards', JSON.stringify(unmarkedCards));
      syncReadCardsUI();
      renderChapterBreakdown();
      scheduleCloudPush(true);

      const pageNum = lastActiveCard ? lastActiveCard.getAttribute('data-page') : '1';
      showToast(`✓ Marked all ${{targetIdx}} paragraphs up to Page ${{pageNum}} as read!`);
    }}

    function resetAllReadingProgress() {{
      if (confirm('Are you sure you want to reset all paragraph reading progress? This will reset all read markers and return to the beginning.')) {{
        readCards = {{}};
        unmarkedCards = {{}};
        localStorage.removeItem('sisyphus-consumed-cards');
        localStorage.removeItem('sisyphus-unmarked-cards');
        document.querySelectorAll('.pair-card').forEach(c => {{
          c.classList.remove('is-read');
          const cid = c.id;
          const btn = document.getElementById(`chk-${{cid}}`);
          if (btn) btn.innerHTML = '<span class="check-icon">○</span> <span class="check-txt">Mark Read</span>';
        }});
        syncReadCardsUI();
        renderChapterBreakdown();
        scheduleCloudPush(true, true);
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
        showToast('🔄 Reading progress reset to beginning');
      }}
    }}

    function updatePacingCalculations(customWords) {{
      let words = customWords;
      if (words === undefined) {{
        words = Object.keys(readCards).reduce((acc, k) => acc + (readCards[k].words || 150), 0);
      }}
      const activeMins = sessionSeconds / 60;
      let wpm = 240;
      if (activeMins > 0.5 && words > 50) {{
        wpm = Math.round(words / activeMins);
      }}
      const wpmEl = document.getElementById('tele-speed');
      const statWpmEl = document.getElementById('stat-avg-wpm');
      if (wpmEl) wpmEl.textContent = `${{wpm}}`;
      if (statWpmEl) statWpmEl.textContent = `${{wpm}}`;

      const paceChip = document.getElementById('pace-chip');
      const pacingFeedback = document.getElementById('pacing-feedback');
      if (paceChip) {{
        const estMinCh = Math.round(3800 / Math.max(100, wpm));
        if (wpm >= 200 && wpm <= 350) {{
          paceChip.className = 'pace-chip on-track';
          paceChip.textContent = `🎯 On Track (~${{estMinCh}}m/ch)`;
        }} else if (wpm > 350) {{
          paceChip.className = 'pace-chip fast';
          paceChip.textContent = `⚡ Fast (~${{estMinCh}}m/ch)`;
        }} else {{
          paceChip.className = 'pace-chip';
          paceChip.textContent = `📖 Deep Focus (~${{estMinCh}}m/ch)`;
        }}

        if (pacingFeedback) {{
          pacingFeedback.innerHTML = `At your current reading pace of <strong>${{wpm}} WPM</strong>, reading a standard chapter takes approximately <strong>~${{estMinCh}} minutes</strong>. Target pace is 15–20 min / chapter.`;
        }}
      }}
    }}

    // Real-Time Scroll Spy & Dynamic Location HUD Engine
    const TOTAL_BOOK_PAGES = 138;
    const progressBar = document.getElementById('reading-progress-bar');
    let lastActiveCard = null;
    let scrollRafId = null;

    function applyCardLocationToHUD(card) {{
      if (!card) return;
      const pIdx = card.getAttribute('data-p-idx') || '1';
      const pTotal = card.getAttribute('data-p-total') || '1';
      const pageNum = card.getAttribute('data-page') || '1';
      const secId = card.getAttribute('data-sec-id');
      const secEl = document.getElementById(secId);
      const secTitle = secEl ? (secEl.getAttribute('data-sec-title') || '') : '';
      const pctCh = Math.round((parseInt(pIdx) / parseInt(pTotal)) * 100);

      currentActivePid = card.id;

      const pageBadge = document.getElementById('tele-page-badge');
      const bookPEl = document.getElementById('tele-book-p');
      const locEl = document.getElementById('tele-loc');
      const chEl = document.getElementById('tele-ch-title');
      const pctEl = document.getElementById('tele-loc-pct');

      if (pageBadge) pageBadge.textContent = `Page ${{pageNum}}`;
      if (bookPEl) bookPEl.textContent = `(p. ${{pageNum}} of ${{TOTAL_BOOK_PAGES}})`;
      if (locEl) locEl.innerHTML = `<strong>§${{pIdx}} of ${{pTotal}}</strong>`;
      if (chEl) chEl.textContent = secTitle.replace(/^[0-9.]+\\s*/, '');
      if (pctEl) pctEl.textContent = `(${{pctCh}}%)`;
    }}

    function updateActiveLocationOnScroll() {{
      const scrollY = window.scrollY;
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      if (maxScroll > 0 && progressBar) {{
        const pct = Math.min(100, Math.max(0, (scrollY / maxScroll) * 100));
        progressBar.style.width = pct + '%';
      }}

      // Step 1: Find Active Book Section (based on reading focal line)
      const sections = document.querySelectorAll('.book-section');
      if (!sections.length) return;

      const focalLine = Math.max(160, window.innerHeight * 0.45);
      const topBarThreshold = 95;

      let activeSection = null;
      for (let i = 0; i < sections.length; i++) {{
        const sec = sections[i];
        const sRect = sec.getBoundingClientRect();
        // Section has reached focal line and hasn't completely scrolled away
        if (sRect.top <= focalLine && sRect.bottom > topBarThreshold) {{
          activeSection = sec;
        }}
      }}

      if (!activeSection) {{
        if (sections[0].getBoundingClientRect().top > focalLine) {{
          activeSection = sections[0];
        }} else {{
          activeSection = sections[sections.length - 1];
        }}
      }}

      // Step 2: Inside active section, find active card
      const cards = activeSection.querySelectorAll('.pair-card');
      let currentCard = null;

      if (cards.length > 0) {{
        currentCard = cards[0];
        for (let j = 0; j < cards.length; j++) {{
          const cRect = cards[j].getBoundingClientRect();
          if (cRect.top <= focalLine) {{
            currentCard = cards[j];
          }} else {{
            break;
          }}
        }}
      }}

      if (currentCard && currentCard !== lastActiveCard) {{
        lastActiveCard = currentCard;
        applyCardLocationToHUD(currentCard);
      }}

      // Auto-track reading consumption as the reader progresses through paragraphs
      if (scrollY > 80 && currentCard) {{
        const currentGlobalIdx = parseInt(currentCard.getAttribute('data-global-idx') || '1');
        const allCards = getAllCards();
        let hasNewRead = false;
        for (let i = 0; i < currentGlobalIdx && i < allCards.length; i++) {{
          const c = allCards[i];
          if (c && !readCards[c.id] && !unmarkedCards[c.id]) {{
            const words = parseInt(c.getAttribute('data-words') || '150');
            readCards[c.id] = {{ words: words, time: Date.now(), auto: true }};
            hasNewRead = true;
          }}
        }}
        if (hasNewRead) {{
          localStorage.setItem('sisyphus-consumed-cards', JSON.stringify(readCards));
          syncReadCardsUI();
          renderChapterBreakdown();
          scheduleCloudPush();
        }}
      }}
    }}

    window.addEventListener('scroll', () => {{
      if (!scrollRafId) {{
        scrollRafId = requestAnimationFrame(() => {{
          updateActiveLocationOnScroll();
          scrollRafId = null;
        }});
      }}
    }}, {{ passive: true }});

    window.addEventListener('resize', updateActiveLocationOnScroll, {{ passive: true }});

    // Chapter Breakdown in Accountability Modal
    function renderChapterBreakdown() {{
      const listEl = document.getElementById('chapter-progress-rows');
      if (!listEl) return;
      const sections = document.querySelectorAll('.book-section');
      let html = '';
      sections.forEach(sec => {{
        const secId = sec.id;
        const title = sec.getAttribute('data-sec-title') || secId;
        const secPages = sec.getAttribute('data-sec-pages') || '';
        const cards = sec.querySelectorAll('.pair-card');
        const total = cards.length;
        let readCount = 0;
        cards.forEach(c => {{
          if (readCards[c.id]) readCount++;
        }});
        const pct = total > 0 ? Math.round((readCount / total) * 100) : 0;
        html += `
          <div class="chapter-row">
            <span class="ch-name" title="${{title}}">${{title}} <span style="font-family:var(--font-mono); font-size:0.7rem; color:var(--gold); margin-left:0.3rem;">(${{secPages}})</span></span>
            <span class="ch-ratio">${{readCount}} / ${{total}} (${{pct}}%)</span>
            <div class="ch-bar">
              <div class="ch-bar-fill" style="width: ${{pct}}%;"></div>
            </div>
          </div>
        `;
      }});
      listEl.innerHTML = html;
    }}

    // ==========================================
    // Cloudflare Zero-Login Cross-Device Sync
    // ==========================================
    let syncToken = '';
    let isSyncing = false;
    let pushTimeout = null;
    let currentActivePid = '';

    function getOrCreateSyncToken() {{
      const urlParams = new URLSearchParams(window.location.search);
      let t = urlParams.get('sync');
      if (!t && window.location.hash.startsWith('#sync=')) {{
        t = window.location.hash.replace('#sync=', '');
      }}
      if (t) {{
        t = t.trim().toLowerCase();
        localStorage.setItem('sisyphus-sync-token', t);
        const cleanUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({{}}, document.title, cleanUrl);
        return t;
      }}

      let stored = localStorage.getItem('sisyphus-sync-token');
      if (!stored) {{
        const rand = Math.random().toString(36).substring(2, 8);
        stored = `sisy-${{rand}}`;
        localStorage.setItem('sisyphus-sync-token', stored);
      }}
      return stored;
    }}

    function setSyncStatus(state, label) {{
      const dotEl = document.getElementById('tele-sync-dot');
      const textEl = document.getElementById('tele-sync-text');
      const footerEl = document.getElementById('sync-status-footer');
      if (dotEl) {{
        if (state === 'syncing') dotEl.textContent = '🟡';
        else if (state === 'synced') dotEl.textContent = '🟢';
        else if (state === 'offline') dotEl.textContent = '⚪';
        else dotEl.textContent = '🔴';
      }}
      if (textEl) textEl.textContent = label;
      if (footerEl) {{
        if (state === 'syncing') footerEl.textContent = 'Syncing to Cloudflare KV Edge...';
        else if (state === 'synced') footerEl.textContent = `Last Synced: ${{new Date().toLocaleTimeString()}} • Global Edge`;
        else if (state === 'offline') footerEl.textContent = 'Offline (changes stored locally)';
      }}
    }}

    function showToast(msg, duration = 3200) {{
      let toast = document.getElementById('app-toast');
      if (!toast) {{
        toast = document.createElement('div');
        toast.id = 'app-toast';
        toast.className = 'app-toast';
        document.body.appendChild(toast);
      }}
      toast.textContent = msg;
      toast.classList.add('visible');
      clearTimeout(toast._timer);
      toast._timer = setTimeout(() => {{
        toast.classList.remove('visible');
      }}, duration);
    }}

    function toggleSyncModal(open) {{
      const m = document.getElementById('sync-modal');
      if (!m) return;
      if (open) {{
        m.classList.add('open');
        renderSyncModalContent();
      }} else {{
        m.classList.remove('open');
      }}
    }}

    let qrCodeObj = null;
    function renderSyncModalContent() {{
      const tokenDisplay = document.getElementById('sync-token-display');
      if (tokenDisplay) tokenDisplay.textContent = syncToken;

      const directUrl = `${{window.location.origin}}${{window.location.pathname}}?sync=${{syncToken}}`;
      const urlPreview = document.getElementById('sync-url-preview');
      if (urlPreview) urlPreview.textContent = directUrl;

      const qrTarget = document.getElementById('qrcode');
      if (qrTarget) {{
        qrTarget.innerHTML = '';
        if (typeof QRCode !== 'undefined') {{
          qrCodeObj = new QRCode(qrTarget, {{
            text: directUrl,
            width: 130,
            height: 130,
            colorDark: "#1a1a1a",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.M
          }});
        }} else {{
          qrTarget.innerHTML = '<div style="font-size:0.75rem; color:#888; padding:10px;">QR ready online</div>';
        }}
      }}
    }}

    function copySyncLink() {{
      const directUrl = `${{window.location.origin}}${{window.location.pathname}}?sync=${{syncToken}}`;
      navigator.clipboard.writeText(directUrl).then(() => {{
        const btn = document.getElementById('btn-copy-sync');
        if (btn) {{
          btn.textContent = '✓ Copied!';
          setTimeout(() => btn.textContent = '📋 Copy Link', 2000);
        }}
        showToast('📋 Cloudflare sync link copied to clipboard!');
      }}).catch(() => {{
        prompt('Copy your sync link:', directUrl);
      }});
    }}

    function generateNewSyncToken() {{
      if (confirm('Generate a fresh sync key? This device will start a new sync room.')) {{
        const rand = Math.random().toString(36).substring(2, 8);
        syncToken = `sisy-${{rand}}`;
        localStorage.setItem('sisyphus-sync-token', syncToken);
        renderSyncModalContent();
        scheduleCloudPush(true);
        showToast(`✨ Generated new sync key: ${{syncToken}}`);
      }}
    }}

    async function pairRemoteDeviceToken() {{
      const input = document.getElementById('sync-input-token');
      if (!input) return;
      let raw = (input.value || '').trim().toLowerCase();
      if (!raw) return;
      if (raw.includes('sync=')) {{
        const match = raw.match(/sync=([a-z0-9-]+)/);
        if (match) raw = match[1];
      }}
      if (raw.length < 4) {{
        alert('Invalid device key');
        return;
      }}

      syncToken = raw;
      localStorage.setItem('sisyphus-sync-token', syncToken);
      input.value = '';
      renderSyncModalContent();
      showToast(`🔗 Linking device key: ${{syncToken}}...`);
      await pullCloudSync(true);
      toggleSyncModal(false);
    }}

    async function pullCloudSync(isInitial = false) {{
      if (!syncToken) return;
      setSyncStatus('syncing', 'Syncing...');
      try {{
        const res = await fetch(`/api/sync?token=${{encodeURIComponent(syncToken)}}`, {{
          cache: 'no-store'
        }});
        if (!res.ok) throw new Error('Sync fetch failed');
        const json = await res.json();
        if (json.ok && json.data) {{
          const remoteData = json.data;
          let newCardsCount = 0;
          if (remoteData.unmarkedCards && typeof remoteData.unmarkedCards === 'object') {{
            for (const cid of Object.keys(remoteData.unmarkedCards)) {{
              unmarkedCards[cid] = true;
              if (readCards[cid]) {{
                delete readCards[cid];
                const card = document.getElementById(cid);
                if (card) {{
                  card.classList.remove('is-read');
                  const btn = document.getElementById(`chk-${{cid}}`);
                  if (btn) btn.innerHTML = '<span class="check-icon">○</span> <span class="check-txt">Mark Read</span>';
                }}
              }}
            }}
            localStorage.setItem('sisyphus-unmarked-cards', JSON.stringify(unmarkedCards));
          }}
          if (remoteData.readCards && typeof remoteData.readCards === 'object') {{
            for (const [cid, val] of Object.entries(remoteData.readCards)) {{
              if (!readCards[cid] && !unmarkedCards[cid]) {{
                readCards[cid] = val;
                newCardsCount++;
              }}
            }}
          }}
          if (remoteData.sessionSeconds && remoteData.sessionSeconds > sessionSeconds) {{
            sessionSeconds = remoteData.sessionSeconds;
          }}
          localStorage.setItem('sisyphus-consumed-cards', JSON.stringify(readCards));
          syncReadCardsUI();
          renderChapterBreakdown();

          if (isInitial && newCardsCount > 0) {{
            showToast(`☁️ Cloudflare Sync: Restored ${{newCardsCount}} paragraphs!`);
          }}
          if (isInitial && remoteData.currentSecId && !window.location.hash) {{
            const targetEl = document.getElementById(remoteData.currentSecId);
            if (targetEl) {{
              setTimeout(() => {{
                targetEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
              }}, 400);
            }}
          }}
        }}
        setSyncStatus('synced', 'Synced');
      }} catch (err) {{
        console.warn('Cloudflare pull error:', err);
        setSyncStatus('offline', 'Offline');
      }}
    }}

    function scheduleCloudPush(immediate = false, isReset = false) {{
      if (pushTimeout) clearTimeout(pushTimeout);
      if (immediate) {{
        pushCloudSync(isReset);
      }} else {{
        setSyncStatus('syncing', 'Saving...');
        pushTimeout = setTimeout(() => pushCloudSync(false), 1200);
      }}
    }}

    async function pushCloudSync(isReset = false) {{
      if (!syncToken || isSyncing) return;
      isSyncing = true;
      setSyncStatus('syncing', 'Syncing...');
      try {{
        const speedVal = parseInt(document.getElementById('tele-speed')?.textContent || '240');
        const payload = {{
          token: syncToken,
          data: {{
            reset: isReset,
            readCards: isReset ? {{}} : readCards,
            unmarkedCards: isReset ? {{}} : unmarkedCards,
            currentSecId: isReset ? '' : currentActivePid,
            sessionSeconds: isReset ? 0 : sessionSeconds,
            avgWpm: speedVal,
            updatedAt: Date.now()
          }}
        }};
        const res = await fetch('/api/sync', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload)
        }});
        if (!res.ok) throw new Error('Sync push failed');
        setSyncStatus('synced', 'Synced');
      }} catch (err) {{
        console.warn('Cloudflare push error:', err);
        setSyncStatus('offline', 'Offline');
      }} finally {{
        isSyncing = false;
      }}
    }}

    // Visibility listener for auto-sync across tabs/devices
    document.addEventListener('visibilitychange', () => {{
      if (document.visibilityState === 'visible') {{
        pullCloudSync(false);
      }}
    }});

    // Initialize state & Cloudflare Sync
    syncToken = getOrCreateSyncToken();
    syncReadCardsUI();
    updateActiveLocationOnScroll();
    pullCloudSync(true);
  </script>
</body>
</html>
"""
    with open(DIST_HTML, "w", encoding="utf-8") as f:
        f.write(app_template)
    with open(ROOT_HTML, "w", encoding="utf-8") as f:
        f.write(app_template)
    print("Generated full web app successfully in dist/ and root!")

def build_modern_masterwork_epub(sections):
    epub_path = os.path.join(BASE_DIR, "The_Myth_of_Sisyphus_Modern_Masterwork.epub")
    print(f"Building Modern Masterwork EPUB with {len(sections)} sections...")
    files = {}
    files["mimetype"] = "application/epub+zip"
    files["META-INF/container.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

    files["OEBPS/style.css"] = """
body {
  font-family: -apple-system-subheadline, "Georgia", "Charter", serif;
  font-size: 1.08em;
  line-height: 1.78;
  color: #1a1a1a;
  margin: 1.4em;
  padding: 0;
}
h1.book-title {
  text-align: center;
  font-size: 2.3em;
  margin-top: 1.6em;
  margin-bottom: 0.3em;
  color: #8b261e;
}
h2.author {
  text-align: center;
  font-size: 1.2em;
  font-weight: normal;
  font-style: italic;
  margin-bottom: 2em;
  color: #666;
}
.chapter-header {
  margin-top: 1.5em;
  margin-bottom: 2.2em;
  page-break-after: avoid;
  break-after: avoid;
  -webkit-column-break-after: avoid;
}
h2.chapter-title {
  font-size: 1.7em;
  color: #8b261e;
  border-bottom: 2px solid #8b261e;
  padding-bottom: 0.3em;
  margin: 0;
}
.chapter-sub {
  font-size: 0.82em;
  font-family: -apple-system, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #777;
  margin-bottom: 0.3em;
}
p.body-para {
  margin-bottom: 1.6em;
  text-align: justify;
}
.noteref {
  display: inline-block;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 0.72em;
  font-weight: 600;
  color: #8b261e;
  text-decoration: none;
  background: rgba(139, 38, 30, 0.08);
  border: 1px solid rgba(139, 38, 30, 0.25);
  padding: 0.12em 0.55em;
  border-radius: 4px;
  margin-left: 0.45em;
  vertical-align: middle;
  white-space: nowrap;
}
aside[epub\\:type="footnote"], aside {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 0.92em;
  line-height: 1.55;
  color: #222222;
}
.fn-badge {
  font-family: -apple-system, sans-serif;
  font-size: 0.72em;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #777777;
  margin-bottom: 0.4em;
}
.fn-orig {
  font-family: "Georgia", serif;
  font-style: italic;
  font-size: 0.96em;
  line-height: 1.65;
  color: #333333;
  margin-bottom: 0.8em;
  border-left: 3px solid #ccc;
  padding-left: 0.8em;
}
.fn-move {
  background: #edf2f7;
  border-left: 3px solid #1e3d59;
  padding: 0.7em 0.9em;
  border-radius: 0 4px 4px 0;
  color: #1e3d59;
  font-size: 0.88em;
  line-height: 1.45;
}
"""

    files["OEBPS/title.xhtml"] = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>The Myth of Sisyphus</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body style="text-align: center; padding-top: 3em;">
  <p style="font-family: -apple-system, sans-serif; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.2em; color: #8b261e; font-weight: bold;">Modern Critical Popover Edition</p>
  <h1 class="book-title">The Myth of Sisyphus</h1>
  <h2 class="author">Albert Camus</h2>
  <p style="color: #666; max-width: 500px; margin: 1.5em auto; line-height: 1.6;">
    Complete Dignified Modern Literary Translation with Instant Native Popovers for Justin O'Brien's 1955 Original Text and Philosophical Move Keys.
  </p>
</body>
</html>"""

    manifest_items = [
        '<item id="style" href="style.css" media-type="text/css"/>',
        '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>'
    ]
    spine_items = ['<itemref idref="title"/>']
    nav_links = ['<li><a href="title.xhtml">Title Page</a></li>']
    ncx_points = ['<navPoint id="np1" playOrder="1"><navLabel><text>Title Page</text></navLabel><content src="title.xhtml"/></navPoint>']

    for idx, sec in enumerate(sections, 2):
        sec_id = sec.get("section_id", f"sec{idx}")
        part = sec.get("part", "")
        title = sec.get("title", "")
        pairs = sec.get("pairs", [])
        xhtml_name = f"{sec_id}.xhtml"

        start_p = CHAPTER_PAGE_STARTS.get(sec_id, 1)
        next_p = 138
        if idx - 2 + 1 < len(sections):
            next_sec_id = sections[idx - 2 + 1].get("section_id")
            next_p = CHAPTER_PAGE_STARTS.get(next_sec_id, 138)
        pages_span = max(1, next_p - start_p)
        end_p = max(start_p, next_p - 1 if pages_span > 1 else start_p)
        sec_words = sum(len(" ".join(p.get("mod_sentences", [])).split()) for p in pairs) or 1

        ch_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>{title}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <div class="chapter-header">
    <div class="chapter-sub">{part} • pp. {start_p}–{end_p}</div>
    <h2 class="chapter-title">{title}</h2>
  </div>
"""
        asides = ""
        cum_sec_words = 0
        for p_idx, pair in enumerate(pairs, 1):
            pid = f"{sec_id}-fn{p_idx}"
            mod_text = pair.get("mod_text") or " ".join(pair.get("mod_sentences", []))
            orig_text = pair.get("orig_text") or " ".join(pair.get("orig_sentences", []))
            move = pair.get("move", "")
            para_words = len(mod_text.split())

            para_page = start_p + int((cum_sec_words / sec_words) * pages_span)
            para_page = min(end_p, max(start_p, para_page))
            cum_sec_words += para_words

            # Sanitize for XML
            mod_text = html.escape(mod_text, quote=False)
            orig_text = html.escape(orig_text, quote=False)
            move = html.escape(move, quote=False)

            ch_html += f"""  <p class="body-para">{mod_text}<a epub:type="noteref" class="noteref" href="#{pid}">✦ p.{para_page}</a></p>\n"""
            asides += f"""
  <aside epub:type="footnote" id="{pid}">
    <p class="fn-badge">Original 1955 Translation (Page {para_page} • §{p_idx})</p>
    <p class="fn-orig">"{orig_text}"</p>
    <p class="fn-move"><strong>The Philosophical Move:</strong> {move}</p>
  </aside>
"""
        ch_html += asides + "</body></html>"
        files[f"OEBPS/{xhtml_name}"] = ch_html

        manifest_items.append(f'<item id="{sec_id}" href="{xhtml_name}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{sec_id}"/>')
        nav_links.append(f'<li><a href="{xhtml_name}">{title}</a></li>')
        ncx_points.append(f'<navPoint id="np{idx}" playOrder="{idx}"><navLabel><text>{title}</text></navLabel><content src="{xhtml_name}"/></navPoint>')

    # nav.xhtml
    manifest_items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

    files["OEBPS/nav.xhtml"] = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
      {''.join(nav_links)}
    </ol>
  </nav>
</body>
</html>"""

    files["OEBPS/toc.ncx"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="urn:uuid:camus-sisyphus-modern-masterwork-full"/></head>
  <docTitle><text>The Myth of Sisyphus (Complete Modern Masterwork)</text></docTitle>
  <navMap>
    {''.join(ncx_points)}
  </navMap>
</ncx>"""

    files["OEBPS/content.opf"] = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">urn:uuid:camus-sisyphus-modern-masterwork-full</dc:identifier>
    <dc:title>The Myth of Sisyphus (Modern Masterwork Edition)</dc:title>
    <dc:creator>Albert Camus</dc:creator>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-09-22T09:00:00Z</meta>
  </metadata>
  <manifest>
    {''.join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {''.join(spine_items)}
  </spine>
</package>"""

    with zipfile.ZipFile(epub_path, 'w') as zf:
        zf.writestr("mimetype", files["mimetype"], compress_type=zipfile.ZIP_STORED)
        for p, c in files.items():
            if p == "mimetype": continue
            zf.writestr(p, c.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
    print(f"Generated Full Modern Masterwork EPUB: {os.path.getsize(epub_path)} bytes")

    # Sync to iCloud
    dest_icloud = os.path.join(ICLOUD_DIR, "The Myth of Sisyphus - Modern Masterwork.epub")
    if os.path.exists(dest_icloud):
        if os.path.isdir(dest_icloud): shutil.rmtree(dest_icloud)
        else: os.remove(dest_icloud)
    shutil.copyfile(epub_path, dest_icloud)
    print(f"Synced to Apple Books iCloud: {dest_icloud}")

def build_markdown_companion(sections):
    md_path = os.path.join(BASE_DIR, "myth_of_sisyphus_modern_translation.md")
    print("Building Master Markdown Companion...")
    lines = [
        "# *The Myth of Sisyphus* — Albert Camus",
        "## Complete Lossless Modern English Translation & Critical Decoder",
        "",
        "> [!NOTE]",
        "> **Source:** *The Myth of Sisyphus* (Albert Camus, 1942 French / 1955 English translation by Justin O'Brien).  ",
        "> **Methodology:** **Lossless Modern Translation.** Strips away mid-century Latinate archaisms, inverted periodic clauses, and academic fog, while retaining **100% of Camus's logical progression, philosophical distinctions, and visceral impact**.",
        "",
        "---",
        ""
    ]
    for sec in sections:
        part = sec.get("part", "")
        title = sec.get("title", "")
        pairs = sec.get("pairs", [])
        lines.append(f"## {title}")
        lines.append(f"*{part}*\n")
        for p_idx, pair in enumerate(pairs, 1):
            orig_text = pair.get("orig_text") or " ".join(pair.get("orig_sentences", []))
            mod_text = pair.get("mod_text") or " ".join(pair.get("mod_sentences", []))
            move = pair.get("move", "")
            lines.append(f"### §{p_idx}")
            lines.append(f"> **Original 1955 Translation:**  \n> {orig_text}\n")
            lines.append(f"**Dignified Modern Translation:**  \n{mod_text}\n")
            lines.append(f"> [!TIP]\n> **The Philosophical Move:** {move}\n")
            lines.append("---\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated Master Markdown Companion: {os.path.getsize(md_path)} bytes")

def build_dual_track_reflow_epub(sections):
    epub_path = os.path.join(BASE_DIR, "The_Myth_of_Sisyphus_Dual_Track_Edition.epub")
    print(f"Building Dual Track Reflow EPUB with {len(sections)} sections...")
    files = {}
    files["mimetype"] = "application/epub+zip"
    files["META-INF/container.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

    files["OEBPS/style.css"] = """
body {
  font-family: -apple-system-subheadline, "Georgia", "Charter", serif;
  font-size: 1.05em;
  line-height: 1.72;
  color: #1a1a1a;
  margin: 1.2em;
  padding: 0;
}
h1.book-title {
  text-align: center;
  font-size: 2.2em;
  margin-top: 1.5em;
  margin-bottom: 0.3em;
  color: #8b261e;
}
h2.author {
  text-align: center;
  font-size: 1.2em;
  font-weight: normal;
  font-style: italic;
  margin-bottom: 2em;
  color: #666;
}
.chapter-header {
  margin-top: 1.5em;
  margin-bottom: 2em;
  page-break-after: avoid;
  break-after: avoid;
}
h2.chapter-title {
  font-size: 1.6em;
  color: #8b261e;
  border-bottom: 2px solid #8b261e;
  padding-bottom: 0.3em;
  margin: 0;
}
.chapter-sub {
  font-size: 0.82em;
  font-family: -apple-system, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #777;
  margin-bottom: 0.3em;
}
.pair-block {
  margin-bottom: 2.5em;
  padding-bottom: 1.8em;
  border-bottom: 1px solid rgba(128,128,128,0.2);
}
.orig-unit {
  margin-bottom: 1.2em;
}
.badge {
  display: inline-block;
  font-family: -apple-system, sans-serif;
  font-size: 0.72em;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.2em 0.6em;
  border-radius: 3px;
  margin-bottom: 0.6em;
}
.badge-orig { background: #edeae2; color: #4a4d55; }
.badge-mod { background: #fae8e6; color: #8b261e; }
.text-orig {
  color: #222222;
  margin: 0 0 0.8em 0;
  font-size: 1.04em;
  line-height: 1.72;
}
.mod-card {
  background: rgba(139, 38, 30, 0.03);
  border-left: 3px solid #8b261e;
  padding: 0.9em 1.2em;
  margin: 1em 0;
  border-radius: 0 6px 6px 0;
}
.text-mod {
  color: #111111;
  font-size: 1.04em;
  line-height: 1.72;
  margin: 0 0 0.6em 0;
}
.move-box {
  margin-top: 0.8em;
  padding: 0.6em 0.9em;
  background: #edf2f7;
  border-radius: 4px;
  font-family: -apple-system, sans-serif;
  font-size: 0.86em;
  line-height: 1.45;
  color: #1e3d59;
}
"""

    files["OEBPS/title.xhtml"] = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>The Myth of Sisyphus</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body style="text-align: center; padding-top: 3em;">
  <p style="font-family: -apple-system, sans-serif; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.2em; color: #8b261e; font-weight: bold;">Dual-Track Reflow Edition</p>
  <h1 class="book-title">The Myth of Sisyphus</h1>
  <h2 class="author">Albert Camus</h2>
  <p style="color: #666; max-width: 500px; margin: 1.5em auto; line-height: 1.6;">
    Complete Critical Dual-Track Edition featuring Justin O'Brien's 1955 Classic Translation alongside a Lossless Modern English Translation and Philosophical Move Keys.
  </p>
</body>
</html>"""

    manifest_items = [
        '<item id="style" href="style.css" media-type="text/css"/>',
        '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>'
    ]
    spine_items = ['<itemref idref="title"/>']
    nav_links = ['<li><a href="title.xhtml">Title Page</a></li>']
    ncx_points = ['<navPoint id="np1" playOrder="1"><navLabel><text>Title Page</text></navLabel><content src="title.xhtml"/></navPoint>']

    for idx, sec in enumerate(sections, 2):
        sec_id = sec.get("section_id", f"sec{idx}")
        part = sec.get("part", "")
        title = sec.get("title", "")
        pairs = sec.get("pairs", [])
        xhtml_name = f"{sec_id}.xhtml"

        start_p = CHAPTER_PAGE_STARTS.get(sec_id, 1)
        next_p = 138
        if idx - 2 + 1 < len(sections):
            next_sec_id = sections[idx - 2 + 1].get("section_id")
            next_p = CHAPTER_PAGE_STARTS.get(next_sec_id, 138)
        pages_span = max(1, next_p - start_p)
        end_p = max(start_p, next_p - 1 if pages_span > 1 else start_p)
        sec_words = sum(len(" ".join(p.get("mod_sentences", [])).split()) for p in pairs) or 1

        ch_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <div class="chapter-header">
    <div class="chapter-sub">{html.escape(part)} • pp. {start_p}–{end_p}</div>
    <h2 class="chapter-title">{html.escape(title)}</h2>
  </div>
"""
        cum_sec_words = 0
        for p_idx, pair in enumerate(pairs, 1):
            orig_text = html.escape(pair.get("orig_text") or " ".join(pair.get("orig_sentences", [])), quote=False)
            mod_text = html.escape(pair.get("mod_text") or " ".join(pair.get("mod_sentences", [])), quote=False)
            move = html.escape(pair.get("move", ""), quote=False)
            para_words = len(mod_text.split())

            para_page = start_p + int((cum_sec_words / sec_words) * pages_span)
            para_page = min(end_p, max(start_p, para_page))
            cum_sec_words += para_words

            ch_html += f"""
  <div class="pair-block">
    <div class="orig-unit">
      <span class="badge badge-orig">Original 1955 Translation (Page {para_page} • §{p_idx})</span>
      <p class="text-orig">"{orig_text}"</p>
    </div>
    <div class="mod-card">
      <span class="badge badge-mod">Dignified Modern Translation (Page {para_page})</span>
      <p class="text-mod">{mod_text}</p>
      <div class="move-box">
        <strong>The Philosophical Move:</strong> {move}
      </div>
    </div>
  </div>
"""
        ch_html += "</body></html>"
        files[f"OEBPS/{xhtml_name}"] = ch_html
        manifest_items.append(f'<item id="{sec_id}" href="{xhtml_name}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{sec_id}"/>')
        nav_links.append(f'<li><a href="{xhtml_name}">{html.escape(title)}</a></li>')
        ncx_points.append(f'<navPoint id="np{idx}" playOrder="{idx}"><navLabel><text>{html.escape(title)}</text></navLabel><content src="{xhtml_name}"/></navPoint>')

    files["OEBPS/nav.xhtml"] = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>{''.join(nav_links)}</ol>
  </nav>
</body>
</html>"""

    files["OEBPS/toc.ncx"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="urn:uuid:camus-sisyphus-dual-track-full"/></head>
  <docTitle><text>The Myth of Sisyphus (Complete Dual Track)</text></docTitle>
  <navMap>{''.join(ncx_points)}</navMap>
</ncx>"""

    manifest_items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

    files["OEBPS/content.opf"] = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">urn:uuid:camus-sisyphus-dual-track-full</dc:identifier>
    <dc:title>The Myth of Sisyphus (Dual-Track Edition)</dc:title>
    <dc:creator>Albert Camus</dc:creator>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-09-22T09:00:00Z</meta>
  </metadata>
  <manifest>{''.join(manifest_items)}</manifest>
  <spine toc="ncx">{''.join(spine_items)}</spine>
</package>"""

    with zipfile.ZipFile(epub_path, 'w') as zf:
        zf.writestr("mimetype", files["mimetype"], compress_type=zipfile.ZIP_STORED)
        for p, c in files.items():
            if p == "mimetype": continue
            zf.writestr(p, c.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
    print(f"Generated Full Dual-Track EPUB: {os.path.getsize(epub_path)} bytes")

    dest_icloud = os.path.join(ICLOUD_DIR, "The Myth of Sisyphus - Dual Track Edition.epub")
    if os.path.exists(dest_icloud):
        if os.path.isdir(dest_icloud): shutil.rmtree(dest_icloud)
        else: os.remove(dest_icloud)
    shutil.copyfile(epub_path, dest_icloud)
    print(f"Synced to Apple Books iCloud: {dest_icloud}")

if __name__ == "__main__":
    secs = load_all_sections()
    print(f"Loaded {len(secs)} / {len(SECTION_ORDER)} sections.")
    build_web_app(secs)
    build_modern_masterwork_epub(secs)
    build_dual_track_reflow_epub(secs)
    build_markdown_companion(secs)
    print("All builds completed successfully!")

