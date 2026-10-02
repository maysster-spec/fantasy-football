Claude Fable 5.1 is Anthropic’s frontier, “Mythos-class” model engineered for long-running autonomous workflows, full-codebase software engineering, and multi-step scientific and technical reasoning.

### **Core Enhancements & Key Features**

* **75% Cheaper Cache Reads:** While base token pricing remains at $10/M input and $50/M output, prompt cache reads were cut from $1.00 to $0.25 per million tokens. This yields an estimated **25% overall cost reduction** for standard workflows and up to **45% savings** for iterative agentic loops.  
*   
* **Enterprise Frontier Safeguards (EFS):** Addresses previous mandatory 30-day safety data retention by allowing eligible enterprise customers to store and audit data within their own customer-controlled cloud environments, enabling effective zero data retention (ZDR).  
*   
* **60% Reduction in False Positives:** Safety classifiers were retuned to eliminate over-refusal on benign security workflows. It natively supports defensive vulnerability research without triggering blocks (unlike weaponized exploit generation).  
*   
* **Extended Capacity & Thinking Controls:** Features a native **1 million token context window** and up to **128,000 maximum output tokens**. Adaptive reasoning is always active, regulated using the effort parameter (Low, Medium, High).  
*   
* **Anti-Shortcut Execution:** Designed specifically to avoid brittle "hacks" common in standard models (such as commenting out failing tests to force a build to pass). It targets root causes, writes self-validating test harnesses, and inspects visual UI output via vision before declaring completion.  
* 

### **How It Differs from Claude Opus and Claude Fable 5**

| Feature / Metric | Claude Opus (4.8 / 5\) | Claude Fable 5 | Claude Fable 5.1 |
| :---- | :---- | :---- | :---- |
| **Model Class** | Standard Frontier Reasoning | First-gen Mythos-class Agent | Refined Mythos-class Agent |
| **Agent Horizon** | Short-to-medium (turn-based reasoning, drafting, analysis) | Multi-hour autonomous execution; prone to nitpicking/verbosity | Multi-hour autonomous execution with tighter precision and root-cause focus |
| **Cache Pricing** | Standard tier pricing | $1.00 / M tokens | **$0.25 / M tokens** |
| **Safety Classifier Friction** | Low baseline refusal on routine tasks | High false-positive rate on security/bio tasks | **60% fewer false positives** in cybersecurity; granular fallbacks |
| **Data Governance** | Standard retention policies | Mandatory 30-day Anthropic retention | **Customer-controlled EFS** / Zero Data Retention paths |
| **Thinking Mode** | Toggleable extended thinking | Always-on adaptive thinking | Always-on adaptive thinking (improved Low/Medium efficiency) |

### **Ideal Tasks Where Other Models Fall Short**

* **End-to-End Codebase Refactoring & Migration:** Handling cross-cutting architectural changes across tens of thousands of lines of code. Where Opus or Sonnet might lose architectural coherence after 10–15 file modifications, Fable 5.1 maintains context across lengthy sessions, resolving dependency conflicts and unit failures without supervision.  
*   
* **Unattended Multi-Hour Agent Loops:** Backlog triage, bug replication, and ticket resolution via environments like Claude Cowork or automated CLI agents. It gracefully pauses, self-corrects broken terminal steps, and reports actual blockers rather than hallucinating task completion.  
*   
* **Computational Science & Systems Optimization:** High-level scientific tasks like writing custom GPU kernels for model acceleration, evaluating structural biology data, or processing massive spatial datasets.  
*   
* **Document Audits Across Disparate Media:** Processing complex institutional reports (hundreds of pages containing interleaved schematics, nested data tables, and legal clauses) where visual understanding and exhaustive cross-referencing must occur simultaneously.

