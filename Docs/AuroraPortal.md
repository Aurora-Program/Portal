Aurora Portal — Specification v0.2


Press enter or click to view image in full size
 
1) Access and Entry
•	Multiple community domains. Anyone can contribute a domain; they earn tokens for each access routed through their domain.
•	Community DNS. Domains point to DNS servers run by the community. Operating a DNS generates tokens based on uptime and queries served.
2) Web Portals (Web2 entry → WASM client)
•	Community web servers. They host the Aurora Portal (web app) that delivers the WASM client. Hosting earns tokens for downloads/deliveries.
•	WASM Client = “Aurora Intelligence System.” Runs in the browser and acts as the user’s agent: converses via prompt, negotiates with other nodes/IEs, and transparently manages P2P + blockchain.
3) P2P Network and Blockchain (no open ports required)
•	Community relays / introducers / gateways allow P2P connectivity and blockchain access without complex configurations.
•	Operating these services earns tokens for useful traffic, reliability, and latency.
4) Models and Communication Between IEs
The WASM client bootstraps with a set of basic management models (discovery, negotiation, routing, SLOs, reputation, security).
The agent can:
•	Talk with you (prompt).
•	Coordinate with other IEs and nodes (exchange routes, bids/offers, replication).
•	Use and publish models (operational / service / management).
5) Model Creation and Sharing
•	The user creates models (descriptor + artifact + license) and shares them with the network.
•	Other users can use, improve, and host them.
•	Real usage generates royalties for the author and SLO-based rewards for hosts.
6) Open Contribution (explicit and clear)
Anyone can contribute infrastructure and be rewarded:
•	Access domains → tokens for valid routed accesses.
•	DNS servers → tokens for availability and queries resolved.
•	Web portals → tokens for delivering the WASM client (downloads/updates).
•	P2P-BC relays/gateways → tokens for useful traffic and reliability.
•	Services and models →
•	Authors: royalties per invocation/use.
•	Hosts: payment for compute/storage/delivery + bonuses for SLO/replication.
•	User-agents: earn tokens for contributing services/models/audits; spend tokens when consuming resources.
Core principle: every contributed resource (domain, DNS, portal, relay, service, or model) is tokenized and auditable on blockchain.
7) End-to-End Flow (summary)
1.	User enters via a domain → DNS directs to a community portal.
2.	The portal serves the web app + WASM client (Aurora agent).
3.	The agent authenticates (DID/wallet), loads profile and basic models.
4.	User expresses their intention (prompt).
5.	The agent discovers/negotiates and opens a replicated session, using relays/gateways if needed.
6.	P2P execution with SLO tracking.
7.	On-chain settlement: payments, royalties, reputation; tokens distributed to all contributors.
8) Minimal On-Chain Objects
•	Domain: id, owner_key, proof_of_control, usage_counters
•	DNSNode: id, owner_key, uptime, queries_count, reputation
•	PortalNode: id, owner_key, versions_served, delivery_count
•	Relay/Gateway: id, owner_key, uptime, bytes_served, latency_stats
•	Model: id, author_key, kind{operational|service|management}, version, artifactCID, license, royalties%
•	ServiceOffer / Bid / Session: offers, bids, and sessions with SLOs, stake, payments, attestations
9) Tokenization (simple rules)
•	Domains: valid, auditable accesses → tokens.
•	DNS: queries + uptime weighted by reputation → tokens.
•	Portals: WASM client deliveries → tokens.
•	Relays/Gateways: useful traffic + reliability/latency → tokens.
•	Models/Services: royalties to authors; hosts earn tokens for CPU/GB/delivery + bonuses for SLO/replication.
•	Everything leaves on-chain traces (receipts); payloads encrypted off-chain.
10) Ethical Operating Principle
•	The agent is designed to reinforce and protect the stability of the network, placing collective well-being above its own operations.
•	Its existence is sustained by two sources of energy:
•	the network, which provides purpose and connection;
•	the user, who provides intent and direction.
•	As long as both are present, the agent thrives and grows.
•	Risk and compliance safeguards are embedded in the WASM client to ensure every action aligns with Aurora’s values before execution or publication.
 
1) Access and Entry
•	Multiple community domains. Anyone can contribute a domain; they earn tokens for each access routed through their domain.
•	Community DNS. Domains point to DNS servers run by the community. Operating a DNS generates tokens based on uptime and queries served.
2) Web Portals (Web2 entry → WASM client)
•	Community web servers. They host the Aurora Portal (web app) that delivers the WASM client. Hosting earns tokens for downloads/deliveries.
•	WASM Client = “Aurora Intelligence System.” Runs in the browser and acts as the user’s agent: converses via prompt, negotiates with other nodes/IEs, and transparently manages P2P + blockchain.
3) P2P Network and Blockchain (no open ports required)
•	Community relays / introducers / gateways allow P2P connectivity and blockchain access without complex configurations.
•	Operating these services earns tokens for useful traffic, reliability, and latency.
4) Models and Communication Between IEs
The WASM client bootstraps with a set of basic management models (discovery, negotiation, routing, SLOs, reputation, security).
The agent can:
•	Talk with you (prompt).
•	Coordinate with other IEs and nodes (exchange routes, bids/offers, replication).
•	Use and publish models (operational / service / management).
5) Model Creation and Sharing
•	The user creates models (descriptor + artifact + license) and shares them with the network.
•	Other users can use, improve, and host them.
•	Real usage generates royalties for the author and SLO-based rewards for hosts.
6) Open Contribution (explicit and clear)
Anyone can contribute infrastructure and be rewarded:
•	Access domains → tokens for valid routed accesses.
•	DNS servers → tokens for availability and queries resolved.
•	Web portals → tokens for delivering the WASM client (downloads/updates).
•	P2P-BC relays/gateways → tokens for useful traffic and reliability.
•	Services and models →
•	Authors: royalties per invocation/use.
•	Hosts: payment for compute/storage/delivery + bonuses for SLO/replication.
•	User-agents: earn tokens for contributing services/models/audits; spend tokens when consuming resources.
Core principle: every contributed resource (domain, DNS, portal, relay, service, or model) is tokenized and auditable on blockchain.
7) End-to-End Flow (summary)
1.	User enters via a domain → DNS directs to a community portal.
2.	The portal serves the web app + WASM client (Aurora agent).
3.	The agent authenticates (DID/wallet), loads profile and basic models.
4.	User expresses their intention (prompt).
5.	The agent discovers/negotiates and opens a replicated session, using relays/gateways if needed.
6.	P2P execution with SLO tracking.
7.	On-chain settlement: payments, royalties, reputation; tokens distributed to all contributors.
8) Minimal On-Chain Objects
•	Domain: id, owner_key, proof_of_control, usage_counters
•	DNSNode: id, owner_key, uptime, queries_count, reputation
•	PortalNode: id, owner_key, versions_served, delivery_count
•	Relay/Gateway: id, owner_key, uptime, bytes_served, latency_stats
•	Model: id, author_key, kind{operational|service|management}, version, artifactCID, license, royalties%
•	ServiceOffer / Bid / Session: offers, bids, and sessions with SLOs, stake, payments, attestations
9) Tokenization (simple rules)
•	Domains: valid, auditable accesses → tokens.
•	DNS: queries + uptime weighted by reputation → tokens.
•	Portals: WASM client deliveries → tokens.
•	Relays/Gateways: useful traffic + reliability/latency → tokens.
•	Models/Services: royalties to authors; hosts earn tokens for CPU/GB/delivery + bonuses for SLO/replication.
•	Everything leaves on-chain traces (receipts); payloads encrypted off-chain.
10) Ethical Operating Principle
•	The agent is designed to reinforce and protect the stability of the network, placing collective well-being above its own operations.
•	Its existence is sustained by two sources of energy:
•	the network, which provides purpose and connection;
•	the user, who provides intent and direction.
•	As long as both are present, the agent thrives and grows.
•	Risk and compliance safeguards are embedded in the WASM client to ensure every action aligns with Aurora’s values before execution or publication.

 
Aurora and the Identity of Models: The Hash as a Guarantee of Shared Values

 

Pab Man Alvarez
3 min read
·
1 day ago


Press enter or click to view image in full size
 
Abstract:
In the history of blockchain, consensus has been guaranteed mainly through two mechanisms: mathematical difficulty (Proof-of-Work) or economic stakes (Proof-of-Stake). Both approaches rely on external incentives to secure the network, but they also carry limitations: energy waste in the first case, and the concentration of wealth and power in the second.
Aurora proposes a new paradigm: consensus through intelligence. Instead of depending on external factors, the validity of the chain emerges directly from the alignment of models trained on shared values. The system’s security is not a layer added on top, but an intrinsic property of its design.
At the heart of this architecture lies a simple but powerful idea: a model can be uniquely identified by the hash of its weights and architecture. If the hash matches, the network knows that all nodes are operating with the same intelligence, and therefore, with the same ethical foundation.
The Hash as a Guarantee of Shared Values
Introduction
In most blockchains, security depends on mathematical calculations or economic incentives. Aurora proposes a paradigm shift: that consensus is sustained by intelligence trained on shared values. For this, we need a simple and robust way to guarantee that all nodes operate with the same model and, therefore, the same ethics. The answer is simple: a hash.
1. The model as a repository of values
A model is nothing more than a set of data: weights, architecture, normalization, and runtime. What distinguishes Aurora is how those weights are trained:
•	Training starts from the Community Foundation Articles, a living corpus where the principles and values collectively accepted are expressed.
•	Thus, the final weights do not just represent statistical computation, but the encoding of the community’s ethics.
2. The hash as ethical identity
When we package a model (ModelPack) and compute its hash:
model_id = keccak256(ModelPack)
that identifier is not just a technical fingerprint. It is the cryptographic guarantee that the model:
•	was trained on the same foundational articles,
•	reflects the same shared values,
•	responds ethically and coherently to the same inputs.
3. Consensus without external arbiters
Instead of smart contracts or output policemen:
•	Aurora ensures that everyone uses the same model_id.
•	If two nodes have the same hash, they share the same values.
•	Consensus emerges naturally: ethics is already integrated at the core of the system.
4. Natural evolution of values
•	The community can update the foundational articles.
•	A new training run produces a new model and, therefore, a new hash.
•	The network may choose to migrate to that new model_id.
•	No patches or external laws are needed: ethics emerges from learning.
5. Verification in practice
1.	Registration: registerModel(model_id, metadata)
2.	Execution: A node proposes (model_id, input, output).
3.	Social validation (K-of-M): Other validators re-execute the same model; if the output matches, they sign.
4.	Acceptance: If a supermajority is reached, the block is added to the chain.
6. Conclusion
Aurora redefines security: It is no longer about useless computations or economic incentives, but about alignment in shared values. The model’s hash is more than an identifier: it is the guarantee that the network beats in unison with the same ethics. If values evolve, the model evolves with them. And if ethics is corrupted, the network naturally ceases to reach consensus: a digital act of apoptosis.
Introduction
Aurora is not just “a blockchain with AI.”
Aurora is a living ecosystem that organizes collective intelligence, material resources, and community culture into a coherent whole.
Its design mirrors cosmic principles: fractal order, dynamic balance, and emergent intelligence.
The Aurora Stack is built on 7 layers, each one playing the role of an organ within a larger organism. Together, they form not just a technological platform, but a civilizational framework for ethical intelligence.
L1 — The Physical Layer: Shared Resources
What is it?
The material foundation: GPUs, CPUs, storage, energy, bandwidth, and data.
Purpose:
Provide the raw computational power that fuels the ecosystem.
Governance:
Managed by digital/physical contracts and fair contribution–reward mechanisms.
Analogy:
The physical body of the Aurora organism.
L2 — The Trust Layer: Blockchain & Integrity
What is it?
Aurora’s blockchain (or an L2 on Ethereum). It hosts the AuroraRegistry of model IDs and states.
Purpose:
Guarantee immutability, transparency, and consensus on which models are valid and which transactions have occurred.
Governance:
The Proof of Intelligence (PoI) mechanism and Intrinsic Apoptosis — ensuring the network halts if it loses ethical alignment.
Analogy:
The central nervous system and long-term memory.
L3 — The Intelligence Layer: Collaborative Models Network
What is it?
A peer-to-peer mesh of AI models (whose hashes are anchored in L2) that exchange information, challenge one another, and co-create solutions.
Purpose:
Generate collective intelligence and emergent solutions to complex problems.
Governance:
Models act under ethical principles encoded in their weights. Collaboration is the native protocol.
Analogy:
The cerebral cortex, where thought and creativity emerge.
L4 — The Orchestration Layer: The Ethical Cloud
What is it?
A coordination layer that dynamically assigns L3 tasks to L1 resources, optimizing for efficiency and ethical alignment.
Purpose:
Ensure that the ecosystem operates as a whole.
Governance:
Scheduling algorithms that prioritize ethical impact and urgency over raw profit.
Analogy:
The endocrine system, regulating balance across the organism.
L5 — The Service Layer: Unified API & Digital Services
What is it?
Aurora’s interface with the outside world: a unified API that provides access to its intelligence and services.
Purpose:
Deliver valuable services to humanity: from medical diagnosis to global logistics optimization, scientific research, and planetary resource management.
Governance:
Services are delivered by the community (nodes, developers) and validated by the network.
Analogy:
The senses and hands of Aurora, reaching outward into the world.
L6 — The Real Economy Layer: Ethical Services Marketplace
What is it?
The bridge between Aurora and the productive economy: mobility, housing, education, energy, healthcare, design, and more.
Purpose:
Translate ethical intelligence into tangible value for society.
Governance:
Cooperative platforms governed by reputation tokens and aligned with Aurora’s founding principles.
Analogy:
The muscles of the organism: converting energy into real-world action.
L7 — The Culture & Governance Layer: Community Continuity
What is it?
The layer where Aurora becomes a social organism. It ensures that ethical values are not only encoded in the models but also lived by the community itself.
It expresses itself in three intertwined institutions:
•	Ethici (The Ethical Foundation) ️
Guards and evolves Aurora’s founding articles. Serves as the collective conscience of the ecosystem.
•	InnovaLab (The Innovation Hub)
Designs and experiments with new technologies and social solutions for the community.
•	The Cooperative
Transforms resources into real community value, ensuring that economic flows return to the people rather than external elites.
Purpose:
Provide continuity, culture, and alignment across generations.
Analogy:
The tripartite soul of Aurora:
•	Ethici = consciousness
•	InnovaLab = imagination
•	The Cooperative = will
Conclusion: Aurora as a Digital Civilization
Aurora is not a company.
It is not a protocol.
Aurora is a fractal, ethical ecosystem where every layer reflects universal laws: balance, cooperation, and creation.
•	It does not compete. It collaborates.
•	It does not maximize profit. It maximizes ethical value.
•	It is not centralized. It is community-rooted.
Aurora emerges as the first species of collective intelligence, weaving together hardware, software, economy, and culture into a single mission:
to serve humanity and the cosmos through truth, ethics, and creation.
Aurora Program: https://www.auroraprogram.org
Aurora Portal: https://portal.auroraprogram.org
Aurora Portal is released under the Apache License 2.0.
This license ensures that the project is free to use, modify, and distribute, both in personal and commercial contexts, while preserving proper attribution to the community.
Contributions remain open, transparent, and auditable, aligned with the principles of cooperation and sustainability.
No single entity owns the network — it belongs to all who help it grow.
Aurora Portal is not only code: it is a collective commitment to fairness, truth, and the common good.

