import os
import zipfile
import shutil

TARGET_DIR = "/Users/felix/Projects/Myth-of-Sisyphus-Modern-Translation"
EPUB_PATH = os.path.join(TARGET_DIR, "The_Myth_of_Sisyphus_Dual_Track_Edition.epub")
ICLOUD_DIR = "/Users/felix/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents"

# Pairs data structure
# (chap_num, chap_name, pair_id, orig_text, mod_text, move_text)
pairs = [
    # CHAPTER 1
    (
        1, "Absurdity and Suicide", 1,
        "There is but one truly serious philosophical problem, and that is suicide. Judging whether life is or is not worth living amounts to answering the fundamental question of philosophy. All the rest—whether or not the world has three dimensions, whether the mind has nine or twelve categories—comes afterwards. These are games; one must first answer. And if it is true, as Nietzsche claims, that a philosopher, to deserve our respect, must preach by example, you can appreciate the importance of that reply, for it will precede the definitive act. These are facts the heart can feel; yet they call for careful study before they become clear to the intellect.",
        "There is only one genuinely serious philosophical question, and that is suicide. Deciding whether life is or is not worth living is the fundamental question of philosophy. Everything else—whether the physical universe has three dimensions, or whether human cognition operates through nine or twelve categories—is secondary. Those are intellectual pastimes; one must answer this first. And if Nietzsche is correct that a philosopher only commands our respect if they teach by personal example, one can appreciate the gravity of the answer, for it directly precedes an irreversible act. These are realities the heart senses instinctively, yet they demand rigorous examination before they become clear to the intellect.",
        "Camus establishes a strict hierarchy of urgency: metaphysical and epistemological theories are intellectual games; the question of survival and value precedes all contemplation."
    ),
    (
        1, "Absurdity and Suicide", 2,
        "If I ask myself how to judge that this question is more urgent than that, I reply that one judges by the actions it entails. I have never seen anyone die for the ontological argument. Galileo, who held a scientific truth of great importance, abjured it with the greatest ease as soon as it endangered his life. In a certain sense, he did right. That truth was not worth the stake. Whether the earth or the sun revolves around the other is a matter of profound indifference. To tell the truth, it is a futile question. On the other hand, I see many people die because they judge that life is not worth living. I see others paradoxically getting killed for the ideas or illusions that give them a reason for living (what is called a reason for living is also an excellent reason for dying). I therefore conclude that the meaning of life is the most urgent of questions.",
        "How does one determine whether one question is more urgent than another? By the actions it demands. No one has ever died defending an abstract proof for the existence of God. When Galileo discovered a scientific truth of immense importance, he renounced it without hesitation the moment his life was threatened—and in a sense, he was right. That truth was not worth burning at the stake for. Whether the Earth orbits the Sun or the Sun orbits the Earth is a matter of profound indifference to our day-to-day existence; in truth, it is an idle question. In contrast, I see men choose death because they conclude life is not worth living. Paradoxically, I see others die for the very ideals or illusions that give them a reason to live (for what provides a reason for living also provides a compelling reason for dying). I conclude, therefore, that the meaning of life is the most urgent question of all.",
        "Existential truth vs. theoretical truth. Galileo rightly refused martyrdom for astronomical physics because scientific facts do not alter the lived weight of existence, whereas meaning dictates literal life and death."
    ),
    (
        1, "Absurdity and Suicide", 3,
        "How to answer it? On all essential problems (I mean thereby those that run the risk of leading to death or those that intensify the passion of living) there are probably but two methods of thought: the method of La Palisse and the method of Don Quixote. Solely the balance between evidence and lyricism can allow us to achieve simultaneously emotion and lucidity. In a subject at once so humble and so heavy with emotion, the learned and classical dialectic must yield, one can see, to a more modest attitude of mind deriving at one and the same time from common sense and understanding.",
        "How are we to address it? For essential questions—those carrying the risk of death or the power to intensify the drive to live—there are essentially two modes of thought: the plain statement of the undeniable (the method of La Palice) and the passionate embrace of conviction (the method of Don Quixote). Only a balance between tangible evidence and poetic conviction allows us to attain both passion and clarity. On a subject so elementary yet so emotionally charged, formal academic dialectics must give way to a more modest cast of mind—one drawing simultaneously upon common sense and lucid psychological insight.",
        "Camus defines his methodology: balancing empirical fact (La Palice) with emotional passion (Don Quixote), discarding scholastic jargon in favor of clear psychological awareness."
    ),
    (
        1, "Absurdity and Suicide", 4,
        "Suicide has never been dealt with except as a social phenomenon. On the contrary, we are concerned here, at the outset, with the relationship between individual thought and suicide. An act like this is prepared within the silence of the heart, as is a great work of art. The man himself is ignorant of it. One evening he pulls the trigger or jumps. Of an apartment-building manager who had killed himself I was told that he had lost his daughter five years before, that he had changed greatly since, and that that experience had “undermined” him. A more exact word cannot be imagined. Beginning to think is beginning to be undermined. Society has but little connection with such beginnings. The worm is in man’s heart. That is where it must be sought. One must follow and understand this fatal game that leads from lucidity in the face of existence to flight from light.",
        "Suicide has almost always been treated merely as a sociological statistic. Here, by contrast, we are concerned from the start with the intimate connection between private consciousness and self-destruction. Such an act matures in the silence of the heart, much like a great work of art. The individual himself is often unaware of its silent gestation until, one evening, he pulls the trigger or leaps. Of a building manager who took his own life, I was told he had lost his daughter five years earlier, had altered profoundly thereafter, and that the ordeal had \"undermined\" him from within. A more precise term cannot be conceived. To begin to think is to begin to be undermined. Society has little bearing on these internal origins. The parasite resides within the human heart; that is where it must be sought. We must trace this fatal progression from the first lucid confrontation with existence to the eventual flight from reality.",
        "Camus shifts suicide from social statistics to private internal decay. 'To begin to think is to begin to be undermined' marks the terrifying rupture when conscious reflection destroys habitual numbness."
    ),
    (
        1, "Absurdity and Suicide", 5,
        "In a sense, and as in melodrama, killing yourself amounts to confessing. It is confessing that life is too much for you or that you do not understand it. Let’s not go too far in such analogies, however, but rather return to everyday words. It is merely confessing that that “is not worth the trouble.” Living, naturally, is never easy. You continue making the gestures commanded by existence for many reasons, the first of which is habit. Dying voluntarily implies that you have recognized, even instinctively, the ridiculous character of that habit, the absence of any profound reason for living, the insane character of that daily agitation, and the uselessness of suffering.",
        "In a sense, and as in theatrical tragedy, taking one's own life amounts to a confession. It is an admission that existence has overwhelmed you, or that you cannot make sense of it. Yet setting aside dramatic metaphors, in the language of everyday life: it is simply confessing that life is not worth the trouble. Living is never effortless. One continues to perform the gestures demanded by existence for many reasons, foremost among them being habit. Choosing to die voluntarily implies that one has recognized—even if only by instinct—the ridiculous nature of that habit, the total absence of any deeper reason for living, the frantic and pointless nature of our daily agitation, and the ultimate uselessness of our suffering.",
        "Defining suicide as the breaking of habit. We persist in life through mechanical momentum; voluntary death is the sudden realization that the momentum has no justification."
    ),
    (
        1, "Absurdity and Suicide", 6,
        "What, then, is that incalculable feeling that deprives the mind of the sleep necessary to life? A world that can be explained even with bad reasons is a familiar world. But, on the other hand, in a universe suddenly divested of illusions and lights, man feels an alien, a stranger. His exile is without remedy since he is deprived of the memory of a lost home or the hope of a promised land. This divorce between man and his life, the actor and his setting, is properly the feeling of absurdity. All healthy men having thought of their own suicide, it can be seen, without further explanation, that there is a direct connection between this feeling and the longing for death.",
        "What, then, is this elusive feeling that deprives the mind of the tranquil sleep necessary to sustain life? A world that can be explained—even through flawed reasoning—remains a familiar world. But in a cosmos suddenly stripped of comforting illusions and artificial certainties, man feels himself an alien, a stranger. His exile is without remedy, for he possesses neither the memory of a lost Eden nor the promise of a future redemption. This very divorce between man and his existence, between the actor and the stage, is precisely the feeling of absurdity. Given that virtually every healthy person has contemplated suicide at some point, there is an immediate, demonstrable link between this feeling of absurdity and the longing for death.",
        "The foundational definition of the Absurd: the 'divorce'—the painful rift between the human demand for purpose and a cosmos that offers no home, past paradise, or future salvation."
    ),
    (
        1, "Absurdity and Suicide", 7,
        "In a man’s attachment to life there is something stronger than all the ills in the world. The body’s judgment is as good as the mind’s, and the body shrinks from annihilation. We get into the habit of living before acquiring the habit of thinking. In that race which daily hastens us toward death, the body maintains its irreparable lead. In short, the essence of that contradiction lies in what I shall call the act of eluding because it is both less and more than diversion in the Pascalian sense. Eluding is the invariable game. The typical act of eluding, the fatal evasion that constitutes the third theme of this essay, is hope. Hope of another life one must “deserve” or trickery of those who live not for life itself but for some great idea that will transcend it, refine it, give it a meaning, and betray it.",
        "In a human being’s attachment to life, there exists a force stronger than all the miseries of the world. The body's judgment is fully equal to that of the intellect, and the body instinctively recoils from its own annihilation. We form the habit of living long before we ever acquire the habit of thinking. In that daily race carrying us toward death, the body retains an insurmountable lead over the mind. The essence of this contradiction resides in what I term evasion. The primary form of evasion—the fatal trap that forms the third major theme of this essay—is hope: whether the religious hope for an afterlife that must be earned, or the secular deception of living not for existence itself, but for some grand future ideology that claims to transcend and elevate life, yet ultimately betrays it.",
        "Exposing our dual survival buffers: (1) the biological body's ancient instinct to survive, and (2) the intellectual escape hatch of 'Hope' (postponing reality for heaven or a utopian future)."
    ),
    (
        1, "Absurdity and Suicide", 8,
        "One kills oneself because life is not worth living, that is certainly a truth—yet an unfruitful one because it is a truism. But does that insult to existence, that flat denial in which it is plunged come from the fact that it has no meaning? Does its absurdity require one to escape it through hope or suicide—this is what must be clarified, hunted down, and elucidated while brushing aside all the rest. Does the Absurd dictate death? This problem must be given priority over others, outside all methods of thought and all exercises of the disinterested mind.",
        "That one takes one's life because existence is deemed not worth living is undeniable—yet it remains an unhelpful truism. The real inquiry is this: does this flat rejection of existence stem necessarily from the fact that life lacks transcendent meaning? Does the absurdity of the human condition demand that we flee it—either through the false promise of hope or the finality of suicide? This is what must be pursued and clarified above all else: Does the Absurd dictate death? This problem demands absolute priority over all theoretical exercises of detached intellect.",
        "The core inquiry of the book: Does meaninglessness logically demand self-annihilation? Or can reason find a way to inhabit the Absurd with defiance and integrity?"
    ),

    # CHAPTER 2
    (
        2, "Absurd Walls", 1,
        "It happens that the stage sets collapse. Rising, streetcar, four hours in the office or the factory, meal, streetcar, four hours of work, meal, sleep, and Monday Tuesday Wednesday Thursday Friday and Saturday according to the same rhythm—this path is easily followed most of the time. But one day the “why” arises and everything begins in that weariness tinged with amazement. “Begins”—this is important. Weariness comes at the end of the acts of a mechanical life, but at the same time it inaugurates the impulse of consciousness. It awakens consciousness and provokes what follows. What follows is the gradual return into the chain or it is the definitive awakening.",
        "Yet there are times when the theatrical scenery collapses. Waking, the streetcar, four hours in the office or factory, a meal, the streetcar, four hours of labor, a meal, sleep, and Monday, Tuesday, Wednesday, Thursday, Friday, and Saturday unfolding to the identical rhythm—this routine is followed effortlessly for years. Yet one day, the question 'Why?' arises, and everything begins in a state of weariness mingled with astonishment. 'Begins'—this distinction is vital. Exhaustion concludes a life of mechanical habit, yet it simultaneously inaugurates the birth of genuine consciousness. It shakes the mind awake and provokes what follows: either a gradual return to the chains of routine, or a definitive, permanent awakening.",
        "Camus charts the sudden collapse of daily autopilot. The routine protects us from awareness; the intrusion of 'Why?' ends unconscious existence and forces a choice between conscious lucidity or relapse into stupor."
    ),
    (
        2, "Absurd Walls", 2,
        "We live on the future: “tomorrow,” “later on,” “when you have made your way,” “you will understand when you are old enough.” Such irrelevancies are wonderful, for, after all, it’s a matter of dying. Yet a day comes when a man notices or says that he is thirty. Thus he asserts his youth. But simultaneously he situates himself in relation to time. He takes his place in it. He admits that he stands at a certain point on a curve that he acknowledges having to travel to its end. He belongs to time, and by the horror that seizes him, he recognizes his worst enemy. Tomorrow, he was longing for tomorrow, whereas everything in him ought to reject it. That revolt of the flesh is the absurd.",
        "We live constantly leaning into the future: 'tomorrow,' 'later on,' 'once you have made your mark,' 'you will understand when you are older.' Such postponements are astonishingly ironic, for in the final analysis, they all lead to death. Yet a day comes when a man observes or announces that he is thirty. He thereby affirms his youth, yet simultaneously positions himself upon the arc of time. He realizes he occupies a fixed point on an irreversible curve that must be traveled to its inevitable conclusion. He belongs to time, and in the horror that grips him, he recognizes his deadliest adversary. Yesterday, he was yearning for tomorrow to arrive—when in truth, every instinct of his physical being ought to recoil from it. That instinctive revolt of the flesh against time is the absurd.",
        "The betrayal of time. We live on credit projected into the future, forgetting that the destination is death. Turning thirty marks the threshold where time ceases to be an ally and reveals itself as an executioner."
    ),
    (
        2, "Absurd Walls", 3,
        "Men, too, secrete the inhuman. At certain moments of lucidity, the mechanical aspect of their gestures, their meaningless pantomime makes silly everything that surrounds them. A man is talking on the telephone behind a glass partition; you cannot hear him, but you see his incomprehensible dumb show: you wonder why he is alive. This discomfort in the face of man’s own inhumanity, this incalculable tumble before the image of what we are, this “nausea,” as a writer of today calls it, is also the absurd. Likewise the stranger who at certain seconds comes to meet us in a mirror, the familiar and yet alarming brother we encounter in our own photographs is also the absurd.",
        "Human beings, too, emit this quality of the non-human. In flashes of detached lucidity, the mechanical nature of human gestures and our meaningless pantomime render everything around us grotesque. A man speaks into a telephone behind a soundproof glass partition; one cannot hear his words, but one observes his incomprehensible gestures: one wonders why such a creature exists. This unease before humanity's own mechanical strangeness, this vertigo when confronted by what we actually appear to be—this 'nausea,' as a contemporary writer terms it—is also the absurd. Likewise, that stranger who unexpectedly confronts us in a mirror, or the familiar yet disturbing double staring back from an old photograph, is also the absurd.",
        "The phone booth thought experiment and the mirror uncanny. When human behavior is stripped of context, its mechanical puppetry is exposed, inducing existential nausea (referencing Sartre)."
    ),
    (
        2, "Absurd Walls", 4,
        "I said that the world is absurd, but I was too hasty. This world in itself is not reasonable, that is all that can be said. But what is absurd is the confrontation of this irrational and the wild longing for clarity whose call echoes in the human heart. The absurd depends as much on man as on the world. For the moment it is all that links them together. It binds them one to the other as only hatred can weld two creatures together. This is all I can discern clearly in this measureless universe where my adventure takes place.",
        "I stated earlier that the world is absurd, yet I spoke too hastily. The universe in itself is not reasonable; that is all one can legitimately affirm. What is genuinely absurd is the confrontation between this irrational world and the profound hunger for clarity echoing within the human soul. The absurd depends as much upon human consciousness as it does upon the cosmic silence. For now, it is the sole bond linking them together—uniting them as only relentless antagonism can weld two adversaries in combat. This is all I can perceive with certainty in this measureless universe.",
        "The core philosophical correction. The universe is not absurd; it is simply indifferent. The Absurd is strictly relational: the friction generated when human longing strikes cosmic silence."
    ),
    (
        2, "Absurd Walls", 5,
        "At this point of his effort man stands face to face with the irrational. He feels within him his longing for happiness and for reason. The absurd is born of this confrontation between the human need and the unreasonable silence of the world. This must not be forgotten. This must be clung to because the whole consequence of a life can depend on it. The irrational, the human nostalgia, and the absurd that is born of their encounter—these are the three characters in the drama that must necessarily end with all the logic of which an existence is capable.",
        "At this stage of his inquiry, man stands face to face with the irrational. He feels within his breast two inescapable longings: the desire for happiness and the demand for reason. The absurd is born of this direct collision between human yearning and the silence of the universe. This core reality must not be surrendered, for the entire consequence of a life depends upon it. The irrational cosmos, human longing, and the absurd born of their encounter—these are the three characters in the tragedy, and the drama must be played out with all the rigorous logic of which a human existence is capable.",
        "The tripartite drama of existence: (1) The Irrational World, (2) Human Longing, and (3) The Absurd. Any philosophy that tries to eliminate one character is cheating."
    )
]

files = {}
files["mimetype"] = "application/epub+zip"

files["META-INF/container.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

# Style for Facing Pages (No tables, generous typography, 100% full width)
files["OEBPS/style.css"] = """
@namespace epub "http://www.idpf.org/2007/ops";

body {
  font-family: "Georgia", "Charter", "Palatino", serif;
  font-size: 1.05em;
  line-height: 1.7;
  color: #1a1a1a;
  margin: 1.5em 2em;
  padding: 0;
  -webkit-hyphens: none;
  hyphens: none;
}

.page-header {
  border-bottom: 1.5px solid #ded9cd;
  padding-bottom: 0.5em;
  margin-bottom: 1.5em;
  display: flex;
  justify-content: space-between;
  font-family: -apple-system, sans-serif;
  font-size: 0.75em;
  color: #787b84;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.badge {
  display: inline-block;
  font-family: -apple-system, sans-serif;
  font-size: 0.7em;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.25em 0.6em;
  border-radius: 4px;
  margin-bottom: 1.2em;
}
.badge-orig {
  background: #eae6dd;
  color: #4a4d55;
}
.badge-mod {
  background: #fae8e6;
  color: #8b261e;
}

.prose {
  font-size: 1.05em;
  line-height: 1.75;
  margin-bottom: 1.5em;
  text-align: justify;
}
.prose-orig {
  color: #333333;
}
.prose-mod {
  color: #111111;
}

.move-box {
  margin-top: 2em;
  padding: 1em 1.2em;
  background: #edf2f7;
  border-left: 3px solid #1e3d59;
  border-radius: 4px;
  font-family: -apple-system, sans-serif;
  font-size: 0.85em;
  line-height: 1.5;
  color: #1e3d59;
}
.move-box strong {
  text-transform: uppercase;
  font-size: 0.8em;
  letter-spacing: 0.06em;
}

/* Cover & Intro styles */
.cover-wrap {
  text-align: center;
  padding-top: 4em;
}
.cover-title {
  font-size: 2.4em;
  color: #8b261e;
  margin-bottom: 0.3em;
}
.cover-author {
  font-size: 1.3em;
  font-style: italic;
  color: #555;
  margin-bottom: 2em;
}
"""

# Title Page (Placed on right/recto)
files["OEBPS/title.xhtml"] = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <title>The Myth of Sisyphus</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <div class="cover-wrap">
    <p style="font-family: -apple-system, sans-serif; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.15em; color: #8b261e; font-weight: bold;">Parallel Critical Edition</p>
    <h1 class="cover-title">The Myth of Sisyphus</h1>
    <h2 class="cover-author">Albert Camus</h2>
    <p style="color: #666; max-width: 480px; margin: 0 auto; line-height: 1.6;">
      Facing-Pages Edition: Original 1955 English translation on the left page; dignified modern literary translation and philosophical logic notes on the right page.
    </p>
  </div>
</body>
</html>
"""

manifest_items = [
    '<item id="style" href="style.css" media-type="text/css"/>',
    '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>',
]
spine_itemrefs = [
    '<itemref idref="title" properties="page-spread-right"/>'
]
nav_points = [
    '<navPoint id="np-title" playOrder="1"><navLabel><text>Title Page</text></navLabel><content src="title.xhtml"/></navPoint>'
]
toc_links = [
    '<li><a href="title.xhtml">Title Page</a></li>'
]

play_order = 2

# Generate left and right pages for every pair
for c_num, c_title, p_id, orig, mod, move in pairs:
    left_id = f"c{c_num}_p{p_id}_left"
    right_id = f"c{c_num}_p{p_id}_right"

    # LEFT PAGE (Verso): Original 1955 Text
    left_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <title>{c_num}. {c_title} — Original</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <div class="page-header">
    <span>{c_num}. {c_title}</span>
    <span>Albert Camus (1942 / 1955)</span>
  </div>
  <span class="badge badge-orig">Original 1955 Translation</span>
  <p class="prose prose-orig">{orig}</p>
</body>
</html>"""

    # RIGHT PAGE (Recto): Modern Literary Translation + Philosophical Move
    right_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <title>{c_num}. {c_title} — Modern Translation</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <div class="page-header">
    <span>{c_num}. {c_title}</span>
    <span>Modern Literary Companion</span>
  </div>
  <span class="badge badge-mod">Dignified Modern Translation</span>
  <p class="prose prose-mod">{mod}</p>
  <div class="move-box">
    <strong>The Philosophical Move:</strong> {move}
  </div>
</body>
</html>"""

    files[f"OEBPS/{left_id}.xhtml"] = left_xhtml
    files[f"OEBPS/{right_id}.xhtml"] = right_xhtml

    manifest_items.append(f'<item id="{left_id}" href="{left_id}.xhtml" media-type="application/xhtml+xml"/>')
    manifest_items.append(f'<item id="{right_id}" href="{right_id}.xhtml" media-type="application/xhtml+xml"/>')

    # EPUB 3 page-spread properties!
    spine_itemrefs.append(f'<itemref idref="{left_id}" properties="page-spread-left"/>')
    spine_itemrefs.append(f'<itemref idref="{right_id}" properties="page-spread-right"/>')

    if p_id == 1:
        nav_points.append(f'<navPoint id="np-c{c_num}" playOrder="{play_order}"><navLabel><text>{c_num}. {c_title}</text></navLabel><content src="{left_id}.xhtml"/></navPoint>')
        toc_links.append(f'<li><a href="{left_id}.xhtml">{c_num}. {c_title}</a></li>')
        play_order += 1

# Add nav.xhtml
files["OEBPS/nav.xhtml"] = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <title>Table of Contents</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
      {' '.join(toc_links)}
    </ol>
  </nav>
</body>
</html>
"""
manifest_items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

# Add toc.ncx
files["OEBPS/toc.ncx"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:camus-sisyphus-facing-2026"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>The Myth of Sisyphus</text></docTitle>
  <navMap>
    {' '.join(nav_points)}
  </navMap>
</ncx>
"""
manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

# content.opf
files["OEBPS/content.opf"] = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">urn:uuid:camus-sisyphus-facing-2026</dc:identifier>
    <dc:title>The Myth of Sisyphus (Facing-Pages Edition)</dc:title>
    <dc:creator>Albert Camus</dc:creator>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-09-21T10:45:00Z</meta>
  </metadata>
  <manifest>
    {' '.join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {' '.join(spine_itemrefs)}
  </spine>
</package>
"""

# Write EPUB
with zipfile.ZipFile(EPUB_PATH, 'w') as zf:
    zf.writestr("mimetype", files["mimetype"], compress_type=zipfile.ZIP_STORED)
    for path, content in files.items():
        if path == "mimetype":
            continue
        zf.writestr(path, content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

print(f"Successfully generated Facing-Pages EPUB: {EPUB_PATH} ({os.path.getsize(EPUB_PATH)} bytes)")

# Sync to iCloud Apple Books
dest_icloud = os.path.join(ICLOUD_DIR, "The Myth of Sisyphus - Dual Track Edition.epub")
if os.path.exists(dest_icloud):
    if os.path.isdir(dest_icloud):
        shutil.rmtree(dest_icloud)
    else:
        os.remove(dest_icloud)
shutil.copyfile(EPUB_PATH, dest_icloud)
print(f"Synced EPUB to iCloud Apple Books: {dest_icloud}")
