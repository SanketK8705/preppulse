import random
from datetime import datetime, timedelta
from bson import ObjectId
from app.database import get_db

# ── Exam/Subject/Chapter/Question data ───────────────────

EXAM_DATA = [
    {
        "name": "UPSC",
        "icon": "🏛️",
        "color": "#1a6b3c",
        "description": "Union Public Service Commission — Civil Services Exam",
        "subjects": [
            {
                "name": "Indian History",
                "icon": "📜",
                "chapters": [
                    {
                        "name": "Ancient India",
                        "questions": [
                            {
                                "text": "Which of the following is the oldest Veda?",
                                "options": ["Samaveda", "Rigveda", "Yajurveda", "Atharvaveda"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "Rigveda is the oldest of the four Vedas, composed around 1500–1200 BCE."
                            },
                            {
                                "text": "The Indus Valley Civilization was discovered in which year?",
                                "options": ["1901", "1911", "1921", "1931"],
                                "correct_index": 2,
                                "difficulty": "medium",
                                "explanation": "The Indus Valley Civilization was discovered in 1921 by archaeologists at Harappa."
                            },
                            {
                                "text": "Who was the founder of the Maurya Empire?",
                                "options": ["Ashoka", "Bindusara", "Chandragupta Maurya", "Bimbisara"],
                                "correct_index": 2,
                                "difficulty": "easy",
                                "explanation": "Chandragupta Maurya founded the Maurya Empire around 322 BCE with the help of Chanakya."
                            },
                            {
                                "text": "The term 'Ahimsa' was most prominently associated with which religion?",
                                "options": ["Buddhism", "Jainism", "Hinduism", "Sikhism"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "Ahimsa (non-violence) is the central tenet of Jainism, though shared by other religions too."
                            },
                            {
                                "text": "Which rock edicts of Ashoka mention his conversion to Buddhism?",
                                "options": ["Minor Rock Edict I", "Rock Edict XIII", "Pillar Edict VII", "Rock Edict XII"],
                                "correct_index": 0,
                                "difficulty": "hard",
                                "explanation": "Minor Rock Edict I describes Ashoka's conversion to Buddhism and his subsequent moral reforms."
                            },
                            {
                                "text": "The Great Bath of Mohenjo-daro was used for:",
                                "options": ["Swimming", "Irrigation", "Religious rituals", "Water storage"],
                                "correct_index": 2,
                                "difficulty": "medium",
                                "explanation": "The Great Bath is believed to have been used for ritual purification, a religious practice."
                            },
                            {
                                "text": "Which dynasty built the Ajanta Caves?",
                                "options": ["Maurya", "Gupta", "Vakataka", "Satavahana"],
                                "correct_index": 2,
                                "difficulty": "hard",
                                "explanation": "The later Ajanta caves (5th–6th century CE) were built under the patronage of the Vakataka dynasty."
                            },
                            {
                                "text": "The 'Golden Age' of ancient India is associated with which dynasty?",
                                "options": ["Maurya", "Gupta", "Kushana", "Chola"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "The Gupta period (4th–6th century CE) is called the Golden Age due to advances in art, science, and literature."
                            },
                            {
                                "text": "Who wrote Arthashastra?",
                                "options": ["Vatsyayana", "Chanakya", "Kalidasa", "Aryabhata"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "Arthashastra, a treatise on statecraft and economic policy, was written by Chanakya (Kautilya)."
                            },
                            {
                                "text": "Gandhara art style was influenced by:",
                                "options": ["Persian art", "Greek art", "Chinese art", "Egyptian art"],
                                "correct_index": 1,
                                "difficulty": "medium",
                                "explanation": "Gandhara art blended Greek and Indian styles, resulting from Alexander's campaigns in the region."
                            },
                        ]
                    },
                    {
                        "name": "Medieval India",
                        "questions": [
                            {
                                "text": "Who founded the Delhi Sultanate?",
                                "options": ["Iltutmish", "Qutb ud-Din Aibak", "Balban", "Alauddin Khilji"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "Qutb ud-Din Aibak founded the Delhi Sultanate in 1206 CE, establishing the Mamluk dynasty."
                            },
                            {
                                "text": "The Bhakti movement in South India was led by which saints?",
                                "options": ["Alvars and Nayanars", "Kabir and Mirabai", "Tukaram and Eknath", "Ramananda and Chaitanya"],
                                "correct_index": 0,
                                "difficulty": "medium",
                                "explanation": "The Alvars (Vaishnava) and Nayanars (Shaiva) were the pioneers of the Bhakti movement in South India."
                            },
                            {
                                "text": "Akbar's policy of Sulh-i-Kul means:",
                                "options": ["Peace through war", "Universal peace", "Religious tolerance", "Absolute peace"],
                                "correct_index": 2,
                                "difficulty": "medium",
                                "explanation": "Sulh-i-Kul, meaning 'peace with all', was Akbar's policy of religious tolerance and universal brotherhood."
                            },
                            {
                                "text": "The Battle of Panipat (1526) was fought between:",
                                "options": ["Akbar and Hemu", "Babur and Ibrahim Lodi", "Humayun and Sher Shah", "Babur and Rana Sanga"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "The First Battle of Panipat (1526) was fought between Babur and Ibrahim Lodi, leading to Mughal rule in India."
                            },
                            {
                                "text": "Which Mughal emperor built the Taj Mahal?",
                                "options": ["Akbar", "Humayun", "Shah Jahan", "Aurangzeb"],
                                "correct_index": 2,
                                "difficulty": "easy",
                                "explanation": "Shah Jahan built the Taj Mahal (1632–1653) in memory of his beloved wife Mumtaz Mahal."
                            },
                            {
                                "text": "The Vijayanagara Empire's peak was under which king?",
                                "options": ["Krishnadevaraya", "Harihara I", "Deva Raya II", "Saluva Narasimha"],
                                "correct_index": 0,
                                "difficulty": "medium",
                                "explanation": "Krishnadevaraya (1509–1529) brought the Vijayanagara Empire to its greatest glory."
                            },
                            {
                                "text": "Mansabdari system was introduced by:",
                                "options": ["Babur", "Humayun", "Akbar", "Jahangir"],
                                "correct_index": 2,
                                "difficulty": "medium",
                                "explanation": "Akbar introduced the Mansabdari system, a military-administrative ranking system for nobles."
                            },
                            {
                                "text": "Who was the last ruler of the Mughal Empire?",
                                "options": ["Aurangzeb", "Shah Alam II", "Bahadur Shah Zafar", "Akbar II"],
                                "correct_index": 2,
                                "difficulty": "easy",
                                "explanation": "Bahadur Shah Zafar was the last Mughal emperor, exiled by the British after the 1857 revolt."
                            },
                            {
                                "text": "The Chola dynasty is known for its:",
                                "options": ["Cave temples", "Bronze sculptures", "Step wells", "Stupas"],
                                "correct_index": 1,
                                "difficulty": "medium",
                                "explanation": "The Chola dynasty (9th–13th century) is renowned for exquisite bronze sculptures of Hindu deities."
                            },
                            {
                                "text": "Alauddin Khilji's market reforms aimed at:",
                                "options": ["Free trade", "Price control", "Monopoly trade", "Export promotion"],
                                "correct_index": 1,
                                "difficulty": "hard",
                                "explanation": "Alauddin Khilji implemented strict price control policies to maintain a large army at low cost."
                            },
                        ]
                    },
                    {
                        "name": "Modern India",
                        "questions": [
                            {
                                "text": "The Indian National Congress was founded in:",
                                "options": ["1875", "1880", "1885", "1890"],
                                "correct_index": 2,
                                "difficulty": "easy",
                                "explanation": "The Indian National Congress was founded on 28 December 1885 by A.O. Hume, Dadabhai Naoroji, and others."
                            },
                            {
                                "text": "The Partition of Bengal (1905) was reversed in:",
                                "options": ["1909", "1911", "1913", "1915"],
                                "correct_index": 1,
                                "difficulty": "medium",
                                "explanation": "The Partition of Bengal was annulled in 1911 due to massive protests and the Swadeshi movement."
                            },
                            {
                                "text": "Dandi March was undertaken to protest against:",
                                "options": ["Land tax", "Salt tax", "Cloth tax", "Income tax"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "Gandhi led the Dandi March (1930) to protest the British salt tax and spark the Civil Disobedience Movement."
                            },
                            {
                                "text": "The Rowlatt Act (1919) allowed the British to:",
                                "options": ["Impose trade taxes", "Detain suspects without trial", "Ban Indian newspapers", "Restrict civil service"],
                                "correct_index": 1,
                                "difficulty": "medium",
                                "explanation": "The Rowlatt Act allowed detention of political suspects without trial, sparking widespread protests."
                            },
                            {
                                "text": "Who gave the slogan 'Do or Die'?",
                                "options": ["Nehru", "Bose", "Gandhi", "Tilak"],
                                "correct_index": 2,
                                "difficulty": "easy",
                                "explanation": "Mahatma Gandhi gave the 'Do or Die' slogan during the Quit India Movement of 1942."
                            },
                            {
                                "text": "The Cabinet Mission Plan (1946) proposed:",
                                "options": ["Full independence immediately", "Partition of India", "Federal union with three groups", "Dominion status"],
                                "correct_index": 2,
                                "difficulty": "hard",
                                "explanation": "The Cabinet Mission proposed a federal union of India with three groups (sections) of provinces."
                            },
                            {
                                "text": "India became a Republic on:",
                                "options": ["15 August 1947", "26 January 1950", "26 November 1949", "2 October 1948"],
                                "correct_index": 1,
                                "difficulty": "easy",
                                "explanation": "India became a Republic on 26 January 1950 when the Constitution came into effect."
                            },
                            {
                                "text": "The Simon Commission was boycotted because:",
                                "options": ["It was expensive", "No Indian member", "It proposed partition", "Gandhi opposed it"],
                                "correct_index": 1,
                                "difficulty": "medium",
                                "explanation": "The Simon Commission (1927) was boycotted because it had no Indian members to discuss India's future."
                            },
                            {
                                "text": "Jallianwala Bagh massacre occurred in:",
                                "options": ["1917", "1918", "1919", "1920"],
                                "correct_index": 2,
                                "difficulty": "easy",
                                "explanation": "The Jallianwala Bagh massacre occurred on 13 April 1919 under General Dyer's orders in Amritsar."
                            },
                            {
                                "text": "Who headed the Constituent Assembly of India?",
                                "options": ["Gandhi", "Nehru", "Rajendra Prasad", "Ambedkar"],
                                "correct_index": 2,
                                "difficulty": "medium",
                                "explanation": "Dr. Rajendra Prasad was the President of the Constituent Assembly of India."
                            },
                        ]
                    },
                ]
            },
            {
                "name": "Indian Polity",
                "icon": "⚖️",
                "chapters": [
                    {
                        "name": "Constitution Basics",
                        "questions": [
                            {"text": "How many articles does the Indian Constitution have originally?", "options": ["395", "400", "380", "450"], "correct_index": 0, "difficulty": "medium", "explanation": "The original Indian Constitution had 395 articles, 22 parts, and 8 schedules."},
                            {"text": "The Constitution of India was adopted on:", "options": ["15 Aug 1947", "26 Jan 1950", "26 Nov 1949", "2 Oct 1949"], "correct_index": 2, "difficulty": "easy", "explanation": "The Constitution was adopted by the Constituent Assembly on 26 November 1949 and came into effect on 26 Jan 1950."},
                            {"text": "Who is called the 'Father of Indian Constitution'?", "options": ["Gandhi", "Nehru", "Ambedkar", "Rajendra Prasad"], "correct_index": 2, "difficulty": "easy", "explanation": "B.R. Ambedkar is called the Father of the Indian Constitution as he chaired the Drafting Committee."},
                            {"text": "The Preamble of India begins with:", "options": ["We the Citizens", "We the People", "We the Nation", "We, the People of India"], "correct_index": 3, "difficulty": "easy", "explanation": "The Preamble begins with 'We, the People of India', reflecting democratic sovereignty."},
                            {"text": "Which schedule contains the list of languages in India?", "options": ["6th", "7th", "8th", "9th"], "correct_index": 2, "difficulty": "medium", "explanation": "The 8th Schedule lists 22 officially recognized languages of India."},
                            {"text": "The concept of 'Judicial Review' in India is borrowed from:", "options": ["UK", "USA", "Canada", "Australia"], "correct_index": 1, "difficulty": "medium", "explanation": "The concept of Judicial Review is borrowed from the US Constitution, allowing courts to strike down laws."},
                            {"text": "Article 21 of the Indian Constitution deals with:", "options": ["Right to equality", "Right to life", "Right to freedom", "Right against exploitation"], "correct_index": 1, "difficulty": "easy", "explanation": "Article 21 guarantees the Right to Life and Personal Liberty — the most fundamental right."},
                            {"text": "The 42nd Amendment of 1976 added which words to the Preamble?", "options": ["Democratic, Republic", "Socialist, Secular", "Sovereign, Democratic", "Justice, Liberty"], "correct_index": 1, "difficulty": "hard", "explanation": "The 42nd Amendment (1976) added 'Socialist' and 'Secular' to the Preamble during the Emergency."},
                            {"text": "Which Article empowers the President to declare National Emergency?", "options": ["Article 352", "Article 356", "Article 360", "Article 370"], "correct_index": 0, "difficulty": "medium", "explanation": "Article 352 empowers the President to declare National Emergency on grounds of war or armed rebellion."},
                            {"text": "Fundamental Rights are enshrined in which Part of the Constitution?", "options": ["Part II", "Part III", "Part IV", "Part V"], "correct_index": 1, "difficulty": "easy", "explanation": "Fundamental Rights are contained in Part III of the Indian Constitution (Articles 12–35)."},
                        ]
                    },
                    {
                        "name": "Parliament & Legislature",
                        "questions": [
                            {"text": "The Rajya Sabha is a:", "options": ["Temporary house", "Permanent house", "Lower house", "People's house"], "correct_index": 1, "difficulty": "easy", "explanation": "Rajya Sabha is a permanent body (upper house) that never dissolves, with 1/3 members retiring every 2 years."},
                            {"text": "Maximum strength of Lok Sabha is:", "options": ["543", "545", "552", "550"], "correct_index": 2, "difficulty": "medium", "explanation": "The maximum strength of Lok Sabha is 552 (530 from states + 20 from UTs + 2 Anglo-Indians, now abolished)."},
                            {"text": "Money Bill can be introduced only in:", "options": ["Rajya Sabha", "Lok Sabha", "Either house", "Joint session"], "correct_index": 1, "difficulty": "easy", "explanation": "A Money Bill can only be introduced in the Lok Sabha; Rajya Sabha can only suggest amendments."},
                            {"text": "The Speaker of Lok Sabha is elected by:", "options": ["President", "Prime Minister", "Members of Lok Sabha", "Both houses together"], "correct_index": 2, "difficulty": "easy", "explanation": "The Speaker of Lok Sabha is elected by the members of the Lok Sabha from among themselves."},
                            {"text": "Quorum to hold a Lok Sabha session is:", "options": ["1/5 of members", "1/10 of members", "1/3 of members", "1/4 of members"], "correct_index": 1, "difficulty": "medium", "explanation": "Quorum for Lok Sabha is 1/10 of the total membership, i.e., at least 55 members must be present."},
                            {"text": "Joint session of Parliament is presided over by:", "options": ["President", "Vice President", "Speaker of Lok Sabha", "PM"], "correct_index": 2, "difficulty": "medium", "explanation": "The Speaker of Lok Sabha presides over joint sessions of Parliament called to resolve deadlocks."},
                            {"text": "The concept of zero hour in Parliament means:", "options": ["Midnight session", "Question hour without notice", "Budget session", "President's address"], "correct_index": 1, "difficulty": "hard", "explanation": "Zero Hour (12 noon) is an informal but vital parliamentary practice where members raise urgent matters without prior notice."},
                            {"text": "No-confidence motion must be supported by at least:", "options": ["25 members", "50 members", "1/4 of members", "100 members"], "correct_index": 1, "difficulty": "medium", "explanation": "A no-confidence motion needs support of at least 50 members to be admitted in Lok Sabha."},
                            {"text": "Which committee examines appropriation and finance bills?", "options": ["PAC", "Estimates Committee", "Both A and B", "Standing Committee"], "correct_index": 0, "difficulty": "hard", "explanation": "Public Accounts Committee (PAC) examines the audit reports of the Comptroller and Auditor General."},
                            {"text": "The Constitution provides for how many sessions of Parliament per year?", "options": ["2", "3", "4", "No fixed number"], "correct_index": 3, "difficulty": "hard", "explanation": "The Constitution doesn't specify the number of sessions; by convention, Parliament meets 3 times a year."},
                        ]
                    },
                    {
                        "name": "Judiciary & Rights",
                        "questions": [
                            {"text": "The Supreme Court of India was established in:", "options": ["1947", "1950", "1952", "1955"], "correct_index": 1, "difficulty": "easy", "explanation": "The Supreme Court of India was established on 28 January 1950, after the Constitution came into effect."},
                            {"text": "Habeas Corpus means:", "options": ["Let the law be obeyed", "You have the body", "Let justice be done", "Power of the court"], "correct_index": 1, "difficulty": "medium", "explanation": "Habeas Corpus is a writ meaning 'you have the body', requiring a person to be brought before the court to check unlawful detention."},
                            {"text": "Which writ is issued against unlawful detention?", "options": ["Mandamus", "Certiorari", "Habeas Corpus", "Quo Warranto"], "correct_index": 2, "difficulty": "easy", "explanation": "Habeas Corpus writ is issued to protect a person from unlawful detention by requiring their production before court."},
                            {"text": "Right to Education (Article 21-A) was added by which amendment?", "options": ["44th", "73rd", "86th", "93rd"], "correct_index": 2, "difficulty": "hard", "explanation": "The 86th Amendment Act (2002) inserted Article 21-A, making education a fundamental right for children 6-14 years."},
                            {"text": "PIL (Public Interest Litigation) in India is associated with:", "options": ["Appellate jurisdiction", "Original jurisdiction", "Advisory jurisdiction", "All of the above"], "correct_index": 1, "difficulty": "medium", "explanation": "PILs are filed under the original jurisdiction of the Supreme Court under Article 32."},
                            {"text": "Judges of the Supreme Court retire at age:", "options": ["60", "62", "65", "70"], "correct_index": 2, "difficulty": "easy", "explanation": "Supreme Court judges retire at age 65 under Article 124(2) of the Indian Constitution."},
                            {"text": "Which article abolishes untouchability?", "options": ["Article 14", "Article 15", "Article 17", "Article 19"], "correct_index": 2, "difficulty": "easy", "explanation": "Article 17 abolishes untouchability and its practice in any form is an offence punishable by law."},
                            {"text": "The National Human Rights Commission was established in:", "options": ["1990", "1993", "1995", "2000"], "correct_index": 1, "difficulty": "medium", "explanation": "NHRC was established in 1993 under the Protection of Human Rights Act, 1993."},
                            {"text": "Which article grants the right to move Supreme Court for enforcement of fundamental rights?", "options": ["Article 19", "Article 21", "Article 32", "Article 226"], "correct_index": 2, "difficulty": "medium", "explanation": "Article 32 (Right to Constitutional Remedies) allows citizens to directly approach the Supreme Court."},
                            {"text": "Directive Principles of State Policy are:", "options": ["Justiciable", "Non-justiciable", "Partly justiciable", "Enforceable by courts"], "correct_index": 1, "difficulty": "medium", "explanation": "DPSPs (Part IV) are non-justiciable, meaning courts cannot enforce them, but they guide state policy."},
                        ]
                    },
                ]
            },
            {
                "name": "Geography",
                "icon": "🗺️",
                "chapters": [
                    {
                        "name": "Physical Geography",
                        "questions": [
                            {"text": "The Tropic of Cancer passes through how many Indian states?", "options": ["6", "7", "8", "9"], "correct_index": 2, "difficulty": "medium", "explanation": "The Tropic of Cancer passes through 8 Indian states: Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura, Mizoram."},
                            {"text": "India's longest river is:", "options": ["Ganga", "Brahmaputra", "Godavari", "Indus"], "correct_index": 0, "difficulty": "easy", "explanation": "The Ganga is India's longest river at about 2,525 km, though the Indus is longer overall (in total length)."},
                            {"text": "The Western Ghats are also known as:", "options": ["Sahyadri", "Aravallis", "Vindhyas", "Satpuras"], "correct_index": 0, "difficulty": "easy", "explanation": "The Western Ghats are known as Sahyadri in Maharashtra and are a UNESCO World Heritage Site."},
                            {"text": "Which is India's highest peak?", "options": ["Nanda Devi", "Kangchenjunga", "K2", "Kamet"], "correct_index": 1, "difficulty": "easy", "explanation": "Kangchenjunga (8,586 m) is India's highest peak and the world's third highest mountain."},
                            {"text": "The Sundarbans delta is formed by rivers:", "options": ["Ganga and Brahmaputra", "Mahanadi and Godavari", "Krishna and Cauvery", "Indus and Jhelum"], "correct_index": 0, "difficulty": "medium", "explanation": "The Sundarbans is formed by the Ganga-Brahmaputra delta, the world's largest mangrove forest."},
                            {"text": "India's largest desert is:", "options": ["Cold desert of Ladakh", "Thar Desert", "Deccan Plateau", "Rann of Kutch"], "correct_index": 1, "difficulty": "easy", "explanation": "The Thar Desert in Rajasthan is India's largest desert and the 17th largest desert in the world."},
                            {"text": "Which state has the largest coastline in India?", "options": ["Tamil Nadu", "Kerala", "Gujarat", "Andhra Pradesh"], "correct_index": 2, "difficulty": "medium", "explanation": "Gujarat has the longest coastline (1,600 km) among Indian states due to its irregular peninsular shape."},
                            {"text": "Loktak Lake is located in:", "options": ["Assam", "Manipur", "Meghalaya", "Sikkim"], "correct_index": 1, "difficulty": "medium", "explanation": "Loktak Lake in Manipur is the largest freshwater lake in Northeast India, famous for its phumdis."},
                            {"text": "The Deccan Plateau is bounded on the west by:", "options": ["Eastern Ghats", "Western Ghats", "Vindhya Range", "Satpura Range"], "correct_index": 1, "difficulty": "easy", "explanation": "The Deccan Plateau is bounded by the Western Ghats on the west and Eastern Ghats on the east."},
                            {"text": "The latitude of the southern tip of India (mainland) is approximately:", "options": ["6°N", "8°N", "10°N", "12°N"], "correct_index": 1, "difficulty": "hard", "explanation": "Kanyakumari, the southernmost tip of mainland India, is at approximately 8°4'N latitude."},
                        ]
                    },
                    {
                        "name": "Economic Geography",
                        "questions": [
                            {"text": "India is the world's largest producer of:", "options": ["Rice", "Wheat", "Milk", "Sugarcane"], "correct_index": 2, "difficulty": "medium", "explanation": "India surpassed the US in 1997 and is now the world's largest producer of milk (Operation Flood's legacy)."},
                            {"text": "Which state is the largest producer of cotton in India?", "options": ["Maharashtra", "Gujarat", "Punjab", "Andhra Pradesh"], "correct_index": 1, "difficulty": "medium", "explanation": "Gujarat is the largest cotton-producing state in India, followed by Maharashtra."},
                            {"text": "The Green Revolution in India is associated with:", "options": ["Wheat and rice", "Pulses and oilseeds", "Cotton and jute", "Sugarcane and tea"], "correct_index": 0, "difficulty": "easy", "explanation": "India's Green Revolution (1960s-70s) focused on high-yielding varieties of wheat and rice."},
                            {"text": "Kudremukh in Karnataka is famous for:", "options": ["Coal mining", "Iron ore", "Manganese", "Gold"], "correct_index": 1, "difficulty": "hard", "explanation": "Kudremukh in the Western Ghats is famous for its iron ore deposits, though mining is now restricted."},
                            {"text": "SAIL stands for:", "options": ["Steel Authority of India Ltd", "Steel Association of Indian Labs", "South Asian Iron Limited", "State Authority for Iron & Limestone"], "correct_index": 0, "difficulty": "easy", "explanation": "SAIL (Steel Authority of India Limited) is one of India's largest steel-producing public sector enterprises."},
                            {"text": "Which Indian city is known as the 'Silicon Valley of India'?", "options": ["Mumbai", "Hyderabad", "Bengaluru", "Pune"], "correct_index": 2, "difficulty": "easy", "explanation": "Bengaluru (Bangalore) is called the Silicon Valley of India due to its concentration of IT companies."},
                            {"text": "The first Special Economic Zone in India was set up in:", "options": ["Mumbai", "Kandla", "Chennai", "Kochi"], "correct_index": 1, "difficulty": "hard", "explanation": "India's first SEZ was established at Kandla, Gujarat (now called Deendayal Port Trust) in 1965."},
                            {"text": "Periyar Tiger Reserve is located in:", "options": ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh"], "correct_index": 1, "difficulty": "medium", "explanation": "Periyar Tiger Reserve is located in Thekkady, Kerala, known for its elephant and tiger population."},
                            {"text": "Which port handles the maximum cargo in India?", "options": ["Kandla", "JNPT", "Mumbai", "Vishakhapatnam"], "correct_index": 0, "difficulty": "hard", "explanation": "Kandla (Deendayal) Port handles the maximum cargo tonnage in India, serving as the primary western port."},
                            {"text": "National Highway 44 (previously NH 7) connects:", "options": ["Delhi to Mumbai", "Varanasi to Kanyakumari", "Srinagar to Kanyakumari", "Delhi to Kolkata"], "correct_index": 2, "difficulty": "medium", "explanation": "NH 44 is India's longest national highway, running from Srinagar to Kanyakumari (about 3,745 km)."},
                        ]
                    },
                    {
                        "name": "Environment & Ecology",
                        "questions": [
                            {"text": "Which gas is primarily responsible for the greenhouse effect?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Argon"], "correct_index": 2, "difficulty": "easy", "explanation": "Carbon dioxide (CO2) is the primary greenhouse gas responsible for global warming and climate change."},
                            {"text": "The Kyoto Protocol was adopted in:", "options": ["1992", "1995", "1997", "2000"], "correct_index": 2, "difficulty": "medium", "explanation": "The Kyoto Protocol was adopted in 1997, requiring developed nations to reduce greenhouse gas emissions."},
                            {"text": "Chipko movement was related to:", "options": ["Water conservation", "Forest conservation", "Soil conservation", "Air pollution"], "correct_index": 1, "difficulty": "easy", "explanation": "The Chipko Movement (1973) was a forest conservation movement in Uttarakhand where villagers hugged trees to prevent logging."},
                            {"text": "The UN Framework Convention on Climate Change was signed at:", "options": ["Rio de Janeiro", "Kyoto", "Paris", "Copenhagen"], "correct_index": 0, "difficulty": "medium", "explanation": "UNFCCC was signed at the Earth Summit in Rio de Janeiro, Brazil in 1992."},
                            {"text": "The concept of 'Carbon Credit' relates to:", "options": ["Banking system", "Greenhouse gas reduction", "Forest revenue", "Water conservation"], "correct_index": 1, "difficulty": "medium", "explanation": "Carbon credits are tradeable certificates representing a reduction of one tonne of CO2 emissions."},
                            {"text": "Silent Valley National Park is in:", "options": ["Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh"], "correct_index": 2, "difficulty": "medium", "explanation": "Silent Valley National Park in Palakkad, Kerala, is known for its undisturbed tropical rainforests."},
                            {"text": "India's first Biosphere Reserve was:", "options": ["Nanda Devi", "Gulf of Mannar", "Nilgiri", "Sundarbans"], "correct_index": 2, "difficulty": "hard", "explanation": "Nilgiri Biosphere Reserve (1986) was India's first biosphere reserve, covering Tamil Nadu, Kerala, and Karnataka."},
                            {"text": "The Paris Agreement aims to limit global warming to:", "options": ["1°C", "1.5-2°C", "2-3°C", "3°C"], "correct_index": 1, "difficulty": "medium", "explanation": "The Paris Agreement (2015) aims to limit global temperature rise to well below 2°C, preferably 1.5°C above pre-industrial levels."},
                            {"text": "Which Article of the Indian Constitution deals with environment protection?", "options": ["Article 48A", "Article 51A(g)", "Both A and B", "Article 21"], "correct_index": 2, "difficulty": "hard", "explanation": "Article 48A (DPSP) directs the state to protect the environment, while Article 51A(g) makes it a fundamental duty."},
                            {"text": "The ozone layer primarily absorbs:", "options": ["Infrared radiation", "UV-B radiation", "Visible light", "X-rays"], "correct_index": 1, "difficulty": "medium", "explanation": "The ozone layer in the stratosphere primarily absorbs harmful UV-B radiation from the sun."},
                        ]
                    },
                ]
            },
        ]
    },
    {
        "name": "JEE",
        "icon": "⚗️",
        "color": "#1565c0",
        "description": "Joint Entrance Examination — Engineering Entrance",
        "subjects": [
            {
                "name": "Physics",
                "icon": "🔭",
                "chapters": [
                    {
                        "name": "Mechanics",
                        "questions": [
                            {"text": "A body is thrown vertically upward with velocity u. The maximum height reached is:", "options": ["u²/g", "u²/2g", "2u²/g", "u/2g"], "correct_index": 1, "difficulty": "easy", "explanation": "Using v² = u² - 2gh, at max height v=0, so h = u²/2g."},
                            {"text": "Newton's second law of motion states:", "options": ["F = mv", "F = ma", "F = m/a", "F = v/t"], "correct_index": 1, "difficulty": "easy", "explanation": "Newton's second law: Force = mass × acceleration (F = ma)."},
                            {"text": "The unit of angular momentum is:", "options": ["kg·m/s", "kg·m²/s", "kg·m²/s²", "N·m"], "correct_index": 1, "difficulty": "medium", "explanation": "Angular momentum L = mvr has units kg·m²/s."},
                            {"text": "A satellite orbiting Earth at height h has time period proportional to:", "options": ["(R+h)^(1/2)", "(R+h)^(3/2)", "(R+h)^2", "(R+h)"], "correct_index": 1, "difficulty": "medium", "explanation": "By Kepler's third law, T² ∝ r³, so T ∝ (R+h)^(3/2)."},
                            {"text": "The escape velocity from Earth's surface is approximately:", "options": ["7.9 km/s", "11.2 km/s", "8.5 km/s", "12.0 km/s"], "correct_index": 1, "difficulty": "easy", "explanation": "Escape velocity = √(2gR) ≈ 11.2 km/s for Earth."},
                            {"text": "For SHM, acceleration is proportional to:", "options": ["Displacement", "Velocity", "Time", "Force squared"], "correct_index": 0, "difficulty": "easy", "explanation": "In SHM, a = -ω²x, so acceleration is proportional to (and opposite to) displacement."},
                            {"text": "Moment of inertia of a solid sphere about its diameter is:", "options": ["MR²", "2MR²/3", "2MR²/5", "MR²/2"], "correct_index": 2, "difficulty": "medium", "explanation": "Moment of inertia of solid sphere = (2/5)MR²."},
                            {"text": "In projectile motion, the horizontal range is maximum at angle:", "options": ["30°", "45°", "60°", "90°"], "correct_index": 1, "difficulty": "easy", "explanation": "Horizontal range R = u²sin2θ/g is maximum when sin2θ = 1, i.e., θ = 45°."},
                            {"text": "Conservation of angular momentum is analogous to:", "options": ["Newton's 1st law for rotation", "Newton's 2nd law", "Law of gravitation", "Kepler's law"], "correct_index": 0, "difficulty": "medium", "explanation": "Conservation of angular momentum applies when net torque is zero, analogous to Newton's 1st law."},
                            {"text": "Bernoulli's theorem is based on:", "options": ["Conservation of mass", "Conservation of momentum", "Conservation of energy", "Conservation of angular momentum"], "correct_index": 2, "difficulty": "medium", "explanation": "Bernoulli's theorem is derived from the principle of conservation of energy for fluid flow."},
                        ]
                    },
                    {
                        "name": "Electromagnetism",
                        "questions": [
                            {"text": "The SI unit of electric field intensity is:", "options": ["N/C", "V/m", "Both A and B", "C/N"], "correct_index": 2, "difficulty": "easy", "explanation": "Electric field intensity is measured in N/C or equivalently V/m."},
                            {"text": "Capacitance of a parallel plate capacitor with dielectric constant K is:", "options": ["C = Kε₀A/d", "C = ε₀A/Kd", "C = ε₀A/d", "C = Kε₀d/A"], "correct_index": 0, "difficulty": "medium", "explanation": "With dielectric: C = Kε₀A/d, where K increases capacitance by factor K."},
                            {"text": "Lenz's law is related to:", "options": ["Faraday's law", "Conservation of energy", "Both A and B", "Ohm's law"], "correct_index": 2, "difficulty": "medium", "explanation": "Lenz's law is a statement of Faraday's law and reflects conservation of energy by opposing change."},
                            {"text": "At resonance in an LCR series circuit:", "options": ["XL = XC", "Z = R", "Power factor = 1", "All of the above"], "correct_index": 3, "difficulty": "medium", "explanation": "At resonance: XL = XC, Z = R (minimum), and power factor = 1 (maximum power transfer)."},
                            {"text": "The magnetic field inside a solenoid is:", "options": ["μ₀nI", "μ₀I/2πr", "μ₀I/4πr", "Zero"], "correct_index": 0, "difficulty": "medium", "explanation": "Inside a solenoid, B = μ₀nI where n is the number of turns per unit length."},
                            {"text": "Photoelectric effect supports:", "options": ["Wave nature of light", "Particle nature of light", "Dual nature", "Neither"], "correct_index": 1, "difficulty": "easy", "explanation": "Photoelectric effect demonstrates that light behaves as particles (photons), supporting quantum theory."},
                            {"text": "Fleming's left-hand rule gives the direction of:", "options": ["Induced EMF", "Force on current-carrying conductor", "Magnetic field", "Current"], "correct_index": 1, "difficulty": "medium", "explanation": "Fleming's left-hand rule gives the direction of force on a current-carrying conductor in a magnetic field."},
                            {"text": "The transformer works on the principle of:", "options": ["Self-induction", "Mutual induction", "Faraday's law", "Both B and C"], "correct_index": 3, "difficulty": "medium", "explanation": "A transformer works on mutual induction, which is based on Faraday's law of electromagnetic induction."},
                            {"text": "The de Broglie wavelength of a particle of mass m and KE E is:", "options": ["h/√(2mE)", "h/√(mE)", "h²/2mE", "√(2mE)/h"], "correct_index": 0, "difficulty": "hard", "explanation": "λ = h/p = h/√(2mE) from p = √(2mE)."},
                            {"text": "In a p-n junction, the depletion region is formed due to:", "options": ["Drift of majority carriers", "Diffusion of majority carriers", "Movement of minority carriers", "Applied voltage"], "correct_index": 1, "difficulty": "medium", "explanation": "The depletion region forms due to diffusion of majority carriers across the junction."},
                        ]
                    },
                    {
                        "name": "Thermodynamics",
                        "questions": [
                            {"text": "The first law of thermodynamics is essentially:", "options": ["Conservation of momentum", "Conservation of energy", "Conservation of mass", "Entropy law"], "correct_index": 1, "difficulty": "easy", "explanation": "The first law of thermodynamics is a statement of conservation of energy: ΔU = Q - W."},
                            {"text": "In an adiabatic process:", "options": ["Temperature is constant", "Pressure is constant", "No heat exchange", "Volume is constant"], "correct_index": 2, "difficulty": "easy", "explanation": "In an adiabatic process, no heat is exchanged with the surroundings (Q = 0)."},
                            {"text": "Efficiency of a Carnot engine operating between T₁ and T₂ (T₁ > T₂) is:", "options": ["1 - T₂/T₁", "T₂/T₁", "1 - T₁/T₂", "T₁/T₂"], "correct_index": 0, "difficulty": "medium", "explanation": "Carnot efficiency η = 1 - T₂/T₁ (cold/hot temperature ratio)."},
                            {"text": "The second law of thermodynamics states that:", "options": ["Energy is conserved", "Entropy of universe always increases", "Heat flows from cold to hot", "Ideal gas laws apply"], "correct_index": 1, "difficulty": "medium", "explanation": "The second law states that total entropy of an isolated system can only increase over time."},
                            {"text": "The specific heat at constant pressure (Cp) is always:", "options": ["Equal to Cv", "Less than Cv", "Greater than Cv", "Zero for ideal gas"], "correct_index": 2, "difficulty": "medium", "explanation": "Cp > Cv always, with Cp - Cv = R for ideal gases, because extra energy is needed for work at constant pressure."},
                            {"text": "In an isothermal expansion of an ideal gas:", "options": ["Internal energy increases", "Temperature decreases", "Internal energy stays constant", "Work done is zero"], "correct_index": 2, "difficulty": "medium", "explanation": "For an ideal gas, internal energy depends only on temperature; in isothermal process, ΔU = 0."},
                            {"text": "A heat engine cannot have 100% efficiency because:", "options": ["Friction losses", "Second law of thermodynamics", "Limited fuel", "Heat conduction"], "correct_index": 1, "difficulty": "medium", "explanation": "The second law of thermodynamics prohibits 100% conversion of heat to work; some must be rejected."},
                            {"text": "Zeroth law of thermodynamics defines:", "options": ["Entropy", "Temperature", "Internal energy", "Heat capacity"], "correct_index": 1, "difficulty": "medium", "explanation": "The zeroth law defines temperature: if A is in thermal equilibrium with B and C, then B and C are also in equilibrium."},
                            {"text": "The process in which PV^γ = constant is:", "options": ["Isothermal", "Isobaric", "Adiabatic", "Isochoric"], "correct_index": 2, "difficulty": "medium", "explanation": "PV^γ = constant for an adiabatic process, where γ = Cp/Cv."},
                            {"text": "Root mean square speed of gas molecules is proportional to:", "options": ["√T", "T", "T²", "1/√T"], "correct_index": 0, "difficulty": "medium", "explanation": "Vrms = √(3RT/M), so Vrms ∝ √T."},
                        ]
                    },
                ]
            },
            {
                "name": "Chemistry",
                "icon": "🧪",
                "chapters": [
                    {
                        "name": "Physical Chemistry",
                        "questions": [
                            {"text": "The molarity of a solution is defined as:", "options": ["Moles of solute per kg of solvent", "Moles of solute per litre of solution", "Grams per litre", "Mole fraction"], "correct_index": 1, "difficulty": "easy", "explanation": "Molarity (M) = moles of solute / volume of solution in litres."},
                            {"text": "Which of the following is NOT a colligative property?", "options": ["Osmotic pressure", "Elevation of boiling point", "Optical activity", "Depression of freezing point"], "correct_index": 2, "difficulty": "medium", "explanation": "Optical activity depends on the nature of the solute, not on the number of particles — so it's not colligative."},
                            {"text": "Rate of a reaction depends on:", "options": ["Concentration of reactants", "Temperature", "Catalyst", "All of the above"], "correct_index": 3, "difficulty": "easy", "explanation": "Reaction rate depends on concentration, temperature, and presence of catalysts."},
                            {"text": "pH of a neutral solution at 25°C is:", "options": ["0", "7", "14", "1"], "correct_index": 1, "difficulty": "easy", "explanation": "At 25°C, pure water has [H⁺] = [OH⁻] = 10⁻⁷ M, giving pH = 7."},
                            {"text": "Raoult's law is applicable to:", "options": ["Ideal solutions", "Concentrated solutions", "Electrolyte solutions", "Non-volatile solutes only"], "correct_index": 0, "difficulty": "medium", "explanation": "Raoult's law perfectly applies to ideal solutions where interactions between components are similar."},
                            {"text": "The Arrhenius equation relates rate constant to:", "options": ["Concentration", "Temperature", "Pressure", "Volume"], "correct_index": 1, "difficulty": "medium", "explanation": "k = Ae^(-Ea/RT) — the Arrhenius equation relates rate constant k to temperature T."},
                            {"text": "Which quantum number determines the shape of an orbital?", "options": ["Principal (n)", "Azimuthal (l)", "Magnetic (m)", "Spin (s)"], "correct_index": 1, "difficulty": "medium", "explanation": "The azimuthal quantum number (l) determines the shape of the orbital (s, p, d, f)."},
                            {"text": "Faraday's first law of electrolysis states:", "options": ["Mass is proportional to current", "Mass is proportional to charge", "Current is proportional to voltage", "Resistance decreases with temperature"], "correct_index": 1, "difficulty": "medium", "explanation": "Faraday's first law: the mass of substance deposited is proportional to the charge passed (m = ZQ)."},
                            {"text": "For an exothermic reaction:", "options": ["ΔH > 0", "ΔH < 0", "ΔH = 0", "ΔG > 0"], "correct_index": 1, "difficulty": "easy", "explanation": "Exothermic reactions release heat, so ΔH < 0 (negative enthalpy change)."},
                            {"text": "The van 't Hoff factor (i) for NaCl in dilute aqueous solution is approximately:", "options": ["1", "1.5", "2", "3"], "correct_index": 2, "difficulty": "medium", "explanation": "NaCl dissociates into Na⁺ and Cl⁻, giving i ≈ 2 in dilute solution."},
                        ]
                    },
                    {
                        "name": "Organic Chemistry",
                        "questions": [
                            {"text": "The IUPAC name of CH₃-CH₂-OH is:", "options": ["Methanol", "Ethanol", "Propanol", "Butanol"], "correct_index": 1, "difficulty": "easy", "explanation": "CH₃-CH₂-OH has 2 carbons with an -OH group, so it's ethanol (ethyl alcohol)."},
                            {"text": "Which of the following is a nucleophile?", "options": ["BF₃", "H⁺", "OH⁻", "AlCl₃"], "correct_index": 2, "difficulty": "easy", "explanation": "OH⁻ is a nucleophile (electron-rich, attacks electron-poor centers). The others are electrophiles/Lewis acids."},
                            {"text": "Benzene shows:", "options": ["Addition reactions only", "Substitution reactions preferentially", "Elimination reactions", "No reactions"], "correct_index": 1, "difficulty": "easy", "explanation": "Benzene prefers electrophilic substitution over addition to preserve its stable aromatic ring."},
                            {"text": "The functional group -COOH represents:", "options": ["Aldehyde", "Ketone", "Carboxylic acid", "Ester"], "correct_index": 2, "difficulty": "easy", "explanation": "-COOH is the carboxyl group, characteristic of carboxylic acids."},
                            {"text": "Which polymer is formed by the polymerization of ethylene?", "options": ["PVC", "Polystyrene", "Polyethylene", "Teflon"], "correct_index": 2, "difficulty": "easy", "explanation": "Polyethylene is formed by addition polymerization of ethylene (CH₂=CH₂)."},
                            {"text": "Fehling's solution is used to detect:", "options": ["Alcohols", "Aldehydes", "Ketones", "Esters"], "correct_index": 1, "difficulty": "medium", "explanation": "Fehling's solution oxidizes aldehydes (not ketones) to give a brick-red precipitate of Cu₂O."},
                            {"text": "The hybridization of carbon in benzene is:", "options": ["sp", "sp²", "sp³", "sp³d"], "correct_index": 1, "difficulty": "medium", "explanation": "Each carbon in benzene is sp² hybridized, forming 3 sigma bonds and 1 pi bond in the delocalized system."},
                            {"text": "SN2 reactions proceed through:", "options": ["Carbocation intermediate", "Carbanion intermediate", "Inversion of configuration", "Retention of configuration"], "correct_index": 2, "difficulty": "medium", "explanation": "SN2 reactions occur via backside attack leading to inversion of configuration (Walden inversion)."},
                            {"text": "Markovnikov's rule applies to:", "options": ["Elimination reactions", "Addition reactions to alkenes", "Substitution reactions", "Rearrangement reactions"], "correct_index": 1, "difficulty": "medium", "explanation": "Markovnikov's rule governs addition to alkenes: the H adds to the carbon with more H atoms."},
                            {"text": "The monomer of natural rubber is:", "options": ["Styrene", "Isoprene", "Butadiene", "Chloroprene"], "correct_index": 1, "difficulty": "medium", "explanation": "Natural rubber (polyisoprene) is formed from isoprene (2-methylbutadiene) monomers."},
                        ]
                    },
                    {
                        "name": "Inorganic Chemistry",
                        "questions": [
                            {"text": "The electronic configuration of Fe²⁺ is:", "options": ["[Ar] 3d⁶", "[Ar] 3d⁵4s¹", "[ Ar] 3d⁴4s²", "[Ar] 3d⁶4s²"], "correct_index": 0, "difficulty": "hard", "explanation": "Fe is [Ar]3d⁶4s². Fe²⁺ loses 2 electrons from 4s: [Ar]3d⁶."},
                            {"text": "Which of the following has the highest electronegativity?", "options": ["Oxygen", "Nitrogen", "Fluorine", "Chlorine"], "correct_index": 2, "difficulty": "easy", "explanation": "Fluorine has the highest electronegativity (3.98 on Pauling scale) of all elements."},
                            {"text": "The shape of SF₆ molecule is:", "options": ["Tetrahedral", "Octahedral", "Square planar", "Trigonal bipyramidal"], "correct_index": 1, "difficulty": "medium", "explanation": "SF₆ has 6 bonding pairs, no lone pairs, giving octahedral geometry."},
                            {"text": "Which noble gas has the largest atomic radius?", "options": ["Helium", "Neon", "Argon", "Radon"], "correct_index": 3, "difficulty": "easy", "explanation": "Radon has the largest atomic radius among noble gases as atomic radius increases down the group."},
                            {"text": "Diagonal relationship in the periodic table exists between:", "options": ["Li and Mg", "Na and Ca", "Be and Al", "Both A and C"], "correct_index": 3, "difficulty": "hard", "explanation": "Diagonal relationships: Li-Mg and Be-Al (and B-Si), where elements show similar properties diagonally."},
                            {"text": "EDTA is a:", "options": ["Monodentate ligand", "Bidentate ligand", "Hexadentate ligand", "Tridentate ligand"], "correct_index": 2, "difficulty": "hard", "explanation": "EDTA (ethylenediaminetetraacetic acid) has 6 donor atoms, making it a hexadentate chelating agent."},
                            {"text": "The ore of aluminium is:", "options": ["Haematite", "Bauxite", "Chalcopyrite", "Galena"], "correct_index": 1, "difficulty": "easy", "explanation": "Bauxite (Al₂O₃·2H₂O) is the primary ore of aluminium used in industrial extraction."},
                            {"text": "Which gas is produced when copper reacts with dilute HNO₃?", "options": ["NO₂", "NO", "N₂O", "N₂"], "correct_index": 1, "difficulty": "medium", "explanation": "Copper + dilute HNO₃ → Cu(NO₃)₂ + NO (nitric oxide) + H₂O."},
                            {"text": "Bleaching powder is:", "options": ["CaCl₂", "Ca(ClO)₂", "Ca(OCl)Cl", "CaO₂"], "correct_index": 2, "difficulty": "medium", "explanation": "Bleaching powder is Ca(OCl)Cl or calcium hypochlorite-chloride, prepared from slaked lime and Cl₂."},
                            {"text": "The coordination number in NaCl crystal is:", "options": ["4", "6", "8", "12"], "correct_index": 1, "difficulty": "medium", "explanation": "In NaCl structure, each Na⁺ is surrounded by 6 Cl⁻ and vice versa — coordination number is 6."},
                        ]
                    },
                ]
            },
            {
                "name": "Mathematics",
                "icon": "📐",
                "chapters": [
                    {
                        "name": "Calculus",
                        "questions": [
                            {"text": "The derivative of sin(x) is:", "options": ["cos(x)", "-cos(x)", "sin(x)", "-sin(x)"], "correct_index": 0, "difficulty": "easy", "explanation": "d/dx[sin(x)] = cos(x). This is a fundamental derivative to memorize."},
                            {"text": "∫eˣ dx equals:", "options": ["eˣ + C", "xeˣ + C", "eˣ/x + C", "eˣ⁺¹ + C"], "correct_index": 0, "difficulty": "easy", "explanation": "The integral of eˣ is eˣ + C, as eˣ is its own derivative."},
                            {"text": "The limit of (sin x)/x as x→0 is:", "options": ["0", "∞", "1", "undefined"], "correct_index": 2, "difficulty": "easy", "explanation": "This is a standard limit: lim(x→0) sin(x)/x = 1, proven by L'Hôpital's rule or squeeze theorem."},
                            {"text": "A function f(x) is continuous at x = a if:", "options": ["f(a) is defined", "lim f(x) as x→a exists", "lim f(x) = f(a)", "All of the above"], "correct_index": 3, "difficulty": "medium", "explanation": "Continuity requires f(a) defined, limit exists, and limit equals f(a) — all three conditions must hold."},
                            {"text": "The second derivative test for maxima requires:", "options": ["f'(a) = 0 and f''(a) > 0", "f'(a) = 0 and f''(a) < 0", "f'(a) > 0", "f''(a) = 0"], "correct_index": 1, "difficulty": "medium", "explanation": "For a local maximum: f'(a) = 0 (critical point) and f''(a) < 0 (concave down)."},
                            {"text": "∫₀^π sin(x) dx equals:", "options": ["0", "1", "2", "π"], "correct_index": 2, "difficulty": "medium", "explanation": "∫₀^π sin(x)dx = [-cos(x)]₀^π = -cos(π) + cos(0) = 1 + 1 = 2."},
                            {"text": "The chain rule states d/dx[f(g(x))] =", "options": ["f'(x)·g'(x)", "f'(g(x))·g'(x)", "f(g'(x))", "f'(g(x))"], "correct_index": 1, "difficulty": "medium", "explanation": "Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x) — differentiate outer function, multiply by inner derivative."},
                            {"text": "The area between y = x² and y = x is:", "options": ["1/4", "1/6", "1/3", "1/2"], "correct_index": 1, "difficulty": "hard", "explanation": "Intersections at 0 and 1. Area = ∫₀¹(x - x²)dx = [x²/2 - x³/3]₀¹ = 1/2 - 1/3 = 1/6."},
                            {"text": "Rolle's theorem requires that on [a,b]:", "options": ["f is continuous and f(a) ≠ f(b)", "f is differentiable and f(a) = f(b)", "f is continuous, differentiable, and f(a) = f(b)", "f is monotonic"], "correct_index": 2, "difficulty": "medium", "explanation": "Rolle's theorem: f continuous on [a,b], differentiable on (a,b), f(a) = f(b) → ∃ c where f'(c) = 0."},
                            {"text": "The derivative of ln(x) is:", "options": ["1/x²", "x", "1/x", "ln(x)/x"], "correct_index": 2, "difficulty": "easy", "explanation": "d/dx[ln(x)] = 1/x for x > 0."},
                        ]
                    },
                    {
                        "name": "Algebra & Coordinate Geometry",
                        "questions": [
                            {"text": "The roots of ax² + bx + c = 0 are given by:", "options": ["(-b ± √(b²-4ac))/2a", "(b ± √(b²-4ac))/2a", "(-b ± √(b²+4ac))/2a", "(-b ± √(4ac-b²))/2a"], "correct_index": 0, "difficulty": "easy", "explanation": "The quadratic formula gives roots x = (-b ± √(b²-4ac))/2a."},
                            {"text": "The equation of a circle with center (h,k) and radius r is:", "options": ["(x+h)² + (y+k)² = r²", "(x-h)² + (y-k)² = r²", "x² + y² = r²", "(x-h)² + (y-k)² = r"], "correct_index": 1, "difficulty": "easy", "explanation": "Standard form of circle: (x-h)² + (y-k)² = r²."},
                            {"text": "The distance between points (x₁,y₁) and (x₂,y₂) is:", "options": ["√((x₂+x₁)² + (y₂+y₁)²)", "√((x₂-x₁)² + (y₂-y₁)²)", "(x₂-x₁) + (y₂-y₁)", "|x₂-x₁| + |y₂-y₁|"], "correct_index": 1, "difficulty": "easy", "explanation": "Distance formula: d = √((x₂-x₁)² + (y₂-y₁)²) from Pythagorean theorem."},
                            {"text": "For AP with first term a and common difference d, the nth term is:", "options": ["a + nd", "a + (n-1)d", "a·d^(n-1)", "a·d^n"], "correct_index": 1, "difficulty": "easy", "explanation": "nth term of AP: aₙ = a + (n-1)d."},
                            {"text": "The number of ways to choose 3 items from 10 is:", "options": ["720", "120", "210", "360"], "correct_index": 1, "difficulty": "medium", "explanation": "C(10,3) = 10!/(3!·7!) = (10×9×8)/(3×2×1) = 120."},
                            {"text": "If |z| = 1, the complex number z lies on:", "options": ["Real axis", "Imaginary axis", "Unit circle", "Parabola"], "correct_index": 2, "difficulty": "easy", "explanation": "|z| = 1 means distance from origin is 1, so z lies on the unit circle in the Argand plane."},
                            {"text": "The eccentricity of a parabola is:", "options": ["< 1", "> 1", "= 0", "= 1"], "correct_index": 3, "difficulty": "medium", "explanation": "For a parabola, eccentricity e = 1 exactly. (Ellipse: e<1, Hyperbola: e>1, Circle: e=0)"},
                            {"text": "The determinant of a 2×2 matrix [[a,b],[c,d]] is:", "options": ["ac - bd", "ab - cd", "ad - bc", "ad + bc"], "correct_index": 2, "difficulty": "easy", "explanation": "det([[a,b],[c,d]]) = ad - bc (product of diagonals minus product of off-diagonals)."},
                            {"text": "In binomial theorem, the general term is:", "options": ["ⁿCᵣ aⁿ⁻ʳ bʳ", "ⁿCᵣ aʳ bⁿ⁻ʳ", "ⁿCᵣ₋₁ aⁿ⁻ʳ bʳ", "ⁿCᵣ aⁿ bʳ"], "correct_index": 0, "difficulty": "medium", "explanation": "General term Tᵣ₊₁ = ⁿCᵣ · aⁿ⁻ʳ · bʳ in the expansion of (a+b)ⁿ."},
                            {"text": "The slope of a line perpendicular to y = 2x + 3 is:", "options": ["2", "-2", "1/2", "-1/2"], "correct_index": 3, "difficulty": "easy", "explanation": "For perpendicular lines, slopes are negative reciprocals. Slope of given line = 2, so perpendicular slope = -1/2."},
                        ]
                    },
                    {
                        "name": "Probability & Statistics",
                        "questions": [
                            {"text": "P(A∪B) equals:", "options": ["P(A) + P(B)", "P(A) + P(B) - P(A∩B)", "P(A) · P(B)", "P(A) - P(B)"], "correct_index": 1, "difficulty": "easy", "explanation": "Addition theorem: P(A∪B) = P(A) + P(B) - P(A∩B)."},
                            {"text": "For mutually exclusive events, P(A∩B) =", "options": ["P(A)·P(B)", "P(A)+P(B)", "0", "1"], "correct_index": 2, "difficulty": "easy", "explanation": "Mutually exclusive events cannot occur simultaneously, so P(A∩B) = 0."},
                            {"text": "Bayes' theorem is used for:", "options": ["Finding union of events", "Conditional probability revision", "Independent events", "Sample space calculation"], "correct_index": 1, "difficulty": "medium", "explanation": "Bayes' theorem updates probability estimates based on new evidence: P(A|B) = P(B|A)P(A)/P(B)."},
                            {"text": "The mean of 1, 2, 3, 4, 5 is:", "options": ["2", "2.5", "3", "3.5"], "correct_index": 2, "difficulty": "easy", "explanation": "Mean = (1+2+3+4+5)/5 = 15/5 = 3."},
                            {"text": "Standard deviation is the square root of:", "options": ["Mean", "Median", "Variance", "Range"], "correct_index": 2, "difficulty": "easy", "explanation": "Standard deviation σ = √(variance), measuring spread of data around the mean."},
                            {"text": "In a normal distribution, approximately what % of data lies within 1 standard deviation?", "options": ["50%", "68%", "95%", "99.7%"], "correct_index": 1, "difficulty": "medium", "explanation": "The 68-95-99.7 rule: ~68% within 1σ, ~95% within 2σ, ~99.7% within 3σ."},
                            {"text": "If P(A) = 0.4 and A and B are independent with P(B) = 0.5, P(A∩B) =", "options": ["0.9", "0.1", "0.2", "0.45"], "correct_index": 2, "difficulty": "medium", "explanation": "For independent events: P(A∩B) = P(A)·P(B) = 0.4 × 0.5 = 0.2."},
                            {"text": "The median of {1, 3, 5, 7, 9} is:", "options": ["3", "4", "5", "6"], "correct_index": 2, "difficulty": "easy", "explanation": "Median is the middle value in sorted data. For 5 values, it's the 3rd: median = 5."},
                            {"text": "Poisson distribution is used when:", "options": ["n is small", "Events are rare and independent", "Probability changes", "Normal distribution fails"], "correct_index": 1, "difficulty": "medium", "explanation": "Poisson distribution models rare, independent events in a fixed interval (e.g., server errors per hour)."},
                            {"text": "The probability of getting exactly 2 heads in 3 tosses of a fair coin is:", "options": ["1/4", "3/8", "1/2", "1/8"], "correct_index": 1, "difficulty": "medium", "explanation": "P(exactly 2 heads) = C(3,2)×(1/2)²×(1/2)¹ = 3×1/8 = 3/8."},
                        ]
                    },
                ]
            },
        ]
    },
    {
        "name": "NEET",
        "icon": "🩺",
        "color": "#b71c1c",
        "description": "National Eligibility cum Entrance Test — Medical Entrance",
        "subjects": [
            {
                "name": "Biology",
                "icon": "🧬",
                "chapters": [
                    {
                        "name": "Cell Biology",
                        "questions": [
                            {"text": "The powerhouse of the cell is:", "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi body"], "correct_index": 2, "difficulty": "easy", "explanation": "Mitochondria produce ATP via cellular respiration — hence called the powerhouse of the cell."},
                            {"text": "DNA replication occurs in which phase of cell cycle?", "options": ["G1 phase", "S phase", "G2 phase", "M phase"], "correct_index": 1, "difficulty": "easy", "explanation": "DNA replication occurs during S (Synthesis) phase of interphase in the cell cycle."},
                            {"text": "Ribosomes are sites of:", "options": ["DNA replication", "Protein synthesis", "Lipid synthesis", "Photosynthesis"], "correct_index": 1, "difficulty": "easy", "explanation": "Ribosomes are the molecular machines where mRNA is translated into proteins."},
                            {"text": "The fluid mosaic model of cell membrane was proposed by:", "options": ["Watson and Crick", "Singer and Nicolson", "Schleiden and Schwann", "Mendel"], "correct_index": 1, "difficulty": "medium", "explanation": "Singer and Nicolson proposed the fluid mosaic model in 1972, describing the cell membrane structure."},
                            {"text": "Mitosis results in:", "options": ["Haploid daughter cells", "Diploid daughter cells", "Reduction in chromosome number", "Genetic variation"], "correct_index": 1, "difficulty": "easy", "explanation": "Mitosis produces 2 genetically identical diploid daughter cells for growth and repair."},
                            {"text": "The longest phase of meiosis is:", "options": ["Prophase I", "Metaphase I", "Prophase II", "Anaphase I"], "correct_index": 0, "difficulty": "medium", "explanation": "Prophase I of meiosis is the longest, involving synapsis, crossing over, and chromosome condensation."},
                            {"text": "Lysosomes are called 'suicidal bags' because they:", "options": ["Kill cells", "Contain digestive enzymes that can destroy the cell", "Are always active", "Produce toxins"], "correct_index": 1, "difficulty": "easy", "explanation": "Lysosomes contain hydrolytic enzymes that can break down cellular components, causing autolysis if released."},
                            {"text": "Endoplasmic reticulum with ribosomes is called:", "options": ["Smooth ER", "Rough ER", "Golgi body", "Peroxisome"], "correct_index": 1, "difficulty": "easy", "explanation": "Rough endoplasmic reticulum (RER) has ribosomes on its surface and is involved in protein synthesis."},
                            {"text": "The cell theory was proposed by:", "options": ["Hooke and Leeuwenhoek", "Schleiden and Schwann", "Virchow alone", "Darwin"], "correct_index": 1, "difficulty": "medium", "explanation": "Schleiden (1838) and Schwann (1839) proposed that all organisms are made of cells — the cell theory."},
                            {"text": "Active transport requires:", "options": ["No energy", "ATP energy", "Sunlight", "Only concentration gradient"], "correct_index": 1, "difficulty": "easy", "explanation": "Active transport moves substances against concentration gradient, requiring ATP energy (e.g., Na-K pump)."},
                        ]
                    },
                    {
                        "name": "Genetics & Evolution",
                        "questions": [
                            {"text": "Mendel's law of segregation states:", "options": ["Genes assort independently", "Alleles separate during gamete formation", "Dominant masks recessive", "Genes are on chromosomes"], "correct_index": 1, "difficulty": "easy", "explanation": "Law of segregation: paired alleles separate during gamete formation, each gamete getting one allele."},
                            {"text": "The ABO blood group system shows:", "options": ["Complete dominance", "Incomplete dominance", "Codominance", "Epistasis"], "correct_index": 2, "difficulty": "medium", "explanation": "ABO blood groups show codominance: both A and B alleles are expressed in AB blood type."},
                            {"text": "A test cross is between:", "options": ["Two homozygous individuals", "Dominant phenotype and homozygous recessive", "Two F1 individuals", "Two F2 individuals"], "correct_index": 1, "difficulty": "medium", "explanation": "Test cross: an individual showing dominant phenotype × homozygous recessive, to determine genotype."},
                            {"text": "In humans, sex is determined by:", "options": ["Age of parents", "Temperature", "Sex chromosomes (XY)", "Autosomal genes"], "correct_index": 2, "difficulty": "easy", "explanation": "Human sex is determined by sex chromosomes: XX = female, XY = male (Y chromosome from father)."},
                            {"text": "Darwin's theory of evolution is based on:", "options": ["Mutation", "Natural selection and survival of fittest", "Acquired characters", "Artificial selection"], "correct_index": 1, "difficulty": "easy", "explanation": "Darwin proposed natural selection: organisms with favorable traits survive better and pass on traits."},
                            {"text": "DNA fingerprinting uses:", "options": ["PCR only", "VNTRs and PCR", "Gel electrophoresis only", "Restriction enzymes only"], "correct_index": 1, "difficulty": "hard", "explanation": "DNA fingerprinting uses VNTRs (Variable Number Tandem Repeats) amplified by PCR and separated by electrophoresis."},
                            {"text": "Haemophilia is:", "options": ["Autosomal dominant", "Autosomal recessive", "X-linked recessive", "X-linked dominant"], "correct_index": 2, "difficulty": "medium", "explanation": "Haemophilia A and B are X-linked recessive disorders, primarily affecting males."},
                            {"text": "Hardy-Weinberg equilibrium holds when:", "options": ["Evolution is occurring", "Population is small", "No mutation, no selection, random mating", "Gene flow occurs"], "correct_index": 2, "difficulty": "hard", "explanation": "Hardy-Weinberg requires: no mutation, no selection, large population, random mating, no gene flow."},
                            {"text": "RNA differs from DNA in containing:", "options": ["Adenine", "Guanine", "Uracil instead of thymine", "Phosphate groups"], "correct_index": 2, "difficulty": "easy", "explanation": "RNA has uracil (U) instead of thymine (T), and ribose sugar instead of deoxyribose."},
                            {"text": "Which enzyme unwinds DNA during replication?", "options": ["DNA polymerase", "Ligase", "Helicase", "Primase"], "correct_index": 2, "difficulty": "medium", "explanation": "Helicase unwinds and separates the DNA double helix by breaking hydrogen bonds between base pairs."},
                        ]
                    },
                    {
                        "name": "Human Physiology",
                        "questions": [
                            {"text": "The normal human body temperature is:", "options": ["36.5°C", "37°C", "37.5°C", "38°C"], "correct_index": 1, "difficulty": "easy", "explanation": "Normal human body temperature is 37°C (98.6°F), maintained by thermoregulation."},
                            {"text": "Which blood cells help in clotting?", "options": ["Red blood cells", "White blood cells", "Platelets", "Plasma"], "correct_index": 2, "difficulty": "easy", "explanation": "Platelets (thrombocytes) are essential for blood clotting by aggregating at wound sites."},
                            {"text": "The largest gland in the human body is:", "options": ["Pancreas", "Thyroid", "Liver", "Spleen"], "correct_index": 2, "difficulty": "easy", "explanation": "The liver is the largest internal gland in humans, weighing about 1.5 kg with 500+ functions."},
                            {"text": "Insulin is produced by:", "options": ["Alpha cells of pancreas", "Beta cells of pancreas", "Delta cells of pancreas", "Liver cells"], "correct_index": 1, "difficulty": "easy", "explanation": "Beta cells of the islets of Langerhans in the pancreas produce insulin to regulate blood glucose."},
                            {"text": "The conducting part of nephron is:", "options": ["Bowman's capsule", "Glomerulus", "Loop of Henle", "All of the above"], "correct_index": 2, "difficulty": "medium", "explanation": "The Loop of Henle is involved in concentration of urine. The conducting segment includes the tubular parts."},
                            {"text": "Which nerve is responsible for vision?", "options": ["Olfactory", "Optic", "Trigeminal", "Facial"], "correct_index": 1, "difficulty": "easy", "explanation": "The optic nerve (cranial nerve II) carries visual information from the retina to the brain."},
                            {"text": "Breathing rate is primarily regulated by:", "options": ["O₂ levels", "CO₂ levels", "N₂ levels", "H₂O vapour levels"], "correct_index": 1, "difficulty": "medium", "explanation": "Breathing rate is primarily regulated by CO₂ concentration (and pH) in blood, detected by medullary chemoreceptors."},
                            {"text": "Amylase enzyme acts on:", "options": ["Proteins", "Fats", "Starch", "Vitamins"], "correct_index": 2, "difficulty": "easy", "explanation": "Amylase (salivary and pancreatic) breaks down starch into maltose and then glucose."},
                            {"text": "The functional unit of the nervous system is:", "options": ["Neuroglia", "Neuron", "Axon", "Synapse"], "correct_index": 1, "difficulty": "easy", "explanation": "Neuron is the structural and functional unit of the nervous system, responsible for signal transmission."},
                            {"text": "Which vitamin is synthesized in the skin by sunlight?", "options": ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D"], "correct_index": 3, "difficulty": "easy", "explanation": "UV radiation converts 7-dehydrocholesterol in skin to Vitamin D3 (cholecalciferol)."},
                        ]
                    },
                ]
            },
            {
                "name": "Physics",
                "icon": "⚛️",
                "chapters": [
                    {
                        "name": "Modern Physics",
                        "questions": [
                            {"text": "The photoelectric effect was explained by:", "options": ["Maxwell", "Einstein", "Bohr", "Planck"], "correct_index": 1, "difficulty": "easy", "explanation": "Einstein explained the photoelectric effect in 1905 using photon concept, winning him the Nobel Prize."},
                            {"text": "Radioactive decay follows:", "options": ["Linear decay", "First order kinetics", "Second order kinetics", "Zero order kinetics"], "correct_index": 1, "difficulty": "medium", "explanation": "Radioactive decay follows first-order kinetics: N = N₀e^(-λt)."},
                            {"text": "Which radiation has the highest penetrating power?", "options": ["Alpha", "Beta", "Gamma", "Neutron"], "correct_index": 2, "difficulty": "easy", "explanation": "Gamma rays have the highest penetrating power among radioactive emissions, requiring lead or thick concrete for shielding."},
                            {"text": "The binding energy per nucleon is maximum for:", "options": ["Hydrogen", "Iron (Fe-56)", "Uranium", "Carbon"], "correct_index": 1, "difficulty": "hard", "explanation": "Iron-56 has the maximum binding energy per nucleon (~8.8 MeV), making it the most stable nucleus."},
                            {"text": "X-rays are produced when:", "options": ["Electrons hit target", "Protons hit target", "Neutrons decay", "Alpha decay occurs"], "correct_index": 0, "difficulty": "medium", "explanation": "X-rays are produced when high-energy electrons are rapidly decelerated by hitting a metal target (bremsstrahlung)."},
                            {"text": "The Bohr model of hydrogen atom predicts energy levels as:", "options": ["En = -13.6/n eV", "En = -13.6/n² eV", "En = 13.6n² eV", "En = -13.6·n eV"], "correct_index": 1, "difficulty": "medium", "explanation": "Bohr's model: En = -13.6/n² eV, where n is the principal quantum number."},
                            {"text": "Nuclear fusion requires:", "options": ["Low temperature", "High temperature and pressure", "Neutron bombardment", "Heavy elements"], "correct_index": 1, "difficulty": "easy", "explanation": "Nuclear fusion requires extremely high temperature (10⁷-10⁸ K) and pressure to overcome electrostatic repulsion."},
                            {"text": "The unit of absorbed radiation dose is:", "options": ["Curie", "Becquerel", "Gray", "Sievert"], "correct_index": 2, "difficulty": "hard", "explanation": "Gray (Gy) is the SI unit of absorbed dose; 1 Gy = 1 J/kg of energy absorbed. Sievert measures effective dose."},
                            {"text": "Wave-particle duality was proposed by:", "options": ["Einstein", "de Broglie", "Heisenberg", "Schrödinger"], "correct_index": 1, "difficulty": "medium", "explanation": "Louis de Broglie proposed in 1924 that matter has wave properties with λ = h/mv."},
                            {"text": "In nuclear fission of U-235, the number of neutrons released per fission is approximately:", "options": ["1", "2", "2.5", "3"], "correct_index": 2, "difficulty": "hard", "explanation": "On average, 2.5 neutrons are released per fission of U-235, sustaining the chain reaction."},
                        ]
                    },
                    {
                        "name": "Optics",
                        "questions": [
                            {"text": "The refractive index of a medium is defined as:", "options": ["Speed of light in vacuum / speed in medium", "Speed in medium / speed in vacuum", "Frequency × wavelength", "Angle of incidence / angle of refraction"], "correct_index": 0, "difficulty": "easy", "explanation": "Refractive index n = c/v (speed of light in vacuum / speed of light in medium)."},
                            {"text": "Total internal reflection occurs when:", "options": ["Angle < critical angle", "Angle = critical angle", "Angle > critical angle", "Light enters denser medium"], "correct_index": 2, "difficulty": "medium", "explanation": "Total internal reflection occurs when light travels from denser to rarer medium at angle greater than critical angle."},
                            {"text": "A convex lens has focal length 20 cm. Its power is:", "options": ["-5 D", "+5 D", "+20 D", "-20 D"], "correct_index": 1, "difficulty": "medium", "explanation": "Power P = 1/f(in metres) = 1/0.2 = +5 diopters. Positive for convex (converging) lens."},
                            {"text": "Young's double slit experiment demonstrates:", "options": ["Photoelectric effect", "Wave nature of light", "Particle nature of light", "Refraction"], "correct_index": 1, "difficulty": "easy", "explanation": "Young's double slit experiment shows interference fringes, demonstrating the wave nature of light."},
                            {"text": "The number of images formed by two plane mirrors at 60° angle is:", "options": ["4", "5", "6", "3"], "correct_index": 1, "difficulty": "medium", "explanation": "Images formed = (360°/θ) - 1 = (360/60) - 1 = 6 - 1 = 5 images."},
                            {"text": "Dispersion of light through prism is due to:", "options": ["Reflection", "Different speeds of different wavelengths", "Absorption", "Polarization"], "correct_index": 1, "difficulty": "medium", "explanation": "Dispersion occurs because different wavelengths travel at different speeds in glass, refracting by different amounts."},
                            {"text": "Optical fibers work on the principle of:", "options": ["Refraction", "Diffraction", "Total internal reflection", "Polarization"], "correct_index": 2, "difficulty": "easy", "explanation": "Optical fibers use total internal reflection to transmit light signals over long distances with minimal loss."},
                            {"text": "The condition for sustained interference is:", "options": ["Same frequency sources", "Coherent sources", "Same amplitude", "Point sources"], "correct_index": 1, "difficulty": "medium", "explanation": "Sustained interference requires coherent sources (constant phase difference) with same frequency."},
                            {"text": "A concave mirror forms a virtual image when object is:", "options": ["Beyond C", "At C", "Between C and F", "Between F and P"], "correct_index": 3, "difficulty": "medium", "explanation": "A concave mirror forms a virtual, erect, magnified image when object is between focus (F) and pole (P)."},
                            {"text": "In VIBGYOR, which color has the maximum wavelength?", "options": ["Violet", "Blue", "Green", "Red"], "correct_index": 3, "difficulty": "easy", "explanation": "Red has the longest wavelength (~700 nm) in the visible spectrum. Violet has the shortest (~400 nm)."},
                        ]
                    },
                    {
                        "name": "Waves & Sound",
                        "questions": [
                            {"text": "The speed of sound in air at 0°C is approximately:", "options": ["232 m/s", "332 m/s", "432 m/s", "532 m/s"], "correct_index": 1, "difficulty": "easy", "explanation": "Speed of sound in air at 0°C is approximately 332 m/s, increasing with temperature."},
                            {"text": "Beats are produced due to:", "options": ["Resonance", "Superposition of waves of slightly different frequencies", "Diffraction", "Polarization"], "correct_index": 1, "difficulty": "easy", "explanation": "Beats result from superposition of two waves with slightly different frequencies, creating periodic amplitude variation."},
                            {"text": "The Doppler effect is observed when:", "options": ["Source is stationary", "Observer is stationary", "There is relative motion between source and observer", "Medium changes"], "correct_index": 2, "difficulty": "easy", "explanation": "The Doppler effect causes apparent frequency change when there is relative motion between source and observer."},
                            {"text": "In a standing wave, nodes are points of:", "options": ["Maximum displacement", "Zero displacement", "Maximum pressure", "Maximum velocity"], "correct_index": 1, "difficulty": "medium", "explanation": "Nodes are points of zero displacement in standing waves, formed by destructive interference."},
                            {"text": "The frequency of a tuning fork depends on:", "options": ["Temperature", "Size and material", "Amplitude of vibration", "Air density"], "correct_index": 1, "difficulty": "medium", "explanation": "Tuning fork frequency depends on its size and material (density and elasticity), not temperature or amplitude."},
                            {"text": "Ultrasonic waves have frequency:", "options": ["< 20 Hz", "20 Hz to 20 kHz", "> 20 kHz", "Exactly 20 kHz"], "correct_index": 2, "difficulty": "easy", "explanation": "Ultrasonic waves have frequency > 20 kHz, above the range of human hearing."},
                            {"text": "The phenomenon of resonance requires:", "options": ["Equal frequencies of driving and natural frequency", "Different frequencies", "High amplitude", "Damping force"], "correct_index": 0, "difficulty": "medium", "explanation": "Resonance occurs when driving frequency equals the natural frequency of the system, maximizing amplitude."},
                            {"text": "Sound cannot travel through:", "options": ["Solids", "Liquids", "Gases", "Vacuum"], "correct_index": 3, "difficulty": "easy", "explanation": "Sound is a mechanical wave requiring a medium; it cannot travel through vacuum."},
                            {"text": "In a closed organ pipe, the ratio of fundamental to first overtone frequency is:", "options": ["1:2", "1:3", "1:4", "2:3"], "correct_index": 1, "difficulty": "hard", "explanation": "Closed pipe has only odd harmonics: fundamental = f, first overtone = 3f, ratio = 1:3."},
                            {"text": "The intensity of sound is measured in:", "options": ["Hertz", "Decibels", "Watts", "Newtons"], "correct_index": 1, "difficulty": "easy", "explanation": "Sound intensity level is measured in decibels (dB), a logarithmic scale of pressure relative to threshold."},
                        ]
                    },
                ]
            },
            {
                "name": "Chemistry",
                "icon": "⚗️",
                "chapters": [
                    {
                        "name": "Biomolecules",
                        "questions": [
                            {"text": "Which of the following is NOT a monosaccharide?", "options": ["Glucose", "Fructose", "Sucrose", "Galactose"], "correct_index": 2, "difficulty": "easy", "explanation": "Sucrose is a disaccharide (glucose + fructose). Glucose, fructose, and galactose are monosaccharides."},
                            {"text": "The primary structure of protein refers to:", "options": ["3D shape", "Helix or sheet", "Amino acid sequence", "Quaternary arrangement"], "correct_index": 2, "difficulty": "easy", "explanation": "Primary structure is the linear sequence of amino acids linked by peptide bonds in a polypeptide chain."},
                            {"text": "DNA double helix is held together by:", "options": ["Covalent bonds", "Hydrogen bonds between bases", "Ionic bonds", "Van der Waals forces"], "correct_index": 1, "difficulty": "medium", "explanation": "The two DNA strands are held together by hydrogen bonds between complementary base pairs (A-T: 2H bonds, G-C: 3H bonds)."},
                            {"text": "Essential fatty acids cannot be:", "options": ["Absorbed by the body", "Synthesized by the body", "Digested", "Stored in the body"], "correct_index": 1, "difficulty": "medium", "explanation": "Essential fatty acids (like linoleic acid) cannot be synthesized by the human body and must be obtained from diet."},
                            {"text": "Enzymes are:", "options": ["Inorganic catalysts", "Biological catalysts (proteins)", "Lipids", "Carbohydrates"], "correct_index": 1, "difficulty": "easy", "explanation": "Enzymes are biological catalysts, mostly proteins, that speed up biochemical reactions without being consumed."},
                            {"text": "Which vitamin is water-soluble?", "options": ["Vitamin A", "Vitamin D", "Vitamin C", "Vitamin E"], "correct_index": 2, "difficulty": "easy", "explanation": "Vitamin C (ascorbic acid) is water-soluble. Vitamins A, D, E, and K are fat-soluble."},
                            {"text": "ATP is called the 'energy currency' because:", "options": ["It stores large amounts of energy", "Its phosphate bonds release energy on hydrolysis", "It's found in all organisms", "It's cheap to produce"], "correct_index": 1, "difficulty": "medium", "explanation": "ATP releases energy (~30.5 kJ/mol) when its terminal phosphate bond is hydrolyzed, powering cellular work."},
                            {"text": "Cellulose is made of:", "options": ["α-glucose units", "β-glucose units", "Fructose units", "Galactose units"], "correct_index": 1, "difficulty": "medium", "explanation": "Cellulose consists of β-D-glucose units linked by β(1→4) glycosidic bonds, forming rigid plant cell walls."},
                            {"text": "The Km value in enzyme kinetics represents:", "options": ["Maximum velocity", "Substrate concentration at half Vmax", "Enzyme concentration", "Product concentration"], "correct_index": 1, "difficulty": "hard", "explanation": "Km (Michaelis constant) is the substrate concentration at which reaction rate = Vmax/2, indicating enzyme affinity."},
                            {"text": "Which base is NOT present in RNA?", "options": ["Adenine", "Thymine", "Guanine", "Uracil"], "correct_index": 1, "difficulty": "easy", "explanation": "RNA contains adenine, guanine, cytosine, and uracil. Thymine is found in DNA, not RNA."},
                        ]
                    },
                    {
                        "name": "Chemical Bonding",
                        "questions": [
                            {"text": "Ionic bonds form between:", "options": ["Two non-metals", "Metal and non-metal", "Two metals", "Non-metal and metalloid"], "correct_index": 1, "difficulty": "easy", "explanation": "Ionic bonds form by electron transfer between metals (which lose electrons) and non-metals (which gain electrons)."},
                            {"text": "The bond angle in water molecule is:", "options": ["90°", "104.5°", "120°", "180°"], "correct_index": 1, "difficulty": "medium", "explanation": "Water has a bent shape with bond angle 104.5° due to two lone pairs on oxygen reducing the bond angle."},
                            {"text": "VSEPR theory predicts molecular geometry based on:", "options": ["Bond length", "Electron pair repulsion", "Electronegativity", "Bond energy"], "correct_index": 1, "difficulty": "medium", "explanation": "VSEPR (Valence Shell Electron Pair Repulsion) theory predicts geometry by minimizing repulsion between electron pairs."},
                            {"text": "Which molecule has a linear shape?", "options": ["H₂O", "NH₃", "CO₂", "SO₂"], "correct_index": 2, "difficulty": "easy", "explanation": "CO₂ has two double bonds and no lone pairs on carbon, giving linear geometry (180°)."},
                            {"text": "Metallic bonds consist of:", "options": ["Electron pair sharing", "Electron transfer", "Sea of delocalized electrons", "Electrostatic attraction between ions"], "correct_index": 2, "difficulty": "medium", "explanation": "Metallic bonding involves a lattice of positive ions surrounded by a 'sea' of delocalized electrons."},
                            {"text": "Hydrogen bonding is strongest in:", "options": ["HCl", "H₂S", "HF", "HI"], "correct_index": 2, "difficulty": "medium", "explanation": "HF has the strongest hydrogen bonding because F is the most electronegative and smallest atom, creating the strongest dipole."},
                            {"text": "The octet rule states that atoms tend to:", "options": ["Lose all electrons", "Gain 8 protons", "Have 8 electrons in valence shell", "Form 8 bonds"], "correct_index": 2, "difficulty": "easy", "explanation": "The octet rule: atoms tend to gain, lose, or share electrons to achieve 8 electrons in their valence shell."},
                            {"text": "Pi (π) bonds are formed by:", "options": ["Head-on overlap of orbitals", "Lateral overlap of p orbitals", "s-s orbital overlap", "sp³ hybridization"], "correct_index": 1, "difficulty": "medium", "explanation": "Pi bonds form by lateral (sideways) overlap of parallel p orbitals, occurring in double and triple bonds."},
                            {"text": "Electronegativity difference > 1.7 indicates:", "options": ["Covalent bond", "Ionic bond", "Metallic bond", "Coordinate bond"], "correct_index": 1, "difficulty": "medium", "explanation": "Electronegativity difference > 1.7 (Pauling scale) indicates predominately ionic character in the bond."},
                            {"text": "Bond order in O₂ is:", "options": ["1", "1.5", "2", "3"], "correct_index": 2, "difficulty": "medium", "explanation": "O₂ has one sigma and one pi bond, giving bond order = 2 (double bond)."},
                        ]
                    },
                    {
                        "name": "Human Health & Disease",
                        "questions": [
                            {"text": "AIDS is caused by:", "options": ["Bacteria", "Fungi", "HIV (virus)", "Protozoa"], "correct_index": 2, "difficulty": "easy", "explanation": "AIDS is caused by HIV (Human Immunodeficiency Virus), which attacks CD4+ T lymphocytes."},
                            {"text": "Malaria is caused by:", "options": ["Virus", "Bacterium", "Plasmodium (protozoan)", "Fungus"], "correct_index": 2, "difficulty": "easy", "explanation": "Malaria is caused by Plasmodium species (P. falciparum, P. vivax, etc.), transmitted by female Anopheles mosquito."},
                            {"text": "Antibiotics are effective against:", "options": ["Viral infections", "Bacterial infections", "Fungal infections", "All of the above"], "correct_index": 1, "difficulty": "easy", "explanation": "Antibiotics specifically target bacterial processes; they are ineffective against viruses."},
                            {"text": "The innate immunity is:", "options": ["Specific to pathogens", "Non-specific, present at birth", "Acquired through vaccination", "Produced by B cells"], "correct_index": 1, "difficulty": "medium", "explanation": "Innate immunity is non-specific, present from birth, and provides the first line of defense against pathogens."},
                            {"text": "Interferons are produced by:", "options": ["B lymphocytes", "Virus-infected cells", "Red blood cells", "Platelets"], "correct_index": 1, "difficulty": "medium", "explanation": "Interferons are signaling proteins released by virus-infected cells to warn neighboring cells and stimulate immune response."},
                            {"text": "The first vaccine was developed for:", "options": ["Measles", "Polio", "Smallpox", "Typhoid"], "correct_index": 2, "difficulty": "medium", "explanation": "Edward Jenner developed the first vaccine for smallpox in 1796 using cowpox virus."},
                            {"text": "Passive immunity is achieved by:", "options": ["Vaccination", "Natural infection", "Transfer of preformed antibodies", "T cell activation"], "correct_index": 2, "difficulty": "medium", "explanation": "Passive immunity involves transfer of preformed antibodies (e.g., maternal antibodies, antiserum) without immune activation."},
                            {"text": "Tuberculosis is caused by:", "options": ["Mycobacterium tuberculosis", "Streptococcus pneumoniae", "Treponema pallidum", "Salmonella typhi"], "correct_index": 0, "difficulty": "easy", "explanation": "TB is caused by Mycobacterium tuberculosis, an acid-fast bacterium primarily affecting lungs."},
                            {"text": "Which of the following is an autoimmune disease?", "options": ["AIDS", "Malaria", "Rheumatoid arthritis", "Tuberculosis"], "correct_index": 2, "difficulty": "medium", "explanation": "Rheumatoid arthritis is an autoimmune disease where the immune system attacks joint tissues."},
                            {"text": "BCG vaccine is used for:", "options": ["Cholera", "Typhoid", "Tuberculosis", "Polio"], "correct_index": 2, "difficulty": "medium", "explanation": "BCG (Bacillus Calmette-Guérin) vaccine protects against tuberculosis and is given at birth in many countries."},
                        ]
                    },
                ]
            },
        ]
    },
]


async def seed_if_empty():
    """Only seed if DB has no exams."""
    db = get_db()
    count = await db.exams.count_documents({})
    if count == 0:
        print("🌱 DB empty — seeding...")
        await seed_all()
    else:
        print(f"✅ DB already has {count} exams — skipping seed")


async def seed_all():
    db = get_db()

    # Clear all collections
    for col in ["users", "exams", "subjects", "chapters", "questions",
                "quiz_sessions", "quiz_responses"]:
        await db[col].drop()

    exam_ids = {}
    subject_ids = {}
    chapter_ids = {}
    all_question_ids_by_chapter = {}

    # Insert exams, subjects, chapters, questions
    for exam_data in EXAM_DATA:
        exam_doc = {
            "name": exam_data["name"],
            "icon": exam_data["icon"],
            "color": exam_data["color"],
            "description": exam_data["description"],
        }
        exam_res = await db.exams.insert_one(exam_doc)
        eid = exam_res.inserted_id
        exam_ids[exam_data["name"]] = eid

        for subj_data in exam_data["subjects"]:
            subj_doc = {
                "exam_id": str(eid),
                "name": subj_data["name"],
                "icon": subj_data["icon"],
            }
            subj_res = await db.subjects.insert_one(subj_doc)
            sid = subj_res.inserted_id
            subject_ids[subj_data["name"]] = sid

            for chap_data in subj_data["chapters"]:
                chap_doc = {
                    "subject_id": str(sid),
                    "name": chap_data["name"],
                    "question_count": len(chap_data["questions"]),
                }
                chap_res = await db.chapters.insert_one(chap_doc)
                cid = chap_res.inserted_id
                chapter_ids[chap_data["name"]] = cid

                q_ids = []
                for q in chap_data["questions"]:
                    q_doc = {
                        "chapter_id": str(cid),
                        "text": q["text"],
                        "options": q["options"],
                        "correct_index": q["correct_index"],
                        "difficulty": q["difficulty"],
                        "explanation": q["explanation"],
                    }
                    q_res = await db.questions.insert_one(q_doc)
                    q_ids.append(q_res.inserted_id)

                all_question_ids_by_chapter[str(cid)] = q_ids

    print(f"✅ Inserted {len(exam_ids)} exams, subjects, chapters, 270 questions")

    # Create 50 simulated users
    nicknames = [
        "Arjun", "Priya", "Rahul", "Ananya", "Vikram", "Deepa", "Kiran",
        "Sneha", "Rohan", "Meera", "Aditya", "Kavya", "Siddharth", "Pooja",
        "Harsh", "Divya", "Akash", "Nisha", "Gaurav", "Ritu", "Manish",
        "Sunita", "Amit", "Rekha", "Vijay", "Usha", "Suresh", "Lata",
        "Ramesh", "Geeta", "Naresh", "Sita", "Lokesh", "Asha", "Dinesh",
        "Mala", "Sunil", "Savita", "Anil", "Puja", "Ravi", "Gita",
        "Mukesh", "Rani", "Ajay", "Komal", "Dev", "Swati", "Jay", "Bhavna"
    ]

    user_ids = []
    now = datetime.utcnow()

    for i, nick in enumerate(nicknames):
        user_doc = {
            "device_id": f"sim-device-{i:04d}",
            "nickname": nick,
            "last_active": now - timedelta(days=random.randint(0, 30)),
            "created_at": now - timedelta(days=random.randint(30, 90)),
        }
        u_res = await db.users.insert_one(user_doc)
        user_ids.append(u_res.inserted_id)

    chapter_id_list = list(all_question_ids_by_chapter.keys())

    # Generate realistic session history
    sessions_inserted = 0
    responses_inserted = 0

    for day_offset in range(30):
        date = now - timedelta(days=day_offset)
        # Simulate 5-20 active users per day
        n_active = random.randint(5, 20)
        active_users = random.sample(user_ids, min(n_active, len(user_ids)))

        for uid in active_users:
            # Each active user does 1-3 sessions per day
            n_sessions = random.randint(1, 3)
            for _ in range(n_sessions):
                chapter_id = random.choice(chapter_id_list)
                q_ids = all_question_ids_by_chapter[chapter_id]

                # Random start hour (peak hours: 6-9am, 5-10pm)
                if random.random() < 0.6:
                    hour = random.choice(list(range(6, 10)) + list(range(17, 23)))
                else:
                    hour = random.randint(0, 23)

                session_start = date.replace(
                    hour=hour,
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59),
                    microsecond=0,
                )

                # Simulate completion: 70% complete, 30% drop off
                n_answered = len(q_ids) if random.random() < 0.7 else random.randint(1, len(q_ids) - 1)
                status = "completed" if n_answered == len(q_ids) else "abandoned"

                session_doc = {
                    "user_id": str(uid),
                    "chapter_id": chapter_id,
                    "question_ids": [str(qid) for qid in q_ids],
                    "current_index": n_answered,
                    "score": 0,  # updated below
                    "status": status,
                    "started_at": session_start,
                    "completed_at": session_start + timedelta(minutes=random.randint(5, 20)) if status == "completed" else None,
                }

                s_res = await db.quiz_sessions.insert_one(session_doc)
                sid = s_res.inserted_id
                sessions_inserted += 1

                score = 0
                response_time = session_start
                for qi, qid in enumerate(q_ids[:n_answered]):
                    shown_at = response_time + timedelta(seconds=random.randint(1, 5))
                    duration_ms = random.randint(3000, 30000)
                    answered_at = shown_at + timedelta(milliseconds=duration_ms)

                    # Simulate realistic accuracy: 60-80%
                    is_correct = random.random() < 0.68
                    if is_correct:
                        score += 1

                    resp_doc = {
                        "session_id": str(sid),
                        "question_id": str(qid),
                        "selected_index": random.randint(0, 3),
                        "is_correct": is_correct,
                        "shown_at": shown_at,
                        "answered_at": answered_at,
                        "response_duration_ms": duration_ms,
                    }
                    await db.quiz_responses.insert_one(resp_doc)
                    responses_inserted += 1
                    response_time = answered_at

                # Update score
                await db.quiz_sessions.update_one(
                    {"_id": sid},
                    {"$set": {"score": score}}
                )

    print(f"✅ Inserted 50 users, {sessions_inserted} sessions, {responses_inserted} responses")
    print("🎉 Seed complete!")