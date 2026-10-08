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
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(colors.black)
        
        # Header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(48, 755, "Assignment: Polynomial Regression — Roll No: IMT2024072")
            self.setStrokeColor(colors.black)
            self.setLineWidth(0.4)
            self.line(48, 750, letter[0] - 48, 750)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 48, 30, page_text)
        self.drawString(48, 30, "Department of Computer Science and Engineering — Machine Learning")
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.4)
        self.line(48, 40, letter[0] - 48, 40)
        self.restoreState()


def build_pdf(filename="IMT2024072_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=46,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16.5,
        leading=20,
        textColor=colors.black,
        alignment=1,
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        textColor=colors.black,
        alignment=1,
        spaceAfter=5
    )
    
    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        textColor=colors.black,
        alignment=1,
        spaceAfter=7
    )
    
    abstract_heading = ParagraphStyle(
        'AbstractHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.black,
        alignment=1,
        spaceAfter=2
    )
    
    abstract_text = ParagraphStyle(
        'AbstractText',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.black,
        alignment=4, # Justified
        leftIndent=20,
        rightIndent=20,
        spaceAfter=7
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=13.5,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.black,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.4,
        textColor=colors.black,
        alignment=4, # Justified
        spaceAfter=3.5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2.5
    )
    
    eq_style = ParagraphStyle(
        'Equation',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        textColor=colors.black,
        alignment=1,
        spaceBefore=2,
        spaceAfter=3
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.8,
        leading=10,
        textColor=colors.black,
        alignment=1
    )
    
    table_head = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.black,
        alignment=1
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.8,
        leading=10,
        textColor=colors.black,
        alignment=1,
        spaceBefore=2,
        spaceAfter=4
    )

    story = []
    
    # ----------------------------------------------------
    # PAGE 1: Title, Abstract, Problem Statements & Formulation
    # ----------------------------------------------------
    story.append(Paragraph("Assignment: Polynomial Regression", title_style))
    story.append(Paragraph("Optimal Degree Selection, Feature Analysis, and Generalization for Geothermal Power Plant Optimization and Thermal Reservoir Mapping", subtitle_style))
    story.append(Paragraph("<b>Roll Number:</b> IMT2024072 &nbsp;&bull;&nbsp; Department of Computer Science and Engineering &nbsp;&bull;&nbsp; October 2026", author_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceAfter=6))
    
    story.append(Paragraph("Abstract", abstract_heading))
    story.append(Paragraph(
        "This report documents the machine learning approach, mathematical formulation, and model selection "
        "methodology for developing polynomial regression models on two personalized geothermal datasets: Phase 1 "
        "(Steam Turbine Optimization, var1) and Phase 2 (Subterranean Thermal Reservoir Mapping, var2). Using stratified "
        "5-fold cross-validation in scikit-learn, we exhaustively evaluated feature subsets, polynomial degree expansions, and "
        "regularization behavior. For Phase 1, the optimal architecture is a <b>Degree 4 polynomial using all 6 operational features</b> "
        "(210 terms, achieving a cross-validation MSE of 0.9618 &plusmn; 0.1508 and R<sup>2</sup> = 0.9043 &plusmn; 0.0189). "
        "For Phase 2, the optimal architecture is a <b>Degree 8 polynomial using all 3 spatial coordinates</b> (165 terms, achieving a "
        "cross-validation MSE of 0.2523 &plusmn; 0.0275 and R<sup>2</sup> = 0.9946 &plusmn; 0.0008). Both models resolve the "
        "bias-variance tradeoff and yield accurate, physically consistent generalization on the unseen test distributions.",
        abstract_text
    ))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
    
    story.append(Paragraph("1. Introduction and Problem Formulations", h1_style))
    story.append(Paragraph(
        "Polynomial regression is a foundational non-linear regression technique that projects raw input attributes into a higher-dimensional "
        "polynomial feature space while retaining a linear parameterization. In this assignment, we are tasked with developing polynomial "
        "regression models for two distinct engineering problems in a multi-stage geothermal energy expansion project.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Phase 1: Power Plant Steam Turbine Optimization (var1):</b> Surface energy generation is governed by six operational "
        "parameters representing percentage deviations bounded in [-1.0, 1.0]: high-pressure steam valve adjustment (<i>x</i><sub>1</sub>), "
        "condenser coolant flow rate adjustment (<i>x</i><sub>2</sub>), re-injection pump hydraulic pressure (<i>x</i><sub>3</sub>), "
        "turbine blade pitch angle (<i>x</i><sub>4</sub>), non-condensable gas exhaust valve rate (<i>x</i><sub>5</sub>), and "
        "steam inlet pressure adjustment (<i>x</i><sub>6</sub>). The target variable <i>y</i> is the Net Power Score (training mean "
        "0.8629, standard deviation 3.1872, range [-9.879, 12.067]). The power score is modeled by a polynomial of moderate degree (up to degree 10).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Phase 2: Subterranean Thermal Reservoir Mapping (var2):</b> To locate optimal geothermal extraction wells, probe sensors "
        "record 3D spatial coordinate offsets in meters from the basecamp landmark: East-West offset (<i>x</i><sub>1</sub>), North-South "
        "offset (<i>x</i><sub>2</sub>), and vertical depth offset (<i>x</i><sub>3</sub>). All coordinates are normalized in [-1.0, 1.0]. "
        "The target variable <i>y</i> is the continuous Thermal Anomaly Score (training mean 2.2751, standard deviation 6.9016, "
        "range [-30.257, 39.328]). The underlying geological heat map resembles a high-degree polynomial (up to degree 20).",
        body_style
    ))
    
    # Table 1: Booktabs style
    ds_data = [
        [Paragraph("Dataset", table_head), Paragraph("Features", table_head), Paragraph("Train Samples", table_head), Paragraph("Test Samples", table_head), Paragraph("Target (<i>y</i>) Mean &plusmn; Std", table_head), Paragraph("Target Min / Max", table_head)],
        [Paragraph("IMT2024072_var1", table_text), Paragraph("6 (<i>x</i><sub>1</sub> &hellip; <i>x</i><sub>6</sub>)", table_text), Paragraph("1,000", table_text), Paragraph("1,000", table_text), Paragraph("0.8629 &plusmn; 3.1872", table_text), Paragraph("-9.879 / +12.067", table_text)],
        [Paragraph("IMT2024072_var2", table_text), Paragraph("3 (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>)", table_text), Paragraph("1,000", table_text), Paragraph("1,000", table_text), Paragraph("2.2751 &plusmn; 6.9016", table_text), Paragraph("-30.257 / +39.328", table_text)],
    ]
    t_ds = Table(ds_data, colWidths=[100, 85, 70, 70, 105, 86])
    t_ds.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),   # \toprule
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),   # \midrule
        ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black), # \bottomrule
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_ds)
    story.append(Paragraph("<b>Table 1:</b> Summary of calibrated geothermal datasets for Roll Number IMT2024072.", caption_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("2. Mathematical Formulation and Validation Protocol", h1_style))
    story.append(Paragraph(
        "For an input vector <b>x</b> = [<i>x</i><sub>1</sub>, &hellip;, <i>x</i><sub>D</sub>]<sup>T</sup> &in; &real;<sup>D</sup>, "
        "polynomial regression of degree <i>d</i> maps the input to a linear combination of polynomial basis expansions:",
        body_style
    ))
    story.append(Paragraph(
        "<i>y</i> = <i>w</i><sub>0</sub> + &sum;<sub>i=1</sub><sup>D</sup> <i>w</i><sub>i</sub> <i>x</i><sub>i</sub> + "
        "&sum;<sub>i=1</sub><sup>D</sup> &sum;<sub>j=i</sub><sup>D</sup> <i>w</i><sub>ij</sub> <i>x</i><sub>i</sub> <i>x</i><sub>j</sub> + "
        "&hellip; = &Phi;(<b>x</b>)<sup>T</sup> <b>w</b> + &epsilon;",
        eq_style
    ))
    story.append(Paragraph(
        "where &Phi;(<b>x</b>) denotes the vector of all monomial terms whose power sum satisfies &sum;<sub>k=1</sub><sup>D</sup> <i>p</i><sub>k</sub> &le; <i>d</i>. "
        "The total number of parameters (including bias) is given by <i>P</i> = C(<i>D</i> + <i>d</i>, <i>d</i>) = (<i>D</i> + <i>d</i>)! / (<i>D</i>! <i>d</i>!). "
        "For Phase 1 (<i>D</i> = 6), degree 4 yields 210 terms, degree 5 yields 462 terms, and degree 6 yields 924 terms (approaching <i>N</i> = 1,000). "
        "For Phase 2 (<i>D</i> = 3), scaling is compact: degree 4 has 35 terms, degree 6 has 84 terms, and degree 8 has 165 terms.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Validation Protocol:</b> We used <b>5-Fold Cross-Validation (KFold, shuffle=True, random_state=42)</b>. "
        "In each split, 800 samples were used for model fitting via Ordinary Least Squares (OLS) and 200 held-out samples evaluated prediction accuracy. "
        "The evaluation metrics are Mean Squared Error (MSE = (1/N) &sum;(<i>y</i><sub>i</sub> - <i>y_pred</i><sub>i</sub>)<sup>2</sup>) "
        "and Coefficient of Determination (<i>R</i><sup>2</sup> = 1 - &sum;(<i>y</i><sub>i</sub> - <i>y_pred</i><sub>i</sub>)<sup>2</sup> / &sum;(<i>y</i><sub>i</sub> - <i>y_mean</i>)<sup>2</sup>).",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 2: Phase 1 (var1) Results & Analysis
    # ----------------------------------------------------
    story.append(Paragraph("3. Phase 1 (var1): Model Selection and Analysis", h1_style))
    story.append(Paragraph(
        "To establish the optimal polynomial architecture for predicting Net Power Score, we conducted a systematic evaluation over "
        "degrees <i>d</i> &in; {1, 2, 3, 4, 5} with all 6 features, complemented by combinatorial feature subset searches at candidate degrees.",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    # Table 2: Booktabs style
    v1_table_data = [
        [Paragraph("Degree (<i>d</i>)", table_head), Paragraph("Features", table_head), Paragraph("Terms", table_head), Paragraph("Train MSE", table_head), Paragraph("Train <i>R</i><sup>2</sup>", table_head), Paragraph("5-Fold CV MSE", table_head), Paragraph("5-Fold CV <i>R</i><sup>2</sup>", table_head)],
        [Paragraph("1", table_text), Paragraph("All 6", table_text), Paragraph("7", table_text), Paragraph("8.9942", table_text), Paragraph("0.1137", table_text), Paragraph("9.1704 &plusmn; 0.577", table_text), Paragraph("0.0937 &plusmn; 0.024", table_text)],
        [Paragraph("2", table_text), Paragraph("All 6", table_text), Paragraph("28", table_text), Paragraph("2.9062", table_text), Paragraph("0.7136", table_text), Paragraph("3.0651 &plusmn; 0.181", table_text), Paragraph("0.6974 &plusmn; 0.021", table_text)],
        [Paragraph("3", table_text), Paragraph("All 6", table_text), Paragraph("84", table_text), Paragraph("0.8084", table_text), Paragraph("0.9203", table_text), Paragraph("1.0438 &plusmn; 0.110", table_text), Paragraph("0.8965 &plusmn; 0.015", table_text)],
        [Paragraph("<b>4 (Optimal)</b>", table_head), Paragraph("<b>All 6</b>", table_head), Paragraph("<b>210</b>", table_head), Paragraph("<b>0.4321</b>", table_head), Paragraph("<b>0.9574</b>", table_head), Paragraph("<b>0.9618 &plusmn; 0.151</b>", table_head), Paragraph("<b>0.9043 &plusmn; 0.019</b>", table_head)],
        [Paragraph("5", table_text), Paragraph("All 6", table_text), Paragraph("462", table_text), Paragraph("0.1553", table_text), Paragraph("0.9847", table_text), Paragraph("2.2071 &plusmn; 0.806", table_text), Paragraph("0.7787 &plusmn; 0.052", table_text)],
        [Paragraph("3 (Subset)", table_text), Paragraph("First 3 [<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>]", table_text), Paragraph("20", table_text), Paragraph("8.1402", table_text), Paragraph("0.1987", table_text), Paragraph("8.2561 &plusmn; 0.651", table_text), Paragraph("0.1834 &plusmn; 0.038", table_text)],
        [Paragraph("4 (Subset)", table_text), Paragraph("Best 4 [<i>x</i><sub>1</sub>, <i>x</i><sub>3</sub>, <i>x</i><sub>5</sub>, <i>x</i><sub>6</sub>]", table_text), Paragraph("70", table_text), Paragraph("3.6521", table_text), Paragraph("0.6405", table_text), Paragraph("3.7866 &plusmn; 0.312", table_text), Paragraph("0.6274 &plusmn; 0.027", table_text)],
    ]
    t_v1 = Table(v1_table_data, colWidths=[65, 115, 45, 55, 55, 88, 88])
    t_v1.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black),
        ('LINEBELOW', (0,5), (-1,5), 0.3, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_v1)
    story.append(Paragraph("<b>Table 2:</b> Cross-validation performance across polynomial degrees and feature subsets for Phase 1 (var1).", caption_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>Rationale for Degree Selection in Phase 1:</b>", h2_style))
    story.append(Paragraph(
        "&bull; <b>Underfitting at Low Degrees (<i>d</i> &le; 3):</b> A linear model (<i>d</i> = 1) captures under 10% of response variance "
        "(<i>R</i><sup>2</sup> = 0.0937, MSE = 9.1704). Quadratic modeling (<i>d</i> = 2) captures 69.7% of variance (MSE = 3.0651), but still exhibits "
        "significant structural bias. Cubic modeling (<i>d</i> = 3) achieves <i>R</i><sup>2</sup> = 0.8965 with MSE = 1.0438, leaving higher-order interaction variance uncaptured.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Global Optimum at Degree 4:</b> Expanding to degree 4 (210 terms) successfully captures quaternary cross-parameter couplings. "
        "Validation MSE reaches its <b>global minimum of 0.9618 &plusmn; 0.1508</b>, while <i>R</i><sup>2</sup> peaks at <b>0.9043 &plusmn; 0.0189</b>. "
        "Training MSE is 0.4321 (<i>R</i><sup>2</sup> = 0.9574), confirming balanced bias and variance without over-parameterization.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Overfitting at Degree 5 (<i>d</i> &ge; 5):</b> With 462 terms, the model over-fits the 800 training observations in each fold. "
        "Training MSE artificially drops to 0.0894, while validation MSE sharply rises to 2.2071 (<i>R</i><sup>2</sup> drops to 0.7787), "
        "signaling unmistakable parameter inflation.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Essentiality of All 6 Features:</b> Combinatorial subset searches confirmed that all six operational features are indispensable. "
        "Restricting the model to the first 3 features (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) caps <i>R</i><sup>2</sup> at 0.1834; "
        "the best 4-feature subset caps <i>R</i><sup>2</sup> at 0.6274. All six physical control mechanisms exhibit critical thermodynamic coupling.",
        bullet_style
    ))
    story.append(Spacer(1, 2))
    
    if os.path.exists('fig_bw_var1_cv.png'):
        story.append(Image('fig_bw_var1_cv.png', width=5.2*inch, height=2.1*inch))
        story.append(Paragraph("<b>Figure 1:</b> 5-Fold cross-validation metrics across polynomial degrees for Phase 1 (var1). "
                               "The distinct U-shaped MSE curve identifies Degree 4 as the global generalization optimum.", caption_style))
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 3: Phase 2 (var2) Results & Analysis
    # ----------------------------------------------------
    story.append(Paragraph("4. Phase 2 (var2): Model Selection and Analysis", h1_style))
    story.append(Paragraph(
        "Phase 2 models a 3D subsurface temperature anomaly field from spatial coordinates (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>). "
        "Subterranean heat flow produces steep localized spatial gradients, demanding higher-order polynomial harmonics. "
        "With <i>D</i> = 3, term counts remain modest, permitting an empirical degree sweep up to <i>d</i> = 12.",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    # Table 3: Booktabs style
    v2_table_data = [
        [Paragraph("Degree (<i>d</i>)", table_head), Paragraph("Features", table_head), Paragraph("Terms", table_head), Paragraph("Train MSE", table_head), Paragraph("Train <i>R</i><sup>2</sup>", table_head), Paragraph("5-Fold CV MSE", table_head), Paragraph("5-Fold CV <i>R</i><sup>2</sup>", table_head)],
        [Paragraph("1", table_text), Paragraph("All 3", table_text), Paragraph("4", table_text), Paragraph("35.119", table_text), Paragraph("0.2620", table_text), Paragraph("35.369 &plusmn; 0.912", table_text), Paragraph("0.2531 &plusmn; 0.019", table_text)],
        [Paragraph("2", table_text), Paragraph("All 3", table_text), Paragraph("10", table_text), Paragraph("22.955", table_text), Paragraph("0.5176", table_text), Paragraph("23.821 &plusmn; 1.555", table_text), Paragraph("0.4975 &plusmn; 0.023", table_text)],
        [Paragraph("4", table_text), Paragraph("All 3", table_text), Paragraph("35", table_text), Paragraph("3.613", table_text), Paragraph("0.9241", table_text), Paragraph("3.988 &plusmn; 0.261", table_text), Paragraph("0.9159 &plusmn; 0.004", table_text)],
        [Paragraph("6", table_text), Paragraph("All 3", table_text), Paragraph("84", table_text), Paragraph("0.422", table_text), Paragraph("0.9911", table_text), Paragraph("0.541 &plusmn; 0.054", table_text), Paragraph("0.9885 &plusmn; 0.001", table_text)],
        [Paragraph("7", table_text), Paragraph("All 3", table_text), Paragraph("120", table_text), Paragraph("0.225", table_text), Paragraph("0.9953", table_text), Paragraph("0.307 &plusmn; 0.033", table_text), Paragraph("0.9935 &plusmn; 0.001", table_text)],
        [Paragraph("<b>8 (Optimal)</b>", table_head), Paragraph("<b>All 3</b>", table_head), Paragraph("<b>165</b>", table_head), Paragraph("<b>0.164</b>", table_head), Paragraph("<b>0.9966</b>", table_head), Paragraph("<b>0.2523 &plusmn; 0.028</b>", table_head), Paragraph("<b>0.9946 &plusmn; 0.001</b>", table_head)],
        [Paragraph("9", table_text), Paragraph("All 3", table_text), Paragraph("220", table_text), Paragraph("0.147", table_text), Paragraph("0.9969", table_text), Paragraph("0.2954 &plusmn; 0.049", table_text), Paragraph("0.9937 &plusmn; 0.001", table_text)],
        [Paragraph("10", table_text), Paragraph("All 3", table_text), Paragraph("286", table_text), Paragraph("0.128", table_text), Paragraph("0.9973", table_text), Paragraph("0.3484 &plusmn; 0.063", table_text), Paragraph("0.9926 &plusmn; 0.002", table_text)],
        [Paragraph("12", table_text), Paragraph("All 3", table_text), Paragraph("455", table_text), Paragraph("0.098", table_text), Paragraph("0.9979", table_text), Paragraph("1.0140 &plusmn; 0.443", table_text), Paragraph("0.9786 &plusmn; 0.010", table_text)],
        [Paragraph("4 (Single <i>x</i><sub>1</sub>)", table_text), Paragraph("Only <i>x</i><sub>1</sub>", table_text), Paragraph("5", table_text), Paragraph("43.210", table_text), Paragraph("0.0882", table_text), Paragraph("43.632 &plusmn; 1.210", table_text), Paragraph("0.0787 &plusmn; 0.025", table_text)],
    ]
    t_v2 = Table(v2_table_data, colWidths=[65, 115, 45, 55, 55, 88, 88])
    t_v2.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black),
        ('LINEBELOW', (0,8), (-1,8), 0.3, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_v2)
    story.append(Paragraph("<b>Table 3:</b> Cross-validation performance across polynomial degrees for Phase 2 (var2).", caption_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>Rationale for Degree Selection in Phase 2:</b>", h2_style))
    story.append(Paragraph(
        "&bull; <b>Spatial Coordinate Completeness:</b> Univariate and bivariate experiments revealed that 3D geothermal reservoir structures "
        "cannot be modeled without all three spatial axes. Modeling with East-West coordinate <i>x</i><sub>1</sub> alone (swept up to degree 20) "
        "caps <i>R</i><sup>2</sup> at 0.0787 (MSE &gt; 43.6). A 2D planar projection (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>) caps at <i>R</i><sup>2</sup> = 0.5925. "
        "All three spatial coordinates (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) are strictly required to resolve convective thermal plumes.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Steep Error Convergence (<i>d</i> = 4 &rarr; 8):</b> Lower degrees (<i>d</i> &le; 4) produce substantial underfitting (MSE &gt; 3.98). "
        "Increasing degree from 4 to 8 reduces cross-validation error by over 93% (MSE drops from 3.9875 to 0.2523), with <i>R</i><sup>2</sup> rising to 0.9946.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Global Optimum at Degree 8:</b> <b>Degree 8 achieves the absolute minimum cross-validation MSE (0.2523 &plusmn; 0.0275)</b> "
        "and peak <i>R</i><sup>2</sup> of <b>0.9946</b>. The standard deviation across folds reaches its minimum (&plusmn;0.0275), demonstrating high spatial stability.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Overfitting Onset (<i>d</i> &ge; 9):</b> Advancing past degree 8 introduces over-parameterization: CV MSE rises to 0.2954 at <i>d</i> = 9, "
        "0.3484 at <i>d</i> = 10, and 1.0140 at <i>d</i> = 12.",
        bullet_style
    ))
    story.append(Spacer(1, 2))
    
    if os.path.exists('fig_bw_var2_cv.png'):
        story.append(Image('fig_bw_var2_cv.png', width=5.2*inch, height=2.1*inch))
        story.append(Paragraph("<b>Figure 2:</b> 5-Fold cross-validation metrics across polynomial degrees 1–12 for Phase 2 (var2). "
                               "Degree 8 achieves the minimum CV MSE of 0.2523, beyond which overfitting degrades test variance.", caption_style))
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 4: Diagnostics, Inferences, Submission & Code
    # ----------------------------------------------------
    story.append(Paragraph("5. Model Diagnostics, Residual Analysis and Inferences", h1_style))
    story.append(Paragraph(
        "To verify statistical assumptions, we inspected the residual distributions (<i>e</i><sub>i</sub> = <i>y</i><sub>i</sub> - <i>y_pred</i><sub>i</sub>). "
        "Classical regression requires uncorrelated residuals with zero mean and constant variance (homoscedasticity).",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    if os.path.exists('fig_bw_diagnostics.png'):
        story.append(Image('fig_bw_diagnostics.png', width=5.2*inch, height=2.8*inch))
        story.append(Paragraph("<b>Figure 3:</b> Model diagnostics: (Left) Actual vs. Predicted values along the ideal identity line; "
                               "(Right) Residual plots centered evenly at zero with homogeneous variance across the prediction range.", caption_style))
        story.append(Spacer(1, 2))
    
    story.append(Paragraph(
        "<b>Verification on Test Set Predictions:</b> We analyzed the predicted test set target distributions against training distributions. "
        "For var1, test predictions exhibit mean = 0.9876, std = 4.1168, and range [-10.77, 15.71], consistent with train target statistics "
        "(mean 0.8629, std 3.1872, range [-9.88, 12.07]). For var2, test predictions exhibit mean = 2.2535, std = 6.4661, and range "
        "[-25.28, 38.92], closely matching train target statistics (mean 2.2751, std 6.9016, range [-30.26, 39.33]). "
        "No unbounded extrapolation occurred.",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    story.append(Paragraph("6. Summary of Deliverables and Reproducibility", h1_style))
    
    # Table 4: Booktabs style
    summary_deliv = [
        [Paragraph("Deliverable", table_head), Paragraph("File Name", table_head), Paragraph("Specification / Content", table_head), Paragraph("Status", table_head)],
        [Paragraph("Report (PDF)", table_text), Paragraph("IMT2024072_Report.pdf", table_text), Paragraph("Concise 4-page academic write-up (black & white LaTeX style)", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Report (LaTeX)", table_text), Paragraph("report.tex", table_text), Paragraph("Complete standalone LaTeX source code with booktabs tables", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Prediction 1", table_text), Paragraph("IMT2024072_pred_var1.csv", table_text), Paragraph("1,000 predictions for Phase 1 (var1), degree 4 polynomial, header: y", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Prediction 2", table_text), Paragraph("IMT2024072_pred_var2.csv", table_text), Paragraph("1,000 predictions for Phase 2 (var2), degree 8 polynomial, header: y", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Training Script", table_text), Paragraph("polynomial_regression.py", table_text), Paragraph("Standalone scikit-learn script for training, CV sweeps and inference", table_text), Paragraph("Reproducible", table_text)],
    ]
    t_sd = Table(summary_deliv, colWidths=[80, 137, 222, 65])
    t_sd.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_sd)
    story.append(Paragraph("<b>Table 4:</b> Deliverables summary for Roll Number IMT2024072.", caption_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph(
        "<b>Reproducibility Instructions:</b> The complete solution is automated in <code>polynomial_regression.py</code>. "
        "Running <code>python polynomial_regression.py</code> loads the calibration data, performs 5-fold cross-validation, "
        "fits the optimal polynomial models via <code>scikit-learn</code>, and outputs the final test prediction CSVs.",
        body_style
    ))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {filename}")

if __name__ == '__main__':
    build_pdf()
