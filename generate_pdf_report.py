import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Machine Learning Assignment: Polynomial Regression — Roll No: IMT2024072")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 750, letter[0] - 54, 750)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 35, page_text)
        self.drawString(54, 35, "Department of Computer Science & Engineering — Machine Learning")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        self.restoreState()


def build_pdf(filename="IMT2024072_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=colors.HexColor('#1a365d'),
        alignment=1,
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2d3748'),
        alignment=1,
        spaceAfter=10
    )
    
    meta_style = ParagraphStyle(
        'MetaBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1a365d'),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=11.8,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=4.5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor('#1a202c')
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#1a202c')
    )
    
    table_head = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.white,
        alignment=1
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )

    story = []
    
    # ----------------------------------------------------
    # PAGE 1: Title, Abstract, Problem Formulation & EDA
    # ----------------------------------------------------
    story.append(Paragraph("Polynomial Regression Modeling for Geothermal Systems", title_style))
    story.append(Paragraph("Optimal Degree Selection, Feature Analysis & Generalization on Calibration Datasets", subtitle_style))
    story.append(Paragraph("<b>Student Roll No:</b> IMT2024072 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Course:</b> Machine Learning &nbsp;&nbsp;|&nbsp;&nbsp; <b>Framework:</b> scikit-learn", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a365d'), spaceAfter=8))
    
    summary_html = (
        "<b>Executive Summary:</b> This study develops polynomial regression models to solve two distinct "
        "geothermal engineering prediction tasks: (1) <i>Steam Turbine Optimization (var1)</i>, governed by 6 operational "
        "control parameters to predict the Net Power Score (<i>y</i>), and (2) <i>Subterranean Thermal Reservoir Mapping (var2)</i>, "
        "governed by 3 spatial coordinate offsets to predict the Thermal Anomaly Score (<i>y</i>). Using 5-fold cross-validation, "
        "we systematically evaluated feature subsets, polynomial degrees, and regularization methods. "
        "For <b>Problem 1</b>, the optimal model is a <b>Degree 4 polynomial using all 6 operational features</b> (210 basis terms, "
        "achieving <i>R</i><sup>2</sup> = 0.9043 &plusmn; 0.0189 and MSE = 0.9618 &plusmn; 0.1508). For <b>Problem 2</b>, the optimal model is a "
        "<b>Degree 8 polynomial using all 3 spatial coordinates</b> (165 basis terms, achieving <i>R</i><sup>2</sup> = 0.9946 &plusmn; 0.0008 "
        "and MSE = 0.2523 &plusmn; 0.0275). Both models successfully resolve the bias-variance tradeoff and generalize accurately on unseen test distributions."
    )
    summary_table = Table([[Paragraph(summary_html, callout_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#edf2f7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("1. Problem Statements & Data Characteristics", h1_style))
    story.append(Paragraph(
        "<b>Phase 1: Power Plant Steam Turbine Optimization (var1):</b> The surface energy generation facility is governed "
        "by 6 continuous operational parameters representing percentage deviations bounded in [-1.0, 1.0]: "
        "high-pressure steam valve adjustment (<i>x</i><sub>1</sub>), condenser coolant flow rate adjustment (<i>x</i><sub>2</sub>), "
        "re-injection pump hydraulic pressure (<i>x</i><sub>3</sub>), turbine blade pitch angle (<i>x</i><sub>4</sub>), "
        "non-condensable gas exhaust valve rate (<i>x</i><sub>5</sub>), and steam inlet pressure adjustment (<i>x</i><sub>6</sub>). "
        "The continuous target variable <i>y</i> is the Net Power Score (train mean = 0.8629, std = 3.1872, range [-9.88, 12.07]).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Phase 2: Subterranean Thermal Reservoir Mapping (var2):</b> To determine optimal drilling coordinates for new "
        "geothermal production wells, sensors record spatial offsets in meters from the central basecamp: East-West offset (<i>x</i><sub>1</sub>), "
        "North-South offset (<i>x</i><sub>2</sub>), and vertical depth offset (<i>x</i><sub>3</sub>). All offsets are normalized within [-1.0, 1.0]. "
        "The continuous target variable <i>y</i> is the Thermal Anomaly Score (train mean = 2.2751, std = 6.9016, range [-30.26, 39.33]).",
        body_style
    ))
    
    ds_data = [
        [Paragraph("Dataset", table_head), Paragraph("Features", table_head), Paragraph("Train Samples", table_head), Paragraph("Test Samples", table_head), Paragraph("Target (<i>y</i>) Mean &plusmn; Std", table_head), Paragraph("Target Min / Max", table_head)],
        [Paragraph("IMT2024072_var1", table_text), Paragraph("6 (<i>x</i><sub>1</sub> &hellip; <i>x</i><sub>6</sub>)", table_text), Paragraph("1,000", table_text), Paragraph("1,000", table_text), Paragraph("0.8629 &plusmn; 3.1872", table_text), Paragraph("-9.879 / +12.067", table_text)],
        [Paragraph("IMT2024072_var2", table_text), Paragraph("3 (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>)", table_text), Paragraph("1,000", table_text), Paragraph("1,000", table_text), Paragraph("2.2751 &plusmn; 6.9016", table_text), Paragraph("-30.257 / +39.328", table_text)],
    ]
    t_ds = Table(ds_data, colWidths=[95, 80, 68, 68, 105, 88])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')])
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("2. Mathematical Formulation & Validation Protocol", h1_style))
    story.append(Paragraph(
        "Polynomial regression models the continuous response <i>y</i> as a linear combination of polynomial basis expansions "
        "of the input feature vector <b>x</b> = [<i>x</i><sub>1</sub>, &hellip;, <i>x</i><sub>D</sub>]<sup>T</sup> up to degree <i>d</i>:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b><i>y</i> = <i>w</i><sub>0</sub> + &sum;<sub>i=1</sub><sup>D</sup> <i>w</i><sub>i</sub> <i>x</i><sub>i</sub> + &sum;<sub>i=1</sub><sup>D</sup> &sum;<sub>j=i</sub><sup>D</sup> <i>w</i><sub>ij</sub> <i>x</i><sub>i</sub> <i>x</i><sub>j</sub> + &hellip; = &Phi;(<b>x</b>)<sup>T</sup> <b>w</b> + &epsilon;</b>",
        callout_style
    ))
    story.append(Paragraph(
        "where &Phi;(<b>x</b>) represents the feature vector of all monomials with total degree sum &le; <i>d</i>. The total number of terms (including bias) "
        "equals the combinatorial expression <b>P = C(D + d, d) = (D + d)! / (D! d!)</b>. "
        "This combinatorial scaling leads to rapid growth: for Problem 1 (<i>D</i> = 6), degree 4 has 210 terms, degree 5 has 462 terms, and degree 6 "
        "has 924 terms (approaching <i>N</i> = 1,000 samples). For Problem 2 (<i>D</i> = 3), scaling is much more compact (degree 8 produces 165 terms), "
        "enabling exploration of higher-order spatial harmonics without premature parameter saturation.",
        body_style
    ))
    story.append(Paragraph(
        "<b>5-Fold Cross-Validation Protocol:</b> To prevent overfitting and avoid data leakage, we employed <b>5-Fold Cross-Validation "
        "(KFold, shuffle=True, random_state=42)</b>. Across each fold, 800 samples were used for model fitting and 200 held-out samples for "
        "validation. The evaluation metrics used are Mean Squared Error (<b>MSE</b> = (1/N) &sum; (<i>y</i><sub>i</sub> - <i>y_pred</i><sub>i</sub>)<sup>2</sup>) "
        "and Coefficient of Determination (<b><i>R</i><sup>2</sup></b> = 1 - &sum;(<i>y</i><sub>i</sub> - <i>y_pred</i><sub>i</sub>)<sup>2</sup> / &sum;(<i>y</i><sub>i</sub> - <i>y_mean</i>)<sup>2</sup>).",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 2: Problem 1 In-depth Analysis & Results
    # ----------------------------------------------------
    story.append(Paragraph("3. Problem 1 (var1): Steam Turbine Optimization", h1_style))
    story.append(Paragraph(
        "To identify the optimal model structure for Net Power Score prediction, we performed systematic cross-validation over "
        "polynomial degrees <i>d</i> &in; {1, 2, 3, 4, 5} with all 6 features, complemented by combinatorial feature subset searches "
        "across all feature subsets at candidate degrees.",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    v1_table_data = [
        [Paragraph("Degree (<i>d</i>)", table_head), Paragraph("Features Used", table_head), Paragraph("Total Terms", table_head), Paragraph("Train MSE", table_head), Paragraph("Train <i>R</i><sup>2</sup>", table_head), Paragraph("5-Fold CV MSE", table_head), Paragraph("5-Fold CV <i>R</i><sup>2</sup>", table_head), Paragraph("Generalization Verdict", table_head)],
        [Paragraph("1", table_text), Paragraph("All 6 features", table_text), Paragraph("7", table_text), Paragraph("9.1248", table_text), Paragraph("0.1018", table_text), Paragraph("9.1704 &plusmn; 0.812", table_text), Paragraph("0.0937 &plusmn; 0.024", table_text), Paragraph("Severe Underfitting", table_text)],
        [Paragraph("2", table_text), Paragraph("All 6 features", table_text), Paragraph("28", table_text), Paragraph("2.9815", table_text), Paragraph("0.7065", table_text), Paragraph("3.0651 &plusmn; 0.294", table_text), Paragraph("0.6974 &plusmn; 0.021", table_text), Paragraph("Moderate Underfitting", table_text)],
        [Paragraph("3", table_text), Paragraph("All 6 features", table_text), Paragraph("84", table_text), Paragraph("0.9621", table_text), Paragraph("0.9053", table_text), Paragraph("1.0438 &plusmn; 0.128", table_text), Paragraph("0.8965 &plusmn; 0.015", table_text), Paragraph("Strong fit, sub-optimal", table_text)],
        [Paragraph("<b>4 (Optimal)</b>", table_text), Paragraph("<b>All 6 features</b>", table_text), Paragraph("<b>210</b>", table_text), Paragraph("<b>0.4321</b>", table_text), Paragraph("<b>0.9574</b>", table_text), Paragraph("<b>0.9618 &plusmn; 0.151</b>", table_text), Paragraph("<b>0.9043 &plusmn; 0.019</b>", table_text), Paragraph("<b>Global Optimum</b>", table_text)],
        [Paragraph("5", table_text), Paragraph("All 6 features", table_text), Paragraph("462", table_text), Paragraph("0.0894", table_text), Paragraph("0.9912", table_text), Paragraph("2.2071 &plusmn; 0.485", table_text), Paragraph("0.7787 &plusmn; 0.052", table_text), Paragraph("Severe Overfitting", table_text)],
        [Paragraph("3 (Subset)", table_text), Paragraph("First 3 [<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>]", table_text), Paragraph("20", table_text), Paragraph("8.1402", table_text), Paragraph("0.1987", table_text), Paragraph("8.2561 &plusmn; 0.651", table_text), Paragraph("0.1834 &plusmn; 0.038", table_text), Paragraph("Truncated / Biased", table_text)],
        [Paragraph("4 (Subset)", table_text), Paragraph("Best 4 [<i>x</i><sub>1</sub>, <i>x</i><sub>3</sub>, <i>x</i><sub>5</sub>, <i>x</i><sub>6</sub>]", table_text), Paragraph("70", table_text), Paragraph("3.6521", table_text), Paragraph("0.6405", table_text), Paragraph("3.7866 &plusmn; 0.312", table_text), Paragraph("0.6274 &plusmn; 0.027", table_text), Paragraph("Omitted Interactions", table_text)],
    ]
    t_v1 = Table(v1_table_data, colWidths=[55, 95, 52, 48, 48, 70, 68, 68])
    t_v1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#e6fffa')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,3), [colors.white, colors.HexColor('#f7fafc')]),
        ('ROWBACKGROUNDS', (0,5), (-1,-1), [colors.white, colors.HexColor('#f7fafc'), colors.white])
    ]))
    story.append(t_v1)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("<b>Detailed Analysis & Rationale for var1:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Feature Subset Exploration:</b> Exhaustive subset ablation demonstrated that all 6 physical operational parameters are essential. "
        "Omitting parameters (e.g. coolant rate <i>x</i><sub>2</sub> or blade pitch <i>x</i><sub>4</sub>) causes significant performance degradation: "
        "the best 3-feature subset attains <i>R</i><sup>2</sup> = 0.5029, and the best 4-feature subset reaches <i>R</i><sup>2</sup> = 0.6274. "
        "Turbine efficiency exhibits high cross-parameter coupling across all six physical controls.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Degree Selection:</b> At degree 1, linear regression underfits (CV <i>R</i><sup>2</sup> = 0.0937). Quadratic expansions reach <i>R</i><sup>2</sup> = 0.6974. "
        "Cubic expansions (<i>d</i> = 3) produce a solid model (CV <i>R</i><sup>2</sup> = 0.8965, CV MSE = 1.0438). "
        "<b>Degree 4 achieves the global performance optimum</b>, lowering CV MSE to <b>0.9618</b> and maximizing CV <i>R</i><sup>2</sup> to <b>0.9043</b>. "
        "At degree 5, 462 parameters cause the training MSE to collapse to 0.0894 while validation MSE spikes to 2.2071 (<i>R</i><sup>2</sup> = 0.7787), "
        "exhibiting substantial overfitting.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Regularization Comparison:</b> We tested Ridge regression with 50 log-spaced &alpha; values &in; [10<sup>-4</sup>, 10<sup>4</sup>]. "
        "At degree 4, the optimal &alpha; &approx; 10<sup>-3</sup> produced CV MSE = 0.9610, showing that Ordinary Least Squares (OLS) is already "
        "numerically stable and unregularized OLS achieves near-identical generalization without introducing shrinkage bias.",
        bullet_style
    ))
    story.append(Spacer(1, 3))
    
    if os.path.exists('fig_var1_cv.png'):
        story.append(Image('fig_var1_cv.png', width=5.2*inch, height=2.3*inch))
        story.append(Paragraph("<b>Figure 1:</b> 5-Fold cross-validation metrics across polynomial degrees for Problem 1 (var1). "
                               "The MSE curve confirms Degree 4 as the global generalization optimum.", caption_style))
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 3: Problem 2 In-depth Analysis & Results
    # ----------------------------------------------------
    story.append(Paragraph("4. Problem 2 (var2): Subterranean Thermal Reservoir Mapping", h1_style))
    story.append(Paragraph(
        "Problem 2 estimates 3D subsurface temperature anomalies from spatial coordinate offsets (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>). "
        "Geological heat plumes generate sharp localized spatial gradients, demanding higher-order polynomial representations. "
        "With <i>D</i> = 3, term counts remain modest, permitting an empirical degree sweep up to <i>d</i> = 12.",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    v2_table_data = [
        [Paragraph("Degree (<i>d</i>)", table_head), Paragraph("Features Used", table_head), Paragraph("Total Terms", table_head), Paragraph("Train MSE", table_head), Paragraph("Train <i>R</i><sup>2</sup>", table_head), Paragraph("5-Fold CV MSE", table_head), Paragraph("5-Fold CV <i>R</i><sup>2</sup>", table_head), Paragraph("Generalization Verdict", table_head)],
        [Paragraph("1", table_text), Paragraph("All 3 features", table_text), Paragraph("4", table_text), Paragraph("35.120", table_text), Paragraph("0.2618", table_text), Paragraph("35.369 &plusmn; 0.912", table_text), Paragraph("0.2531 &plusmn; 0.019", table_text), Paragraph("Gross Underfitting", table_text)],
        [Paragraph("2", table_text), Paragraph("All 3 features", table_text), Paragraph("10", table_text), Paragraph("23.514", table_text), Paragraph("0.5057", table_text), Paragraph("23.821 &plusmn; 1.555", table_text), Paragraph("0.4975 &plusmn; 0.023", table_text), Paragraph("Severe Underfitting", table_text)],
        [Paragraph("4", table_text), Paragraph("All 3 features", table_text), Paragraph("35", table_text), Paragraph("3.821", table_text), Paragraph("0.9197", table_text), Paragraph("3.988 &plusmn; 0.261", table_text), Paragraph("0.9159 &plusmn; 0.004", table_text), Paragraph("Underfitting boundary", table_text)],
        [Paragraph("6", table_text), Paragraph("All 3 features", table_text), Paragraph("84", table_text), Paragraph("0.492", table_text), Paragraph("0.9897", table_text), Paragraph("0.541 &plusmn; 0.054", table_text), Paragraph("0.9885 &plusmn; 0.001", table_text), Paragraph("Strong fit", table_text)],
        [Paragraph("7", table_text), Paragraph("All 3 features", table_text), Paragraph("120", table_text), Paragraph("0.245", table_text), Paragraph("0.9948", table_text), Paragraph("0.307 &plusmn; 0.033", table_text), Paragraph("0.9935 &plusmn; 0.001", table_text), Paragraph("Near-optimal", table_text)],
        [Paragraph("<b>8 (Optimal)</b>", table_text), Paragraph("<b>All 3 features</b>", table_text), Paragraph("<b>165</b>", table_text), Paragraph("<b>0.164</b>", table_text), Paragraph("<b>0.9966</b>", table_text), Paragraph("<b>0.2523 &plusmn; 0.028</b>", table_text), Paragraph("<b>0.9946 &plusmn; 0.001</b>", table_text), Paragraph("<b>Global Optimum</b>", table_text)],
        [Paragraph("9", table_text), Paragraph("All 3 features", table_text), Paragraph("220", table_text), Paragraph("0.138", table_text), Paragraph("0.9971", table_text), Paragraph("0.2954 &plusmn; 0.049", table_text), Paragraph("0.9937 &plusmn; 0.001", table_text), Paragraph("Slight Overparameterization", table_text)],
        [Paragraph("10", table_text), Paragraph("All 3 features", table_text), Paragraph("286", table_text), Paragraph("0.112", table_text), Paragraph("0.9976", table_text), Paragraph("0.3484 &plusmn; 0.063", table_text), Paragraph("0.9926 &plusmn; 0.002", table_text), Paragraph("Overfitting onset", table_text)],
        [Paragraph("12", table_text), Paragraph("All 3 features", table_text), Paragraph("455", table_text), Paragraph("0.068", table_text), Paragraph("0.9986", table_text), Paragraph("1.0140 &plusmn; 0.443", table_text), Paragraph("0.9786 &plusmn; 0.010", table_text), Paragraph("Clear Overfitting", table_text)],
        [Paragraph("4 (Single <i>x</i><sub>1</sub>)", table_text), Paragraph("Only <i>x</i><sub>1</sub>", table_text), Paragraph("5", table_text), Paragraph("43.210", table_text), Paragraph("0.0882", table_text), Paragraph("43.632 &plusmn; 1.210", table_text), Paragraph("0.0787 &plusmn; 0.025", table_text), Paragraph("Extreme Bias / Failure", table_text)],
    ]
    t_v2 = Table(v2_table_data, colWidths=[55, 95, 52, 48, 48, 70, 68, 68])
    t_v2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#e6fffa')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,5), [colors.white, colors.HexColor('#f7fafc')]),
        ('ROWBACKGROUNDS', (0,7), (-1,-1), [colors.white, colors.HexColor('#f7fafc'), colors.white, colors.HexColor('#f7fafc')])
    ]))
    story.append(t_v2)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("<b>Detailed Analysis & Rationale for var2:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Spatial Coordinate Completeness:</b> Univariate and bivariate experiments revealed that 3D geothermal reservoir structures "
        "cannot be modeled without all three spatial axes. Relying on East-West coordinate <i>x</i><sub>1</sub> alone (swept up to degree 20) "
        "caps <i>R</i><sup>2</sup> at 0.0787 (MSE &gt; 43.6). A 2D planar projection (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>) caps at <i>R</i><sup>2</sup> = 0.5925. "
        "All three spatial coordinates (<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) are required to capture vertical and lateral convective gradients.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Degree Optimization:</b> Degrees <i>d</i> &le; 4 produce substantial underfitting (MSE &gt; 3.98). "
        "Increasing degree from 4 to 8 reduces cross-validation error by over 93% (MSE drops from 3.9875 to 0.2523), with <i>R</i><sup>2</sup> "
        "reaching 0.9946. <b>Degree 8 attains the absolute global minimum validation MSE (0.2523 &plusmn; 0.0275)</b>. "
        "Advancing past degree 8 introduces overparameterization: CV MSE rises to 0.2954 at <i>d</i> = 9, 0.3484 at <i>d</i> = 10, and 1.0140 at <i>d</i> = 12.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Variance Stability:</b> The standard deviation of validation MSE across the 5 folds reaches its minimum at degree 8 (&plusmn;0.0275), "
        "confirming that the degree 8 model achieves high spatial stability across disparate sampling partitions.",
        bullet_style
    ))
    story.append(Spacer(1, 3))
    
    if os.path.exists('fig_var2_cv.png'):
        story.append(Image('fig_var2_cv.png', width=5.2*inch, height=2.3*inch))
        story.append(Paragraph("<b>Figure 2:</b> 5-Fold cross-validation metrics across polynomial degrees 1–12 for Problem 2 (var2). "
                               "Degree 8 achieves the minimum CV MSE of 0.2523, beyond which overfitting degrades test variance.", caption_style))
    
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 4: Diagnostics, Inferences, Submission & Code
    # ----------------------------------------------------
    story.append(Paragraph("5. Model Diagnostics, Residual Analysis & Inferences", h1_style))
    story.append(Paragraph(
        "To confirm the physical and statistical validity of both fitted models, we inspected residual distributions "
        "(<i>e</i><sub>i</sub> = <i>y</i><sub>i</sub> - <i>y_pred</i><sub>i</sub>). Valid regression models require uncorrelated residuals "
        "with zero mean and constant variance (homoscedasticity).",
        body_style
    ))
    story.append(Spacer(1, 2))
    
    if os.path.exists('fig_fits_and_residuals.png'):
        story.append(Image('fig_fits_and_residuals.png', width=5.2*inch, height=3.0*inch))
        story.append(Paragraph("<b>Figure 3:</b> (Left) Actual vs Predicted response for both models demonstrating tight linearity along the diagonal. "
                               "(Right) Residual plots centered evenly around zero with no heteroscedastic fan patterns or curvature.", caption_style))
        story.append(Spacer(1, 3))
    
    story.append(Paragraph(
        "<b>Sanity Verification on Test Set Predictions:</b> We analyzed the predicted test set target distributions against training distributions. "
        "For var1, test predictions exhibit mean = 0.9876, std = 4.1168, and range [-10.77, 15.71], consistent with train target statistics "
        "(mean 0.8629, std 3.1872, range [-9.88, 12.07]). For var2, test predictions exhibit mean = 2.2535, std = 6.4661, and range "
        "[-25.28, 38.92], closely matching train target statistics (mean 2.2751, std 6.9016, range [-30.26, 39.33]). "
        "No unbounded extrapolation or numerical instability was observed.",
        body_style
    ))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("6. Summary of Deliverables & Reproducibility", h1_style))
    
    summary_deliv = [
        [Paragraph("Deliverable", table_head), Paragraph("File Name", table_head), Paragraph("Specification / Content", table_head), Paragraph("Status", table_head)],
        [Paragraph("Report", table_text), Paragraph("IMT2024072_Report.pdf", table_text), Paragraph("4-page academic write-up documenting methodology, CV sweeps & rationales", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Prediction 1", table_text), Paragraph("IMT2024072_pred_var1.csv", table_text), Paragraph("1,000 predictions for Phase 1 (var1), degree 4 polynomial, header: y", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Prediction 2", table_text), Paragraph("IMT2024072_pred_var2.csv", table_text), Paragraph("1,000 predictions for Phase 2 (var2), degree 8 polynomial, header: y", table_text), Paragraph("Completed", table_text)],
        [Paragraph("Training Script", table_text), Paragraph("polynomial_regression.py", table_text), Paragraph("Self-contained scikit-learn script for training, CV evaluation & inference", table_text), Paragraph("Reproducible", table_text)],
    ]
    t_sd = Table(summary_deliv, colWidths=[78, 137, 222, 67])
    t_sd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')])
    ]))
    story.append(t_sd)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph(
        "<b>Reproducibility Instructions:</b> The complete solution is automated in <code>polynomial_regression.py</code>. "
        "Running <code>python polynomial_regression.py</code> loads the calibration data, performs 5-fold cross-validation, "
        "fits the optimal polynomial models via <code>scikit-learn</code>, and produces the final test prediction CSVs and evaluation figures.",
        body_style
    ))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {filename}")

if __name__ == '__main__':
    build_pdf()
