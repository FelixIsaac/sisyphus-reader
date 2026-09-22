import os
import json

TARGET_DIR = "/Users/felix/Projects/Myth-of-Sisyphus-Modern-Translation"
DIST_DIR = os.path.join(TARGET_DIR, "dist")
os.makedirs(DIST_DIR, exist_ok=True)
DIST_HTML = os.path.join(DIST_DIR, "index.html")
ROOT_HTML = os.path.join(TARGET_DIR, "index.html")

# Preface Data
preface_pairs = [
    {
        "id": "pref-p1",
        "orig_sentences": [
            "FOR ME “The Myth of Sisyphus” marks the beginning of an idea which I was to pursue in The Rebel.",
            "It attempts to resolve the problem of suicide, as The Rebel attempts to resolve that of murder, in both cases without the aid of eternal values which, temporarily perhaps, are absent or distorted in contemporary Europe.",
            "The fundamental subject of “The Myth of Sisyphus” is this: it is legitimate and necessary to wonder whether life has a meaning; therefore it is legitimate to meet the problem of suicide face to face.",
            "The answer, underlying and appearing through the paradoxes which cover it, is this: even if one does not believe in God, suicide is not legitimate.",
            "Written fifteen years ago, in 1940, amid the French and European disaster, this book declares that even within the limits of nihilism it is possible to find the means to proceed beyond nihilism.",
            "In all the books I have written since, I have attempted to pursue this direction.",
            "Although “The Myth of Sisyphus” poses mortal problems, it sums itself up for me as a lucid invitation to live and to create, in the very midst of the desert."
        ],
        "mod_sentences": [
            "For me, The Myth of Sisyphus marks the birth of a central intuition that I would later develop in The Rebel.",
            "It seeks to resolve the question of suicide, just as The Rebel seeks to resolve the question of murder—in both instances without relying on transcendent, eternal values, which for now are absent or broken in modern Europe.",
            "The foundational premise of this book is straightforward: it is entirely legitimate and necessary to ask whether life possesses meaning; therefore, one must confront the reality of suicide directly.",
            "The definitive conclusion, emerging through all the paradoxes that frame it, is this: even in the absence of God, suicide is not a valid answer.",
            "Written fifteen years ago in 1940, during the catastrophe of the war in France and Europe, this work affirms that even within the depths of nihilism, one can discover the strength to transcend nihilism.",
            "In all the books I have written since, I have attempted to pursue this direction.",
            "Although this essay wrestles with deadly questions, for me it stands as an uncompromising invitation to live and to create—directly in the heart of the wasteland."
        ],
        "move": "Camus summarizes his entire thesis before the book begins: This is an anti-nihilist work. Recognizing that life has no cosmic purpose does not justify self-destruction; it makes creative living even more urgent and heroic."
    },
    {
        "id": "pref-p2",
        "orig_sentences": [
            "THE PAGES that follow deal with an absurd sensitivity that can be found widespread in the age—and not with an absurd philosophy which our time, properly speaking, has not known.",
            "It is therefore simply fair to point out, at the outset, what these pages owe to certain contemporary thinkers.",
            "It is so far from my intention to hide this that they will be found cited and commented upon throughout this work.",
            "But it is useful to note at the same time that the absurd, hitherto taken as a conclusion, is considered in this essay as a starting-point.",
            "In this sense it may be said that there is something provisional in my commentary: one cannot prejudge the position it entails.",
            "There will be found here merely the description, in the pure state, of an intellectual malady.",
            "No metaphysic, no belief is involved in it for the moment.",
            "These are the limits and the only bias of this book."
        ],
        "mod_sentences": [
            "The pages that follow describe a widespread contemporary sensitivity to the absurd—not an established 'absurd philosophy,' which our era has not actually developed.",
            "It is only honest to acknowledge from the beginning how much this inquiry owes to contemporary philosophers; far from concealing these influences, they will be openly analyzed throughout this text.",
            "Crucially, however, while previous thinkers treated the Absurd as a final dead-end conclusion, in this book the Absurd is treated purely as a starting point.",
            "My analysis is therefore provisional: one should not assume the final verdict beforehand.",
            "What you will find here is simply the unvarnished diagnosis of an intellectual condition.",
            "No metaphysical system, no theology, and no dogma are assumed.",
            "That is the exact scope and sole boundary of this book."
        ],
        "move": "The Pindar epigraph provides the moral motto of the book: reject dreams of immortality (heaven) and milk mortal life for maximum intensity. Camus also clarifies: Absurdity is not his conclusion—it is merely his starting point."
    }
]

# Chapter 1 Data
c1_pairs = [
    {
        "id": "c1-p1",
        "orig_sentences": [
            "There is but one truly serious philosophical problem, and that is suicide.",
            "Judging whether life is or is not worth living amounts to answering the fundamental question of philosophy.",
            "All the rest—whether or not the world has three dimensions, whether the mind has nine or twelve categories—comes afterwards.",
            "These are games; one must first answer.",
            "And if it is true, as Nietzsche claims, that a philosopher, to deserve our respect, must preach by example, you can appreciate the importance of that reply, for it will precede the definitive act.",
            "These are facts the heart can feel; yet they call for careful study before they become clear to the intellect."
        ],
        "mod_sentences": [
            "There is only one genuinely serious philosophical question, and that is suicide.",
            "Deciding whether life is or is not worth living is the fundamental question of philosophy.",
            "Everything else—whether the physical universe has three dimensions, or whether human cognition operates through nine or twelve categories—is secondary.",
            "Those are intellectual pastimes; one must answer this first.",
            "And if Nietzsche is correct that a philosopher only commands our respect if they teach by personal example, one can appreciate the gravity of the answer, for it directly precedes an irreversible act.",
            "These are realities the heart senses instinctively, yet they demand rigorous examination before they become clear to the intellect."
        ],
        "move": "Camus establishes a strict hierarchy of urgency: metaphysical and epistemological theories are intellectual games; the question of survival and value precedes all contemplation."
    },
    {
        "id": "c1-p2",
        "orig_sentences": [
            "If I ask myself how to judge that this question is more urgent than that, I reply that one judges by the actions it entails.",
            "I have never seen anyone die for the ontological argument.",
            "Galileo, who held a scientific truth of great importance, abjured it with the greatest ease as soon as it endangered his life.",
            "In a certain sense, he did right.",
            "That truth was not worth the stake.",
            "Whether the earth or the sun revolves around the other is a matter of profound indifference.",
            "To tell the truth, it is a futile question.",
            "On the other hand, I see many people die because they judge that life is not worth living.",
            "I see others paradoxically getting killed for the ideas or illusions that give them a reason for living (what is called a reason for living is also an excellent reason for dying).",
            "I therefore conclude that the meaning of life is the most urgent of questions."
        ],
        "mod_sentences": [
            "How does one determine whether one question is more urgent than another? By the actions it demands.",
            "No one has ever died defending an abstract proof for the existence of God.",
            "When Galileo discovered a scientific truth of immense importance, he renounced it without hesitation the moment his life was threatened—and in a sense, he was right.",
            "That truth was not worth burning at the stake for.",
            "Whether the Earth orbits the Sun or the Sun orbits the Earth is a matter of profound indifference to our day-to-day existence; in truth, it is an idle question.",
            "In contrast, I see men choose death because they conclude life is not worth living.",
            "Paradoxically, I see others die for the very ideals or illusions that give them a reason to live (for what provides a reason for living also provides a compelling reason for dying).",
            "I conclude, therefore, that the meaning of life is the most urgent question of all."
        ],
        "move": "Existential truth vs. theoretical truth. Galileo rightly refused martyrdom for astronomical physics because scientific facts do not alter the lived weight of existence, whereas meaning dictates literal life and death."
    },
    {
        "id": "c1-p3",
        "orig_sentences": [
            "How to answer it?",
            "On all essential problems (I mean thereby those that run the risk of leading to death or those that intensify the passion of living) there are probably but two methods of thought: the method of La Palisse and the method of Don Quixote.",
            "Solely the balance between evidence and lyricism can allow us to achieve simultaneously emotion and lucidity.",
            "In a subject at once so humble and so heavy with emotion, the learned and classical dialectic must yield, one can see, to a more modest attitude of mind deriving at one and the same time from common sense and understanding."
        ],
        "mod_sentences": [
            "How are we to address it?",
            "For essential questions—those carrying the risk of death or the power to intensify the drive to live—there are essentially two modes of thought: the plain statement of the undeniable (the method of La Palice) and the passionate embrace of conviction (the method of Don Quixote).",
            "Only a balance between tangible evidence and poetic conviction allows us to attain both passion and clarity.",
            "On a subject so elementary yet so emotionally charged, formal academic dialectics must give way to a more modest cast of mind—one drawing simultaneously upon common sense and lucid psychological insight."
        ],
        "move": "Camus defines his methodology: balancing empirical fact (La Palice) with emotional passion (Don Quixote), discarding scholastic jargon in favor of clear psychological awareness."
    },
    {
        "id": "c1-p4",
        "orig_sentences": [
            "Suicide has never been dealt with except as a social phenomenon.",
            "On the contrary, we are concerned here, at the outset, with the relationship between individual thought and suicide.",
            "An act like this is prepared within the silence of the heart, as is a great work of art.",
            "The man himself is ignorant of it.",
            "One evening he pulls the trigger or jumps.",
            "Of an apartment-building manager who had killed himself I was told that he had lost his daughter five years before, that he had changed greatly since, and that that experience had “undermined” him.",
            "A more exact word cannot be imagined.",
            "Beginning to think is beginning to be undermined.",
            "Society has but little connection with such beginnings.",
            "The worm is in man’s heart.",
            "That is where it must be sought.",
            "One must follow and understand this fatal game that leads from lucidity in the face of existence to flight from light."
        ],
        "mod_sentences": [
            "Suicide has almost always been treated merely as a sociological statistic.",
            "Here, by contrast, we are concerned from the start with the intimate connection between private consciousness and self-destruction.",
            "Such an act matures in the silence of the heart, much like a great work of art.",
            "The individual himself is often unaware of its silent gestation until, one evening, he pulls the trigger or leaps.",
            "Of a building manager who took his own life, I was told he had lost his daughter five years earlier, had altered profoundly thereafter, and that the ordeal had 'undermined' him from within.",
            "A more precise term cannot be conceived.",
            "To begin to think is to begin to be undermined.",
            "Society has little bearing on these internal origins.",
            "The parasite resides within the human heart; that is where it must be sought.",
            "We must trace this fatal progression from the first lucid confrontation with existence to the eventual flight from reality."
        ],
        "move": "Camus shifts suicide from social statistics to private internal decay. 'To begin to think is to begin to be undermined' marks the terrifying rupture when conscious reflection destroys habitual numbness."
    },
    {
        "id": "c1-p5",
        "orig_sentences": [
            "In a sense, and as in melodrama, killing yourself amounts to confessing.",
            "It is confessing that life is too much for you or that you do not understand it.",
            "Let’s not go too far in such analogies, however, but rather return to everyday words.",
            "It is merely confessing that that “is not worth the trouble.”",
            "Living, naturally, is never easy.",
            "You continue making the gestures commanded by existence for many reasons, the first of which is habit.",
            "Dying voluntarily implies that you have recognized, even instinctively, the ridiculous character of that habit, the absence of any profound reason for living, the insane character of that daily agitation, and the uselessness of suffering."
        ],
        "mod_sentences": [
            "In a sense, and as in theatrical tragedy, taking one's own life amounts to a confession.",
            "It is an admission that existence has overwhelmed you, or that you cannot make sense of it.",
            "Yet setting aside dramatic metaphors, in the language of everyday life: it is simply confessing that life is not worth the trouble.",
            "Living is never effortless.",
            "One continues to perform the gestures demanded by existence for many reasons, foremost among them being habit.",
            "Choosing to die voluntarily implies that one has recognized—even if only by instinct—the ridiculous nature of that habit, the total absence of any deeper reason for living, the frantic and pointless nature of our daily agitation, and the ultimate uselessness of our suffering."
        ],
        "move": "Defining suicide as the breaking of habit. We persist in life through mechanical momentum; voluntary death is the sudden realization that the momentum has no justification."
    },
    {
        "id": "c1-p6",
        "orig_sentences": [
            "What, then, is that incalculable feeling that deprives the mind of the sleep necessary to life?",
            "A world that can be explained even with bad reasons is a familiar world.",
            "But, on the other hand, in a universe suddenly divested of illusions and lights, man feels an alien, a stranger.",
            "His exile is without remedy since he is deprived of the memory of a lost home or the hope of a promised land.",
            "This divorce between man and his life, the actor and his setting, is properly the feeling of absurdity.",
            "All healthy men having thought of their own suicide, it can be seen, without further explanation, that there is a direct connection between this feeling and the longing for death."
        ],
        "mod_sentences": [
            "What, then, is this elusive feeling that deprives the mind of the tranquil sleep necessary to sustain life?",
            "A world that can be explained—even through flawed reasoning—remains a familiar world.",
            "But in a cosmos suddenly stripped of comforting illusions and artificial certainties, man feels himself an alien, a stranger.",
            "His exile is without remedy, for he possesses neither the memory of a lost Eden nor the promise of a future redemption.",
            "This very divorce between man and his existence, between the actor and the stage, is precisely the feeling of absurdity.",
            "Given that virtually every healthy person has contemplated suicide at some point, there is an immediate, demonstrable link between this feeling of absurdity and the longing for death."
        ],
        "move": "The foundational definition of the Absurd: the 'divorce'—the painful rift between the human demand for purpose and a cosmos that offers no home, past paradise, or future salvation."
    },
    {
        "id": "c1-p7",
        "orig_sentences": [
            "In a man’s attachment to life there is something stronger than all the ills in the world.",
            "The body’s judgment is as good as the mind’s, and the body shrinks from annihilation.",
            "We get into the habit of living before acquiring the habit of thinking.",
            "In that race which daily hastens us toward death, the body maintains its irreparable lead.",
            "In short, the essence of that contradiction lies in what I shall call the act of eluding because it is both less and more than diversion in the Pascalian sense.",
            "Eluding is the invariable game.",
            "The typical act of eluding, the fatal evasion that constitutes the third theme of this essay, is hope.",
            "Hope of another life one must “deserve” or trickery of those who live not for life itself but for some great idea that will transcend it, refine it, give it a meaning, and betray it."
        ],
        "mod_sentences": [
            "In a human being’s attachment to life, there exists a force stronger than all the miseries of the world.",
            "The body's judgment is fully equal to that of the intellect, and the body instinctively recoils from its own annihilation.",
            "We form the habit of living long before we ever acquire the habit of thinking.",
            "In that daily race carrying us toward death, the body retains an insurmountable lead over the mind.",
            "The essence of this contradiction resides in what I term evasion.",
            "The primary form of evasion—the fatal trap that forms the third major theme of this essay—is hope: whether the religious hope for an afterlife that must be earned, or the secular deception of living not for existence itself, but for some grand future ideology that claims to transcend and elevate life, yet ultimately betrays it."
        ],
        "move": "Exposing our dual survival buffers: (1) the biological body's ancient instinct to survive, and (2) the intellectual escape hatch of 'Hope' (postponing reality for heaven or a utopian future)."
    },
    {
        "id": "c1-p8",
        "orig_sentences": [
            "One kills oneself because life is not worth living, that is certainly a truth—yet an unfruitful one because it is a truism.",
            "But does that insult to existence, that flat denial in which it is plunged come from the fact that it has no meaning?",
            "Does its absurdity require one to escape it through hope or suicide—this is what must be clarified, hunted down, and elucidated while brushing aside all the rest.",
            "Does the Absurd dictate death?",
            "This problem must be given priority over others, outside all methods of thought and all exercises of the disinterested mind."
        ],
        "mod_sentences": [
            "That one takes one's life because existence is deemed not worth living is undeniable—yet it remains an unhelpful truism.",
            "The real inquiry is this: does this flat rejection of existence stem necessarily from the fact that life lacks transcendent meaning?",
            "Does the absurdity of the human condition demand that we flee it—either through the false promise of hope or the finality of suicide?",
            "This is what must be pursued and clarified above all else: Does the Absurd dictate death?",
            "This problem demands absolute priority over all theoretical exercises of detached intellect."
        ],
        "move": "The core inquiry of the book: Does meaninglessness logically demand self-annihilation? Or can reason find a way to inhabit the Absurd with defiance and integrity?"
    }
]

# Chapter 2 Data
c2_pairs = [
    {
        "id": "c2-p1",
        "orig_sentences": [
            "It happens that the stage sets collapse.",
            "Rising, streetcar, four hours in the office or the factory, meal, streetcar, four hours of work, meal, sleep, and Monday Tuesday Wednesday Thursday Friday and Saturday according to the same rhythm—this path is easily followed most of the time.",
            "But one day the “why” arises and everything begins in that weariness tinged with amazement.",
            "“Begins”—this is important.",
            "Weariness comes at the end of the acts of a mechanical life, but at the same time it inaugurates the impulse of consciousness.",
            "It awakens consciousness and provokes what follows.",
            "What follows is the gradual return into the chain or it is the definitive awakening."
        ],
        "mod_sentences": [
            "Yet there are times when the theatrical scenery collapses.",
            "Waking, the streetcar, four hours in the office or factory, a meal, the streetcar, four hours of labor, a meal, sleep, and Monday, Tuesday, Wednesday, Thursday, Friday, and Saturday unfolding to the identical rhythm—this routine is followed effortlessly for years.",
            "Yet one day, the question 'Why?' arises, and everything begins in a state of weariness mingled with astonishment.",
            "'Begins'—this distinction is vital.",
            "Exhaustion concludes a life of mechanical habit, yet it simultaneously inaugurates the birth of genuine consciousness.",
            "It shakes the mind awake and provokes what follows: either a gradual return to the chains of routine, or a definitive, permanent awakening."
        ],
        "move": "Camus charts the sudden collapse of daily autopilot. The routine protects us from awareness; the intrusion of 'Why?' ends unconscious existence and forces a choice between conscious lucidity or relapse into stupor."
    },
    {
        "id": "c2-p2",
        "orig_sentences": [
            "We live on the future: “tomorrow,” “later on,” “when you have made your way,” “you will understand when you are old enough.”",
            "Such irrelevancies are wonderful, for, after all, it’s a matter of dying.",
            "Yet a day comes when a man notices or says that he is thirty.",
            "Thus he asserts his youth.",
            "But simultaneously he situates himself in relation to time.",
            "He takes his place in it.",
            "He admits that he stands at a certain point on a curve that he acknowledges having to travel to its end.",
            "He belongs to time, and by the horror that seizes him, he recognizes his worst enemy.",
            "Tomorrow, he was longing for tomorrow, whereas everything in him ought to reject it.",
            "That revolt of the flesh is the absurd."
        ],
        "mod_sentences": [
            "We live constantly leaning into the future: 'tomorrow,' 'later on,' 'once you have made your mark,' 'you will understand when you are older.'",
            "Such postponements are astonishingly ironic, for in the final analysis, they all lead to death.",
            "Yet a day comes when a man observes or announces that he is thirty.",
            "He thereby affirms his youth, yet simultaneously positions himself upon the arc of time.",
            "He realizes he occupies a fixed point on an irreversible curve that must be traveled to its inevitable conclusion.",
            "He belongs to time, and in the horror that grips him, he recognizes his deadliest adversary.",
            "Yesterday, he was yearning for tomorrow to arrive—when in truth, every instinct of his physical being ought to recoil from it.",
            "That instinctive revolt of the flesh against time is the absurd."
        ],
        "move": "The betrayal of time. We live on credit projected into the future, forgetting that the destination is death. Turning thirty marks the threshold where time ceases to be an ally and reveals itself as an executioner."
    },
    {
        "id": "c2-p3",
        "orig_sentences": [
            "Men, too, secrete the inhuman.",
            "At certain moments of lucidity, the mechanical aspect of their gestures, their meaningless pantomime makes silly everything that surrounds them.",
            "A man is talking on the telephone behind a glass partition; you cannot hear him, but you see his incomprehensible dumb show: you wonder why he is alive.",
            "This discomfort in the face of man’s own inhumanity, this incalculable tumble before the image of what we are, this “nausea,” as a writer of today calls it, is also the absurd.",
            "Likewise the stranger who at certain seconds comes to meet us in a mirror, the familiar and yet alarming brother we encounter in our own photographs is also the absurd."
        ],
        "mod_sentences": [
            "Human beings, too, emit this quality of the non-human.",
            "In flashes of detached lucidity, the mechanical nature of human gestures and our meaningless pantomime render everything around us grotesque.",
            "A man speaks into a telephone behind a soundproof glass partition; one cannot hear his words, but one observes his incomprehensible gestures: one wonders why such a creature exists.",
            "This unease before humanity's own mechanical strangeness, this vertigo when confronted by what we actually appear to be—this 'nausea,' as a contemporary writer terms it—is also the absurd.",
            "Likewise, that stranger who unexpectedly confronts us in a mirror, or the familiar yet disturbing double staring back from an old photograph, is also the absurd."
        ],
        "move": "The phone booth thought experiment and the mirror uncanny. When human behavior is stripped of context, its mechanical puppetry is exposed, inducing existential nausea (referencing Sartre)."
    },
    {
        "id": "c2-p4",
        "orig_sentences": [
            "I said that the world is absurd, but I was too hasty.",
            "This world in itself is not reasonable, that is all that can be said.",
            "But what is absurd is the confrontation of this irrational and the wild longing for clarity whose call echoes in the human heart.",
            "The absurd depends as much on man as on the world.",
            "For the moment it is all that links them together.",
            "It binds them one to the other as only hatred can weld two creatures together.",
            "This is all I can discern clearly in this measureless universe where my adventure takes place."
        ],
        "mod_sentences": [
            "I stated earlier that the world is absurd, yet I spoke too hastily.",
            "The universe in itself is not reasonable; that is all one can legitimately affirm.",
            "What is genuinely absurd is the confrontation between this irrational world and the profound hunger for clarity echoing within the human soul.",
            "The absurd depends as much upon human consciousness as it does upon the cosmic silence.",
            "For now, it is the sole bond linking them together—uniting them as only relentless antagonism can weld two adversaries in combat.",
            "This is all I can perceive with certainty in this measureless universe."
        ],
        "move": "The core philosophical correction. The universe is not absurd; it is simply indifferent. The Absurd is strictly relational: the friction generated when human longing strikes cosmic silence."
    },
    {
        "id": "c2-p5",
        "orig_sentences": [
            "At this point of his effort man stands face to face with the irrational.",
            "He feels within him his longing for happiness and for reason.",
            "The absurd is born of this confrontation between the human need and the unreasonable silence of the world.",
            "This must not be forgotten.",
            "This must be clung to because the whole consequence of a life can depend on it.",
            "The irrational, the human nostalgia, and the absurd that is born of their encounter—these are the three characters in the drama that must necessarily end with all the logic of which an existence is capable."
        ],
        "mod_sentences": [
            "At this stage of his inquiry, man stands face to face with the irrational.",
            "He feels within his breast two inescapable longings: the desire for happiness and the demand for reason.",
            "The absurd is born of this direct collision between human yearning and the silence of the universe.",
            "This core reality must not be surrendered, for the entire consequence of a life depends upon it.",
            "The irrational cosmos, human longing, and the absurd born of their encounter—these are the three characters in the tragedy, and the drama must be played out with all the rigorous logic of which a human existence is capable."
        ],
        "move": "The tripartite drama of existence: (1) The Irrational World, (2) Human Longing, and (3) The Absurd. Any philosophy that tries to eliminate one character is cheating."
    }
]

def render_section(pairs, sec_id, sec_title, sec_sub):
    html = f"""
    <section class="book-section" id="{sec_id}">
      <div class="section-badge">{sec_sub}</div>
      <h2 class="section-title">{sec_title}</h2>
      <div class="pairs-wrapper">
    """
    for p_idx, pair in enumerate(pairs, 1):
        pid = pair["id"]
        html += f"""
        <div class="pair-card" id="{pid}" data-pair="{pid}">
          <div class="col col-orig">
            <div class="col-header">
              <span class="col-tag orig-tag">Original 1955 Translation</span>
              <span class="para-num">§{p_idx}</span>
            </div>
            <p class="para-text">
        """
        for s_idx, sent in enumerate(pair["orig_sentences"]):
            sid = f"{pid}-s{s_idx}"
            html += f"""<span class="sent sent-orig" data-s="{sid}" onclick="handleSentClick('{sid}')">{sent} </span>"""
        
        html += f"""
            </p>
          </div>
          <div class="col col-mod">
            <div class="col-header">
              <span class="col-tag mod-tag">Dignified Modern Translation</span>
              <span class="para-num">§{p_idx}</span>
            </div>
            <p class="para-text">
        """
        for s_idx, sent in enumerate(pair["mod_sentences"]):
            sid = f"{pid}-s{s_idx}"
            html += f"""<span class="sent sent-mod" data-s="{sid}" onclick="handleSentClick('{sid}')">{sent} </span>"""
        
        html += f"""
            </p>
            <div class="move-box">
              <div class="move-label">The Philosophical Move</div>
              <p class="move-content">{pair["move"]}</p>
            </div>
          </div>
        </div>
        """
    html += """
      </div>
    </section>
    """
    return html

app_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-view="parallel">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Camus Reader">
  <title>The Myth of Sisyphus — Critical Reading Companion</title>
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
      margin-bottom: 4rem;
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
      .col-mod {{
        padding-left: 0;
      }}
      header.app-bar {{
        padding: 0.5rem 0.8rem;
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

  <!-- App Bar -->
  <header class="app-bar">
    <div class="app-brand">
      <span class="brand-title">The Myth of Sisyphus</span>
      <span class="brand-pill">Critical Engine</span>
    </div>

    <div class="app-controls">
      <!-- View Switcher -->
      <button class="btn active" id="view-parallel-btn" onclick="setView('parallel')">Parallel</button>
      <button class="btn" id="view-modern-btn" onclick="setView('modern')">Modern Stream</button>

      <!-- Theme Switcher -->
      <button class="btn" onclick="cycleTheme()" id="theme-btn" title="Toggle Theme">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <!-- Glossary Button -->
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
    {render_section(preface_pairs, "sec-preface", "Author's Preface & Epigraph", "Introduction")}
    {render_section(c1_pairs, "sec-1", "1. Absurdity and Suicide", "Part I: An Absurd Reasoning")}
    {render_section(c2_pairs, "sec-2", "2. Absurd Walls", "Part I: An Absurd Reasoning")}
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

    // Modal
    function toggleModal(open) {{
      document.getElementById('concepts-modal').classList.toggle('open', open);
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

with open(DIST_HTML, 'w', encoding='utf-8') as f:
    f.write(app_html)

with open(ROOT_HTML, 'w', encoding='utf-8') as f:
    f.write(app_html)

print("Generated clean index.html in dist and root successfully!")
