import os

# Categories and their sample text
categories = {
    "Legal": [
        "A detailed employment contract specifying the terms of engagement, job responsibilities, compensation details, non-compete clauses, termination conditions, and arbitration procedures for dispute resolution.",
        "A non-disclosure agreement (NDA) tailored for a software development project, including clauses to protect source code, algorithms, and trade secrets, along with penalties for unauthorized disclosures.",
        "A court ruling summary detailing the outcome of a high-profile intellectual property dispute, outlining key arguments, judicial reasoning, and the impact on existing copyright laws.",
        "Terms and conditions of a SaaS platform, explaining subscription plans, refund policies, data ownership, limitations of liability, and the governing jurisdiction for legal disputes."
    ],
    "Finance": [
        "A quarterly earnings report breaking down revenue by product categories, regions, and customer demographics. The report includes net income, operating margins, and strategic initiatives that drove growth.",
        "A balance sheet showing a detailed breakdown of current and non-current assets, equity distribution among stakeholders, and a detailed note on financial risks such as market volatility and credit defaults.",
        "An investment proposal analyzing real estate opportunities in emerging markets, highlighting ROI, risk assessments, and diversification benefits backed by historical market trends.",
        "A comprehensive budget plan for a manufacturing company, including cost allocation for raw materials, labor, marketing, logistics, and R&D initiatives. The plan is aligned with projected production volumes."
    ],
    "Healthcare": [
        "A clinical trial report evaluating a new vaccine, including data on test subjects, dosage schedules, efficacy rates across age groups, and a breakdown of side effects observed during the trial phases.",
        "A hospital's operational improvement plan emphasizing the integration of telemedicine, patient feedback mechanisms, and digital tools for better patient records management.",
        "A whitepaper discussing the role of AI in early cancer detection, backed by case studies, algorithms used, and a comparison of AI diagnostics with traditional methods.",
        "A nutrition guide for managing chronic illnesses like diabetes and hypertension, with tailored meal plans, suggested physical activities, and medical consultation recommendations."
    ],
    "Technology": [
        "A research paper detailing advancements in quantum computing, including the latest algorithms for cryptography and a discussion on their potential applications in industries like finance and healthcare.",
        "A user manual for a home automation system, including installation instructions, troubleshooting for connectivity issues, and tips for integrating devices like smart thermostats and security cameras.",
        "A market analysis report evaluating the adoption rates of 5G technology across different regions, challenges in deployment, and its implications for IoT and autonomous vehicles.",
        "A product specifications document for a new graphics processing unit (GPU), detailing core performance metrics such as processing speed, power consumption, and compatibility with major software platforms."
    ],
    "Education": [
        "A curriculum framework for K-12 schools focusing on STEM education, with modules on robotics, coding languages, and environmental science projects designed for experiential learning.",
        "A report analyzing the impact of online learning platforms during the COVID-19 pandemic, including user engagement data, accessibility challenges, and proposed solutions for digital inclusivity.",
        "An academic research paper on the effectiveness of competency-based learning compared to traditional grade-based systems, supported by longitudinal studies from diverse educational settings.",
        "A student guide to scholarships for international studies, detailing eligibility criteria, application processes, deadlines, and tips for writing effective personal statements."
    ],
    "Marketing": [
        "A market segmentation study for a beverage company, dividing customers by age, income, and lifestyle. The study includes personalized marketing strategies for each segment and projected sales uplift.",
        "A comprehensive guide on using social media for brand building, with a focus on content strategies for Instagram, TikTok, and LinkedIn, along with metrics for measuring campaign success.",
        "A case study of a successful rebranding effort, highlighting changes in logo design, messaging, target demographics, and the ROI from updated marketing campaigns.",
        "A report on email marketing strategies, detailing best practices for subject lines, personalization techniques, optimal sending times, and avoiding spam filters."
    ],
    "Human Resources (HR)": [
        "An employee handbook detailing workplace policies on attendance, dress code, harassment prevention, performance reviews, and professional development programs.",
        "A diversity, equity, and inclusion (DEI) strategy document outlining measurable goals for hiring underrepresented groups, training programs to reduce unconscious bias, and regular progress reporting.",
        "A recruitment plan for a technology company, specifying job roles, candidate persona definitions, sourcing strategies, and interview formats tailored to assess technical and cultural fit.",
        "A report on trends in employee engagement, discussing the impact of hybrid work environments, mental health initiatives, and gamified performance tracking tools."
    ],
    "Government & Policy": [
        "A government whitepaper outlining a roadmap for renewable energy adoption, with specific goals for wind, solar, and hydroelectric energy capacity over the next decade.",
        "An analysis of a newly implemented tax reform, discussing its impact on small businesses, middle-income families, and foreign investments in the country.",
        "A policy brief on urban housing shortages, proposing solutions like vertical expansion, affordable housing incentives, and public-private partnerships for sustainable development.",
        "A report on the socio-economic impacts of free education programs in rural areas, supported by statistics on literacy rates, employment levels, and community development indicators."
    ],
    "Retail & E-commerce": [
        "A business report on the growth of direct-to-consumer (DTC) brands in the fashion sector, including strategies for customer acquisition, pricing, and product diversification.",
        "A step-by-step guide for setting up an e-commerce store, covering platform selection, payment gateway integration, inventory management, and customer support setup.",
        "A sales performance report for a seasonal sale campaign, analyzing top-performing product categories, conversion rates, and the impact of discounting strategies.",
        "A loyalty program analysis comparing tier-based and points-based systems, with customer feedback surveys and retention metrics across different age groups."
    ],
    "Science": [
        "A journal article on the effects of climate change on Arctic ecosystems, including data on melting ice caps, changes in species migration patterns, and long-term global implications.",
        "A laboratory experiment report studying the efficiency of different materials in solar cell technology, supported by graphs showing energy output under varying conditions.",
        "A study on the human genome project’s latest findings, including breakthroughs in personalized medicine and ethical considerations around genetic data privacy.",
        "A whitepaper discussing the role of CRISPR technology in genetic engineering, with potential applications in agriculture, medicine, and environmental restoration."
    ],
    "News & Media": [
        "An investigative article on the rise of misinformation on social media, supported by case studies of viral fake news and the platforms' responses to address the issue.",
        "A press release announcing the launch of a new media streaming platform, detailing its unique features, subscription plans, and partnerships with content creators.",
        "An editorial discussing the role of journalism in a post-truth era, reflecting on challenges such as public trust, press freedom, and financial sustainability.",
        "A report summarizing the outcomes of a major international conference, including key resolutions, participating countries, and implications for global policies."
    ],
    "Travel & Tourism": [
        "A travel guide to exploring the historic sites of Italy, including recommendations for accommodations, local cuisine, transportation tips, and must-visit destinations.",
        "A hotel brochure highlighting luxury amenities, room packages, and promotional offers for family and business travelers.",
        "A report on the economic impact of tourism in Southeast Asia, with data on foreign arrivals, revenue generation, and employment opportunities created by the industry.",
        "An itinerary for a 7-day trekking adventure in the Himalayas, complete with details on routes, gear recommendations, and weather conditions."
    ],
    "Real Estate": [
        "A property investment analysis report comparing ROI across residential, commercial, and mixed-use developments in urban areas.",
        "A detailed property listing showcasing a luxury villa, including high-resolution photos, descriptions of features, neighborhood highlights, and pricing breakdowns.",
        "A report on real estate market trends, analyzing the impact of interest rate fluctuations on property prices and buyer behavior.",
        "A rental agreement template covering terms such as rent payment schedules, maintenance responsibilities, and conditions for lease termination."
    ],
    "Entertainment": [
        "A movie production plan detailing the budget allocation for casting, locations, special effects, and promotional campaigns.",
        "A concert program outlining the lineup of performers, event schedule, ticket pricing tiers, and sponsorship details.",
        "A review of a newly released video game, discussing its storyline, graphics, gameplay mechanics, and reception among gaming communities.",
        "A script for a TV commercial promoting a consumer product, including dialogue, visual elements, and target audience considerations."
    ],
    "Personal Documents": [
        "A personal resume highlighting academic achievements, professional experience, skills, and references.",
        "A diary entry reflecting on a major life event, discussing personal emotions, lessons learned, and future plans.",
        "A household budget plan for managing monthly expenses, including categories for rent, utilities, groceries, and savings goals.",
        "A letter of recommendation for a student applying to graduate school, detailing their academic performance, work ethic, and leadership skills."
    ],
    "Business Operations": [
        "A project management report summarizing milestones achieved, resources used, and pending tasks for a product development initiative.",
        "A workflow process document for onboarding new employees, detailing steps like IT setup, policy orientation, and role-specific training.",
        "An operations audit report highlighting inefficiencies in supply chain management and recommending technology solutions for optimization.",
        "A vendor agreement for procuring raw materials, specifying delivery timelines, quality standards, and penalties for non-compliance."
    ],
    "Environment & Sustainability": [
        "An environmental impact assessment report for a proposed construction project, analyzing its effects on local ecosystems and recommending mitigation measures.",
        "A case study on a company's carbon offset initiatives, highlighting renewable energy adoption, waste reduction strategies, and progress toward net-zero goals.",
        "A guide for individuals on reducing household energy consumption, including tips for using energy-efficient appliances and adopting renewable energy sources.",
        "A research paper on the impact of deforestation on biodiversity, discussing causes, affected species, and global restoration efforts."
    ],
    "Sports": [
        "A post-match analysis highlighting strategic plays, player statistics, and turning points in a major soccer league final.",
        "A biography of a legendary athlete, covering their career milestones, personal life, and philanthropic efforts.",
        "A training regimen for marathon runners, including weekly schedules, nutrition tips, and recovery strategies.",
        "An article exploring the rise of fantasy sports leagues and their impact on fan engagement and sponsorships."
    ],
    "Fashion": [
        "A catalog featuring a luxury clothing line, complete with fabric details, styling tips, and pricing information.",
        "A trend report analyzing the influence of cultural diversity on global fashion trends over the past decade.",
        "A technical specification sheet for a new sneaker design, detailing materials, ergonomics, and production methods.",
        "An interview with a prominent designer discussing the inspiration behind their latest collection and industry challenges."
    ],
    "Food & Beverages": [
        "A restaurant's recipe book showcasing signature dishes, including preparation techniques, ingredient sourcing, and plating tips.",
        "A supply chain analysis of a coffee brand, highlighting ethical sourcing practices and partnerships with local farmers.",
        "A market study evaluating the growth of plant-based food products in urban markets, with sales projections for the next five years.",
        "A blog post featuring creative holiday-themed cocktail recipes, complete with pairing suggestions and garnish ideas."
    ]
}


# Create the processed folder if it doesn't exist
PROCESSED_FOLDER = "processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Write documents to the folder
for category, texts in categories.items():
    for i, text in enumerate(texts, start=1):
        filename = f"{category}{i}.txt"
        filepath = os.path.join(PROCESSED_FOLDER, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)

print(f"Sample dataset created in the '{PROCESSED_FOLDER}' folder.")
