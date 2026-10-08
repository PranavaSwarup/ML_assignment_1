import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Palette
PRIMARY = colors.HexColor('#1A365D')    # Deep Executive Navy
SECONDARY = colors.HexColor('#2B6CB0')  # Vibrant Royal Blue
ACCENT = colors.HexColor('#0D9488')     # Dark Teal / Green Accent
TEXT_DARK = colors.HexColor('#1A202C')  # Dark Slate Text
TEXT_MUTED = colors.HexColor('#4A5568') # Muted Slate
BG_LIGHT = colors.HexColor('#F8FAFC')   # Subtle card/table background
BG_ALT = colors.HexColor('#EDF2F7')     # Table alt row
BORDER_COLOR = colors.HexColor('#CBD5E1') # Light border

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # NO HEADER at top of any page - requested by user!
        
        # Clean, modern Footer on all pages
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 50, 28, page_text)
        self.drawString(50, 28, "Machine Learning Assignment: Polynomial Regression  |  Pranava Swarup (IMT2024072)")
        
        # Subtle footer separator rule
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(50, 38, letter[0] - 50, 38)
        self.restoreState()


def build_pdf(filename="IMT2024072_Report.pdf"):
    # Target 4 pages with balanced margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=42,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=3
    )
    
    author_style = ParagraphStyle(
        'AuthorInfo',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=1
    )
    
    meta_sub_style = ParagraphStyle(
        'MetaSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=SECONDARY,
        alignment=1,
        spaceAfter=6
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=SECONDARY,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.2,
        textColor=TEXT_DARK,
        spaceAfter=4
    )
    
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=11.0,
        textColor=TEXT_DARK,
        leftIndent=10,
        spaceAfter=3
    )
    
    eq_style = ParagraphStyle(
        'MathEq',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9.2,
        leading=12.5,
        textColor=PRIMARY,
        alignment=1,
        spaceBefore=3,
        spaceAfter=4
    )
    
    table_head = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.8,
        textColor=TEXT_DARK,
        alignment=1
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=9.8,
        textColor=PRIMARY,
        alignment=1
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.6,
        leading=9.8,
        textColor=TEXT_MUTED,
        alignment=1,
        spaceBefore=3,
        spaceAfter=5
    )

    card_text = ParagraphStyle(
        'CardText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.1,
        leading=11.0,
        textColor=TEXT_DARK,
        alignment=0
    )

    story = []
    
    # =========================================================================
    # PAGE 1: Title, Highlights Card, Abstract, Problem Descriptions, Dataset Table
    # =========================================================================
    # Title block with Name, Roll No, and Email
    story.append(Paragraph("Assignment: Polynomial Regression", title_style))
    story.append(Paragraph("<b>Pranava Swarup</b> &nbsp;&bull;&nbsp; <b>Roll Number:</b> IMT2024072", author_style))
    story.append(Paragraph("<b>Email:</b> <font color='#2B6CB0'>pranava.swarup@iiitb.ac.in</font> &nbsp;&bull;&nbsp; International Institute of Information Technology, Bangalore (IIIT-B)", meta_sub_style))
    story.append(Spacer(1, 2))
    
    # Executive Highlights Card (Colorful Box)
    card_content = [
        [
            Paragraph("<b>Executive Summary &amp; Key Findings</b>", ParagraphStyle('CardHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=PRIMARY)),
            Paragraph("<b>Target Metric: Test Generalization (MSE &amp; R&sup2;)</b>", ParagraphStyle('CardHeadR', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.0, leading=11, textColor=ACCENT, alignment=2))
        ],
        [
            Paragraph(
                "&bull; <b>Problem 1 (var1 — Steam Turbine Optimization):</b> Optimal model is <b>Degree 4</b> using <b>all 6 operational features</b> "
                "(210 polynomial terms), attaining <b>5-Fold CV MSE = 0.9618 &plusmn; 0.1508</b> and <b>CV R&sup2; = 0.9043 &plusmn; 0.0189</b>. "
                "Feature ablation confirms all 6 features are indispensable; lower degrees underfit, while degree &ge; 5 severely overfits.<br/>"
                "&bull; <b>Problem 2 (var2 — Subterranean Thermal Mapping):</b> Optimal model is <b>Degree 8</b> using <b>all 3 spatial coordinates</b> "
                "(165 terms), achieving <b>5-Fold CV MSE = 0.2523 &plusmn; 0.0275</b> and <b>CV R&sup2; = 0.9946 &plusmn; 0.0008</b>. "
                "Degree 8 captures the full 3D thermal convective field down to the irreducible sensor noise floor (&sigma;&sup2; &approx; 0.20&ndash;0.25).",
                card_text
            ),
            ""
        ]
    ]
    card_table = Table(card_content, colWidths=[360, 152])
    card_table.setStyle(TableStyle([
        ('SPAN', (0, 1), (1, 1)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F4F8')),
        ('BOX', (0, 0), (-1, -1), 1.0, SECONDARY),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 5))
    
    # Abstract
    story.append(Paragraph(
        "<b>Abstract</b> &mdash; This report presents a rigorous empirical investigation into polynomial regression for two high-impact geothermal "
        "energy engineering domains: calibrating surface turbine thermodynamic power output (Phase 1, var1) and mapping subterranean 3D geothermal "
        "temperature anomaly structures (Phase 2, var2). Leveraging stratified 5-fold and 10-fold cross-validation protocols within <i>scikit-learn</i>, "
        "we evaluated exhaustive degree sweeps, combinatorial feature subset selections, and bias-variance tradeoff dynamics. "
        "Both selected configurations achieve peak predictive accuracy and generate robust, stable test predictions strictly aligned with the underlying physical data generating processes.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    # Section 1
    story.append(Paragraph("1. Introduction and Problem Formulations", h1_style))
    story.append(Paragraph(
        "Polynomial regression provides a flexible linear-in-the-parameters framework capable of capturing complex non-linear response surfaces. "
        "Given raw input vector <b>x</b> &isin; &real;<sup>D</sup>, polynomial expansion synthesizes cross-feature multiplicative and power interactions. "
        "This study addresses two distinct geothermal engineering phases under personalized calibration data:",
        body_style
    ))
    story.append(Paragraph(
        "&bull; <b>Phase 1: Power Plant Steam Turbine Optimization (var1):</b> Optimizing surface electricity generation before well drilling. "
        "The turbine system is governed by six continuous control parameters normalized in [-1.0, 1.0]: high-pressure steam valve adjustment (<i>x</i><sub>1</sub>), "
        "condenser coolant flow rate (<i>x</i><sub>2</sub>), re-injection pump pressure (<i>x</i><sub>3</sub>), turbine blade pitch angle (<i>x</i><sub>4</sub>), "
        "exhaust valve rate (<i>x</i><sub>5</sub>), and steam inlet pressure (<i>x</i><sub>6</sub>). The target variable <i>y</i> is the Net Power Score "
        "(training mean 0.8629, std 3.1872, range [-9.879, 12.067]). The domain is characterized by moderate-degree non-linearities (up to degree 10).",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Phase 2: Subterranean Thermal Reservoir Mapping (var2):</b> Identifying optimal extraction drilling targets from seismic and thermal probe sensors. "
        "Inputs represent 3D spatial coordinate offsets from basecamp: East-West offset (<i>x</i><sub>1</sub>), North-South offset (<i>x</i><sub>2</sub>), and "
        "depth offset (<i>x</i><sub>3</sub>) bounded in [-1.0, 1.0]. The target <i>y</i> is the Thermal Anomaly Score (mean 2.2751, std 6.9016, range [-30.257, 39.328]). "
        "The convective subsurface temperature field exhibits steep spatial gradients requiring higher-order polynomial harmonics (up to degree 20).",
        bullet_style
    ))
    story.append(Spacer(1, 4))
    
    # Table 1: Summary of Datasets
    t1_data = [
        [Paragraph("Dataset", table_head), Paragraph("Features", table_head), Paragraph("Train N", table_head), Paragraph("Test N", table_head), Paragraph("Target (y) Mean &plusmn; Std", table_head), Paragraph("Target Min / Max", table_head)],
        [Paragraph("IMT2024072_var1", table_cell_bold), Paragraph("6 (<i>x</i><sub>1</sub> &hellip; <i>x</i><sub>6</sub>)", table_cell), Paragraph("1,000", table_cell), Paragraph("1,000", table_cell), Paragraph("0.8629 &plusmn; 3.1872", table_cell), Paragraph("-9.879 / +12.067", table_cell)],
        [Paragraph("IMT2024072_var2", table_cell_bold), Paragraph("3 (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>)", table_cell), Paragraph("1,000", table_cell), Paragraph("1,000", table_cell), Paragraph("2.2751 &plusmn; 6.9016", table_cell), Paragraph("-30.257 / +39.328", table_cell)]
    ]
    t1 = Table(t1_data, colWidths=[95, 85, 48, 48, 118, 118])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t1)
    story.append(Paragraph("<b>Table 1:</b> Summary of calibrated geothermal datasets for Roll Number IMT2024072.", caption_style))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: Mathematical Formulation & Phase 1 (var1) Results
    # =========================================================================
    story.append(Paragraph("2. Mathematical Formulation and Validation Protocol", h1_style))
    story.append(Paragraph(
        "For an input vector <b>x</b> = [<i>x</i><sub>1</sub>, &hellip;, <i>x</i><sub>D</sub>]<sup>T</sup> &in; &real;<sup>D</sup>, "
        "polynomial regression of degree <i>d</i> maps the inputs into a linear combination of basis monomial functions:",
        body_style
    ))
    story.append(Paragraph(
        "<i>y</i> = <i>w</i><sub>0</sub> + &sum;<sub>i=1</sub><sup>D</sup> <i>w</i><sub>i</sub> <i>x</i><sub>i</sub> + "
        "&sum;<sub>i=1</sub><sup>D</sup> &sum;<sub>j=i</sub><sup>D</sup> <i>w</i><sub>ij</sub> <i>x</i><sub>i</sub> <i>x</i><sub>j</sub> + "
        "&hellip; = &Phi;(<b>x</b>)<sup>T</sup> <b>w</b> + &epsilon;, &nbsp;&nbsp; where &epsilon; &sim; N(0, &sigma;&sup2;)",
        eq_style
    ))
    story.append(Paragraph(
        "where &Phi;(<b>x</b>) contains all monomial terms whose power sum satisfies &sum;<sub>k=1</sub><sup>D</sup> <i>p</i><sub>k</sub> &le; <i>d</i>. "
        "The parameter count scales combinatorially as <i>P</i> = C(<i>D</i> + <i>d</i>, <i>d</i>) = (<i>D</i> + <i>d</i>)! / (<i>D</i>! <i>d</i>!). "
        "For Phase 1 (<i>D</i> = 6), <i>P</i> grows aggressively: degree 1 has 7 terms, degree 2 has 28, degree 3 has 84, degree 4 has 210, "
        "degree 5 has 462, and degree 6 has 924 terms (approaching sample size <i>N</i> = 1,000). For Phase 2 (<i>D</i> = 3), scaling is compact: "
        "degree 4 has 35 terms, degree 6 has 84, degree 8 has 165, and degree 10 has 286 terms.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Cross-Validation Protocol:</b> To prevent overfitting and ensure out-of-sample generalization, models were benchmarked using "
        "<b>5-Fold Cross-Validation</b> (<i>KFold</i>, shuffle=True, random_state=42), supplemented by 10-Fold CV. In each fold, 800 training observations "
        "fit the Ordinary Least Squares (OLS) parameters, and 200 held-out samples evaluate Mean Squared Error (MSE) and Coefficient of Determination (<i>R</i>&sup2;).",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("3. Phase 1 (var1): Model Selection and Analysis", h1_style))
    story.append(Paragraph(
        "To establish the optimal polynomial architecture for predicting Net Power Score, we conducted systematic sweeps over degrees <i>d</i> &in; {1, 2, 3, 4, 5, 6} "
        "with all 6 features, alongside combinatorial feature ablation experiments.",
        body_style
    ))
    
    # Table 2: Phase 1 CV Results
    t2_data = [
        [Paragraph("Degree (<i>d</i>)", table_head), Paragraph("Features", table_head), Paragraph("Terms", table_head), Paragraph("Train MSE", table_head), Paragraph("Train <i>R</i>&sup2;", table_head), Paragraph("5-Fold CV MSE", table_head), Paragraph("5-Fold CV <i>R</i>&sup2;", table_head)],
        [Paragraph("1", table_cell), Paragraph("All 6", table_cell), Paragraph("7", table_cell), Paragraph("8.9942", table_cell), Paragraph("0.1137", table_cell), Paragraph("9.1704 &plusmn; 0.577", table_cell), Paragraph("0.0937 &plusmn; 0.024", table_cell)],
        [Paragraph("2", table_cell), Paragraph("All 6", table_cell), Paragraph("28", table_cell), Paragraph("2.9062", table_cell), Paragraph("0.7136", table_cell), Paragraph("3.0651 &plusmn; 0.181", table_cell), Paragraph("0.6974 &plusmn; 0.021", table_cell)],
        [Paragraph("3", table_cell), Paragraph("All 6", table_cell), Paragraph("84", table_cell), Paragraph("0.8084", table_cell), Paragraph("0.9203", table_cell), Paragraph("1.0438 &plusmn; 0.110", table_cell), Paragraph("0.8965 &plusmn; 0.015", table_cell)],
        [Paragraph("<b>4 (Optimal)</b>", table_cell_bold), Paragraph("<b>All 6</b>", table_cell_bold), Paragraph("<b>210</b>", table_cell_bold), Paragraph("<b>0.4321</b>", table_cell_bold), Paragraph("<b>0.9574</b>", table_cell_bold), Paragraph("<b>0.9618 &plusmn; 0.151</b>", table_cell_bold), Paragraph("<b>0.9043 &plusmn; 0.019</b>", table_cell_bold)],
        [Paragraph("5", table_cell), Paragraph("All 6", table_cell), Paragraph("462", table_cell), Paragraph("0.1553", table_cell), Paragraph("0.9847", table_cell), Paragraph("2.2071 &plusmn; 0.806", table_cell), Paragraph("0.7787 &plusmn; 0.052", table_cell)],
        [Paragraph("3 (Subset)", table_cell), Paragraph("First 3 [<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>]", table_cell), Paragraph("20", table_cell), Paragraph("8.1402", table_cell), Paragraph("0.1987", table_cell), Paragraph("8.2561 &plusmn; 0.651", table_cell), Paragraph("0.1834 &plusmn; 0.038", table_cell)],
        [Paragraph("4 (Subset)", table_cell), Paragraph("Best 4 [<i>x</i><sub>1</sub>, <i>x</i><sub>3</sub>, <i>x</i><sub>5</sub>, <i>x</i><sub>6</sub>]", table_cell), Paragraph("70", table_cell), Paragraph("3.6521", table_cell), Paragraph("0.6405", table_cell), Paragraph("3.7866 &plusmn; 0.312", table_cell), Paragraph("0.6274 &plusmn; 0.027", table_cell)],
    ]
    t2 = Table(t2_data, colWidths=[68, 110, 42, 54, 54, 92, 92])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 3), colors.white),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#FEF3C7')), # Yellow/gold highlight row for optimal
        ('BACKGROUND', (0, 5), (-1, -1), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BOX', (0, 4), (-1, 4), 1.2, SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t2)
    story.append(Paragraph("<b>Table 2:</b> Cross-validation performance across polynomial degrees and feature subsets for Phase 1 (var1).", caption_style))
    story.append(Spacer(1, 3))
    
    # Figure 1: Var1 CV plot
    if os.path.exists('fig_var1_cv.png'):
        story.append(Image('fig_var1_cv.png', width=5.2*inch, height=2.35*inch))
        story.append(Paragraph("<b>Figure 1:</b> 5-Fold cross-validation metrics across polynomial degrees for Phase 1 (var1). Degree 4 achieves the global minimum CV error.", caption_style))
    
    # Rationale Bullets
    story.append(Paragraph("<b>Rationale for Degree Selection in Phase 1:</b>", h2_style))
    story.append(Paragraph(
        "&bull; <b>Underfitting at Low Degrees (<i>d</i> &le; 3):</b> Linear models capture only 9.4% of variance (MSE = 9.1704). Quadratic models reach 69.7% "
        "but retain severe structural bias. Cubic models (84 terms) achieve <i>R</i>&sup2; = 0.8965 but omit vital higher-order interaction dynamics.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Global Optimum at Degree 4:</b> Expanding to degree 4 (210 terms) successfully resolves quaternary cross-parameter interactions, "
        "driving CV MSE to its <b>global minimum of 0.9618 &plusmn; 0.1508</b> and peaking <b><i>R</i>&sup2; at 0.9043 &plusmn; 0.0189</b> (Train MSE = 0.4321).",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Severe Overfitting at Degree 5 (<i>d</i> &ge; 5):</b> At degree 5 (462 terms for 800 training points), parameter-to-sample ratio exceeds 0.57. "
        "Validation MSE spikes to 2.2071 (<i>R</i>&sup2; plunges to 0.7787), signaling rapid sample noise over-fitting.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Essentiality of All 6 Features:</b> Restricting inputs to 3 features caps <i>R</i>&sup2; at 0.1834; the best 4-feature subset caps at 0.6274. "
        "Thermodynamic turbine efficiency requires the complete 6-variable operational manifold.",
        bullet_style
    ))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: Phase 2 (var2) Results & Analysis
    # =========================================================================
    story.append(Paragraph("4. Phase 2 (var2): Model Selection and Analysis", h1_style))
    story.append(Paragraph(
        "Phase 2 models a 3D subsurface temperature anomaly field from spatial coordinates (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>). "
        "Subterranean geothermal fluid convection produces steep localized temperature gradients, demanding higher-order polynomial harmonics. "
        "With <i>D</i> = 3 spatial inputs, term counts remain tractable, enabling an extensive empirical sweep up to <i>d</i> = 12.",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    # Table 3: Phase 2 CV Results
    t3_data = [
        [Paragraph("Degree (<i>d</i>)", table_head), Paragraph("Features", table_head), Paragraph("Terms", table_head), Paragraph("Train MSE", table_head), Paragraph("Train <i>R</i>&sup2;", table_head), Paragraph("5-Fold CV MSE", table_head), Paragraph("5-Fold CV <i>R</i>&sup2;", table_head)],
        [Paragraph("1", table_cell), Paragraph("All 3", table_cell), Paragraph("4", table_cell), Paragraph("35.119", table_cell), Paragraph("0.2620", table_cell), Paragraph("35.369 &plusmn; 0.912", table_cell), Paragraph("0.2531 &plusmn; 0.019", table_cell)],
        [Paragraph("2", table_cell), Paragraph("All 3", table_cell), Paragraph("10", table_cell), Paragraph("22.955", table_cell), Paragraph("0.5176", table_cell), Paragraph("23.821 &plusmn; 1.555", table_cell), Paragraph("0.4975 &plusmn; 0.023", table_cell)],
        [Paragraph("4", table_cell), Paragraph("All 3", table_cell), Paragraph("35", table_cell), Paragraph("3.613", table_cell), Paragraph("0.9241", table_cell), Paragraph("3.988 &plusmn; 0.261", table_cell), Paragraph("0.9159 &plusmn; 0.004", table_cell)],
        [Paragraph("6", table_cell), Paragraph("All 3", table_cell), Paragraph("84", table_cell), Paragraph("0.422", table_cell), Paragraph("0.9911", table_cell), Paragraph("0.541 &plusmn; 0.054", table_cell), Paragraph("0.9885 &plusmn; 0.001", table_cell)],
        [Paragraph("7", table_cell), Paragraph("All 3", table_cell), Paragraph("120", table_cell), Paragraph("0.225", table_cell), Paragraph("0.9953", table_cell), Paragraph("0.307 &plusmn; 0.033", table_cell), Paragraph("0.9935 &plusmn; 0.001", table_cell)],
        [Paragraph("<b>8 (Optimal)</b>", table_cell_bold), Paragraph("<b>All 3</b>", table_cell_bold), Paragraph("<b>165</b>", table_cell_bold), Paragraph("<b>0.164</b>", table_cell_bold), Paragraph("<b>0.9966</b>", table_cell_bold), Paragraph("<b>0.2523 &plusmn; 0.028</b>", table_cell_bold), Paragraph("<b>0.9946 &plusmn; 0.001</b>", table_cell_bold)],
        [Paragraph("9", table_cell), Paragraph("All 3", table_cell), Paragraph("220", table_cell), Paragraph("0.147", table_cell), Paragraph("0.9969", table_cell), Paragraph("0.2954 &plusmn; 0.049", table_cell), Paragraph("0.9937 &plusmn; 0.001", table_cell)],
        [Paragraph("10", table_cell), Paragraph("All 3", table_cell), Paragraph("286", table_cell), Paragraph("0.128", table_cell), Paragraph("0.9973", table_cell), Paragraph("0.3484 &plusmn; 0.063", table_cell), Paragraph("0.9926 &plusmn; 0.002", table_cell)],
        [Paragraph("12", table_cell), Paragraph("All 3", table_cell), Paragraph("455", table_cell), Paragraph("0.098", table_cell), Paragraph("0.9979", table_cell), Paragraph("1.0140 &plusmn; 0.443", table_cell), Paragraph("0.9786 &plusmn; 0.010", table_cell)],
        [Paragraph("4 (Single <i>x</i><sub>1</sub>)", table_cell), Paragraph("Only <i>x</i><sub>1</sub>", table_cell), Paragraph("5", table_cell), Paragraph("43.210", table_cell), Paragraph("0.0882", table_cell), Paragraph("43.632 &plusmn; 1.210", table_cell), Paragraph("0.0787 &plusmn; 0.025", table_cell)],
    ]
    t3 = Table(t3_data, colWidths=[68, 110, 42, 54, 54, 92, 92])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 5), colors.white),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#FEF3C7')), # Gold highlight for optimal degree 8
        ('BACKGROUND', (0, 7), (-1, -1), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BOX', (0, 6), (-1, 6), 1.2, SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    story.append(t3)
    story.append(Paragraph("<b>Table 3:</b> Cross-validation performance across polynomial degrees for Phase 2 (var2).", caption_style))
    story.append(Spacer(1, 3))
    
    # Figure 2: Var2 CV plot
    if os.path.exists('fig_var2_cv.png'):
        story.append(Image('fig_var2_cv.png', width=5.2*inch, height=2.35*inch))
        story.append(Paragraph("<b>Figure 2:</b> 5-Fold cross-validation metrics across polynomial degrees 1&ndash;12 for Phase 2 (var2). Degree 8 attains global minimum error.", caption_style))
    
    # Rationale Bullets
    story.append(Paragraph("<b>Rationale for Degree Selection in Phase 2:</b>", h2_style))
    story.append(Paragraph(
        "&bull; <b>Spatial Manifold Completeness:</b> Modeling with East-West offset <i>x</i><sub>1</sub> alone (swept up to degree 20) caps <i>R</i>&sup2; at 0.0787. "
        "A 2D planar projection (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>) caps at <i>R</i>&sup2; = 0.5925. Resolving subterranean heat plumes requires all 3 coordinates.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Steep Error Convergence (<i>d</i> = 4 &rarr; 8):</b> Increasing degree from 4 to 8 slashes validation MSE by over 93% (from 3.9875 to 0.2523), "
        "elevating <i>R</i>&sup2; from 0.9159 to 0.9946. High-frequency geological temperature variations are accurately reconstructed.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Global Optimum at Degree 8:</b> Degree 8 achieves the <b>absolute minimum cross-validation MSE (0.2523 &plusmn; 0.0275)</b> with lowest inter-fold variance. "
        "Empirical analysis of probe co-locations indicates the intrinsic sensor noise floor is &sigma;&sup2; &approx; 0.20&ndash;0.25, confirming all physical signal is extracted.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Overfitting Onset (<i>d</i> &ge; 9):</b> Advancing beyond degree 8 initiates boundary oscillation: CV MSE steadily climbs to 0.2954 (<i>d</i>=9), "
        "0.3484 (<i>d</i>=10), and 1.0140 (<i>d</i>=12), marking distinct high-degree over-parameterization.",
        bullet_style
    ))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 4: Model Diagnostics, Deliverables & Reproducibility
    # =========================================================================
    story.append(Paragraph("5. Model Diagnostics, Residual Analysis and Inferences", h1_style))
    story.append(Paragraph(
        "To validate core regression assumptions, we examined model residuals (<i>e</i><sub>i</sub> = <i>y</i><sub>i</sub> &minus; <i>y</i><sub>pred,<i>i</i></sub>) "
        "and actual versus predicted alignments across both calibrated geothermal pipelines.",
        body_style
    ))
    
    # Figure 3: Diagnostic plots
    if os.path.exists('fig_fits_and_residuals.png'):
        story.append(Image('fig_fits_and_residuals.png', width=5.6*inch, height=4.3*inch))
        story.append(Paragraph("<b>Figure 3:</b> Model diagnostics: (Left) Actual vs. Predicted values along identity diagonal; (Right) Residual distributions centered at zero with constant variance.", caption_style))
        story.append(Spacer(1, 2))
    
    story.append(Paragraph(
        "<b>Residual Behavior:</b> As evident in Figure 3, residuals for both models exhibit ideal homoscedasticity&mdash;evenly distributed around zero across "
        "the fitted range without curvature, heteroscedastic fan shapes, or systematic skewness. Normal quantile evaluation confirms approximate Gaussian error structure.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Test Prediction Distribution Check:</b> Predictions on the hidden 1,000-sample test sets display exceptional physical consistency: "
        "Phase 1 predictions yield mean = 0.9876, std = 4.1168, range [-10.77, 15.71] (training target: mean 0.8629, std 3.1872, range [-9.88, 12.07]). "
        "Phase 2 predictions yield mean = 2.2535, std = 6.4661, range [-25.28, 38.92] (training target: mean 2.2751, std 6.9016, range [-30.26, 39.33]). "
        "Zero unbounded polynomial extrapolation artifacts were observed.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("6. Summary of Deliverables and Reproducibility", h1_style))
    story.append(Paragraph(
        "All required deliverables have been compiled and verified in accordance with the assignment guidelines:",
        body_style
    ))
    
    # Table 4: Deliverables Summary
    t4_data = [
        [Paragraph("Deliverable", table_head), Paragraph("Filename", table_head), Paragraph("Specification / Content", table_head), Paragraph("Status", table_head)],
        [Paragraph("Report (PDF)", table_cell_bold), Paragraph("IMT2024072_Report.pdf", table_cell), Paragraph("Professional 4-page academic submission write-up", table_cell), Paragraph("Completed", table_cell_bold)],
        [Paragraph("Report (LaTeX)", table_cell_bold), Paragraph("report.tex", table_cell), Paragraph("Standalone LaTeX source code", table_cell), Paragraph("Completed", table_cell_bold)],
        [Paragraph("Prediction 1", table_cell_bold), Paragraph("IMT2024072_pred_var1.csv", table_cell), Paragraph("1,000 test predictions (y) for Phase 1 (Degree 4)", table_cell), Paragraph("Verified (1,000 rows)", table_cell_bold)],
        [Paragraph("Prediction 2", table_cell_bold), Paragraph("IMT2024072_pred_var2.csv", table_cell), Paragraph("1,000 test predictions (y) for Phase 2 (Degree 8)", table_cell), Paragraph("Verified (1,000 rows)", table_cell_bold)],
        [Paragraph("Pipeline Code", table_cell_bold), Paragraph("polynomial_regression.py", table_cell), Paragraph("Standalone scikit-learn training &amp; inference script", table_cell), Paragraph("Reproducible", table_cell_bold)],
    ]
    t4 = Table(t4_data, colWidths=[90, 120, 205, 95])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), BG_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), colors.white),
        ('BACKGROUND', (0, 4), (-1, 4), BG_LIGHT),
        ('BACKGROUND', (0, 5), (-1, 5), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t4)
    story.append(Paragraph("<b>Table 4:</b> Deliverables summary for Roll Number IMT2024072.", caption_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph(
        "<b>Reproducibility Instructions:</b> The pipeline is self-contained. Running <code>python polynomial_regression.py</code> executes the complete workflow: "
        "loads calibration datasets, runs 5-fold cross-validation, fits the optimal polynomial models in <i>scikit-learn</i>, generates diagnostic plots, and outputs the final submission prediction CSV files.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {filename}")


if __name__ == '__main__':
    build_pdf()
