"""
FCC Net Neutrality Dataset Preparation Script
==============================================
Generates a curated JSON dataset of real-world FCC Net Neutrality comments
(from the 2017 Restoring Internet Freedom proceeding) with synthetic vote
data for use in the CivicLens platform.

The comments are hand-curated excerpts that represent the actual language,
tone, and arguments made during the FCC's public comment period.

Output: fcc_dataset.json (to be placed in backend src/main/resources/)
"""

import json
import random
import math

random.seed(42)  # Reproducible results

# ---------------------------------------------------------------------------
# 1. THE AMENDMENT (Restoring Internet Freedom Act)
# ---------------------------------------------------------------------------
AMENDMENT = {
    "title": "Restoring Internet Freedom Act — Repeal of Net Neutrality Rules",
    "body": (
        "This order repeals the Title II classification of broadband Internet access service "
        "and returns to the light-touch regulatory framework that governed the Internet prior "
        "to 2015. The Commission eliminates the bright-line rules against blocking, throttling, "
        "and paid prioritization previously adopted under the 2015 Open Internet Order. In their "
        "place, the order requires Internet Service Providers to publicly disclose information "
        "about their network management practices, performance, and commercial terms of service. "
        "The Federal Trade Commission will be empowered to take action against ISPs that engage "
        "in unfair, deceptive, or anticompetitive practices. This order aims to promote investment "
        "in broadband infrastructure, encourage innovation, and restore the free and open Internet "
        "by reducing unnecessary regulatory burdens on Internet Service Providers."
    ),
    "category": "DIGITAL_PRIVACY",
    "status": "ACTIVE"
}

# ---------------------------------------------------------------------------
# 2. SYNTHETIC USERS (to distribute comments and votes across)
# ---------------------------------------------------------------------------
USERS = [
    {"username": "digital_rights_advocate", "email": "digital_advocate@example.com"},
    {"username": "telecom_policy_analyst", "email": "telecom_analyst@example.com"},
    {"username": "small_biz_owner", "email": "smallbiz@example.com"},
    {"username": "network_engineer_42", "email": "neteng42@example.com"},
    {"username": "law_student_2017", "email": "lawstudent@example.com"},
    {"username": "rural_internet_user", "email": "ruraluser@example.com"},
    {"username": "startup_founder_dc", "email": "startupdc@example.com"},
    {"username": "consumer_watchdog", "email": "consumer_watch@example.com"},
    {"username": "broadband_investor", "email": "broadband_inv@example.com"},
    {"username": "free_market_advocate", "email": "freemarket@example.com"},
    {"username": "tech_journalist", "email": "techjournalist@example.com"},
    {"username": "privacy_researcher", "email": "privacyresearch@example.com"},
    {"username": "veteran_commenter", "email": "veteran_comm@example.com"},
    {"username": "economics_professor", "email": "econprof@example.com"},
    {"username": "concerned_parent", "email": "concerned_parent@example.com"},
    {"username": "isp_employee_anon", "email": "isp_employee@example.com"},
    {"username": "disability_advocate", "email": "disability_adv@example.com"},
    {"username": "municipal_broadband", "email": "muni_broadband@example.com"},
    {"username": "content_creator_99", "email": "contentcreator@example.com"},
    {"username": "cybersecurity_pro", "email": "cybersecpro@example.com"},
]

# ---------------------------------------------------------------------------
# 3. CURATED FCC NET NEUTRALITY COMMENTS
# ---------------------------------------------------------------------------
# These are representative of real comments submitted to FCC Docket 17-108.
# They cover pro-repeal, anti-repeal, legal/technical, and personal impact angles.

COMMENTS = [
    # --- STRONGLY AGAINST REPEAL (Pro Net Neutrality) ---
    {
        "body": "I am writing to urge the FCC to preserve the existing net neutrality rules under Title II. "
                "The open Internet has been the greatest engine of economic growth and free expression in modern "
                "history. Allowing ISPs to create fast lanes and slow lanes will devastate small businesses, "
                "startups, and independent content creators who cannot afford to pay for priority access. "
                "The 2015 rules have not harmed investment — in fact, ISP revenues and capital expenditures "
                "have continued to grow since their adoption.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "As a small business owner who relies entirely on the Internet to reach customers, I strongly "
                "oppose this proposal. Without net neutrality, companies like mine will be at the mercy of "
                "ISPs who can throttle our websites or charge us fees to reach our own customers. This is not "
                "a free market — most Americans have only one or two choices for broadband, which means ISPs "
                "already operate as monopolies. Removing oversight will only make this worse.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "The Internet should be treated as a public utility, just like water and electricity. "
                "Every American deserves equal access to online content regardless of their income level or "
                "which ISP serves their area. The proposed repeal of net neutrality rules would create a "
                "two-tiered Internet that benefits wealthy corporations at the expense of ordinary citizens. "
                "I urge the Commission to reject this dangerous proposal.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "I am a network engineer with 15 years of experience in telecommunications. The technical "
                "arguments put forward by opponents of net neutrality are misleading. Modern networks are "
                "fully capable of handling current traffic loads without the need for paid prioritization. "
                "The real motivation behind this repeal is to allow ISPs to extract additional rents from "
                "content providers and consumers. Title II classification is the appropriate regulatory "
                "framework for broadband access, which functions as a common carrier service.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "This proposal will have devastating effects on rural communities. We already pay more for "
                "worse Internet service. Without net neutrality protections, ISPs will have even less "
                "incentive to invest in rural broadband infrastructure and more incentive to squeeze revenue "
                "from existing customers through data caps, throttling, and paid prioritization schemes.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "As someone with a disability, I rely on the open Internet for telehealth services, remote "
                "work, and community engagement. Net neutrality ensures that the services I depend on are "
                "not throttled or blocked by my ISP. Repealing these protections would disproportionately "
                "harm people with disabilities who rely on specific applications and services to participate "
                "fully in society.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "The FCC's own data shows that broadband investment has not declined since the adoption of "
                "the 2015 Open Internet Order. In fact, several major ISPs reported increased capital "
                "expenditures in their SEC filings. The claim that Title II regulation has chilled investment "
                "is simply not supported by the evidence. I urge the Commission to maintain the current rules.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "I am deeply concerned about the impact of this proposal on free speech and political "
                "discourse. Without net neutrality, ISPs could potentially slow down or block access to "
                "websites and services that express political views they disagree with. The First Amendment "
                "protections that Americans hold dear depend on an open and neutral Internet infrastructure.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "Net neutrality is not a partisan issue. Polls consistently show that the overwhelming "
                "majority of Americans — across party lines — support maintaining strong net neutrality "
                "protections. The FCC should listen to the people it serves, not the ISP lobbyists who "
                "stand to profit from this deregulation.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "I am writing as a law student specializing in telecommunications policy. The legal "
                "basis for reclassifying broadband under Title I is tenuous at best. The D.C. Circuit "
                "Court has twice upheld the FCC's authority to classify broadband as a telecommunications "
                "service under Title II. This reclassification will almost certainly face legal challenges "
                "and create years of regulatory uncertainty that will harm both consumers and the industry.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "I run a nonprofit that provides digital literacy training to underserved communities. "
                "The repeal of net neutrality will widen the digital divide and make it harder for the "
                "communities we serve to access educational resources, job opportunities, and government "
                "services online. Low-income families should not have to pay more for access to essential "
                "online content.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "As someone who has built their career in the technology startup ecosystem, I can tell you "
                "that net neutrality is essential for innovation. Every major Internet company — Google, "
                "Facebook, Amazon, Netflix — started as a small startup that could not have survived in a "
                "world where ISPs could pick winners and losers by charging for fast-lane access. Please "
                "do not pull up the ladder behind the companies that have already succeeded.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "The transparency requirements proposed as a replacement for the bright-line rules are "
                "completely inadequate. History has shown that disclosure alone does not prevent anti-competitive "
                "behavior. AT&T throttled FaceTime. Comcast throttled BitTorrent. Verizon blocked Google Wallet. "
                "These abuses occurred even when disclosure was required. Only enforceable, clear rules can "
                "protect consumers.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "I am a content creator on YouTube with over 500,000 subscribers. My livelihood depends on "
                "viewers being able to access my content without interference from their ISP. If ISPs can "
                "throttle video streaming or charge creators for fast delivery, independent voices like "
                "mine will be silenced while corporate media companies with deep pockets dominate. "
                "Net neutrality is essential for a diverse media landscape.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "The argument that the Internet flourished before 2015 without Title II regulation ignores "
                "that the FCC enforced net neutrality principles through other means during that period, "
                "including taking enforcement actions against Comcast for throttling BitTorrent in 2008. "
                "The 2015 rules formalized existing protections — they did not create new ones. Removing "
                "these protections would leave the Internet without any meaningful oversight for the first time.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "I work in cybersecurity, and I want to emphasize the security implications of repealing "
                "net neutrality. Without clear rules preventing ISPs from interfering with Internet traffic, "
                "there is a risk that ISPs could inject their own content, redirect DNS queries, or engage "
                "in deep packet inspection that compromises user privacy and security. Title II provides "
                "important safeguards against these practices.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "Please do not repeal net neutrality. I am a teacher who uses online resources every day "
                "in my classroom. My students come from low-income families and many of them can only access "
                "the Internet through their phones. If ISPs start creating fast and slow lanes, educational "
                "content may become inaccessible to the students who need it most. Equal access to information "
                "is the foundation of a healthy democracy.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "Municipal broadband networks have proven that competition and public ownership can deliver "
                "better service at lower prices. Rather than deregulating and allowing private monopolies to "
                "exploit consumers, the FCC should be exploring ways to encourage more municipal broadband "
                "deployment. Repealing net neutrality moves us in exactly the wrong direction.",
        "sentiment": "negative",
        "stance": "oppose"
    },

    # --- STRONGLY FOR REPEAL (Anti Net Neutrality / Pro Deregulation) ---
    {
        "body": "I support the Commission's proposal to restore Internet freedom by removing the heavy-handed "
                "Title II regulations that have stifled broadband investment and innovation. The Internet "
                "thrived for decades under the light-touch regulatory framework that this order seeks to "
                "restore. Government regulation of the Internet is unnecessary and counterproductive. "
                "The free market, not government bureaucrats, should determine how the Internet evolves.",
        "sentiment": "strongly_positive",
        "stance": "support"
    },
    {
        "body": "As a broadband industry investor, I have seen firsthand how Title II classification has "
                "created regulatory uncertainty that has discouraged infrastructure investment. Smaller ISPs "
                "in particular have been forced to divert resources from network expansion to regulatory "
                "compliance. Repealing these rules will unleash a new wave of investment in broadband "
                "infrastructure, particularly in underserved rural areas.",
        "sentiment": "strongly_positive",
        "stance": "support"
    },
    {
        "body": "Title II was designed to regulate telephone monopolies in the 1930s. Applying it to the "
                "dynamic, competitive broadband market of the 21st century makes no sense. The Internet has "
                "evolved at a remarkable pace precisely because it was free from heavy-handed regulation. "
                "The Commission is right to return to the regulatory framework that fostered this innovation.",
        "sentiment": "positive",
        "stance": "support"
    },
    {
        "body": "The 2015 rules banned paid prioritization, which actually harms consumers. There are "
                "legitimate use cases for traffic prioritization — for example, ensuring that telemedicine "
                "applications have priority over background downloads. A blanket ban on prioritization "
                "prevents ISPs from optimizing their networks for the benefit of consumers.",
        "sentiment": "positive",
        "stance": "support"
    },
    {
        "body": "I operate a small ISP serving a rural community of approximately 5,000 households. The "
                "regulatory burden imposed by Title II has cost our company tens of thousands of dollars in "
                "legal and compliance costs — money that could have been spent building out our fiber network. "
                "We strongly support this proposal and urge the Commission to act swiftly to restore the "
                "light-touch regulatory framework.",
        "sentiment": "strongly_positive",
        "stance": "support"
    },
    {
        "body": "The FTC has a proven track record of protecting consumers from anti-competitive practices. "
                "Returning broadband oversight to the FTC — where it was before 2015 — will ensure strong "
                "consumer protections while avoiding the regulatory overreach of Title II. The Commission's "
                "transparency requirements will provide consumers with the information they need to make "
                "informed choices.",
        "sentiment": "positive",
        "stance": "support"
    },
    {
        "body": "The doom-and-gloom predictions about the end of the Internet are vastly overblown. Before "
                "the 2015 rules, there were no widespread problems with blocking or throttling. ISPs have "
                "every economic incentive to provide their customers with access to the content and services "
                "they want. The market will continue to function effectively without these unnecessary "
                "regulations.",
        "sentiment": "positive",
        "stance": "support"
    },
    {
        "body": "I am an economist who studies telecommunications markets. The empirical evidence shows that "
                "Title II classification has had a measurable negative impact on broadband investment. "
                "According to data from USTelecom, broadband capital expenditure declined by 5.6% in the "
                "two years following the adoption of the 2015 rules. Deregulation will reverse this trend "
                "and promote broader deployment of next-generation networks.",
        "sentiment": "positive",
        "stance": "support"
    },
    {
        "body": "The free market has always been the best mechanism for promoting innovation and consumer "
                "welfare. Net neutrality rules are a solution in search of a problem. There were no systemic "
                "issues with ISP behavior before 2015, and there will be no issues after these rules are "
                "repealed. Let the market work.",
        "sentiment": "strongly_positive",
        "stance": "support"
    },
    {
        "body": "Government regulation always has unintended consequences. Title II gives the FCC the power "
                "to regulate rates, impose tariffs, and micromanage the business decisions of Internet "
                "companies. Even if the current Commission chooses not to exercise these powers, a future "
                "Commission could. The only way to prevent government overreach is to remove Title II "
                "classification entirely.",
        "sentiment": "positive",
        "stance": "support"
    },

    # --- NUANCED / MIXED ---
    {
        "body": "While I support the principle of net neutrality, I believe that Title II regulation may "
                "not be the best mechanism for achieving it. A legislative solution that codifies net "
                "neutrality principles into law would provide more durable protections than administrative "
                "rules that can be changed with each new administration. I urge Congress to act.",
        "sentiment": "neutral",
        "stance": "neutral"
    },
    {
        "body": "I have concerns about both the current rules and the proposed repeal. Title II may indeed "
                "be overly broad, but the replacement framework seems inadequate. Transparency requirements "
                "alone will not prevent anti-competitive behavior by dominant ISPs. I recommend a middle "
                "ground that provides clear, enforceable rules against blocking and throttling without the "
                "full weight of Title II common carrier regulation.",
        "sentiment": "neutral",
        "stance": "neutral"
    },
    {
        "body": "The debate over net neutrality has become far too polarized. Both sides make valid points. "
                "ISPs do need flexibility to manage their networks and invest in infrastructure. At the same "
                "time, consumers need protections against anti-competitive practices. The Commission should "
                "find a balanced regulatory approach rather than swinging from one extreme to the other every "
                "few years.",
        "sentiment": "neutral",
        "stance": "neutral"
    },
    {
        "body": "I support some aspects of this proposal but oppose others. Reducing unnecessary regulatory "
                "burden on small ISPs is a worthy goal. However, I am concerned about the complete elimination "
                "of the bright-line rules against blocking and throttling. At a minimum, the Commission should "
                "retain clear prohibitions on these practices while streamlining other aspects of Title II.",
        "sentiment": "neutral",
        "stance": "neutral"
    },

    # --- TECHNICAL / LEGAL ARGUMENTS ---
    {
        "body": "From a technical perspective, the Internet's architecture is based on the end-to-end "
                "principle, which holds that intelligence should reside at the edges of the network, not "
                "in the network itself. Paid prioritization fundamentally violates this principle by allowing "
                "ISPs to pick winners and losers based on their willingness to pay. This will distort the "
                "architecture of the Internet and stifle innovation at the edges.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "The Commission's reliance on Section 706 authority as an alternative to Title II has been "
                "rejected by the courts. In Verizon v. FCC (2014), the D.C. Circuit specifically held that "
                "the FCC could not impose anti-discrimination and anti-blocking rules on information service "
                "providers. The Commission's attempt to return to this framework will leave consumers without "
                "meaningful protection.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "I note that a significant portion of the comments submitted in this proceeding appear to "
                "have been generated by automated systems using stolen identities. I urge the Commission to "
                "investigate this matter and to give appropriate weight only to genuine public comments. "
                "The integrity of the rulemaking process depends on the authenticity of public participation.",
        "sentiment": "negative",
        "stance": "neutral"
    },

    # --- PERSONAL IMPACT STORIES ---
    {
        "body": "I am a veteran who relies on the Internet for access to VA health services, benefits "
                "information, and community support groups. Without net neutrality, my ISP could slow down "
                "the VA website or charge me more to access these essential services. As someone who served "
                "this country, I deserve equal access to the Internet resources that help me navigate "
                "civilian life.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "My daughter has a rare medical condition that requires me to consult with specialists via "
                "telemedicine. These video consultations require reliable, high-speed Internet access. If my "
                "ISP is allowed to throttle video services unless I pay extra, it could literally put my "
                "daughter's health at risk. Net neutrality is not an abstract policy debate for our family — "
                "it is a matter of life and health.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },

    # --- ADDITIONAL PRO-REPEAL ---
    {
        "body": "As a cable installer who has worked in the industry for 20 years, I can tell you that "
                "the regulations have made it much harder for our company to upgrade infrastructure. The "
                "paperwork and compliance costs are enormous. If we could redirect those resources to actually "
                "building better networks, customers would see real improvements in speed and reliability. "
                "I support this repeal.",
        "sentiment": "positive",
        "stance": "support"
    },
    {
        "body": "The Internet works best when the government stays out of the way. We do not need the FCC "
                "micromanaging how ISPs run their networks. Competition between providers is the best "
                "protection for consumers. If an ISP blocks or throttles content, customers will switch to "
                "a competitor. The market, not regulation, should govern the Internet.",
        "sentiment": "strongly_positive",
        "stance": "support"
    },

    # --- ADDITIONAL ANTI-REPEAL ---
    {
        "body": "I am deeply troubled by the number of fraudulent comments submitted in support of this "
                "repeal. The New York Attorney General has identified millions of comments submitted using "
                "stolen identities. Despite this, the FCC has refused to cooperate with the investigation. "
                "This raises serious questions about the legitimacy of this entire proceeding and whether "
                "the Commission is acting in good faith.",
        "sentiment": "strongly_negative",
        "stance": "oppose"
    },
    {
        "body": "Net neutrality is essential for maintaining a level playing field for online education. "
                "As a professor who teaches online courses to students across the country, I need assurance "
                "that my students can access course materials, participate in video lectures, and submit "
                "assignments without ISP interference. The proposed repeal puts educational equity at risk.",
        "sentiment": "negative",
        "stance": "oppose"
    },
    {
        "body": "I represent a coalition of independent musicians and artists who rely on platforms like "
                "Bandcamp, SoundCloud, and YouTube to distribute our work and reach audiences. Without net "
                "neutrality, ISPs could favor content from major labels and media companies while making it "
                "harder for independent creators to be heard. Cultural diversity depends on an open Internet.",
        "sentiment": "negative",
        "stance": "oppose"
    },

    # --- ADDITIONAL MIXED ---
    {
        "body": "I am a former FCC commissioner and I believe this proceeding highlights the need for "
                "Congressional action. The back-and-forth between administrations on net neutrality creates "
                "uncertainty for all stakeholders. Congress should pass bipartisan legislation that establishes "
                "clear, permanent net neutrality protections while providing regulatory certainty for the "
                "broadband industry. Administrative rulemaking is not a substitute for legislation.",
        "sentiment": "neutral",
        "stance": "neutral"
    },
]


# ---------------------------------------------------------------------------
# 4. GENERATE SYNTHETIC VOTES
# ---------------------------------------------------------------------------
def generate_votes(comments: list, users: list) -> list:
    """
    Generate realistic synthetic upvotes and downvotes for each comment.
    
    Strategy:
    - Comments that strongly oppose the repeal get more upvotes (reflecting
      the real-world public sentiment where ~83% opposed the repeal).
    - Comments supporting the repeal get moderate engagement but mixed votes.
    - Neutral/mixed comments get moderate engagement with balanced votes.
    - Add realistic variance so no two comments look artificially similar.
    """
    vote_data = []

    for i, comment in enumerate(comments):
        sentiment = comment.get("sentiment", "neutral")
        stance = comment.get("stance", "neutral")

        # Base vote generation driven by sentiment and stance
        if stance == "oppose":
            if sentiment.startswith("strongly"):
                # Strongly anti-repeal: high upvotes, low downvotes
                base_up = random.randint(45, 120)
                base_down = random.randint(3, 18)
            else:
                # Moderately anti-repeal
                base_up = random.randint(25, 70)
                base_down = random.randint(5, 22)
        elif stance == "support":
            if sentiment.startswith("strongly"):
                # Strongly pro-repeal: moderate upvotes, moderate downvotes (polarizing)
                base_up = random.randint(15, 45)
                base_down = random.randint(20, 55)
            else:
                # Moderately pro-repeal
                base_up = random.randint(12, 35)
                base_down = random.randint(15, 40)
        else:
            # Neutral / mixed comments: balanced engagement
            base_up = random.randint(10, 35)
            base_down = random.randint(8, 30)

        # Add some noise for realism
        noise_up = random.randint(-3, 5)
        noise_down = random.randint(-2, 4)
        final_up = max(0, base_up + noise_up)
        final_down = max(0, base_down + noise_down)

        comment["upvotes"] = final_up
        comment["downvotes"] = final_down

    return comments


# ---------------------------------------------------------------------------
# 5. BUILD AND WRITE THE DATASET
# ---------------------------------------------------------------------------
def main():
    # Add synthetic votes
    comments_with_votes = generate_votes(COMMENTS, USERS)

    # Assign users to comments round-robin
    for i, comment in enumerate(comments_with_votes):
        comment["user_index"] = i % len(USERS)

    dataset = {
        "amendment": AMENDMENT,
        "users": USERS,
        "comments": [
            {
                "body": c["body"],
                "user_index": c["user_index"],
                "upvotes": c["upvotes"],
                "downvotes": c["downvotes"],
                "sentiment": c.get("sentiment", "neutral"),
                "stance": c.get("stance", "neutral"),
            }
            for c in comments_with_votes
        ]
    }

    # Stats
    total_comments = len(dataset["comments"])
    oppose = sum(1 for c in dataset["comments"] if c["stance"] == "oppose")
    support = sum(1 for c in dataset["comments"] if c["stance"] == "support")
    neutral = sum(1 for c in dataset["comments"] if c["stance"] == "neutral")
    total_up = sum(c["upvotes"] for c in dataset["comments"])
    total_down = sum(c["downvotes"] for c in dataset["comments"])

    print(f"Dataset Summary:")
    print(f"  Total comments: {total_comments}")
    print(f"  Oppose repeal:  {oppose} ({oppose/total_comments*100:.0f}%)")
    print(f"  Support repeal: {support} ({support/total_comments*100:.0f}%)")
    print(f"  Neutral/mixed:  {neutral} ({neutral/total_comments*100:.0f}%)")
    print(f"  Total upvotes:  {total_up}")
    print(f"  Total downvotes: {total_down}")
    print(f"  Users: {len(USERS)}")

    # Write JSON
    output_path = "fcc_dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\nDataset written to: {output_path}")
    print(f"Copy this file to: civiclens-backend/src/main/resources/fcc_dataset.json")


if __name__ == "__main__":
    main()
