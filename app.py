"""
BrightPath Online Coaching - Fee Calculator Website
===================================================
Course   : Python Programming for Business Students (End Term Project)
Business : Tuition / Coaching Centre  ->  "Fee Calculator"
Framework: Streamlit   (run with:  streamlit run app.py)

Only concepts taught in class are used:
  variables, int / float / str / bool, lists, input values, arithmetic operators
  (+ - * / // %), comparison operators, logical operators (and / or / not),
  membership operator (in), if / elif / else, nested if, ternary (short-hand if),
  for loops with range(), f-strings, .lower() / .upper(), len().

ALGORITHM (pseudo code)
-----------------------
Step 1 : Start
Step 2 : Read class level, subjects, mode, batch, months, plan, add-ons,
         exam percentage, sibling (yes/no) and coupon code
Step 3 : If no subject is selected -> show warning and go to Step 12
Step 4 : Find the fee per subject for the level, mode and batch
Step 5 : tuition = monthly fee x number of subjects x months
Step 6 : add-ons = (sum of add-on prices) x months
Step 7 : If months >= 6 (or paying upfront) registration = 0, else registration = 500
Step 8 : Find each discount % using if / elif / else and add them together
Step 9 : If total discount > 35%, set it to 35%
Step 10: taxable = tuition - discount + add-ons + registration ; GST = 18% of taxable
Step 11: total = taxable + GST ; instalment = total / number of instalments
Step 12: Display the result
Step 13: Stop

NOTE: Institute name, teachers, prices and address are SAMPLE data made up for
this academic project. Change the lists below to change the website.
"""

import streamlit as st                          # the web framework
import streamlit.components.v1 as components    # used only to embed the Google Map
from datetime import date                       # today's date for the fee quote

# ---------------------------------------------------------------------------
# 1. PAGE SETTINGS (must be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="BrightPath Online Coaching", page_icon="🎓", layout="wide")

# ---------------------------------------------------------------------------
# 2. BUSINESS DATA  (stored in variables and lists - no database needed)
# ---------------------------------------------------------------------------
institute = "BrightPath Online Coaching"        # str
phone = "+91 98765 43210"                       # str
email = "hello@brightpath-coaching.example"     # str
address = "Model Town, Sonipat, Haryana 131001, India"
map_query = "Model Town, Sonipat, Haryana, India"   # text that Google Maps searches for

gst_rate = 0.18             # float : 18% GST on coaching services
registration_fee = 500      # int   : one-time fee (free for plans of 6+ months)
max_discount = 0.35         # float : total discount can never be more than 35%

# Class levels. The lists below are "parallel": position 0 of every list
# belongs to the first level, position 1 to the second level, and so on.
levels = ["Class 6-8", "Class 9-10", "Class 11-12", "JEE Preparation", "NEET Preparation"]
level_fees = [800, 1200, 1800, 2800, 2800]          # group-class fee per subject per month
level_subjects = [
    ["Mathematics", "Science", "English", "Social Science", "Hindi"],
    ["Mathematics", "Science", "English", "Social Science", "Computer Science"],
    ["Physics", "Chemistry", "Mathematics", "Biology", "English", "Computer Science"],
    ["Physics", "Chemistry", "Mathematics"],
    ["Physics", "Chemistry", "Biology"],
]
level_info = [
    "Strong foundation in concepts, NCERT based, with weekly practice tests.",
    "Board exam focus (CBSE / HBSE) with sample papers and Olympiad preparation.",
    "Board + competitive exam base. Concept videos and doubt classes.",
    "Complete JEE Main & Advanced programme with all-India test series.",
    "Complete NEET-UG programme with NCERT line-by-line coverage.",
]
level_days = ["5 days / week", "5 days / week", "6 days / week", "6 days / week", "6 days / week"]
level_time = ["4:00 PM - 6:00 PM", "5:00 PM - 7:30 PM", "6:00 PM - 9:00 PM",
              "5:00 PM - 9:30 PM", "5:00 PM - 9:30 PM"]

# How the class is delivered, and the price multiplier for each
modes = ["Live Classes", "Recorded Lectures", "Live + Recordings (Hybrid)"]
mode_multipliers = [1.00, 0.60, 1.15]

# Batch size, and the price multiplier. One-on-One is priced by teacher hourly rate.
batches = ["Group Batch (25-30 students)", "Small Batch (max 8 students)", "One-on-One (private)"]
batch_multipliers = [1.0, 1.5, 1.0]

# Optional add-ons and their price per month
addon_names = ["Printed + PDF Study Material", "Weekly Mock Test Series",
               "Unlimited Doubt-Clearing Sessions"]
addon_prices = [400, 600, 300]

# Payment plans and the discount for each
plan_names = ["Monthly", "Quarterly (every 3 months)", "Full payment upfront"]
plan_discounts = [0.00, 0.03, 0.07]

# Teachers. Each row is: subject, name, qualification, experience (years),
# rating, students taught, private fee per hour (Rs), languages, short bio
teachers = [
    ["Mathematics", "Dr. Rakesh Malhotra", "Ph.D. Mathematics, IIT Delhi", 15, 4.9, 3200, 900,
     "English, Hindi", "Makes calculus and algebra easy with real-life examples. JEE Advanced mentor."],
    ["Physics", "Prof. Anita Sharma", "M.Sc. Physics, B.Ed., Delhi University", 12, 4.8, 2700, 850,
     "English, Hindi", "Known for animated concept videos and numerical-solving shortcuts."],
    ["Chemistry", "Mr. Vivek Arora", "M.Sc. Chemistry, Kurukshetra University", 10, 4.7, 2400, 800,
     "English, Hindi", "Organic chemistry specialist with easy memory tricks for reactions."],
    ["Biology", "Dr. Neha Kapoor", "M.Sc., Ph.D. Life Sciences", 11, 4.9, 2100, 850,
     "English, Hindi", "NEET topper-trainer; teaches with diagrams and flowcharts."],
    ["English", "Ms. Priya Sethi", "M.A. English, B.Ed.", 9, 4.8, 1900, 600,
     "English", "Grammar, writing skills and spoken English for all levels."],
    ["Science", "Mr. Sandeep Yadav", "M.Sc. Physics, B.Ed.", 8, 4.7, 2300, 600,
     "English, Hindi", "Experiment-based teaching for Class 6-10 integrated science."],
    ["Social Science", "Mrs. Kavita Rana", "M.A. History, B.Ed.", 14, 4.8, 2000, 550,
     "English, Hindi", "Turns history, civics and geography into stories with maps and timelines."],
    ["Hindi", "Mr. Mohit Dahiya", "M.A. Hindi, B.Ed.", 13, 4.6, 1500, 500,
     "Hindi", "Vyakaran and literature expert; helps with letter and essay writing."],
    ["Computer Science", "Mr. Aman Verma", "B.Tech. CSE, M.Tech. AI", 7, 4.9, 1300, 750,
     "English, Hindi", "Teaches Python from scratch with mini-projects and coding challenges."],
]

# Weekly timetable: day, slot 1, slot 2, slot 3
timetable = [
    ["Monday", "Mathematics", "Physics", "English"],
    ["Tuesday", "Chemistry", "Science", "Computer Science"],
    ["Wednesday", "Mathematics", "Biology", "Social Science"],
    ["Thursday", "Physics", "Chemistry", "Hindi"],
    ["Friday", "Mathematics", "Biology", "English"],
    ["Saturday", "Doubt Class", "Mock Test", "Revision"],
]

faq_questions = [
    "How do the online classes work?",
    "Can I try a class before paying?",
    "What is the refund policy?",
    "Which devices can I use?",
    "How is the fee calculated?",
]
faq_answers = [
    "Classes run on a live video platform. You can ask questions in chat, and every class is recorded so you can watch it again.",
    "Yes. Every student gets 2 free demo classes. Use the Contact page to book one.",
    "100% refund within the first 7 days if you are not satisfied. After that, unused full months are refunded.",
    "A phone, tablet, laptop or desktop with a normal internet connection is enough.",
    "Use the Fee Calculator tab. It adds subject fees, add-ons and registration, subtracts discounts, and finally adds 18% GST.",
]

# ---------------------------------------------------------------------------
# 3. STYLING (CSS) - makes the website look professional
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=DM+Sans:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap');
    :root { --brand:#0e4f5c; --accent:#f0a202; --ink:#13222b; --muted:#5b6b75; --line:#dde3e8; --tint:#e6f0f2; }
    html, body, [class*="css"], .stApp { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    .stApp { background: #f4f6f8; }
    h1, h2, h3, h4 { font-family: 'Bricolage Grotesque', sans-serif !important; color: var(--ink); letter-spacing: -.01em; }
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    .block-container { padding-top: 1rem; max-width: 1180px; }

    /* top brand bar */
    .brandbar { display:flex; align-items:center; gap:10px; padding:.4rem 0 .2rem 0; }
    .logo { width:34px; height:34px; border-radius:9px; background:var(--brand); color:#fff;
            display:grid; place-items:center; font-family:'Bricolage Grotesque',sans-serif; font-weight:800; }
    .brandname { font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.25rem; color:var(--brand); }

    /* navigation tabs look like the pill menu of the preview */
    .stTabs [data-baseweb="tab-list"] { gap:4px; border-bottom:1px solid var(--line); padding-bottom:10px; flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"] { height:auto; padding:8px 14px; border-radius:8px; color:var(--muted);
                                   font-weight:500; background:transparent; }
    .stTabs [data-baseweb="tab"]:hover { background:var(--tint); color:var(--ink); }
    .stTabs [aria-selected="true"] { background:var(--brand) !important; color:#fff !important; }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }

    /* hero */
    .eyebrow { font-family:'DM Mono',monospace; font-size:.78rem; text-transform:uppercase;
               letter-spacing:.12em; color:var(--brand); }
    .hero h1 { font-size:clamp(2.1rem,4.6vw,3.4rem); font-weight:800; line-height:1.1; margin:.6rem 0 .9rem 0; }
    .hero h1 em { font-style:normal; color:var(--brand);
                  background:linear-gradient(transparent 62%, rgba(240,162,2,.5) 62%); }
    .hero p.lead { color:var(--muted); max-width:60ch; }
    .ticket { background:#fff; border:1px solid var(--line); border-radius:14px; padding:1.2rem 1.3rem; }
    .ticket h4 { margin:.3rem 0 .8rem 0; font-size:1.05rem; }
    .trow { display:flex; justify-content:space-between; gap:12px; border-bottom:1px dashed var(--line);
            padding:.4rem 0; }
    .trow span { color:var(--muted); }
    .trow b { font-family:'DM Mono',monospace; }
    .trow.last { border:0; font-size:1.2rem; }
    .trow.last b { color:var(--brand); }

    /* stats strip */
    .stats { display:grid; grid-template-columns:repeat(4,1fr); border-top:1px solid var(--line);
             border-bottom:1px solid var(--line); margin:1.4rem 0; }
    .stats div { padding:1rem; border-right:1px solid var(--line); }
    .stats div:last-child { border-right:0; }
    .stats b { display:block; font-family:'Bricolage Grotesque',sans-serif; font-size:1.9rem; color:var(--brand); }
    .stats span { color:var(--muted); font-size:.9rem; }

    /* cards */
    .card { background:#fff; border:1px solid var(--line); border-radius:14px; padding:1.1rem 1.2rem;
            margin-bottom:1rem; color:var(--ink); }
    .card h4 { margin:0 0 .3rem 0; }
    .avatar { width:64px; height:64px; border-radius:50%; background:var(--tint); color:var(--brand);
              border:2px solid var(--brand); display:flex; align-items:center; justify-content:center;
              font-family:'Bricolage Grotesque',sans-serif; font-size:1.3rem; font-weight:800;
              float:left; margin-right:1rem; }
    .tag { display:inline-block; background:var(--tint); color:var(--brand); border-radius:99px;
           padding:.1rem .65rem; font-size:.76rem; margin:.2rem .3rem 0 0; font-weight:700; }

    /* result box of the calculator */
    .total-box { background:var(--brand); color:#fff; border-radius:12px; padding:1.1rem 1.3rem; margin:.5rem 0 1rem 0; }
    .big { font-family:'Bricolage Grotesque',sans-serif; font-size:2.5rem; font-weight:800; line-height:1.1; }
    .small { color:rgba(255,255,255,.85); font-size:.9rem; }

    /* Streamlit widgets styled like the preview */
    .stTextInput input, .stNumberInput input, [data-baseweb="select"] > div {
        border-radius:9px !important; border:1.5px solid var(--line) !important; background:#fff; }
    span[data-baseweb="tag"] { background:var(--brand) !important; color:#fff !important; border-radius:99px !important; }
    span[data-baseweb="tag"] span { color:#fff !important; }
    [data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:10px; padding:.6rem .8rem; }
    [data-testid="stMetricValue"] { font-family:'DM Mono',monospace; font-size:1.1rem; }
    .stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
        background:var(--brand); color:#fff; border:0; border-radius:10px; font-weight:700; padding:.55rem 1.2rem; }
    .stButton > button:hover, .stDownloadButton > button:hover { background:#0b3f49; color:#fff; }
    [data-testid="stExpander"] { background:#fff; border:1px solid var(--line); border-radius:12px; }
    table { font-size:.93rem; }
    th { font-family:'DM Mono',monospace; font-size:.75rem; text-transform:uppercase; color:var(--muted); }
    .footer { text-align:center; color:var(--muted); font-size:.85rem; padding:1.5rem 0 .5rem 0;
              border-top:1px solid var(--line); margin-top:2rem; }
    @media (max-width:800px) { .stats { grid-template-columns:repeat(2,1fr); } }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 4. HERO BANNER + NAVIGATION TABS
# ---------------------------------------------------------------------------
# brand bar at the top
st.markdown(
    f'<div class="brandbar"><span class="logo">B</span><span class="brandname">BrightPath</span></div>',
    unsafe_allow_html=True,
)

tab_home, tab_calc, tab_price, tab_classes, tab_teachers, tab_contact = st.tabs(
    ["Home", "Fee Calculator", "Pricing", "Subjects & Classes", "Teachers", "Contact & Map"]
)

# ===========================================================================
# TAB 1 : HOME
# ===========================================================================
with tab_home:
    # Example quote shown in the hero: Class 9-10, Maths + Science, 6 months (simple arithmetic)
    ex_tuition = 1200 * 2 * 6              # fee x subjects x months
    ex_discount = ex_tuition * 0.15        # 5% multi-subject + 10% duration
    ex_gst = (ex_tuition - ex_discount) * gst_rate
    ex_total = ex_tuition - ex_discount + ex_gst

    hero_left, hero_right = st.columns([1.2, 0.9], gap="large")
    with hero_left:
        st.markdown(
            '<div class="hero"><span class="eyebrow">Admissions open 2026-27</span>'
            '<h1>Know your coaching fee <em>before</em> you enrol.</h1>'
            '<p class="lead">Live classes from nine expert teachers, for Class 6 to NEET and JEE. '
            'Pick subjects, batch and duration, and the Fee Calculator tab prices it in seconds, GST included.</p></div>',
            unsafe_allow_html=True,
        )
    with hero_right:
        st.markdown(
            '<div class="ticket"><span class="eyebrow">Example quote</span>'
            '<h4>Class 9-10 · Maths + Science · 6 months</h4>'
            f'<div class="trow"><span>Tuition</span><b>₹{ex_tuition:,.2f}</b></div>'
            f'<div class="trow"><span>Discount (15%)</span><b>-₹{ex_discount:,.2f}</b></div>'
            f'<div class="trow"><span>GST 18%</span><b>₹{ex_gst:,.2f}</b></div>'
            f'<div class="trow last"><span>Total</span><b>₹{ex_total:,.2f}</b></div></div>',
            unsafe_allow_html=True,
        )

    # statistics strip: numbers and labels are stored in two lists, built with a for loop
    stat_numbers = ["12,000+", "9", "96%", "4.8 / 5"]
    stat_labels = ["Students taught", "Expert teachers", "Pass with 80%+", "Average rating"]
    stats_html = '<div class="stats">'
    for i in range(4):
        stats_html += f"<div><b>{stat_numbers[i]}</b><span>{stat_labels[i]}</span></div>"
    stats_html += "</div>"
    st.markdown(stats_html, unsafe_allow_html=True)

    st.subheader("Why students choose us")
    feature_titles = ["Live + recorded classes", "Small batches", "Weekly tests",
                      "Doubt clearing", "Transparent fees", "Proven results"]
    feature_texts = [
        "Attend live or revise later with lifetime recordings.",
        "Group, small batch (max 8) or fully private one-on-one.",
        "Mock tests with detailed performance reports for parents.",
        "Ask doubts any time and get answers within 2 hours.",
        "Up to 35% discount. No hidden charges. Easy instalments.",
        "Our students scored 95%+ in CBSE boards, JEE and NEET.",
    ]
    feature_cols = st.columns(3)
    for i in range(6):
        # i % 3 gives the column number 0,1,2,0,1,2  (modulus operator)
        feature_cols[i % 3].markdown(
            f'<div class="card"><h4>{feature_titles[i]}</h4>{feature_texts[i]}</div>',
            unsafe_allow_html=True,
        )

    st.subheader("Frequently asked questions")
    for i in range(len(faq_questions)):
        with st.expander(faq_questions[i]):
            st.write(faq_answers[i])

# ===========================================================================
# TAB 2 : FEE CALCULATOR  (main feature)
# ===========================================================================
with tab_calc:
    st.header("Course fee calculator")
    st.caption("Choose your options on the left. Your fee updates instantly on the right.")

    left, right = st.columns([1, 1.15], gap="large")

    # ----------------------------- INPUTS (left side) -----------------------
    with left:
        st.subheader("1. Student details")
        student_name = st.text_input("Student name (optional)", placeholder="e.g. Aarav Sharma")

        # INPUT 1 : class level (str)
        level = st.selectbox("Class / Course", levels, index=1)

        # Find the subjects of the chosen level (loop + if + list indexing)
        subject_options = []
        for i in range(len(levels)):
            if levels[i] == level:
                subject_options = level_subjects[i]

        # INPUT 2 : subjects (list of str)
        subjects = st.multiselect("Subjects", subject_options, default=subject_options[:2],
                                  help="Join 2 or more subjects to get a multi-subject discount.")

        st.subheader("2. How do you want to learn?")
        # INPUT 3 : class mode (str)
        mode = st.radio("Class mode", modes, horizontal=True)

        # INPUT 4 : batch type (str)
        batch = st.selectbox("Batch type", batches)

        # Conditional input: ask for hours only for One-on-One classes
        hours_per_week = 2                                  # int (default value)
        if batch == "One-on-One (private)":
            hours_per_week = st.slider("Private hours per subject per week", 1, 5, 2)
            st.info("One-on-One classes are always live and are priced by the teacher's hourly rate.")

        st.subheader("3. Duration & payment")
        # INPUT 5 : number of months (int)
        months = st.number_input("Duration (months)", min_value=1, max_value=12, value=6, step=1)

        # INPUT 6 : payment plan (str)
        plan = st.selectbox("Payment plan", plan_names)

        st.subheader("4. Add-ons & discounts")
        # INPUT 7 : add-ons (list of str)
        chosen_addons = st.multiselect("Optional add-ons", addon_names)

        # INPUT 8 : last exam percentage (float)
        score = st.number_input("Last exam percentage (for scholarship)",
                                min_value=0.0, max_value=100.0, value=75.0, step=0.5)

        # INPUT 9 : sibling checkbox (bool)
        sibling = st.checkbox("Sibling already studying with us (extra 5% off)")

        # INPUT 10 : coupon code (str)
        coupon_code = st.text_input("Coupon code", placeholder="Try WELCOME10 or BRIGHT5")

    # ----------------------------- OUTPUT (right side) ----------------------
    with right:
        st.subheader("Your fee estimate")

        months = int(months)                     # make sure months is a whole number (int)
        coupon = coupon_code.strip().upper()     # string methods: remove spaces, capital letters

        # ---- INPUT VALIDATION: the app never crashes on bad input -----------
        if len(subjects) == 0:
            st.warning("Please select at least one subject.")
        elif months < 1:
            st.warning("Duration must be at least 1 month.")
        elif score < 0 or score > 100:
            st.warning("Percentage must be between 0 and 100.")
        else:
            # ==================== STEP 1 : fee per subject ====================
            n_subjects = len(subjects)                     # number of chosen subjects (int)

            # find the group fee of the chosen level
            level_fee = 0
            for i in range(len(levels)):
                if levels[i] == level:
                    level_fee = level_fees[i]

            # find mode multiplier and batch multiplier
            mode_multiplier = 1.0
            for i in range(len(modes)):
                if modes[i] == mode:
                    mode_multiplier = mode_multipliers[i]

            batch_multiplier = 1.0
            for i in range(len(batches)):
                if batches[i] == batch:
                    batch_multiplier = batch_multipliers[i]

            # ==================== STEP 2 : monthly tuition ====================
            monthly_tuition = 0.0
            if batch == "One-on-One (private)":
                # private class: teacher hourly rate x hours per week x 4 weeks
                for subject in subjects:
                    for t in teachers:
                        if t[0] == subject:
                            monthly_tuition += t[6] * hours_per_week * 4
            else:
                # group / small batch: fee x mode x batch multiplier, for each subject
                monthly_tuition = level_fee * mode_multiplier * batch_multiplier * n_subjects

            tuition_total = monthly_tuition * months

            # ==================== STEP 3 : add-ons ============================
            addon_total = 0
            for i in range(len(addon_names)):
                if addon_names[i] in chosen_addons:        # membership operator
                    addon_total += addon_prices[i] * months

            # ==================== STEP 4 : registration fee ===================
            # waived for long plans OR when the whole fee is paid upfront
            if months >= 6 or plan == "Full payment upfront":
                registration = 0
            else:
                registration = registration_fee

            # ==================== STEP 5 : discounts ==========================
            # (a) multi-subject discount
            if n_subjects >= 4:
                multi_disc = 0.15
            elif n_subjects == 3:
                multi_disc = 0.10
            elif n_subjects == 2:
                multi_disc = 0.05
            else:
                multi_disc = 0.0

            # (b) duration discount
            if months >= 12:
                duration_disc = 0.15
            elif months >= 6:
                duration_disc = 0.10
            elif months >= 3:
                duration_disc = 0.05
            else:
                duration_disc = 0.0

            # (c) payment plan discount
            plan_disc = 0.0
            for i in range(len(plan_names)):
                if plan_names[i] == plan:
                    plan_disc = plan_discounts[i]

            # (d) merit scholarship based on last exam percentage
            if score >= 90:
                merit_disc = 0.10
            elif score >= 80:
                merit_disc = 0.05
            else:
                merit_disc = 0.0

            # (e) sibling discount (short-hand if / ternary operator)
            sibling_disc = 0.05 if sibling else 0.0

            # (f) coupon code - nested if
            coupon_disc = 0.0
            coupon_message = ""
            if coupon != "":
                if coupon == "WELCOME10":
                    coupon_disc = 0.10
                    coupon_message = "valid"
                elif coupon == "BRIGHT5":
                    coupon_disc = 0.05
                    coupon_message = "valid"
                else:
                    coupon_message = "invalid"

            # add all discount rates together
            discount_rate = (multi_disc + duration_disc + plan_disc +
                             merit_disc + sibling_disc + coupon_disc)

            # the discount can never be more than the maximum allowed
            capped = False
            if discount_rate > max_discount:
                discount_rate = max_discount
                capped = True

            discount_amount = tuition_total * discount_rate     # discount on tuition only

            # ==================== STEP 6 : GST and grand total ================
            taxable = tuition_total - discount_amount + addon_total + registration
            gst = taxable * gst_rate
            grand_total = taxable + gst

            # ==================== STEP 7 : instalments ========================
            if plan == "Monthly":
                installments = months
            elif plan == "Quarterly (every 3 months)":
                installments = (months + 2) // 3        # floor division: rounds up to whole quarters
            else:
                installments = 1
            per_installment = grand_total / installments
            per_month = grand_total / months

            # ==================== SHOW THE RESULT =============================
            st.markdown(
                '<div class="total-box"><div class="small">Total payable (incl. 18% GST)</div>'
                f'<div class="big">₹{grand_total:,.2f}</div>'
                f'<div class="small">{installments} instalment(s) of ₹{per_installment:,.2f} '
                f'&nbsp;·&nbsp; about ₹{per_month:,.2f} / month</div></div>',
                unsafe_allow_html=True,
            )

            m1, m2, m3 = st.columns(3)
            m1.metric("Monthly tuition", f"₹{monthly_tuition:,.2f}")
            m2.metric("You save", f"₹{discount_amount:,.2f}", f"{discount_rate * 100:.0f}% off")
            m3.metric("GST (18%)", f"₹{gst:,.2f}")

            # messages for coupon, discount cap and registration waiver
            if coupon_message == "valid":
                st.success("Coupon applied.")
            elif coupon_message == "invalid":
                st.warning("This coupon code is not valid. Try WELCOME10 or BRIGHT5.")
            if capped:
                st.info(f"Discounts were capped at the maximum of {max_discount * 100:.0f}%.")
            if registration == 0:
                st.success("Registration fee waived for you.")

            # ---- fee breakdown table (built as a string and shown as Markdown) ----
            st.markdown("##### Fee breakdown")
            table = "| Item | Amount |\n|---|---:|\n"
            table += f"| Tuition fee ({n_subjects} subject(s) × {months} month(s)) | ₹{tuition_total:,.2f} |\n"
            table += f"| Add-ons | ₹{addon_total:,.2f} |\n"
            table += f"| Registration fee | ₹{registration:,.2f} |\n"
            table += f"| Discount ({discount_rate * 100:.0f}%) | -₹{discount_amount:,.2f} |\n"
            table += f"| Taxable amount | ₹{taxable:,.2f} |\n"
            table += f"| GST (18%) | ₹{gst:,.2f} |\n"
            table += f"| **TOTAL PAYABLE** | **₹{grand_total:,.2f}** |\n"
            st.markdown(table)

            # ---- how the discount was calculated -----------------------------
            with st.expander("See how your discount was calculated"):
                discount_names = ["Multi-subject discount", "Duration discount", "Payment plan discount",
                                  "Merit scholarship", "Sibling discount", "Coupon"]
                discount_values = [multi_disc, duration_disc, plan_disc, merit_disc, sibling_disc, coupon_disc]
                for i in range(len(discount_names)):
                    if discount_values[i] > 0:                  # show only the discounts you got
                        st.write(f"- {discount_names[i]}: **{discount_values[i] * 100:.0f}%**")
                st.write(f"**Total discount: {discount_rate * 100:.0f}%**")

            # ---- payment schedule (loop) -------------------------------------
            st.markdown("##### Payment schedule")
            schedule = "| Instalment | Amount |\n|---|---:|\n"
            for n in range(1, installments + 1):
                schedule += f"| {n} | ₹{per_installment:,.2f} |\n"
            st.markdown(schedule)

            # ---- teachers for the chosen subjects ----------------------------
            st.markdown("##### Your teachers")
            for subject in subjects:
                for t in teachers:
                    if t[0] == subject:
                        st.write(f"**{subject}** - {t[1]} ({t[3]} years experience, ★ {t[4]})")

            # ---- downloadable fee quote (plain text) -------------------------
            quote = f"{institute} - FEE QUOTE\n"
            quote += "=" * 44 + "\n"
            quote += f"Date           : {date.today().strftime('%d %b %Y')}\n"
            quote += f"Student        : {student_name if student_name != '' else 'Not provided'}\n"
            quote += f"Class level    : {level}\n"
            quote += "Subjects       : " + ", ".join(subjects) + "\n"
            quote += f"Mode / Batch   : {mode} / {batch}\n"
            quote += f"Duration       : {months} month(s)\n"
            quote += f"Payment plan   : {plan}\n"
            quote += "-" * 44 + "\n"
            quote += f"Tuition fee         : Rs {tuition_total:,.2f}\n"
            quote += f"Add-ons             : Rs {addon_total:,.2f}\n"
            quote += f"Registration fee    : Rs {registration:,.2f}\n"
            quote += f"Discount ({discount_rate * 100:.0f}%)      : -Rs {discount_amount:,.2f}\n"
            quote += f"GST (18%)           : Rs {gst:,.2f}\n"
            quote += "-" * 44 + "\n"
            quote += f"TOTAL PAYABLE       : Rs {grand_total:,.2f}\n"
            quote += f"{installments} instalment(s) of Rs {per_installment:,.2f}\n\n"
            quote += "This is an estimate. Contact: " + phone + "\n"
            st.download_button("Download fee quote (.txt)", quote, file_name="BrightPath_fee_quote.txt")

# ===========================================================================
# TAB 3 : PRICING
# ===========================================================================
with tab_price:
    st.header("Transparent pricing")
    st.write("Monthly fee **per subject** for each class level. Use the calculator for your exact total.")

    # one row per level; columns = mode / batch (fee x multiplier)
    price_table = "| Class / Course | Live (Group) | Hybrid | Recorded | Small Batch (max 8) |\n|---|---|---|---|---|\n"
    for i in range(len(levels)):
        live = level_fees[i] * mode_multipliers[0]
        hybrid = level_fees[i] * mode_multipliers[2]
        recorded = level_fees[i] * mode_multipliers[1]
        small = level_fees[i] * batch_multipliers[1]
        price_table += f"| {levels[i]} | ₹{live:,.0f} | ₹{hybrid:,.0f} | ₹{recorded:,.0f} | ₹{small:,.0f} |\n"
    st.markdown(price_table)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Discounts you can get")
        st.markdown(
            "| Offer | Discount |\n|---|---|\n"
            "| 2 subjects / 3 subjects / 4+ subjects | 5% / 10% / 15% |\n"
            "| 3-5 months / 6-11 months / 12 months | 5% / 10% / 15% |\n"
            "| Pay quarterly / pay full upfront | 3% / 7% |\n"
            "| Last exam 80%+ / 90%+ | 5% / 10% |\n"
            "| Sibling already enrolled | 5% |\n"
            "| Coupons `WELCOME10` / `BRIGHT5` | 10% / 5% |\n"
        )
        st.caption(f"Maximum total discount: {max_discount * 100:.0f}%. Discounts apply on tuition only.")

    with c2:
        st.subheader("Add-ons & other charges")
        addon_table = "| Add-on | Price |\n|---|---|\n"
        for i in range(len(addon_names)):
            addon_table += f"| {addon_names[i]} | ₹{addon_prices[i]:,} / month |\n"
        addon_table += f"| Registration (one-time, free for 6+ months) | ₹{registration_fee:,} |\n"
        addon_table += "| GST on all services | 18% |\n"
        st.markdown(addon_table)

    st.subheader("One-on-One private tuition (per hour)")
    private_table = "| Subject | Teacher | Fee per hour |\n|---|---|---|\n"
    for t in teachers:
        private_table += f"| {t[0]} | {t[1]} | ₹{t[6]:,} |\n"
    st.markdown(private_table)

# ===========================================================================
# TAB 4 : SUBJECTS & CLASSES
# ===========================================================================
with tab_classes:
    st.header("Subjects and classes")

    chosen_level = st.selectbox("Select class / course", levels, key="class_level")

    for i in range(len(levels)):
        if levels[i] == chosen_level:
            st.markdown(
                f'<div class="card"><h4>{levels[i]}</h4>{level_info[i]}<br><br>'
                f'<span class="tag">{level_days[i]}</span><span class="tag">{level_time[i]}</span>'
                f'<span class="tag">From ₹{level_fees[i] * mode_multipliers[1]:,.0f} / subject / month</span></div>',
                unsafe_allow_html=True,
            )

            st.subheader("Subjects in this course")
            subject_cols = st.columns(3)
            position = 0
            for subject in level_subjects[i]:
                for t in teachers:
                    if t[0] == subject:
                        subject_cols[position % 3].markdown(
                            f'<div class="card"><h4>{subject}</h4>Teacher: <b>{t[1]}</b><br>'
                            f'Group fee: ₹{level_fees[i]:,}/month<br>'
                            f'Private: ₹{t[6]:,}/hour</div>',
                            unsafe_allow_html=True,
                        )
                position += 1

    st.subheader("Weekly timetable (sample)")
    time_table = "| Day | Slot 1 | Slot 2 | Slot 3 |\n|---|---|---|---|\n"
    for row in timetable:
        time_table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |\n"
    st.markdown(time_table)
    st.caption("Exact timings depend on your batch. Saturday is for doubts, tests and revision.")

# ===========================================================================
# TAB 5 : TEACHERS
# ===========================================================================
with tab_teachers:
    st.header("Meet our teachers")

    # build the filter list with a loop
    subject_filter = ["All subjects"]
    for t in teachers:
        subject_filter.append(t[0])
    pick = st.selectbox("Filter by subject", subject_filter)

    # keep only the teachers that match the filter
    shown = []
    for t in teachers:
        if pick == "All subjects" or t[0] == pick:
            shown.append(t)

    teacher_cols = st.columns(2)
    for i in range(len(shown)):
        t = shown[i]
        # initials = first letters of the first and last name  (e.g. "Dr. Rakesh Malhotra" -> "RM")
        words = t[1].split()
        initials = words[1][0] + words[-1][0]
        teacher_cols[i % 2].markdown(
            f'<div class="card"><div class="avatar">{initials}</div>'
            f'<h4>{t[1]}</h4><span class="tag">{t[0]}</span><span class="tag">★ {t[4]}</span>'
            f'<p style="margin:.6rem 0 0 0; clear:both;">'
            f'{t[2]}<br>{t[3]} years experience · {t[5]:,}+ students<br>'
            f'Languages: {t[7]}<br>Private tuition: <b>₹{t[6]:,}/hour</b><br><i>{t[8]}</i></p></div>',
            unsafe_allow_html=True,
        )

    st.caption("Teacher profiles are sample data created for this academic project.")

# ===========================================================================
# TAB 6 : CONTACT & MAP
# ===========================================================================
with tab_contact:
    st.header("Contact and location")
    info_col, form_col = st.columns([1, 1], gap="large")

    with info_col:
        st.markdown(
            f'<div class="card"><h4>Visit our centre</h4>{address}<br>{phone}<br>'
            f'{email}<br>Mon-Sat: 9:00 AM - 8:00 PM</div>',
            unsafe_allow_html=True,
        )

        # Google Maps embed - no API key needed (spaces in the text are replaced by +)
        map_text = map_query.replace(" ", "+")
        components.iframe("https://maps.google.com/maps?q=" + map_text + "&output=embed", height=360)
        st.markdown(f"[Open in Google Maps ↗](https://www.google.com/maps/search/?api=1&query={map_text})")

    with form_col:
        st.subheader("Book a free demo class")
        with st.form("enquiry_form"):
            f_name = st.text_input("Your name")
            f_phone = st.text_input("Phone number (10 digits)")
            f_email = st.text_input("E-mail")
            f_course = st.selectbox("Interested in", levels)
            f_msg = st.text_area("Message (optional)")
            submitted = st.form_submit_button("Request demo class")

        if submitted:
            # input validation using if / elif / else
            if f_name.strip() == "":
                st.error("Please enter your name.")
            elif not (f_phone.isdigit() and len(f_phone) == 10):
                st.error("Phone number must be exactly 10 digits.")
            elif "@" not in f_email or "." not in f_email:
                st.error("Please enter a valid e-mail address.")
            else:
                st.success(f"Thank you {f_name.strip()}! We will call you on {f_phone} "
                           f"within 24 hours to schedule your {f_course} demo class.")

# ---------------------------------------------------------------------------
# 5. FOOTER
# ---------------------------------------------------------------------------
st.markdown(
    f'<div class="footer">© 2026 {institute} · Sample website for an academic project · '
    f'Built with Python & Streamlit</div>',
    unsafe_allow_html=True,
)
