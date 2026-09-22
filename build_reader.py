import subprocess
import os
import shutil

TARGET_DIR = "/Users/felix/Projects/Myth-of-Sisyphus-Modern-Translation"
ICLOUD_DIR = "/Users/felix/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Myth of Sisyphus — Dual-Track Critical Edition</title>
<style>
  @page {
    size: A4 landscape;
    margin: 1.2cm 1.5cm;
  }

  :root {
    --bg-page: #fbfaf7;
    --bg-card: #ffffff;
    --bg-col-orig: #f6f4ee;
    --text-primary: #1a1a1a;
    --text-secondary: #4a4d55;
    --text-muted: #787b84;
    --border-color: #ded9cd;
    --accent-red: #8b261e;
    --accent-red-light: #fae8e6;
    --accent-blue: #1e3d59;
    --accent-blue-light: #edf2f7;
    --font-serif: "Charter", "Georgia", "Merriweather", "Palatino", serif;
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  [data-theme="dark"] {
    --bg-page: #141518;
    --bg-card: #1c1d22;
    --bg-col-orig: #18191d;
    --text-primary: #e6e5e1;
    --text-secondary: #a3a6ad;
    --text-muted: #696c73;
    --border-color: #2e3037;
    --accent-red: #e06c5f;
    --accent-red-light: #2a1b1b;
    --accent-blue: #72a5d8;
    --accent-blue-light: #16222f;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: var(--bg-page);
    color: var(--text-primary);
    font-family: var(--font-serif);
    font-size: 11pt;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  /* Interactive Navigation Header (hidden on print) */
  header.nav-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(251, 250, 247, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-color);
    padding: 0.6rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-sans);
  }
  [data-theme="dark"] header.nav-header {
    background: rgba(20, 21, 24, 0.95);
  }
  .nav-title {
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--accent-red);
  }
  .nav-title span { color: var(--text-muted); font-weight: 400; font-size: 0.8rem; }
  .nav-controls { display: flex; gap: 0.5rem; }
  .btn {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.35rem 0.65rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 500;
  }
  .btn:hover { border-color: var(--accent-red); color: var(--accent-red); }
  .btn.active { background: var(--accent-red); color: #fff; border-color: var(--accent-red); }

  .book-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 1.5rem 2rem 4rem 2rem;
  }

  /* Title / Cover Page */
  .cover-page {
    text-align: center;
    padding: 3rem 1rem 3rem 1rem;
    margin-bottom: 2rem;
    border-bottom: 2px solid var(--border-color);
    page-break-after: always;
  }
  .cover-tag {
    font-family: var(--font-sans);
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--accent-red);
    margin-bottom: 0.8rem;
  }
  .cover-title {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
  }
  .cover-author {
    font-size: 1.4rem;
    font-weight: 400;
    font-style: italic;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
  }
  .cover-desc {
    max-width: 750px;
    margin: 0 auto 2rem auto;
    font-size: 1rem;
    color: var(--text-secondary);
    line-height: 1.6;
  }

  /* Conceptual Map Box */
  .concept-box {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.2rem;
    margin: 1.5rem 0;
    page-break-inside: avoid;
  }
  .concept-box h3 {
    font-family: var(--font-sans);
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-red);
    margin-bottom: 0.8rem;
  }
  .concept-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
  }
  .concept-item {
    background: var(--bg-col-orig);
    padding: 0.7rem 0.9rem;
    border-radius: 6px;
    border-left: 3px solid var(--accent-red);
  }
  .concept-item .term {
    font-family: var(--font-sans);
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--accent-red);
    margin-bottom: 0.2rem;
  }
  .concept-item .def {
    font-size: 0.78rem;
    color: var(--text-primary);
    line-height: 1.4;
  }

  /* Chapter Header */
  .chapter-header {
    border-bottom: 2px solid var(--accent-red);
    padding-bottom: 6px;
    margin: 2.5rem 0 1.2rem 0;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-family: var(--font-sans);
    page-break-before: always;
    break-before: page;
  }
  .chapter-header:first-of-type {
    margin-top: 1rem;
  }
  .chapter-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--accent-red);
  }
  .chapter-meta {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 500;
  }

  /* TRUE TWO-COLUMN PARALLEL ROW (TABLE-BASED FOR PRINT RELIABILITY) */
  .parallel-unit {
    display: table;
    width: 100%;
    table-layout: fixed;
    margin-bottom: 1.1rem;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background: var(--bg-card);
    page-break-inside: avoid;
    break-inside: avoid;
    overflow: hidden;
  }
  .parallel-row {
    display: table-row;
  }
  .col-orig, .col-mod {
    display: table-cell;
    width: 50%;
    vertical-align: top;
    padding: 0.9rem 1.1rem;
  }
  .col-orig {
    background: var(--bg-col-orig);
    border-right: 1px solid var(--border-color);
  }
  .col-mod {
    background: var(--bg-card);
  }

  .badge {
    display: inline-block;
    font-family: var(--font-sans);
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.15rem 0.45rem;
    border-radius: 3px;
    margin-bottom: 0.5rem;
  }
  .badge-orig { background: #e2ddd3; color: #555860; }
  .badge-mod { background: var(--accent-red-light); color: var(--accent-red); }

  .prose-orig {
    color: var(--text-secondary);
    font-size: 0.92rem;
    line-height: 1.58;
  }
  .prose-mod {
    color: var(--text-primary);
    font-size: 0.95rem;
    line-height: 1.58;
  }

  /* The Philosophical Move Footer */
  .move-footer {
    display: table-footer-group;
    background: var(--accent-blue-light);
    border-top: 1px solid rgba(30, 61, 89, 0.15);
  }
  .move-footer td {
    padding: 0.45rem 1rem;
    font-family: var(--font-sans);
    font-size: 0.78rem;
    line-height: 1.45;
    color: var(--accent-blue);
  }
  .move-footer strong {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.7rem;
    margin-right: 0.3rem;
  }

  /* PRINT STYLES */
  @media print {
    body {
      background: #ffffff !important;
      color: #111111 !important;
      font-size: 9.5pt !important;
      line-height: 1.5 !important;
    }
    header.nav-header { display: none !important; }
    .book-container { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
    .parallel-unit {
      margin-bottom: 0.8cm !important;
      border: 1px solid #d0cbc2 !important;
      box-shadow: none !important;
    }
    .col-orig {
      background: #f7f5f0 !important;
      border-right: 1px solid #d0cbc2 !important;
      padding: 0.35cm 0.45cm !important;
    }
    .col-mod {
      background: #ffffff !important;
      padding: 0.35cm 0.45cm !important;
    }
    .prose-orig { font-size: 9pt !important; }
    .prose-mod { font-size: 9.3pt !important; }
    .move-footer td { font-size: 8pt !important; padding: 0.2cm 0.45cm !important; }
  }

  /* Responsive Stack for Phone (Screen only) */
  @media screen and (max-width: 800px) {
    .parallel-unit { display: block; }
    .parallel-row { display: block; }
    .col-orig, .col-mod { display: block; width: 100%; }
    .col-orig { border-right: none; border-bottom: 1px solid var(--border-color); }
    .move-footer { display: block; }
    .move-footer td { display: block; }
    .concept-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header class="nav-header">
  <div class="nav-title">
    The Myth of Sisyphus <span>— Parallel Dual-Column Edition</span>
  </div>
  <div class="nav-controls">
    <button class="btn" onclick="window.print()">🖨️ Print / Save PDF</button>
    <button class="btn" onclick="toggleTheme()">🌓 Dark Mode</button>
  </div>
</header>

<div class="book-container">

  <!-- Title / Cover -->
  <section class="cover-page">
    <div class="cover-tag">Parallel Critical Edition • Side-by-Side Reading</div>
    <h1 class="cover-title">The Myth of Sisyphus</h1>
    <div class="cover-author">Albert Camus</div>
    <p class="cover-desc">
      A strict parallel column layout designed for side-by-side study on iPad, laptop, or desktop.
      The left column preserves Justin O'Brien's 1955 English translation. The right column provides a dignified modern literary translation that resolves mid-century syntactic gridlocks without colloquial slang.
    </p>

    <div class="concept-box">
      <h3>Key Conceptual Anchors</h3>
      <div class="concept-grid">
        <div class="concept-item">
          <div class="term">The Absurd (L'Absurde)</div>
          <div class="def">The friction struck between humanity's desperate demand for reason and the silent indifference of the universe.</div>
        </div>
        <div class="concept-item">
          <div class="term">Philosophical Suicide</div>
          <div class="def">Intellectual surrender: forcing a leap of faith (in God, mysticism, or ideology) to escape the tension of the Absurd.</div>
        </div>
        <div class="concept-item">
          <div class="term">Lucid Revolt (La Révolte)</div>
          <div class="def">Living with total conscious awareness, refusing both physical suicide and intellectual escapism.</div>
        </div>
      </div>
    </div>
  </section>

  <!-- CHAPTER 1 -->
  <div class="chapter-header">
    <div class="chapter-title">1. Absurdity and Suicide</div>
    <div class="chapter-meta">Part I: An Absurd Reasoning — Albert Camus (1942)</div>
  </div>

  <!-- C1 P1 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">There is but one truly serious philosophical problem, and that is suicide. Judging whether life is or is not worth living amounts to answering the fundamental question of philosophy. All the rest—whether or not the world has three dimensions, whether the mind has nine or twelve categories—comes afterwards. These are games; one must first answer. And if it is true, as Nietzsche claims, that a philosopher, to deserve our respect, must preach by example, you can appreciate the importance of that reply, for it will precede the definitive act. These are facts the heart can feel; yet they call for careful study before they become clear to the intellect.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">There is only one genuinely serious philosophical question, and that is suicide. Deciding whether life is or is not worth living is the fundamental question of philosophy. Everything else—whether the physical universe has three dimensions, or whether human cognition operates through nine or twelve categories—is secondary. Those are intellectual pastimes; one must answer this first. And if Nietzsche is correct that a philosopher only commands our respect if they teach by personal example, one can appreciate the gravity of the answer, for it directly precedes an irreversible act. These are realities the heart senses instinctively, yet they demand rigorous examination before they become clear to the intellect.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Camus establishes a strict hierarchy of urgency: metaphysical and epistemological theories are intellectual games; the question of survival and value precedes all contemplation.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P2 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">If I ask myself how to judge that this question is more urgent than that, I reply that one judges by the actions it entails. I have never seen anyone die for the ontological argument. Galileo, who held a scientific truth of great importance, abjured it with the greatest ease as soon as it endangered his life. In a certain sense, he did right. That truth was not worth the stake. Whether the earth or the sun revolves around the other is a matter of profound indifference. To tell the truth, it is a futile question. On the other hand, I see many people die because they judge that life is not worth living. I see others paradoxically getting killed for the ideas or illusions that give them a reason for living (what is called a reason for living is also an excellent reason for dying). I therefore conclude that the meaning of life is the most urgent of questions.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">How does one determine whether one question is more urgent than another? By the actions it demands. No one has ever died defending an abstract proof for the existence of God. When Galileo discovered a scientific truth of immense importance, he renounced it without hesitation the moment his life was threatened—and in a sense, he was right. That truth was not worth burning at the stake for. Whether the Earth orbits the Sun or the Sun orbits the Earth is a matter of profound indifference to our day-to-day existence; in truth, it is an idle question. In contrast, I see men choose death because they conclude life is not worth living. Paradoxically, I see others die for the very ideals or illusions that give them a reason to live (for what provides a reason for living also provides a compelling reason for dying). I conclude, therefore, that the meaning of life is the most urgent question of all.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Existential truth vs. theoretical truth. Galileo rightly refused martyrdom for astronomical physics because scientific facts do not alter the lived weight of existence, whereas meaning dictates literal life and death.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P3 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">How to answer it? On all essential problems (I mean thereby those that run the risk of leading to death or those that intensify the passion of living) there are probably but two methods of thought: the method of La Palisse and the method of Don Quixote. Solely the balance between evidence and lyricism can allow us to achieve simultaneously emotion and lucidity. In a subject at once so humble and so heavy with emotion, the learned and classical dialectic must yield, one can see, to a more modest attitude of mind deriving at one and the same time from common sense and understanding.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">How are we to address it? For essential questions—those carrying the risk of death or the power to intensify the drive to live—there are essentially two modes of thought: the plain statement of the undeniable (the method of La Palice) and the passionate embrace of conviction (the method of Don Quixote). Only a balance between tangible evidence and poetic conviction allows us to attain both passion and clarity. On a subject so elementary yet so emotionally charged, formal academic dialectics must give way to a more modest cast of mind—one drawing simultaneously upon common sense and lucid psychological insight.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Camus defines his methodology: balancing empirical fact (La Palice) with emotional passion (Don Quixote), discarding scholastic jargon in favor of clear psychological awareness.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P4 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">Suicide has never been dealt with except as a social phenomenon. On the contrary, we are concerned here, at the outset, with the relationship between individual thought and suicide. An act like this is prepared within the silence of the heart, as is a great work of art. The man himself is ignorant of it. One evening he pulls the trigger or jumps. Of an apartment-building manager who had killed himself I was told that he had lost his daughter five years before, that he had changed greatly since, and that that experience had “undermined” him. A more exact word cannot be imagined. Beginning to think is beginning to be undermined. Society has but little connection with such beginnings. The worm is in man’s heart. That is where it must be sought. One must follow and understand this fatal game that leads from lucidity in the face of existence to flight from light.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">Suicide has almost always been treated merely as a sociological statistic. Here, by contrast, we are concerned from the start with the intimate connection between private consciousness and self-destruction. Such an act matures in the silence of the heart, much like a great work of art. The individual himself is often unaware of its silent gestation until, one evening, he pulls the trigger or leaps. Of a building manager who took his own life, I was told he had lost his daughter five years earlier, had altered profoundly thereafter, and that the ordeal had "undermined" him from within. A more precise term cannot be conceived. <em>To begin to think is to begin to be undermined.</em> Society has little bearing on these internal origins. The parasite resides within the human heart; that is where it must be sought. We must trace this fatal progression from the first lucid confrontation with existence to the eventual flight from reality.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Camus shifts suicide from social statistics to private internal decay. "To begin to think is to begin to be undermined" marks the terrifying rupture when conscious reflection destroys habitual numbness.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P6 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">In a sense, and as in melodrama, killing yourself amounts to confessing. It is confessing that life is too much for you or that you do not understand it. Let’s not go too far in such analogies, however, but rather return to everyday words. It is merely confessing that that “is not worth the trouble.” Living, naturally, is never easy. You continue making the gestures commanded by existence for many reasons, the first of which is habit. Dying voluntarily implies that you have recognized, even instinctively, the ridiculous character of that habit, the absence of any profound reason for living, the insane character of that daily agitation, and the uselessness of suffering.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">In a sense, and as in theatrical tragedy, taking one's own life amounts to a confession. It is an admission that existence has overwhelmed you, or that you cannot make sense of it. Yet setting aside dramatic metaphors, in the language of everyday life: it is simply confessing that life <em>is not worth the trouble</em>. Living is never effortless. One continues to perform the gestures demanded by existence for many reasons, foremost among them being habit. Choosing to die voluntarily implies that one has recognized—even if only by instinct—the ridiculous nature of that habit, the total absence of any deeper reason for living, the frantic and pointless nature of our daily agitation, and the ultimate uselessness of our suffering.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Defining suicide as the breaking of habit. We persist in life through mechanical momentum; voluntary death is the sudden realization that the momentum has no justification.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P7 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">What, then, is that incalculable feeling that deprives the mind of the sleep necessary to life? A world that can be explained even with bad reasons is a familiar world. But, on the other hand, in a universe suddenly divested of illusions and lights, man feels an alien, a stranger. His exile is without remedy since he is deprived of the memory of a lost home or the hope of a promised land. This divorce between man and his life, the actor and his setting, is properly the feeling of absurdity. All healthy men having thought of their own suicide, it can be seen, without further explanation, that there is a direct connection between this feeling and the longing for death.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">What, then, is this elusive feeling that deprives the mind of the tranquil sleep necessary to sustain life? A world that can be explained—even through flawed reasoning—remains a familiar world. But in a cosmos suddenly stripped of comforting illusions and artificial certainties, man feels himself an alien, a stranger. His exile is without remedy, for he possesses neither the memory of a lost Eden nor the promise of a future redemption. <strong>This very divorce between man and his existence, between the actor and the stage, is precisely the feeling of absurdity.</strong> Given that virtually every healthy person has contemplated suicide at some point, there is an immediate, demonstrable link between this feeling of absurdity and the longing for death.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> The foundational definition of the Absurd. Absurdity is the "divorce"—the painful rift between the human demand for purpose and a cosmos that offers no home, past paradise, or future salvation.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P11 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">In a man’s attachment to life there is something stronger than all the ills in the world. The body’s judgment is as good as the mind’s, and the body shrinks from annihilation. We get into the habit of living before acquiring the habit of thinking. In that race which daily hastens us toward death, the body maintains its irreparable lead. In short, the essence of that contradiction lies in what I shall call the act of eluding because it is both less and more than diversion in the Pascalian sense. Eluding is the invariable game. The typical act of eluding, the fatal evasion that constitutes the third theme of this essay, is hope. Hope of another life one must “deserve” or trickery of those who live not for life itself but for some great idea that will transcend it, refine it, give it a meaning, and betray it.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">In a human being’s attachment to life, there exists a force stronger than all the miseries of the world. The body's judgment is fully equal to that of the intellect, and the body instinctively recoils from its own annihilation. <em>We form the habit of living long before we ever acquire the habit of thinking.</em> In that daily race carrying us toward death, the body retains an insurmountable lead over the mind. The essence of this contradiction resides in what I term <strong>evasion</strong>. The primary form of evasion—the fatal trap that forms the third major theme of this essay—is <strong>hope</strong>: whether the religious hope for an afterlife that must be earned, or the secular deception of living not for existence itself, but for some grand future ideology that claims to transcend and elevate life, yet ultimately betrays it.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Exposing our dual survival buffers: (1) the biological body's ancient instinct to survive, and (2) the intellectual escape hatch of "Hope" (postponing reality for heaven or a utopian future).
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C1 P12 -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">One kills oneself because life is not worth living, that is certainly a truth—yet an unfruitful one because it is a truism. But does that insult to existence, that flat denial in which it is plunged come from the fact that it has no meaning? Does its absurdity require one to escape it through hope or suicide—this is what must be clarified, hunted down, and elucidated while brushing aside all the rest. Does the Absurd dictate death? This problem must be given priority over others, outside all methods of thought and all exercises of the disinterested mind.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">That one takes one's life because existence is deemed not worth living is undeniable—yet it remains an unhelpful truism. The real inquiry is this: does this flat rejection of existence stem necessarily from the fact that life lacks transcendent meaning? Does the absurdity of the human condition demand that we flee it—either through the false promise of hope or the finality of suicide? This is what must be pursued and clarified above all else: <strong>Does the Absurd dictate death?</strong> This problem demands absolute priority over all theoretical exercises of detached intellect.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> The core inquiry of the book. Does meaninglessness logically demand self-annihilation? Or can reason find a way to inhabit the Absurd with defiance and integrity?
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- CHAPTER 2 -->
  <div class="chapter-header">
    <div class="chapter-title">2. Absurd Walls</div>
    <div class="chapter-meta">Part I: An Absurd Reasoning — Albert Camus (1942)</div>
  </div>

  <!-- C2 P2 Routine -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">It happens that the stage sets collapse. Rising, streetcar, four hours in the office or the factory, meal, streetcar, four hours of work, meal, sleep, and Monday Tuesday Wednesday Thursday Friday and Saturday according to the same rhythm—this path is easily followed most of the time. But one day the “why” arises and everything begins in that weariness tinged with amazement. “Begins”—this is important. Weariness comes at the end of the acts of a mechanical life, but at the same time it inaugurates the impulse of consciousness. It awakens consciousness and provokes what follows. What follows is the gradual return into the chain or it is the definitive awakening.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">Yet there are times when the theatrical scenery collapses. Waking, the streetcar, four hours in the office or factory, a meal, the streetcar, four hours of labor, a meal, sleep, and Monday, Tuesday, Wednesday, Thursday, Friday, and Saturday unfolding to the identical rhythm—this routine is followed effortlessly for years. <strong>Yet one day, the question "Why?" arises, and everything begins in a state of weariness mingled with astonishment.</strong> "Begins"—this distinction is vital. Exhaustion concludes a life of mechanical habit, yet it simultaneously inaugurates the birth of genuine consciousness. It shakes the mind awake and provokes what follows: either a gradual return to the chains of routine, or a definitive, permanent awakening.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> Camus charts the sudden collapse of daily autopilot. The routine protects us from awareness; the intrusion of "Why?" ends unconscious existence and forces a choice between conscious lucidity or relapse into stupor.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C2 P3 Time -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">We live on the future: “tomorrow,” “later on,” “when you have made your way,” “you will understand when you are old enough.” Such irrelevancies are wonderful, for, after all, it’s a matter of dying. Yet a day comes when a man notices or says that he is thirty. Thus he asserts his youth. But simultaneously he situates himself in relation to time. He takes his place in it. He admits that he stands at a certain point on a curve that he acknowledges having to travel to its end. He belongs to time, and by the horror that seizes him, he recognizes his worst enemy. Tomorrow, he was longing for tomorrow, whereas everything in him ought to reject it. That revolt of the flesh is the absurd.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">We live constantly leaning into the future: "tomorrow," "later on," "once you have made your mark," "you will understand when you are older." Such postponements are astonishingly ironic, for in the final analysis, they all lead to death. Yet a day comes when a man observes or announces that he is thirty. He thereby affirms his youth, yet simultaneously positions himself upon the arc of time. He realizes he occupies a fixed point on an irreversible curve that must be traveled to its inevitable conclusion. He belongs to time, and in the horror that grips him, he recognizes his deadliest adversary. Yesterday, he was yearning for tomorrow to arrive—when in truth, every instinct of his physical being ought to recoil from it. <strong>That instinctive revolt of the flesh against time is the absurd.</strong></p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> The betrayal of time. We live on credit projected into the future, forgetting that the destination is death. Turning thirty marks the threshold where time ceases to be an ally and reveals itself as an executioner.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C2 P5 Inhumanity -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">Men, too, secrete the inhuman. At certain moments of lucidity, the mechanical aspect of their gestures, their meaningless pantomime makes silly everything that surrounds them. A man is talking on the telephone behind a glass partition; you cannot hear him, but you see his incomprehensible dumb show: you wonder why he is alive. This discomfort in the face of man’s own inhumanity, this incalculable tumble before the image of what we are, this “nausea,” as a writer of today calls it, is also the absurd. Likewise the stranger who at certain seconds comes to meet us in a mirror, the familiar and yet alarming brother we encounter in our own photographs is also the absurd.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">Human beings, too, emit this quality of the non-human. In flashes of detached lucidity, the mechanical nature of human gestures and our meaningless pantomime render everything around us grotesque. A man speaks into a telephone behind a soundproof glass partition; one cannot hear his words, but one observes his incomprehensible gestures: one wonders why such a creature exists. This unease before humanity's own mechanical strangeness, this vertigo when confronted by what we actually appear to be—this "nausea," as a contemporary writer terms it—is also the absurd. Likewise, that stranger who unexpectedly confronts us in a mirror, or the familiar yet disturbing double staring back from an old photograph, is also the absurd.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> The phone booth thought experiment and the mirror uncanny. When human behavior is stripped of context, its mechanical puppetry is exposed, inducing existential nausea (referencing Sartre).
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C2 P9 Science & Formula -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">I said that the world is absurd, but I was too hasty. This world in itself is not reasonable, that is all that can be said. But what is absurd is the confrontation of this irrational and the wild longing for clarity whose call echoes in the human heart. The absurd depends as much on man as on the world. For the moment it is all that links them together. It binds them one to the other as only hatred can weld two creatures together. This is all I can discern clearly in this measureless universe where my adventure takes place.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">I stated earlier that the world is absurd, yet I spoke too hastily. The universe in itself is not reasonable; that is all one can legitimately affirm. <strong>What is genuinely absurd is the confrontation between this irrational world and the profound hunger for clarity echoing within the human soul.</strong> The absurd depends as much upon human consciousness as it does upon the cosmic silence. For now, it is the sole bond linking them together—uniting them as only relentless antagonism can weld two adversaries in combat. This is all I can perceive with certainty in this measureless universe.</p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> The core philosophical correction. The universe is not absurd; it is simply indifferent. The Absurd is strictly relational: the friction generated when human longing strikes cosmic silence.
        </td>
      </tr>
    </tfoot>
  </table>

  <!-- C2 P11 Climax -->
  <table class="parallel-unit">
    <tr class="parallel-row">
      <td class="col-orig">
        <span class="badge badge-orig">Original 1955 Translation</span>
        <p class="prose-orig">At this point of his effort man stands face to face with the irrational. He feels within him his longing for happiness and for reason. The absurd is born of this confrontation between the human need and the unreasonable silence of the world. This must not be forgotten. This must be clung to because the whole consequence of a life can depend on it. The irrational, the human nostalgia, and the absurd that is born of their encounter—these are the three characters in the drama that must necessarily end with all the logic of which an existence is capable.</p>
      </td>
      <td class="col-mod">
        <span class="badge badge-mod">Dignified Modern Translation</span>
        <p class="prose-mod">At this stage of his inquiry, man stands face to face with the irrational. He feels within his breast two inescapable longings: the desire for happiness and the demand for reason. The absurd is born of this direct collision between human yearning and the silence of the universe. This core reality must not be surrendered, for the entire consequence of a life depends upon it. <strong>The irrational cosmos, human longing, and the absurd born of their encounter—these are the three characters in the tragedy, and the drama must be played out with all the rigorous logic of which a human existence is capable.</strong></p>
      </td>
    </tr>
    <tfoot class="move-footer">
      <tr>
        <td colspan="2">
          <strong>The Philosophical Move:</strong> The tripartite drama of existence: (1) The Irrational World, (2) Human Longing, and (3) The Absurd. Any philosophy that tries to eliminate one character is cheating.
        </td>
      </tr>
    </tfoot>
  </table>

</div>

<script>
  function toggleTheme() {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
  }
</script>

</body>
</html>
"""

html_path = os.path.join(TARGET_DIR, "camus_dual_track_reader.html")
pdf_path = os.path.join(TARGET_DIR, "The_Myth_of_Sisyphus_Dual_Track_Edition.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Wrote updated HTML reader to {html_path}")

# Compile to landscape PDF via Chrome Headless
cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file://{html_path}"
]

print("Rendering True Two-Column Landscape PDF via Chrome...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"Rendered PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
    # Sync to Apple Books
    dest_icloud = os.path.join(ICLOUD_DIR, "The Myth of Sisyphus - Dual Track Edition.pdf")
    shutil.copyfile(pdf_path, dest_icloud)
    print(f"Synced updated PDF to iCloud Apple Books: {dest_icloud}")
else:
    print("Error rendering PDF:", res.stderr)
