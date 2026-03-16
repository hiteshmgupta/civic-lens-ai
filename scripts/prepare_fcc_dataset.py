"""
CivicLens Dataset Preparation Script
=====================================
Generates curated comments for 7 real-world legislative amendments with
realistic synthetic vote data for the CivicLens platform.

HF API budget per amendment analysis:
  - Sentiment:  ceil(N/32) calls (batched)
  - Classifier: N calls (1 per comment, zero-shot)
  - Summarizer: 1 call
  - Topic:      0 calls (local TF-IDF)
  Total = N + ceil(N/32) + 1

With ~35 comments × 7 amendments: ~259 API calls, well within HF free tier (1000/hr).

Output: fcc_dataset.json → place in backend src/main/resources/
"""

import json
import random

random.seed(42)

# ---------------------------------------------------------------------------
# SYNTHETIC USERS (20 users to distribute comments and votes)
# ---------------------------------------------------------------------------
USERS = [
    {"username": "digital_rights_advocate", "email": "digital_advocate@civiclens.com"},
    {"username": "telecom_policy_analyst", "email": "telecom_analyst@civiclens.com"},
    {"username": "small_biz_owner", "email": "smallbiz@civiclens.com"},
    {"username": "network_engineer_42", "email": "neteng42@civiclens.com"},
    {"username": "law_student_2017", "email": "lawstudent@civiclens.com"},
    {"username": "rural_internet_user", "email": "ruraluser@civiclens.com"},
    {"username": "startup_founder_dc", "email": "startupdc@civiclens.com"},
    {"username": "consumer_watchdog", "email": "consumer_watch@civiclens.com"},
    {"username": "broadband_investor", "email": "broadband_inv@civiclens.com"},
    {"username": "free_market_advocate", "email": "freemarket@civiclens.com"},
    {"username": "tech_journalist", "email": "techjournalist@civiclens.com"},
    {"username": "privacy_researcher", "email": "privacyresearch@civiclens.com"},
    {"username": "veteran_commenter", "email": "veteran_comm@civiclens.com"},
    {"username": "economics_professor", "email": "econprof@civiclens.com"},
    {"username": "concerned_parent", "email": "concerned_parent@civiclens.com"},
    {"username": "healthcare_worker", "email": "healthcare_worker@civiclens.com"},
    {"username": "disability_advocate", "email": "disability_adv@civiclens.com"},
    {"username": "municipal_official", "email": "muni_official@civiclens.com"},
    {"username": "content_creator_99", "email": "contentcreator@civiclens.com"},
    {"username": "cybersecurity_pro", "email": "cybersecpro@civiclens.com"},
]

# ---------------------------------------------------------------------------
# AMENDMENT 1: Net Neutrality (DIGITAL_PRIVACY) — ~35 comments
# ---------------------------------------------------------------------------
AMENDMENT_1 = {
    "title": "Restoring Internet Freedom Act — Repeal of Net Neutrality Rules",
    "body": (
        "This order repeals the Title II classification of broadband Internet access service "
        "and returns to the light-touch regulatory framework that governed the Internet prior "
        "to 2015. The Commission eliminates the bright-line rules against blocking, throttling, "
        "and paid prioritization previously adopted under the 2015 Open Internet Order. In their "
        "place, the order requires Internet Service Providers to publicly disclose information "
        "about their network management practices, performance, and commercial terms of service. "
        "The Federal Trade Commission will be empowered to take action against ISPs that engage "
        "in unfair, deceptive, or anticompetitive practices."
    ),
    "category": "DIGITAL_PRIVACY",
    "comments": [
        {"body": "I am writing to urge the FCC to preserve the existing net neutrality rules under Title II. The open Internet has been the greatest engine of economic growth and free expression in modern history. Allowing ISPs to create fast lanes and slow lanes will devastate small businesses, startups, and independent content creators who cannot afford to pay for priority access.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "As a small business owner who relies entirely on the Internet to reach customers, I strongly oppose this proposal. Without net neutrality, companies like mine will be at the mercy of ISPs who can throttle our websites or charge us fees to reach our own customers. Most Americans have only one or two choices for broadband, meaning ISPs already operate as monopolies.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The Internet should be treated as a public utility, just like water and electricity. Every American deserves equal access to online content regardless of their income level or which ISP serves their area. The proposed repeal would create a two-tiered Internet that benefits wealthy corporations at the expense of ordinary citizens.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "I am a network engineer with 15 years of experience in telecommunications. The technical arguments put forward by opponents of net neutrality are misleading. Modern networks are fully capable of handling current traffic loads without paid prioritization. The real motivation behind this repeal is to allow ISPs to extract additional rents from content providers and consumers.", "stance": "oppose", "sentiment": "negative"},
        {"body": "This proposal will have devastating effects on rural communities. We already pay more for worse Internet service. Without net neutrality protections, ISPs will have even less incentive to invest in rural broadband infrastructure and more incentive to squeeze revenue from existing customers through data caps, throttling, and paid prioritization.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "As someone with a disability, I rely on the open Internet for telehealth services, remote work, and community engagement. Net neutrality ensures that the services I depend on are not throttled or blocked by my ISP. Repealing these protections would disproportionately harm people with disabilities.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The FCC's own data shows that broadband investment has not declined since the adoption of the 2015 Open Internet Order. ISP revenues and capital expenditures have continued to grow since their adoption. The claim that Title II regulation has chilled investment is not supported by evidence.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I am deeply concerned about the impact on free speech and political discourse. Without net neutrality, ISPs could slow down or block access to websites that express political views they disagree with. The First Amendment depends on an open and neutral Internet infrastructure.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "Net neutrality is not a partisan issue. Polls consistently show that the overwhelming majority of Americans — across party lines — support maintaining strong net neutrality protections. The FCC should listen to the people it serves, not the ISP lobbyists who stand to profit.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The transparency requirements proposed as a replacement for bright-line rules are completely inadequate. History has shown that disclosure alone does not prevent anti-competitive behavior. AT&T throttled FaceTime. Comcast throttled BitTorrent. Verizon blocked Google Wallet. Only enforceable rules protect consumers.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "I am a content creator on YouTube with over 500,000 subscribers. My livelihood depends on viewers being able to access my content without interference from their ISP. If ISPs can throttle video streaming, independent voices will be silenced while corporate media with deep pockets dominates.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "I run a nonprofit that provides digital literacy training to underserved communities. The repeal of net neutrality will widen the digital divide and make it harder for the communities we serve to access educational resources, job opportunities, and government services online.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "I work in cybersecurity, and I want to emphasize the security implications. Without clear rules preventing ISPs from interfering with traffic, there is a risk that ISPs could inject content, redirect DNS queries, or engage in deep packet inspection that compromises user privacy and security.", "stance": "oppose", "sentiment": "negative"},
        {"body": "As a law student specializing in telecommunications policy, the legal basis for reclassifying broadband under Title I is tenuous. The D.C. Circuit Court has twice upheld the FCC's authority under Title II. This reclassification will face legal challenges and create years of regulatory uncertainty.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The argument that the Internet flourished before 2015 without Title II ignores that the FCC enforced net neutrality principles through other means, including enforcement actions against Comcast for throttling BitTorrent in 2008. The 2015 rules formalized existing protections.", "stance": "oppose", "sentiment": "negative"},
        {"body": "My daughter has a rare medical condition requiring telemedicine consultations. If my ISP is allowed to throttle video services unless I pay extra, it could put my daughter's health at risk. Net neutrality is not an abstract policy debate for our family — it is a matter of health.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "Municipal broadband networks have proven that competition delivers better service at lower prices. Rather than deregulating and allowing private monopolies to exploit consumers, the FCC should encourage more municipal broadband. Repealing net neutrality moves in the wrong direction.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I represent a coalition of independent musicians who rely on platforms like Bandcamp and SoundCloud. Without net neutrality, ISPs could favor content from major labels while making it harder for independent creators to be heard. Cultural diversity depends on an open Internet.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I support the Commission's proposal to restore Internet freedom by removing the heavy-handed Title II regulations that have stifled broadband investment and innovation. The Internet thrived for decades under light-touch regulation. The free market should determine how the Internet evolves.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "As a broadband industry investor, I have seen firsthand how Title II classification has created regulatory uncertainty that has discouraged infrastructure investment. Repealing these rules will unleash a new wave of investment, particularly in underserved rural areas.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "Title II was designed to regulate telephone monopolies in the 1930s. Applying it to the dynamic, competitive broadband market of the 21st century makes no sense. The Commission is right to return to the regulatory framework that fostered this innovation.", "stance": "support", "sentiment": "positive"},
        {"body": "The 2015 rules banned paid prioritization, which actually harms consumers. There are legitimate use cases for traffic prioritization — for example, ensuring that telemedicine applications have priority over background downloads. A blanket ban prevents ISPs from optimizing for consumers.", "stance": "support", "sentiment": "positive"},
        {"body": "I operate a small ISP serving a rural community of approximately 5,000 households. The regulatory burden imposed by Title II has cost our company tens of thousands in legal and compliance costs — money that could have been spent building out our fiber network.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The FTC has a proven track record of protecting consumers from anti-competitive practices. Returning broadband oversight to the FTC will ensure strong consumer protections while avoiding the regulatory overreach of Title II.", "stance": "support", "sentiment": "positive"},
        {"body": "The doom-and-gloom predictions are vastly overblown. Before the 2015 rules, there were no widespread problems with blocking or throttling. ISPs have every economic incentive to provide customers with access to the content they want. The market works.", "stance": "support", "sentiment": "positive"},
        {"body": "I am an economist studying telecommunications markets. The empirical evidence shows that Title II classification had a measurable negative impact on broadband investment. According to USTelecom data, broadband capital expenditure declined 5.6% in the two years following the 2015 rules.", "stance": "support", "sentiment": "positive"},
        {"body": "Government regulation always has unintended consequences. Title II gives the FCC the power to regulate rates, impose tariffs, and micromanage business decisions. Even if the current Commission restrains itself, a future Commission could use these powers. Removing Title II is the safest course.", "stance": "support", "sentiment": "positive"},
        {"body": "As a cable installer who has worked in the industry for 20 years, the regulations have made it harder for our company to upgrade infrastructure. If we could redirect compliance costs to actually building better networks, customers would see real speed and reliability improvements.", "stance": "support", "sentiment": "positive"},
        {"body": "The Internet works best when the government stays out of the way. Competition between providers is the best protection for consumers. If an ISP blocks or throttles content, customers will switch to a competitor.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "While I support the principle of net neutrality, I believe Title II regulation may not be the best mechanism. A legislative solution codifying net neutrality into law would provide more durable protections than administrative rules that change with each administration. I urge Congress to act.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The debate has become far too polarized. Both sides make valid points. ISPs need flexibility to manage networks, but consumers need protections against anti-competitive practices. The Commission should find a balanced approach rather than swinging between extremes.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I support some aspects but oppose others. Reducing regulatory burden on small ISPs is worthy. However, the complete elimination of bright-line rules against blocking and throttling goes too far. At minimum, retain clear prohibitions on those practices.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I note that a significant portion of comments submitted in this proceeding appear to have been generated by automated systems using stolen identities. I urge the Commission to investigate and give appropriate weight only to genuine public comments.", "stance": "neutral", "sentiment": "negative"},
        {"body": "I am deeply troubled by the number of fraudulent comments submitted in support of this repeal. The New York Attorney General has identified millions submitted using stolen identities. The FCC has refused to cooperate with the investigation, raising serious legitimacy questions.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "As a former FCC commissioner, this proceeding highlights the need for Congressional action. The back-and-forth between administrations creates uncertainty for all stakeholders. Congress should pass bipartisan legislation establishing clear, permanent protections.", "stance": "neutral", "sentiment": "neutral"},
    ]
}

# ---------------------------------------------------------------------------
# AMENDMENT 2: Clean Air and Climate Action (ENVIRONMENT) — ~30 comments
# ---------------------------------------------------------------------------
AMENDMENT_2 = {
    "title": "Clean Air and Climate Accountability Act Amendment",
    "body": (
        "This amendment strengthens the Clean Air Act by establishing binding greenhouse gas "
        "emission reduction targets of 50% below 2005 levels by 2030 and net-zero emissions "
        "by 2050. It creates a carbon pricing mechanism for industrial emitters producing more "
        "than 25,000 tons of CO2 equivalent annually, establishes a Green Infrastructure Fund "
        "to support communities transitioning from fossil fuel economies, and mandates that "
        "federal agencies incorporate climate risk assessments into all major regulatory actions "
        "and infrastructure investments."
    ),
    "category": "ENVIRONMENT",
    "comments": [
        {"body": "I strongly support this amendment. Climate change is the defining challenge of our generation, and the science is unequivocal — we must reduce greenhouse gas emissions dramatically within this decade to avoid catastrophic warming. The targets are consistent with IPCC recommendations and represent the minimum necessary action.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "As a farmer in the Midwest, I have seen firsthand how changing weather patterns are affecting crop yields and making farming increasingly unpredictable. Droughts, floods, and unseasonable temperatures are no longer rare events. This amendment is essential to protect the livelihoods of millions of agricultural workers.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The carbon pricing mechanism is a market-based approach that economists across the political spectrum support. By putting a price on carbon, we allow the market to find the most efficient way to reduce emissions while generating revenue for the Green Infrastructure Fund.", "stance": "support", "sentiment": "positive"},
        {"body": "I am a public health researcher. Air pollution from fossil fuels causes an estimated 350,000 premature deaths annually in the United States alone. This amendment is not just about climate — it is about protecting the health of every American, especially children, the elderly, and communities near industrial facilities.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I work in the renewable energy sector and can tell you that the transition to clean energy is already creating millions of jobs. This amendment will accelerate that transition and ensure the economic benefits are shared broadly, including in communities that currently depend on fossil fuels.", "stance": "support", "sentiment": "positive"},
        {"body": "The Green Infrastructure Fund is critical. We cannot simply shut down coal mines and oil refineries without providing alternative economic opportunities for affected workers and communities. This fund ensures a just transition that leaves no community behind.", "stance": "support", "sentiment": "positive"},
        {"body": "As a mother of three, I am terrified about the world we are leaving our children. The wildfires, hurricanes, and heat waves are getting worse every year. Please pass this amendment — our children's future depends on it.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The federal climate risk assessment requirement is perhaps the most important provision. Currently, agencies approve infrastructure projects without considering flood risk, sea level rise, or extreme weather, leading to billions in taxpayer losses when infrastructure fails prematurely.", "stance": "support", "sentiment": "positive"},
        {"body": "I represent a coalition of small businesses that support climate action. We have signed onto the Climate Declaration and believe that a stable climate is essential for business prosperity. Policy uncertainty is far more damaging than clear, predictable regulations.", "stance": "support", "sentiment": "positive"},
        {"body": "As a coastal homeowner, I have watched my insurance premiums triple in the past decade due to increasing hurricane and flood risk. The cost of inaction on climate change is far greater than the cost of this amendment. We are already paying the price for decades of delay.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The scientific consensus on climate change is overwhelming. Over 97% of climate scientists agree that human activities are driving global warming. This amendment is not about ideology — it is about listening to the science and acting responsibly.", "stance": "support", "sentiment": "positive"},
        {"body": "I am a clean energy investor and can confirm that the renewable energy market is booming globally. Countries that invest now in clean energy infrastructure will dominate the industries of the future. This amendment positions America as a leader rather than a laggard.", "stance": "support", "sentiment": "positive"},
        {"body": "This amendment will destroy the American economy. The proposed emission reduction targets are unrealistic and will drive up energy costs for consumers and businesses. Manufacturing will move overseas to countries with weaker standards, resulting in no net reduction in global emissions.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "As an energy industry executive, the carbon pricing mechanism will cost the American economy billions annually. Natural gas has already reduced emissions significantly, and the market is moving toward cleaner energy without government mandates. This regulatory overreach is unnecessary.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The 2030 target of 50% reduction below 2005 levels is completely unrealistic given our current energy infrastructure. Even with aggressive renewable investment, we cannot replace baseload power generation in less than a decade without compromising grid reliability and causing blackouts.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I am deeply concerned that this amendment will disproportionately burden low-income families through higher energy costs. A carbon price is effectively a regressive tax that hits the poorest Americans hardest. Without robust consumer protection mechanisms, this will increase energy poverty.", "stance": "oppose", "sentiment": "negative"},
        {"body": "China and India are the world's largest emitters. Until those countries commit to binding emission reductions, unilateral action by the United States will put American businesses at a competitive disadvantage while having negligible impact on global temperatures.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The coal industry employs hundreds of thousands of Americans in communities that have no alternative economic base. This amendment will devastate these communities. The Green Infrastructure Fund is a Band-Aid on a catastrophic wound that this policy would inflict.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The climate models used to justify this amendment have repeatedly overestimated warming. Basing policy on uncertain projections while imposing certain economic costs is irresponsible. We should invest in adaptation rather than trying to control the global thermostat.", "stance": "oppose", "sentiment": "negative"},
        {"body": "Energy independence is a national security priority. This amendment would make us more dependent on foreign supply chains for solar panels, wind turbines, and battery minerals that are largely controlled by China. We would be trading energy independence for green dependency.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The cost-benefit analysis of carbon pricing depends entirely on the social cost of carbon estimate used. The current administration's estimates are based on disputed methodologies and are significantly higher than those used by previous administrations.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I support the goals of this amendment but have concerns about the timeline. A phased approach with interim milestones and regular review would be more practical than rigid targets. We need to balance ambition with feasibility.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "Nuclear energy should be explicitly included as part of the clean energy solution. It is the only proven technology capable of providing reliable, large-scale, zero-carbon baseload power. The amendment's silence on nuclear is a significant oversight.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I would support this amendment if it included stronger provisions for affected workers. Retraining programs must be robust and well-funded, not just symbolic. The just transition must be genuinely just, not just a talking point.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment should include provisions for carbon capture and storage technology. CCS can significantly reduce emissions from existing industrial facilities while maintaining economic activity. A technology-neutral approach is more likely to succeed.", "stance": "neutral", "sentiment": "neutral"},
    ]
}

# ---------------------------------------------------------------------------
# AMENDMENT 3: Rural Broadband (INFRASTRUCTURE) — ~30 comments
# ---------------------------------------------------------------------------
AMENDMENT_3 = {
    "title": "Digital Infrastructure and Rural Broadband Expansion Act",
    "body": (
        "This amendment allocates $65 billion in federal funding for broadband infrastructure "
        "deployment, with priority given to unserved and underserved areas. It establishes a "
        "minimum speed standard of 100 Mbps download and 20 Mbps upload for all federally "
        "funded broadband projects, creates a Digital Equity Grant Program to support digital "
        "literacy and device access programs, and requires ISPs receiving federal subsidies to "
        "offer an affordable connectivity plan at no more than $30 per month for qualifying "
        "low-income households."
    ),
    "category": "INFRASTRUCTURE",
    "comments": [
        {"body": "I live in a rural county where the best available Internet speed is 5 Mbps download. My children cannot participate in remote learning, I cannot work from home, and we cannot access telehealth services. This amendment is desperately needed to bridge the digital divide that threatens to leave rural America behind.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The minimum speed standard of 100/20 Mbps is forward-looking and appropriate. Previous federal broadband programs defined broadband at absurdly low speeds, allowing ISPs to claim they had served an area while delivering service that was practically unusable for modern applications.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The affordable connectivity requirement is essential. Even where broadband is available, many low-income families cannot afford monthly service. The $30 per month cap ensures that the benefits of broadband expansion actually reach the communities that need it most.", "stance": "support", "sentiment": "positive"},
        {"body": "I am a county commissioner in Appalachia. Our community has been trying to attract businesses and remote workers, but the lack of reliable broadband is our biggest obstacle. This amendment would be transformative for rural economic development and would help stem the outmigration of young people.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The Digital Equity Grant Program addresses a critical gap. Providing broadband infrastructure is not enough — we also need to ensure that people have the skills and devices to use it effectively. Digital literacy is the civil rights issue of our time.", "stance": "support", "sentiment": "positive"},
        {"body": "As a telehealth provider serving rural patients, I can attest that broadband access is literally a matter of life and death. Patients who cannot access video consultations must drive hours to see specialists, often delaying critical care. This amendment will save lives in underserved communities.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am a tribal member on a reservation where broadband access is virtually nonexistent. Our community has been left behind by every previous broadband initiative. I urge the Commission to ensure that tribal lands receive priority in the allocation of these funds.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "Municipal broadband networks should be eligible for this funding. In many areas, private ISPs have failed to deploy adequate broadband despite decades of subsidies. Local communities should have the option to build their own networks with federal support.", "stance": "support", "sentiment": "positive"},
        {"body": "This level of federal spending on broadband infrastructure is justified by the economic returns. Studies consistently show that broadband access generates $3-4 in economic activity for every $1 invested. This is not spending — it is investment with proven returns.", "stance": "support", "sentiment": "positive"},
        {"body": "The pandemic exposed just how critical broadband access is for education, healthcare, and economic participation. Students sitting in parking lots to access Wi-Fi is a national disgrace. We cannot afford to let this moment pass without transformative investment.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am a librarian in a small town. Our library is the only place many community members can access the Internet. The Digital Equity Grant Program would help us expand our services and provide training that helps people participate in the digital economy.", "stance": "support", "sentiment": "positive"},
        {"body": "As a small business owner in a rural area, I pay $120 per month for 25 Mbps Internet that frequently drops. My competitors in urban areas pay less for fiber connections that are 40 times faster. This digital divide puts rural businesses at an enormous competitive disadvantage.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "$65 billion is an enormous amount of taxpayer money. History shows that government broadband programs are plagued by waste, fraud, and abuse. The USDA's ReConnect program has already awarded grants to areas that private ISPs were actively building out. We need oversight, not more spending.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The minimum speed standard will make deployment in remote areas prohibitively expensive. Requiring 100/20 Mbps means fiber or advanced wireless is the only option — satellite and fixed wireless solutions that could serve these areas more quickly and affordably are effectively excluded.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The $30 per month cap will discourage private investment in rural broadband. ISPs need to earn a return on their infrastructure investment, and price controls make rural deployment even less financially viable. This well-intentioned provision will actually slow buildout.", "stance": "oppose", "sentiment": "negative"},
        {"body": "We have seen this movie before. The federal government gives billions to ISPs, and they pocket the money while deploying the bare minimum of infrastructure. Without strict accountability measures and clawback provisions, this will be another boondoggle.", "stance": "oppose", "sentiment": "negative"},
        {"body": "Private enterprise, not government programs, has built the greatest communications infrastructure in human history. Rather than spending $65 billion on government-directed buildout, we should remove regulatory barriers that prevent ISPs from deploying in rural areas economically.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The federal government has a poor track record of picking technology winners. Mandating specific speed standards locks in current technology and may actually slow adoption of next-generation solutions like low-earth-orbit satellite Internet that could serve rural areas more cost-effectively.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I support this amendment but believe the speed standard should be symmetrical — 100/100 Mbps. Upload speed is increasingly important for remote work, video conferencing, telemedicine, and content creation. The asymmetric standard reflects an outdated consumption-only model.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment should include provisions for middle-mile infrastructure, not just last-mile connections. In many rural areas, the core issue is the lack of affordable middle-mile fiber that can carry traffic from local networks to Internet exchange points.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I support the broadband expansion goals but am concerned about the digital literacy provisions. They should be developed in partnership with community organizations that already serve these populations, not handed to contractors with no local knowledge or relationships.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment needs stronger mapping requirements. Current FCC broadband maps vastly overstate coverage. Areas shown as served often have no actual broadband options. Without accurate maps, funding will continue to be directed to the wrong places.", "stance": "neutral", "sentiment": "neutral"},
    ]
}

# ---------------------------------------------------------------------------
# AMENDMENT 4: Healthcare Data Privacy (HEALTHCARE) — ~30 comments
# ---------------------------------------------------------------------------
AMENDMENT_4 = {
    "title": "Healthcare Data Privacy and Patient Rights Enhancement Act",
    "body": (
        "This amendment strengthens patient data protections by expanding HIPAA to cover "
        "health-adjacent data collected by fitness trackers, health apps, and genetic testing "
        "services. It establishes a patient's right to access, correct, and delete their health "
        "data held by any covered entity, requires explicit opt-in consent before health data "
        "can be shared with third parties for non-treatment purposes, and creates civil penalties "
        "of up to $50,000 per violation for unauthorized data sharing. The amendment also mandates "
        "data breach notification within 72 hours and requires annual security audits for all "
        "entities handling protected health information."
    ),
    "category": "HEALTHCARE",
    "comments": [
        {"body": "As a physician, I strongly support this amendment. The current patchwork of health data regulations leaves enormous gaps that put patients at risk. Health apps and fitness trackers collect incredibly sensitive data — heart rate, sleep patterns, menstrual cycles — but are not covered by HIPAA. This must change.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I used a popular fertility tracking app for two years before discovering that my data was being sold to insurance companies and data brokers. The fact that this is currently legal is outrageous. This amendment would prevent such exploitative practices and restore trust in digital health tools.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The right to delete health data is critical. I had a misdiagnosis in my medical record that took years to correct and affected my insurance premiums. Patients must have the ability to ensure their records are accurate and to request deletion of data that is no longer clinically relevant.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The 72-hour breach notification requirement is reasonable and overdue. Currently, some entities take months or years to notify patients of data breaches. By that time, the damage — identity theft, insurance fraud, stigmatization — has already been done.", "stance": "support", "sentiment": "positive"},
        {"body": "Genetic testing data deserves the strongest possible protections. My DNA contains information not just about me, but about my family members who never consented to having their genetic predispositions shared. Companies like 23andMe should be held to the same standards as hospitals.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am a healthcare IT professional. The annual security audit requirement is essential but must be accompanied by clear technical standards. Many healthcare organizations have woefully inadequate cybersecurity. Ransomware attacks on hospitals have tripled in the past three years.", "stance": "support", "sentiment": "positive"},
        {"body": "As a mental health patient, I am acutely aware of the stigma attached to mental health records. I support this amendment because it gives me control over who can access my therapy records. No employer or insurer should access this information without my explicit consent.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am a cancer survivor. During my treatment, my health data was shared with dozens of entities I never authorized — insurance adjusters, pharmacy benefit managers, data analytics companies. I had no idea and no recourse. This amendment would have protected me.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The opt-in consent model is the only ethical approach. The current opt-out model assumes consent by default and buries the opt-out option in pages of legal jargon that no patient reads. Patients should be asked clearly and given a genuine choice.", "stance": "support", "sentiment": "positive"},
        {"body": "I work in a hospital emergency department. Every day I see patients whose care is delayed because we cannot access their records from other providers. While privacy is important, we also need interoperability. I support this amendment but urge that it not create additional barriers to legitimate clinical data sharing.", "stance": "support", "sentiment": "positive"},
        {"body": "This amendment correctly recognizes that health data is not limited to what happens in a doctor's office. My smartwatch knows my heart rate, blood oxygen levels, and sleep patterns. My grocery delivery app knows my diet. These data points, combined, paint an intimate health portrait that deserves protection.", "stance": "support", "sentiment": "positive"},
        {"body": "This amendment will stifle medical innovation. Health data research has led to breakthroughs in disease detection, drug development, and personalized medicine. Overly restrictive data access rules will slow down research and ultimately cost lives.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The compliance burden will be devastating for small healthcare providers and health tech startups. Annual security audits alone can cost $50,000-$100,000. Many small practices and innovative companies will not be able to absorb these costs and will shut down.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The $50,000 per violation penalty is excessive and will create a cottage industry of frivolous litigation. Healthcare providers will practice defensive data management, withholding information sharing that could benefit patient care, out of fear of liability.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I work in health data analytics. The opt-in consent requirement will dramatically reduce datasets available for population health research. Opt-in models typically achieve only 5-10% participation rates, which are insufficient for statistically valid research.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The right to delete data conflicts with medical record retention requirements. Healthcare providers are legally required to maintain records for specified periods. This amendment creates a direct conflict between patient rights and provider obligations that will create legal confusion.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The definition of health-adjacent data is dangerously broad. If a step-counting app is covered, what about a weather app that affects allergy sufferers? A restaurant review app that tracks dietary preferences? The scope creep will extend regulatory burden to countless unrelated industries.", "stance": "oppose", "sentiment": "negative"},
        {"body": "As a medical researcher studying rare diseases, I rely on large datasets to identify patterns and develop treatments. The consent requirements in this amendment would make it virtually impossible to conduct the kind of population-level studies that lead to medical breakthroughs.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The amendment should include provisions for de-identified data. Properly anonymized datasets should be exempt from consent requirements, as they pose no privacy risk while enabling valuable research that benefits all patients.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I support the intent but am concerned about interoperability. Currently, getting medical records transferred between providers is already difficult. We need to ensure that privacy protections do not further fragment the health data ecosystem.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment should distinguish between data used for clinical purposes and data used for commercial purposes. Legitimate clinical uses should be permitted with appropriate safeguards, while commercial exploitation should require explicit consent.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I believe this amendment strikes the right balance between privacy and access. The opt-in consent requirement applies only to non-treatment purposes, so clinical care will not be affected. Research can continue with de-identified datasets and IRB-approved protocols.", "stance": "support", "sentiment": "positive"},
    ]
}

# ---------------------------------------------------------------------------
# AMENDMENT 5: Student Digital Privacy (EDUCATION) — ~30 comments
# ---------------------------------------------------------------------------
AMENDMENT_5 = {
    "title": "Student Digital Privacy and Educational Technology Accountability Act",
    "body": (
        "This amendment establishes comprehensive protections for student data collected by "
        "educational technology platforms. It prohibits the use of student data for targeted "
        "advertising, requires parental consent for data collection from students under 16, "
        "mandates annual transparency reports from EdTech companies detailing what data is "
        "collected and how it is used, establishes a Student Data Bill of Rights including the "
        "right to data portability and deletion upon graduation, and creates cybersecurity "
        "standards for educational institutions receiving federal funding."
    ),
    "category": "EDUCATION",
    "comments": [
        {"body": "As a parent, I am horrified by the amount of data that educational technology companies collect about my children. From keystroke patterns to facial recognition during online exams, the surveillance is pervasive and deeply concerning. This amendment is urgently needed to protect our children.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am a high school teacher who was required to use multiple EdTech platforms during the pandemic. I was shocked to discover that student behavioral data was being used to build advertising profiles. These are children — they deserve protection, not exploitation.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The Student Data Bill of Rights is the most important provision. Currently, when students graduate, their data remains with EdTech companies indefinitely. The right to deletion upon graduation ensures that youthful data does not follow students into adulthood.", "stance": "support", "sentiment": "positive"},
        {"body": "The prohibition on targeted advertising using student data should be absolute and unambiguous. Currently, some platforms claim they do not sell data while using it internally to serve targeted content. This loophole must be closed by this amendment.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "Cybersecurity standards for educational institutions are critical. Schools have become prime targets for ransomware attacks, with dozens of districts affected annually. Student social security numbers, grades, disciplinary records, and health information have been exposed.", "stance": "support", "sentiment": "positive"},
        {"body": "I work at an EdTech startup, and I support reasonable regulation of our industry. The lack of clear rules creates an uneven playing field where responsible companies are undercut by competitors who monetize student data. Clear standards benefit everyone.", "stance": "support", "sentiment": "positive"},
        {"body": "As a school administrator, I can tell you that our district has virtually no capacity to evaluate the privacy practices of the dozens of EdTech vendors we use. Federal standards would actually help us by providing clear criteria for vendor selection.", "stance": "support", "sentiment": "positive"},
        {"body": "The data portability provision is forward-thinking. Students should be able to take their learning portfolios when they change schools or graduate. Currently, years of academic work are locked into proprietary platforms that students lose access to.", "stance": "support", "sentiment": "positive"},
        {"body": "I am a child psychologist who has studied the effects of surveillance on adolescent development. Constant monitoring creates anxiety and inhibits the risk-taking that is essential for learning and growth. Students need digital spaces where they can explore freely.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "As a college student, I was horrified to learn that the proctoring software used during my exams was scanning my face and tracking my eye movements. This level of surveillance is dehumanizing and has no place in education. I support this amendment fully.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I represent a group of educators who have seen how AI-powered surveillance tools disproportionately flag students of color and students with disabilities. This amendment should include explicit anti-discrimination provisions for algorithmic monitoring systems used in schools.", "stance": "support", "sentiment": "positive"},
        {"body": "The parental consent requirement for students under 16 will create enormous administrative burden for schools. Managing consent forms for every student on every platform is logistically impractical, especially in districts with limited IT staff and resources.", "stance": "oppose", "sentiment": "negative"},
        {"body": "This amendment will devastate the EdTech industry. Many companies rely on data analytics to improve their products and sustain free or low-cost offerings for schools. If they cannot analyze student data, they will charge schools significantly more or shut down.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The annual transparency reporting requirement is excessively burdensome. Small EdTech companies do not have the resources to produce detailed reports. This will consolidate the market in favor of large corporations like Google and Microsoft who can absorb compliance costs.", "stance": "oppose", "sentiment": "negative"},
        {"body": "Adaptive learning technology requires data to personalize instruction for each student. Restricting data collection will reduce the effectiveness of these tools and harm the students they are designed to help. We should not let privacy fears prevent educational innovation.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The age threshold of 16 is arbitrary and overly restrictive. COPPA already covers children under 13. High school students aged 14-16 are capable of understanding and providing informed consent for educational applications they use daily.", "stance": "oppose", "sentiment": "negative"},
        {"body": "Public schools are already underfunded. Imposing cybersecurity standards without providing additional funding is an unfunded mandate that will force schools to divert resources from instruction to IT compliance. The federal government must put money behind its mandates.", "stance": "oppose", "sentiment": "negative"},
        {"body": "As a student with a learning disability, adaptive technology has been transformative for me. These tools use my data to adjust lesson difficulty and provide targeted support. I worry that overly broad restrictions could undermine the assistive technologies I depend on.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I support student privacy protections but believe the age threshold should be 13, aligned with COPPA. High school students aged 14-16 should not need parental permission for every educational app — this creates practical barriers to learning.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment should distinguish between data used for educational purposes and data used for commercial purposes. Legitimate educational uses — tracking progress, identifying at-risk students, improving curriculum — should be permitted with appropriate safeguards.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I support this amendment but believe it should include mandatory digital citizenship education alongside data protections. Students need to understand their digital rights and how to protect themselves — legislation alone is not enough.", "stance": "neutral", "sentiment": "neutral"},
    ]
}

# ---------------------------------------------------------------------------
# AMENDMENT 6: Tax Reform for Small Businesses (TAXATION) — ~30 comments
# ---------------------------------------------------------------------------
AMENDMENT_6 = {
    "title": "Small Business Tax Fairness and Economic Opportunity Act",
    "body": (
        "This amendment reforms the tax code to reduce the tax burden on small businesses with "
        "annual revenues below $10 million. It lowers the effective tax rate for qualifying "
        "businesses to 15%, creates an enhanced deduction for health insurance costs incurred "
        "by small employers, establishes a five-year loss carryforward provision for startup "
        "businesses, simplifies quarterly tax filing requirements, and creates tax credits for "
        "small businesses that hire workers from economically disadvantaged backgrounds. The "
        "revenue impact is offset by closing corporate tax loopholes used primarily by large "
        "multinational corporations."
    ),
    "category": "TAXATION",
    "comments": [
        {"body": "As a small business owner with 12 employees, I spend more time dealing with tax compliance than actually growing my business. The simplified quarterly filing alone would save me thousands of dollars in accounting fees. This amendment is a lifeline for small enterprises like mine.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The enhanced health insurance deduction is critically important. As a small employer, providing health coverage to my employees costs nearly as much as their salaries. Any tax relief in this area helps me compete for talent against large corporations that can negotiate better rates.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I started my business two years ago and lost money both years due to initial investment costs. The five-year loss carryforward provision recognizes that startups need time to become profitable and should not be penalized for investing in future growth during their early years.", "stance": "support", "sentiment": "positive"},
        {"body": "The hiring tax credits for disadvantaged workers combine good economics with good social policy. Small businesses are the largest job creators in America, and incentivizing them to hire from underserved communities creates opportunity where it is needed most.", "stance": "support", "sentiment": "positive"},
        {"body": "Closing corporate tax loopholes used by large multinationals to offset revenue losses is both fair and practical. These loopholes allow billion-dollar companies to pay effective tax rates lower than their small business competitors. Leveling the playing field is long overdue.", "stance": "support", "sentiment": "positive"},
        {"body": "I run a small manufacturing company in Ohio. We compete directly with products from large corporations that shift profits overseas to avoid taxes. This amendment would help level the competitive landscape and keep American small manufacturers viable.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The $10 million revenue threshold is appropriate. It captures the vast majority of genuinely small businesses while excluding larger companies that have access to sophisticated tax planning and lobbying resources. This is targeted relief for those who need it most.", "stance": "support", "sentiment": "positive"},
        {"body": "As a first-generation immigrant who started a business with $5,000 in savings, I can attest that the tax burden on small businesses is crushing in the early years. This amendment would make the American Dream more accessible to entrepreneurs from all backgrounds.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am an accountant who serves small business clients. The current quarterly filing requirements are unnecessarily complex and create significant compliance costs. Simplification would allow my clients to redirect those resources toward growing their businesses.", "stance": "support", "sentiment": "positive"},
        {"body": "Small businesses create two-thirds of new jobs in America. Any policy that helps them thrive helps the entire economy. This amendment is smart economic policy that will generate returns far exceeding its cost.", "stance": "support", "sentiment": "positive"},
        {"body": "This amendment picks winners and losers by providing preferential tax treatment to certain businesses based solely on size. The tax code should be neutral. If we want lower tax rates, we should lower them for all businesses, not just those below an arbitrary revenue threshold.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The revenue offset from closing so-called loopholes is overly optimistic. These provisions are legal tax planning strategies that serve legitimate business purposes. Eliminating them will drive corporate investment overseas and reduce total tax revenue, not increase it.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "The $10 million threshold creates a perverse incentive. Businesses approaching that threshold will deliberately limit growth to maintain their preferential tax rate. This is the opposite of what tax policy should do — it punishes success and discourages scaling.", "stance": "oppose", "sentiment": "negative"},
        {"body": "As a tax policy researcher, I am concerned about the complexity this adds to an already incomprehensible tax code. Each new deduction, credit, and threshold creates opportunities for abuse and increases compliance costs. We need simplification, not more special provisions.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The hiring tax credits sound good in theory but are ripe for abuse. Previous programs showed that many businesses simply claimed credits for hires they would have made anyway. The deadweight loss from these programs typically exceeds the benefits.", "stance": "oppose", "sentiment": "negative"},
        {"body": "Lowering the effective rate to 15% for small businesses while maintaining higher rates for larger companies creates an arbitrage opportunity. Sophisticated investors will restructure their holdings into multiple small entities to capture the lower rate.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The loss carryforward provision is reasonable but should be paired with guardrails to prevent abuse. Without limits, some taxpayers will use artificial losses from shell entities to offset income from profitable operations indefinitely.", "stance": "oppose", "sentiment": "negative"},
        {"body": "I support tax relief for small businesses but believe this amendment is too narrowly focused. A broader reform that simplifies the entire tax code would provide more sustainable and equitable benefits than targeted provisions that will be eroded by future legislation.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The health insurance deduction enhancement is well-intentioned but addresses a symptom rather than the root cause. The real problem is the cost of healthcare itself. Until we address healthcare pricing, tax deductions simply shift the burden to taxpayers.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I agree with the principle of reducing small business tax burden but question whether $10 million is the right threshold. In some industries and high-cost regions, $10 million in revenue represents a genuinely small operation. In others, it is a substantial enterprise.", "stance": "neutral", "sentiment": "neutral"},
    ]
}

# ---------------------------------------------------------------------------
# AMENDMENT 7: National Defense and Cybersecurity (DEFENSE) — ~30 comments
# ---------------------------------------------------------------------------
AMENDMENT_7 = {
    "title": "National Cybersecurity Infrastructure and Critical Defense Systems Act",
    "body": (
        "This amendment allocates $15 billion toward modernizing the nation's cybersecurity "
        "infrastructure for critical systems including power grids, water treatment facilities, "
        "transportation networks, and financial systems. It establishes mandatory cybersecurity "
        "standards for critical infrastructure operators, creates a National Cybersecurity "
        "Response Force to coordinate federal, state, and private sector responses to cyber "
        "attacks, mandates real-time threat intelligence sharing between government agencies and "
        "critical infrastructure operators, and requires annual penetration testing and security "
        "assessments of all designated critical infrastructure."
    ),
    "category": "DEFENSE",
    "comments": [
        {"body": "The threat of cyber attacks on critical infrastructure is real and growing. The Colonial Pipeline attack demonstrated how vulnerable our essential systems are. This amendment is a critical investment in national security that is long overdue.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "I am a cybersecurity professional who has conducted assessments of critical infrastructure systems. The state of security in many water treatment facilities, power plants, and transportation systems is alarming. Some are running decades-old software with known vulnerabilities.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The National Cybersecurity Response Force is an excellent concept. Currently, when a major cyber attack occurs, the response is fragmented across dozens of federal agencies, state governments, and private companies. Coordination is essential for effective incident response.", "stance": "support", "sentiment": "positive"},
        {"body": "Mandatory cybersecurity standards for critical infrastructure are absolutely necessary. The current voluntary approach has clearly failed — too many operators treat cybersecurity as an optional expense rather than a fundamental requirement. Market forces alone cannot solve this.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "Real-time threat intelligence sharing between government and the private sector is critical. Too often, the government has information about threats that it does not share with the companies being targeted, and vice versa. This information asymmetry benefits only the attackers.", "stance": "support", "sentiment": "positive"},
        {"body": "As a military veteran who served in cyber operations, I can confirm that nation-state actors are actively probing and mapping our critical infrastructure for potential future attacks. The question is not if a major cyber attack on US infrastructure will occur, but when.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "Annual penetration testing should be the bare minimum. Critical infrastructure systems should be continuously monitored and tested. The threat landscape evolves daily, and annual assessments may miss vulnerabilities that emerge between testing cycles.", "stance": "support", "sentiment": "positive"},
        {"body": "I represent a water utility serving 200,000 customers. The Oldsmar, Florida incident — where hackers attempted to poison a town's water supply — was a wake-up call for our industry. We support mandatory cybersecurity standards and welcome the federal funding to achieve them.", "stance": "support", "sentiment": "strongly_positive"},
        {"body": "The $15 billion price tag is a bargain compared to the potential cost of a successful large-scale cyber attack on critical infrastructure. The economic damage from a sustained attack on the power grid alone could exceed $1 trillion.", "stance": "support", "sentiment": "positive"},
        {"body": "I am a professor of computer science specializing in cybersecurity. This amendment correctly identifies that our critical infrastructure was designed for reliability and safety, not security. Retrofitting security into these systems requires significant investment.", "stance": "support", "sentiment": "positive"},
        {"body": "As someone who works in electrical grid operations, I support the goals of this amendment, but we need trained professionals to implement these standards. The cybersecurity talent shortage is the biggest obstacle. This amendment should include workforce development provisions.", "stance": "support", "sentiment": "positive"},
        {"body": "Mandatory cybersecurity standards will impose enormous costs on critical infrastructure operators, many of which are small municipal utilities with limited budgets. Without adequate federal funding to cover compliance costs, these mandates will lead to rate increases for consumers.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The threat intelligence sharing mandate raises serious civil liberties concerns. When governments require private companies to share network data in real-time, the line between cybersecurity and mass surveillance becomes dangerously blurred.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "Government-mandated cybersecurity standards are typically outdated by the time they are finalized. The regulatory process takes years, while cyber threats evolve daily. Prescriptive standards may actually reduce security by creating a compliance-focused mindset rather than a threat-focused one.", "stance": "oppose", "sentiment": "negative"},
        {"body": "$15 billion is a massive expenditure that will likely be plagued by the same procurement inefficiencies that affect all federal technology programs. Government cybersecurity contractors have a poor track record of delivering effective solutions on time and on budget.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The creation of another federal entity — the National Cybersecurity Response Force — will add bureaucratic layers to an already complex federal cybersecurity apparatus. We should strengthen existing agencies like CISA rather than creating new ones.", "stance": "oppose", "sentiment": "negative"},
        {"body": "Mandatory penetration testing requirements will create a windfall for cybersecurity consulting firms while doing little to actually improve security. Many critical infrastructure operators need basic security hygiene — patching, access controls, monitoring — not expensive red team exercises.", "stance": "oppose", "sentiment": "negative"},
        {"body": "The private sector is better positioned than the government to develop and implement cybersecurity solutions. Companies like CrowdStrike and Palo Alto Networks are already providing effective protection. Government mandates will crowd out private innovation.", "stance": "oppose", "sentiment": "strongly_negative"},
        {"body": "I support cybersecurity investment but believe this amendment overemphasizes defensive measures at the expense of offensive capabilities. Deterrence requires that adversaries know there will be consequences for attacking US infrastructure. Defense alone is insufficient.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment should address the root cause of many cyber vulnerabilities: the software supply chain. Most critical infrastructure systems rely on third-party software components with unknown security properties. Supply chain security standards are at least as important as perimeter defense.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "I am concerned that the focus on large-scale critical infrastructure neglects the cybersecurity needs of small businesses, which are increasingly targeted by ransomware and phishing attacks. A comprehensive national cybersecurity strategy must address threats at all levels.", "stance": "neutral", "sentiment": "neutral"},
        {"body": "The amendment should explicitly address the security of operational technology systems, which are fundamentally different from traditional IT systems. OT security requires specialized expertise and approaches that are not adequately addressed by standards designed for IT environments.", "stance": "neutral", "sentiment": "neutral"},
    ]
}


# ---------------------------------------------------------------------------
# VOTE GENERATION
# ---------------------------------------------------------------------------
def generate_votes(comments: list) -> list:
    """
    Generate realistic synthetic upvotes/downvotes per comment.
    Weights based on stance and sentiment intensity.
    """
    for comment in comments:
        sentiment = comment.get("sentiment", "neutral")
        stance = comment.get("stance", "neutral")

        if stance == "support":
            if sentiment.startswith("strongly"):
                base_up = random.randint(40, 110)
                base_down = random.randint(3, 15)
            else:
                base_up = random.randint(22, 60)
                base_down = random.randint(5, 20)
        elif stance == "oppose":
            if sentiment.startswith("strongly"):
                base_up = random.randint(20, 55)
                base_down = random.randint(15, 50)
            else:
                base_up = random.randint(15, 40)
                base_down = random.randint(10, 35)
        else:
            base_up = random.randint(10, 35)
            base_down = random.randint(8, 28)

        noise_up = random.randint(-3, 5)
        noise_down = random.randint(-2, 4)
        comment["upvotes"] = max(1, base_up + noise_up)
        comment["downvotes"] = max(0, base_down + noise_down)

    return comments


# ---------------------------------------------------------------------------
# BUILD AND WRITE DATASET
# ---------------------------------------------------------------------------
def main():
    all_amendments = [AMENDMENT_1, AMENDMENT_2, AMENDMENT_3, AMENDMENT_4, AMENDMENT_5, AMENDMENT_6, AMENDMENT_7]

    dataset = {"users": USERS, "amendments": []}

    global_idx = 0
    total_comments = 0
    total_up = 0
    total_down = 0
    total_api_calls = 0

    print("=" * 65)
    print("CivicLens Dataset Summary")
    print("=" * 65)

    for amd in all_amendments:
        comments = generate_votes(amd["comments"])
        formatted = []
        for c in comments:
            formatted.append({
                "body": c["body"],
                "user_index": global_idx % len(USERS),
                "upvotes": c["upvotes"],
                "downvotes": c["downvotes"],
                "sentiment": c.get("sentiment", "neutral"),
                "stance": c.get("stance", "neutral"),
            })
            global_idx += 1

        dataset["amendments"].append({
            "title": amd["title"],
            "body": amd["body"],
            "category": amd["category"],
            "status": "ACTIVE",
            "comments": formatted,
        })

        nc = len(formatted)
        api_calls = nc + (nc + 31) // 32 + 1  # classifier + sentiment batches + summarizer
        total_comments += nc
        total_up += sum(c["upvotes"] for c in formatted)
        total_down += sum(c["downvotes"] for c in formatted)
        total_api_calls += api_calls

        opp = sum(1 for c in formatted if c["stance"] == "oppose")
        sup = sum(1 for c in formatted if c["stance"] == "support")
        neu = sum(1 for c in formatted if c["stance"] == "neutral")
        print(f"\n  [{amd['category']}] {amd['title'][:55]}...")
        print(f"    Comments: {nc}  |  Support: {sup}  Oppose: {opp}  Neutral: {neu}")
        print(f"    Est. HF API calls: {api_calls}")

    print(f"\n{'=' * 65}")
    print(f"  TOTALS:")
    print(f"    Amendments:        {len(dataset['amendments'])}")
    print(f"    Total comments:    {total_comments}")
    print(f"    Total upvotes:     {total_up}")
    print(f"    Total downvotes:   {total_down}")
    print(f"    Users:             {len(USERS)}")
    print(f"    Est. total API calls (all amendments): {total_api_calls}")
    print(f"    HF free tier limit: ~1000/hr -> {'SAFE' if total_api_calls < 800 else 'CAUTION'}")
    print(f"{'=' * 65}")

    with open("fcc_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\nDataset written to: fcc_dataset.json")


if __name__ == "__main__":
    main()
