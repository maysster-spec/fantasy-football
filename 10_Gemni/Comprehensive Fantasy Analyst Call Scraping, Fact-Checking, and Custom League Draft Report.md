# **2026 Fantasy Football Draft Analysis & Market Consensus Synthesis**

## **League Structural Dynamics & Strategic Scoring Impacts**

Optimizing draft strategy for a 12-team ESPN keeper league requires a precise mathematical alignment between roster rules, custom scoring settings, and draft position. Roster parameters mandate starting 1 QB, 2 RBs, 2 WRs, 1 TE, 1 FLEX (RB/WR/TE), 1 D/ST, and 1 K. The draft pick allocation follows position 8 across a 14-round snake structure: Pick 8 (Round 1), Pick 17 (Round 2), Pick 32 (Round 3), Pick 41 (Round 4), Pick 56 (Round 5), Pick 65 (Round 6), Pick 80 (Round 7), Pick 89 (Round 8), Pick 104 (Round 9), Pick 113 (Round 10), Pick 128 (Round 11), Pick 137 (Round 12), Pick 152 (Round 13), and Pick 161 (Round 14\)1.  
Retaining wide receiver George Pickens as a designated keeper (drafted Round 5 or later and held all season, Bye 14\) provides structural leverage1. Anchoring an upper-tier WR2/WR1 option at zero current-year draft capital cost diminishes the necessity of over-drafting wide receivers in the initial four rounds1. This structural advantage permits aggressive accumulation of elite running backs, premier tight ends, or high-volume quarterbacks at picks 8, 17, 32, and 411.

| Scoring Parameter | Standard Baseline | Custom League Setting | Quantitative Valuation & Positional Impact |
| :---- | :---- | :---- | :---- |
| **Passing Touchdowns** | 4 Points per TD | **6 Points per TD** | Flattens the rushing-to-passing TD value ratio from 2.5:1 down to 1:1. Significantly boosts high-volume pocket passers (e.g., Joe Burrow, Drake Maye) relative to pure rushing QBs1. Elevates QB draft priority at Picks 32 and 411. |
| **Reception Scoring** | 1.0 Full PPR | **0.5 Half PPR** | Reduces point value of satellite pass-catching backs by 1.0 to 1.5 PPG1. Increases relative weighting of early-down touch volume, goal-line carries, yards per route run (YPRR), and depth of target (aDOT)2. |
| **Keeper Allocation** | Standard Draft | **George Pickens (WR, Bye 14\)** | Locks in a starting WR slot without utilizing Rounds 1–4 capital1. Allows flexible positional pivoting toward elite tight ends (Brock Bowers/Trey McBride) or heavy backfield volume (Chase Brown) at Picks 32 and 411. |

Under standard 4-point passing TD formats, dual-threat quarterbacks gain a disproportionate advantage because rushing touchdowns yield 6 points compared to 4 for passing touchdowns1. In a 6-point passing TD format, high-volume passers projecting for 30+ touchdowns receive a baseline increase of 60+ fantasy points over a 17-game season, elevating tier-one and tier-two signal-callers into Round 3 and Round 4 consideration1.  
Simultaneously, 0.5 PPR scoring alters pass-catcher dynamics relative to full PPR formats1. High-frequency, low-yardage slot receivers and third-down backs experience a reduction in baseline floor, whereas high-efficiency, explosive downfield target-earners and early-down bell-cows absorb a relative valuation surge2.

## **Red-Teaming Audit & Fact-Checking of Baseline CSV Data**

A rigorous audit of the cataloged analyst call dataset (raw-analyst-calls-v2.csv merged with external analyst content) reveals several data anomalies, legacy artifacts, phonetic transcription errors, and roster movement shifts that require correction prior to draft execution1.

| Target Player | Raw CSV / Source Data Issue | Fact-Checking Audit Finding | Tactical & Positional Correction |
| :---- | :---- | :---- | :---- |
| **Ricky Pearsall** | Listed with date 2025-08-19 | Legacy 2025 entry included in baseline dataset1. | Re-evaluate purely as a 2026 sophomore route-runner; market ADP resides in Rounds 8–101. |
| **Cam Skattebo** | Transcribed as "Cam Scataboo" | Phonetic audio transcription error for Arizona State RB prospect1. | Standardize spelling; analysts note coaching staff hesitations regarding a true feature workhorse role1. |
| **Ladd McConkey** | Transcribed as "Lad Maki" | Phonetic audio transcription error1. | Standardize spelling; primary target-earner in Chargers passing attack, prime target at Picks 32–411. |
| **Dontayvion Wicks** | Transcribed as "Davian Wicks" | Phonetic audio transcription error1. | Standardize spelling; top-15 route efficiency metrics make him a priority pick at Picks 89–1041. |
| **Stefon Diggs** | Unassigned/legacy team context | Signed with Washington Commanders2. | Evaluated as veteran target volume play alongside second-year QB development2. |
| **Luke Musgrave** | Active status in older calls | Moved to reserve/PUP list with a neck injury6. | Directly elevates Tucker Kraft to clear starting TE role in Green Bay1. |
| **Zach Charbonnet** | Active status in older calls | Placed on reserve/PUP list to open the season6. | Solidifies Kenneth Walker III's early-season volume floor2. |
| **Quinn Analyst Calls** | Dated 2024 Sleeper lists | Legacy 2024 dataset entries2. | Cross-reference against 2026 depth charts before relying on draft ADP2. |

The dataset contains temporal anomalies, specifically analyst entries from August 2025 evaluating Ricky Pearsall, Marvin Mims Jr., Rome Odunze, and Tucker Kraft, alongside 2024 sleeper lists from sources such as Quinn1. While core talent evaluations—such as Dontayvion Wicks' route-running efficiency or Rome Odunze's ball-tracking traits—remain analytically sound, their market ADPs must be dynamically updated to reflect 2026 conditions1.  
Phonetic transcription errors in raw media logs require standardization: "Cam Scataboo" represents Cam Skattebo; "Lad Maki" represents Ladd McConkey; "Coulson Love" / "Colston Lovelin" represents Colston Loveland; "Davian Wicks" represents Dontayvion Wicks; "Ben cinate" represents Ben Sinnott; and "Gibbs Bejon" refers to Jahmyr Gibbs and Bijan Robinson1.  
Furthermore, player movement cross-checks confirm that Stefon Diggs signed with Washington, establishing veteran target-earning upside2; Chris Rodriguez Jr. has absorbed goal-line responsibilities in Washington following backfield shifts2; and Curtis Samuel operates in Joe Brady's Buffalo offense as a manufactured-touch weapon for Josh Allen1.

## **Unified Master Analyst Calls & Player Evaluation Database**

The table below unifies all cataloged analyst calls from the raw dataset and expanded industry analyst sources (Fantasy Footballers, Justin Boone, Matt Harmon, FantasyLife, JJ Zachariason, Ben Gretch, Chris Raybon, Rob Waziak) into a standardized format1.

| Player | Position | Team | Analyst Call & Direction | Market Stance vs. ADP | Target Draft Capital / Round | Scoring & Format Impact (0.5 PPR / 6-pt TD) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Garrett Wilson** | WR | NYJ | Paired with elite QB play; possesses overall WR1 ceiling1. | UP (High Conviction) | Picks 17–32 (Rounds 2–3) | Neutral in 0.5 PPR; high TD ceiling boosts absolute value1. |
| **Jaylen Waddle** | WR | MIA | Most mispriced receiver in fantasy; elite separation metrics1. | UP (Strong Buy) | Picks 17–32 (Rounds 2–3) | Slightly lowered by 0.5 PPR but offset by big-play YPC1. |
| **Ladd McConkey** | WR | LAC | Go-to option for Justin Herbert; projected for 120+ targets1. | UP (Breakout) | Picks 32–41 (Rounds 3–4) | High target volume maintains elite status in 0.5 PPR1. |
| **Rome Odunze** | WR | CHI | Generational ball skills; set up for sophomore leap1. | UP (Breakout) | Picks 32–41 (Rounds 3–4) | High depth of target (aDOT) makes him more valuable in 0.5 PPR1. |
| **Chase Brown** | RB | CIN | Workhorse potential in Cincinnati; clear RB1 volume path2. | UP (Strong Target) | Picks 32–41 (Rounds 3–4) | Goal-line & early-down work enhances value in 0.5 PPR2. |
| **Javonte Williams** | RB | DEN | Two years post-ACL; offensive environment greatly improved1. | NEUTRAL (Split Analyst) | Picks 41–56 (Rounds 4–5) | 0.5 PPR rewards his tackle-breaking and goal-line profile2. |
| **Brock Bowers** | TE | LV | Elite athletic profile; functions as primary wide receiver2. | UP (Strong Target) | Picks 17–32 (Rounds 2–3) | Positional advantage remains dominant in 0.5 PPR2. |
| **Trey McBride** | TE | ARI | Core target-earner; staple Round 3 target2. | UP (Target) | Picks 32–41 (Rounds 3–4) | Volume-based TE1 value holds firm in 0.5 PPR2. |
| **Drake Maye** | QB | NE | Premier value among rushing QBs with passing volume2. | UP (Value Target) | Picks 41–89 (Rounds 4–8) | **Significant UPGRADE** in 6-pt passing TD format2. |
| **Jonathon Brooks** | RB | CAR | Elite athletic ceiling; midseason workhorse takeover expected1. | UP (Sleeper/Breakout) | Picks 65–89 (Rounds 6–8) | Bell-cow profile fits 0.5 PPR structural build1. |
| **Rico Dowdle** | RB | DAL | Clearest path to early-down and goal-line touches in Dallas2. | UP (Sleeper Target) | Picks 80–89 (Rounds 7–8) | Goal-line role drives value over satellite backs2. |
| **Josh Downs** | WR | IND | Elite separation metrics; dominant target share in slot1. | UP (Value Sleeper) | Picks 89–104 (Rounds 8–9) | Slight downgrade in 0.5 PPR vs full PPR, but volume wins1. |
| **Dontayvion Wicks** | WR | GB | Top-15 route efficiency metrics across the board1. | UP (Priority Target) | Picks 89–104 (Rounds 8–9) | YPRR and TD efficiency shine in 0.5 PPR1. |
| **Curtis Samuel** | WR | BUF | Manufactured touch role in Josh Allen offense1. | UP (Late Value) | Picks 104–128 (Rounds 9–11) | Rushing touches add floor in 0.5 PPR leagues1. |
| **Parker Washington** | WR | JAC | Locked down slot job; high early target volume expected1. | UP (Deep Sleeper) | Picks 113–137 (Rounds 10–12) | Low cost renders him zero-risk depth play1. |
| **Stefon Diggs** | WR | WAS | Veteran savvy and target volume upside in Washington2. | UP (Value Target) | Picks 104–128 (Rounds 9–11) | Good WR3/FLEX target in 0.5 PPR builds2. |
| **Tucker Kraft** | TE | GB | Elite run-after-catch metrics; discounted post-injury1. | NEUTRAL (Split Analyst) | Picks 113–137 (Rounds 10–12) | RAC efficiency suits 0.5 PPR scoring; boosted by Musgrave PUP1. |
| **Pat Freiermuth** | TE | PIT | Reliable low-end TE1 option at minimal draft cost2. | UP (Late Target) | Picks 128–137 (Rounds 11–12) | Red-zone target share supports 0.5 PPR floor2. |
| **Chigoziem Okonkwo** | TE | TEN | Dynamic athletic profile; secondary target in Tennessee1. | UP (Sleeper) | Picks 128–137 (Rounds 11–12) | High YPC potential aids 0.5 PPR viability1. |
| **Malik Willis** | QB | MIA | Konami Code rushing upside in Miami scheme environment1. | UP (Late Dart) | Picks 137+ (Round 12+) | Rushing floor retains value, but 6-pt TD aids passers1. |
| **Bucky Irving** | RB | TB | Overvalued draft price; ceiling questioned post-injury2. | DOWN (Fade/Bust) | Avoid at ADP | Efficiency drops reduce 0.5 PPR utility2. |
| **Cam Skattebo** | RB | NYG | Lack of team trust for feature workhorse workload1. | DOWN (Fade/Bust) | Avoid at ADP | Touchdown-dependent back lacking receiving volume1. |
| **DJ Moore** | WR | CHI | Heavy target competition from Odunze and Allen1. | DOWN (Overvalued) | Avoid at ADP | Target share dilution hurts 0.5 PPR ceiling1. |
| **Jordan Addison** | WR | MIN | Market fear overblown, but secondary WR status caps ceiling1. | NEUTRAL | Picks 80–89 (Rounds 7–8) | Big-play capability holds value in 0.5 PPR1. |
| **Rashee Rice** | WR | KC | Perception outpaces actual fantasy role profile1. | DOWN (Market Fade) | Avoid at ADP | High reception dependency hurts in 0.5 PPR1. |
| **Sam LaPorta** | TE | DET | Market price assumes health; back injury adjustment needed2. | DOWN (Overvalued) | Avoid at Round 3–4 ADP | High draft cost unaligned with 0.5 PPR TE tiers2. |

## **Strategic Targets for Key Draft Picks (Picks 32, 41, 89, and 104–137)**

Executing an optimal draft sequence requires analyzing realistic player availability at the manager's designated pick slots: Pick 32 (Round 3), Pick 41 (Round 4), Pick 89 (Round 8), and Picks 104–137 (Rounds 9 through 12\)1.

### **Pick 32 (Round 3, Pick 8\)**

* **Brock Bowers (TE, LV)**: Retaining George Pickens as a WR keeper frees Pick 32 to target elite tight end positioning1. Analyst consensus highlights Bowers as a player who functions as an alpha wide receiver, offering positional leverage in 0.5 PPR scoring where tight end target concentration dominates2.  
* **Ladd McConkey (WR, LAC)**: Matt Harmon's *Reception Perception* analysis establishes McConkey as Justin Herbert's clear primary target, projecting over 120 targets1. His high route separation metrics ensure consistent target volume that thrives in 0.5 PPR formats1.  
* **Jaylen Waddle (WR, MIA)**: Identified by analysts as one of the most mispriced wide receivers in fantasy football, Waddle's explosive yards-per-catch ability offsets half-PPR point reductions and provides elite WR1 upside if available at Pick 321.  
* **Trey McBride (TE, ARI)**: Kev Mahserejian and Sean Koerner emphasize McBride as a core target-earner in Arizona's offense, presenting a structural alternative if Bowers is selected earlier in Round 32.

### **Pick 41 (Round 4, Pick 5\)**

* **Chase Brown (RB, CIN)**: Pat Fitzmaurice and Derek Brown emphasize Brown's workhorse potential in Cincinnati, projecting him to absorb Joe Mixon's historical volume2. In 0.5 PPR, his early-down running strength combined with goal-line opportunity makes him a premier RB selection2.  
* **Rome Odunze (WR, CHI)**: Jason Moore and Rich Hribar evaluate Odunze as a breakout wideout possessing elite ball skills1. Because 0.5 PPR favors downfield efficiency and touchdown conversion over short dump-offs, Odunze's profile excels at Pick 411.  
* **Drake Maye (QB, NE)**: Under 6-point passing touchdown rules, Maye's combination of rushing floor and downfield passing volume makes him a target at Pick 41, unlocking elite QB scoring without requiring Round 1 or 2 capital2.

### **Pick 89 (Round 8, Pick 5\)**

* **Jonathon Brooks (RB, CAR)**: Mike Wright and industry updates project Brooks to completely dominate Carolina's backfield once fully integrated, presenting bell-cow potential at an RB3 draft price1.  
* **Dontayvion Wicks (WR, GB)**: JJ Zachariason and Matt Harmon cite Wicks' top-15 efficiency metrics across all major separation categories, making him a priority target at Pick 891.  
* **Rico Dowdle (RB, DAL)**: Analysts identify Dowdle as possessing the clearest path to goal-line and early-down work in Dallas, offering weekly starting utility in 0.5 PPR formats2.

### **Picks 104–137 (Rounds 9 through 12\)**

* **Curtis Samuel (WR, BUF \- Pick 104/113)**: Highlighted by JJ Zachariason and Pierre Camus, Samuel operates in Joe Brady's scheme attached to Josh Allen, offering manufactured touches and rushing baseline points1.  
* **Parker Washington (WR, JAC \- Pick 113/128)**: Andy Holloway notes Washington has secured Jacksonville's primary slot role, providing immediate target volume at zero cost1.  
* **Jalen Coker (WR, CAR \- Pick 128/137)**: Matt Harmon targets Coker as an underrated separator capable of outperforming higher-drafted rookies in Carolina1.  
* **Tucker Kraft (TE, GB \- Pick 113/128)**: Jason Moore identifies Kraft's elite run-after-catch metrics, presenting starting tight end upside at a deep draft discount1.  
* **Pat Freiermuth (TE, PIT \- Pick 128/137)**: Andrew Erickson and Pat Fitzmaurice highlight Freiermuth as a late-round tight end capable of delivering steady TE1 red-zone production2.  
* **Chigoziem Okonkwo (TE, TEN \- Pick 128/137)**: Justin Boone notes Okonkwo's athletic profile, positioning him as an ideal secondary target option in late rounds1.

## **Late-August 2026 Breaking News & Depth Chart Re-alignments**

Preseason injury scares regarding Ja'Marr Chase (knee hyperextension) and Kenneth Walker III have been resolved, with both players cleared for full participation8. Chase confirmed complete health, maintaining his status as a top-three overall selection8. Concurrently, Ashton Jeanty underwent a late-August injury evaluation; medical tests returned negative, though his high draft cost requires careful monitoring during draft execution9. Puka Nacua officially resumed full practice participation in late August, removing injury risk flags from his early-round projection6.  
Significant roster transactions have altered late-round target dynamics6. Seattle placed running back Zach Charbonnet on the reserve/PUP list to open the regular season, removing immediate backfield competition for Kenneth Walker III6. Green Bay transferred tight end Luke Musgrave to the reserve/PUP list due to a persistent neck issue, clearing the path for Tucker Kraft to assume starter snaps and route participation1. Additionally, San Francisco placed wide receiver Christian Kirk on injured reserve with a designation to return due to a calf strain, while wide receiver Jordyn Tyson and running back Adam Randall were placed on IR6.  
Depth chart role confirmations provide actionable late-round targets1. Jacksonville coaching staff logs confirm Parker Washington has secured the primary slot wide receiver role in three-wide sets, establishing chemistry with Trevor Lawrence1. In Carolina, Jonathon Brooks made his preseason debut, prompting coaching updates that outline a structured workload progression toward a full backfield takeover by midseason1. In Washington, Stefon Diggs signed a veteran deal to bolster the receiving corps, while Chris Rodriguez Jr. earned goal-line duties following backfield shifts2. Meanwhile, rookie Tyrone Tracy Jr. officially secured his spot on the initial 53-man roster, establishing himself as a late-round handcuff target6.

## **Analytical Mechanisms Driving Market Disagreements**

Analyst divergence from consensus market ADP stems from specific underlying analytical mechanisms rather than subjective preference1.

| Target Player | Consensus Market ADP | Analyst Stance & Direction | Primary Analytical Mechanism Driving Disagreement |
| :---- | :---- | :---- | :---- |
| **Dontayvion Wicks** | Late-round after-thought | Strong Target / Priority Pick | Top-15 target share per route run (TPRR) and route efficiency metrics predict a year-two breakout regardless of Green Bay's receiver depth1. |
| **Ladd McConkey** | Mid-round WR3 price | Breakout / High Target | *Reception Perception* metrics show a 70%+ success rate versus man coverage; Chargers offensive environment projects 120+ targets1. |
| **Javonte Williams** | Suppressed by injury history | Target / Breakout | Two-year post-ACL recovery curve aligns with tackle-breaking normalization; improved offensive environment elevates baseline efficiency1. |
| **Bucky Irving** | Elevated Round 3/4 price | Fade / Bust | Low yards after contact per attempt and limited goal-line touch share restrict upside, making his draft price overly fragile2. |
| **Cam Skattebo** | Mid-round RB price | Fade / Bust | Internal touch distributions indicate coaching staff hesitations regarding a true feature workhorse role1. |
| **Drake Maye** | Mid-to-late round QB | Priority Upgrade | 6-point passing TD league scoring elevates his combined downfield passing efficiency and rushing floor into elite tiering2. |

Matt Harmon's *Reception Perception* data isolates route separation rates against man and zone coverage1. Analysts use this data to aggressively target Dontayvion Wicks and Ladd McConkey ahead of market consensus1. Wicks demonstrates top-15 target earning efficiency per route run, indicating that playing time expansion will trigger a fantasy breakout regardless of Green Bay's crowded receiver room1.  
In backfields, Evan Silva and Pat Fitzmaurice disagree with the market fade on Javonte Williams1. Market ADP penalizes Williams based on post-surgery inefficiency; however, historical recovery curves show that tackle-breaking metrics and explosive run rates normalize during year two post-ACL reconstruction2. Conversely, analysts such as Adam Levitan and John Daigle fade Bucky Irving and Cam Skattebo based on touch quality metrics2. Irving's market price assumes three-down work, yet his low yards after contact and team usage patterns suggest a limited ceiling2. Skattebo's downgrade stems from coaching staff touch distributions that favor a committee rather than a true bell-cow workload1.  
For quarterbacks, JJ Zachariason isolates rushing attempt probability inside the red zone (the "Konami Code" effect)1. Dual-threat options like Drake Maye and Malik Willis generate high baseline fantasy points per dropback, creating significant draft value when coupled with 6-point passing touchdown league rules1.

## **Pick-Altering Tactical Flags & Draft Execution Protocol**

| Draft Phase / Slot | Actionable Pick Flag | Tactical Pivot Rationale & Roster Strategy |
| :---- | :---- | :---- |
| **Pick 32 Execution** | **TE Priority Flag** | If Brock Bowers or Trey McBride is available, draft immediately2. Securing elite tight end positional leverage in 0.5 PPR outweighs WR demand due to the Pickens keeper anchor1. |
| **Pick 41 Execution** | **6-Pt QB Pivot Flag** | If top passing quarterbacks (e.g., Drake Maye) fall to Pick 41, prioritize QB2. 6-point passing TDs elevate top-tier signal-callers over mid-tier RB committees1. |
| **Picks 56 & 65 Transition** | **RB Workhorse Flag** | Target early-down bell-cows (e.g., Chase Brown, Javonte Williams) over satellite pass-catchers1. 0.5 PPR scoring heavily favors goal-line touch share1. |
| **Pick 89 Execution** | **Efficiency Sleeper Flag** | Prioritize Jonathon Brooks or Dontayvion Wicks1. High route efficiency and second-half workload projections yield league-winning potential at an RB3/WR4 cost1. |
| **Picks 104–137 Execution** | **Late Target Depth Flag** | Draft Curtis Samuel, Parker Washington, and Tucker Kraft1. Captures manufactured touches, starting slot volume, and post-PUP tight end targets at zero risk1. |

The combination of holding George Pickens as a low-cost WR keeper, navigating 0.5 PPR scoring, and capitalizing on 6-point passing touchdowns provides a clear competitive edge1. By adhering to analyst separation metrics, avoiding overvalued committee backs, and executing high-conviction targets across picks 32, 41, 89, and 104–137, the roster can be built to optimize both floor and championship ceiling1.

#### **Works cited**

> 1. favorite-analysts-calls-2026.csv  
> 2. raw-analyst-calls-v2.csv  
> 3. 2026 Fantasy Football Cheat Sheet | Positional Rankings, [https://www.fantasypros.com/nfl/cheatsheets/](https://www.fantasypros.com/nfl/cheatsheets/)  
> 4. Raybon: Favorite 2025 Fantasy Football Sleepers | FantasyLabs, [https://www.fantasylabs.com/articles/raybon-favorite-2025-fantasy-football-sleepers/](https://www.fantasylabs.com/articles/raybon-favorite-2025-fantasy-football-sleepers/)  
> 5. Fantasy Football Half PPR Flex Rankings: Waz vs. ADP, [https://www.fantasylife.com/articles/fantasy/fantasy-football-half-ppr-flex-rankings-vs-adp](https://www.fantasylife.com/articles/fantasy/fantasy-football-half-ppr-flex-rankings-vs-adp)  
> 6. \#1 Fantasy Football Podcast \- Fantasy Footballers Podcast, [https://www.thefantasyfootballers.com/](https://www.thefantasyfootballers.com/)  
> 7. Get Ready for 2026 Fantasy Football with FantasyLabs, [https://www.actionnetwork.com/fantasy-football/get-ready-for-2026-fantasy-football-with-fantasylabs](https://www.actionnetwork.com/fantasy-football/get-ready-for-2026-fantasy-football-with-fantasylabs)  
> 8. The 2026 “My Guys” Episode\! \- Fantasy Football Podcast for 8/26, [https://podcasts.happyscribe.com/fantasy-footballers-fantasy-football-podcast/26-9d82e84d-b301-4e58-ada4-e00c3c213772](https://podcasts.happyscribe.com/fantasy-footballers-fantasy-football-podcast/26-9d82e84d-b301-4e58-ada4-e00c3c213772)  
> 9. Fantasy Football Podcast Transcripts, [https://podcasts.musixmatch.com/podcast/fantasy-footballers-fantasy-football-podcast-01h1ngdz40mdn88ctzfd22ff5h](https://podcasts.musixmatch.com/podcast/fantasy-footballers-fantasy-football-podcast-01h1ngdz40mdn88ctzfd22ff5h)  
> 10. PlayerProfiler Fantasy Football Podcast Network, [https://podcasttranscript.ai/show/fantasy-footballers-fantasy-football-podcast](https://podcasttranscript.ai/show/fantasy-footballers-fantasy-football-podcast)  
> 11. Reception Perception: Home Page, [https://receptionperception.com/](https://receptionperception.com/)