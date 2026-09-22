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
        toc_html += f'<li><a href="#{sec_id}" onclick="toggleTOC(false)">{title}</a></li>\n'
    
    # Generate Sections HTML
    sections_html = ""
    for sec in sections:
        sec_id = sec.get("section_id", "")
        part = sec.get("part", "")
        title = sec.get("title", "")
        pairs = sec.get("pairs", [])
        
        sections_html += f"""
        <section class="book-section" id="{sec_id}">
          <div class="section-badge">{part}</div>
          <h2 class="section-title">{title}</h2>
          <div class="pairs-wrapper">
        """
        for p_idx, pair in enumerate(pairs, 1):
            pid = pair.get("id", f"{sec_id}-p{p_idx}")
            orig_sents = pair.get("orig_sentences", [])
            mod_sents = pair.get("mod_sentences", [])
            move = pair.get("move", "")
            
            sections_html += f"""
            <div class="pair-card" id="{pid}" data-pair="{pid}">
              <div class="col col-orig">
                <div class="col-header">
                  <span class="col-tag orig-tag">Original 1955 Translation</span>
                  <span class="para-num">§{p_idx}</span>
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
                  <span class="col-tag mod-tag">Dignified Modern Translation</span>
                  <span class="para-num">§{p_idx}</span>
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

    /* Telemetry Bar */
    .telemetry-bar {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 0.45rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-sans);
      font-size: 0.78rem;
      color: var(--text-muted);
    }}
    .tele-stats {{
      display: flex;
      gap: 1.4rem;
    }}
    .tele-item strong {{
      color: var(--text);
      font-weight: 600;
    }}

    /* Main Container */
    main.reader-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem 6rem 1.5rem;
    }}

    .book-section {{
      margin-bottom: 5rem;
      scroll-margin-top: 5rem;
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
      margin-bottom: 2rem;
      letter-spacing: -0.01em;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.6rem;
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
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .pair-card:hover {{
      border-color: var(--border-highlight);
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
    .para-num {{
      font-size: 0.72rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
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
      .tele-stats {{
        display: none;
      }}
    }}

    /* Key Concepts Modal */
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
    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.2rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.6rem;
    }}
    .modal-title {{ font-size: 1.2rem; font-weight: 700; color: var(--crimson); }}
    .close-btn {{ background: transparent; border: none; font-size: 1.4rem; color: var(--text-muted); cursor: pointer; }}
    .concept-item {{ margin-bottom: 1.2rem; }}
    .concept-name {{ font-weight: 700; font-size: 0.95rem; color: var(--gold); }}
    .concept-desc {{ font-size: 0.88rem; color: var(--text); margin-top: 0.2rem; line-height: 1.5; }}
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

      <button class="btn" onclick="toggleModal(true)">Concepts</button>
    </div>
  </header>

  <!-- Reading Telemetry Bar -->
  <div class="telemetry-bar">
    <div class="tele-stats">
      <span class="tele-item">Session: <strong id="timer-val">00:00</strong></span>
      <span class="tele-item">Pace: <strong>240 wpm</strong></span>
      <span class="tele-item">Status: <strong>Lossless Modern Translation</strong></span>
    </div>
    <div style="font-size: 0.74rem; color: var(--text-dim);">
      💡 Tap any sentence in either column to highlight its corresponding match.
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

    // Hover effect
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

    // Modal & TOC
    function toggleModal(open) {{
      document.getElementById('concepts-modal').classList.toggle('open', open);
    }}
    function toggleTOC(open) {{
      document.getElementById('toc-drawer').classList.toggle('open', open);
    }}

    // Session Timer
    let seconds = 0;
    setInterval(() => {{
      seconds++;
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      document.getElementById('timer-val').textContent = 
        String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
    }}, 1000);
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

        ch_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>{title}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <div class="chapter-header">
    <div class="chapter-sub">{part}</div>
    <h2 class="chapter-title">{title}</h2>
  </div>
"""
        asides = ""
        for p_idx, pair in enumerate(pairs, 1):
            pid = f"{sec_id}-fn{p_idx}"
            mod_text = pair.get("mod_text") or " ".join(pair.get("mod_sentences", []))
            orig_text = pair.get("orig_text") or " ".join(pair.get("orig_sentences", []))
            move = pair.get("move", "")

            # Sanitize for XML
            mod_text = html.escape(mod_text, quote=False)
            orig_text = html.escape(orig_text, quote=False)
            move = html.escape(move, quote=False)

            ch_html += f"""  <p class="body-para">{mod_text}<a epub:type="noteref" class="noteref" href="#{pid}">✦ Decode</a></p>\n"""
            asides += f"""
  <aside epub:type="footnote" id="{pid}">
    <p class="fn-badge">Original 1955 Translation (O'Brien)</p>
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

        ch_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <div class="chapter-header">
    <div class="chapter-sub">{html.escape(part)}</div>
    <h2 class="chapter-title">{html.escape(title)}</h2>
  </div>
"""
        for p_idx, pair in enumerate(pairs, 1):
            orig_text = html.escape(pair.get("orig_text") or " ".join(pair.get("orig_sentences", [])), quote=False)
            mod_text = html.escape(pair.get("mod_text") or " ".join(pair.get("mod_sentences", [])), quote=False)
            move = html.escape(pair.get("move", ""), quote=False)

            ch_html += f"""
  <div class="pair-block">
    <div class="orig-unit">
      <span class="badge badge-orig">Original 1955 Translation (§{p_idx})</span>
      <p class="text-orig">"{orig_text}"</p>
    </div>
    <div class="mod-card">
      <span class="badge badge-mod">Dignified Modern Translation</span>
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

