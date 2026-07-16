import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
import structlog

logger = structlog.get_logger()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            "ReportTitle",
            parent=self.styles["Heading1"],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.HexColor("#1e293b"),
        ))
        self.styles.add(ParagraphStyle(
            "SectionHeader",
            parent=self.styles["Heading2"],
            fontSize=14,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.HexColor("#334155"),
        ))
        self.styles.add(ParagraphStyle(
            "BodyText2",
            parent=self.styles["BodyText"],
            fontSize=10,
            leading=14,
        ))

    def _generate_filename(self, report_type: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        uid = uuid.uuid4().hex[:8]
        return f"{report_type}_{timestamp}_{uid}.pdf"

    def _add_header(self, doc, title: str, subtitle: str = ""):
        elements = []
        elements.append(Paragraph(title, self.styles["ReportTitle"]))
        if subtitle:
            elements.append(Paragraph(subtitle, self.styles["BodyText2"]))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", color=colors.HexColor("#cbd5e1")))
        elements.append(Spacer(1, 12))
        return elements

    def _add_footer(self, doc):
        elements = []
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", color=colors.HexColor("#cbd5e1")))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(
            f"CrimeMatrix Report • Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles["BodyText2"],
        ))
        return elements

    def _make_table(self, data: list, headers: list = None) -> Table:
        table_data = []
        if headers:
            table_data.append(headers)
        for row in data:
            table_data.append([str(cell) for cell in row])

        table = Table(table_data)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TOPPADDING", (0, 1), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ]
        table.setStyle(TableStyle(style))
        return table

    def generate_summary(self, data: dict) -> str:
        filename = self._generate_filename("summary")
        filepath = os.path.join(OUTPUT_DIR, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []

        elements.extend(self._add_header(doc, "Case Summary Report", f"Crime #{data.get('crime_id', 'N/A')}"))

        elements.append(Paragraph("Case Information", self.styles["SectionHeader"]))
        summary_data = [
            ["Title", str(data.get("title", "N/A"))],
            ["Status", str(data.get("status", "N/A"))],
            ["Priority", str(data.get("priority", "N/A"))],
            ["Crime Type", str(data.get("crime_type", "N/A"))],
            ["District", str(data.get("district", "N/A"))],
            ["Reported Date", str(data.get("created_at", "N/A"))],
        ]
        elements.append(self._make_table(summary_data, ["Field", "Value"]))
        elements.append(Spacer(1, 16))

        if data.get("description"):
            elements.append(Paragraph("Description", self.styles["SectionHeader"]))
            elements.append(Paragraph(data["description"], self.styles["BodyText2"]))
            elements.append(Spacer(1, 16))

        if data.get("persons"):
            elements.append(Paragraph("Related Persons", self.styles["SectionHeader"]))
            persons_data = [[p.get("name", ""), p.get("role", ""), p.get("status", "")] for p in data["persons"]]
            elements.append(self._make_table(persons_data, ["Name", "Role", "Status"]))

        elements.extend(self._add_footer(doc))
        doc.build(elements)
        return filepath

    def generate_timeline(self, data: dict) -> str:
        filename = self._generate_filename("timeline")
        filepath = os.path.join(OUTPUT_DIR, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []

        elements.extend(self._add_header(doc, "Timeline Report", f"Crime #{data.get('crime_id', 'N/A')}"))

        events = data.get("events", [])
        if events:
            elements.append(Paragraph("Timeline Events", self.styles["SectionHeader"]))
            table_data = [[e.get("date", ""), e.get("title", ""), e.get("description", "")] for e in events]
            elements.append(self._make_table(table_data, ["Date", "Event", "Details"]))
        else:
            elements.append(Paragraph("No timeline events recorded.", self.styles["BodyText2"]))

        elements.extend(self._add_footer(doc))
        doc.build(elements)
        return filepath

    def generate_evidence(self, data: dict) -> str:
        filename = self._generate_filename("evidence")
        filepath = os.path.join(OUTPUT_DIR, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []

        elements.extend(self._add_header(doc, "Evidence Report", f"Crime #{data.get('crime_id', 'N/A')}"))

        items = data.get("evidence", [])
        if items:
            elements.append(Paragraph("Evidence Items", self.styles["SectionHeader"]))
            table_data = [
                [e.get("title", ""), e.get("type", ""), e.get("collected_at", ""), e.get("officer", "")]
                for e in items
            ]
            elements.append(self._make_table(table_data, ["Title", "Type", "Collected", "Officer"]))

            elements.append(Spacer(1, 16))
            for e in items:
                if e.get("description"):
                    elements.append(Paragraph(f"<b>{e.get('title', 'Item')}</b>", self.styles["BodyText2"]))
                    elements.append(Paragraph(e["description"], self.styles["BodyText2"]))
                    elements.append(Spacer(1, 8))
        else:
            elements.append(Paragraph("No evidence items recorded.", self.styles["BodyText2"]))

        elements.extend(self._add_footer(doc))
        doc.build(elements)
        return filepath

    def generate_investigation(self, data: dict) -> str:
        filename = self._generate_filename("investigation")
        filepath = os.path.join(OUTPUT_DIR, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []

        elements.extend(self._add_header(doc, "Investigation Report", f"Crime #{data.get('crime_id', 'N/A')}"))

        # Case Summary
        elements.append(Paragraph("Case Summary", self.styles["SectionHeader"]))
        summary_data = [
            ["Title", str(data.get("title", "N/A"))],
            ["Status", str(data.get("status", "N/A"))],
            ["Priority", str(data.get("priority", "N/A"))],
            ["District", str(data.get("district", "N/A"))],
        ]
        elements.append(self._make_table(summary_data, ["Field", "Value"]))
        elements.append(Spacer(1, 16))

        # Timeline
        events = data.get("timeline", [])
        if events:
            elements.append(Paragraph("Timeline", self.styles["SectionHeader"]))
            table_data = [[e.get("date", ""), e.get("title", "")] for e in events]
            elements.append(self._make_table(table_data, ["Date", "Event"]))
            elements.append(Spacer(1, 16))

        # Evidence
        items = data.get("evidence", [])
        if items:
            elements.append(Paragraph("Evidence", self.styles["SectionHeader"]))
            table_data = [[e.get("title", ""), e.get("type", "")] for e in items]
            elements.append(self._make_table(table_data, ["Title", "Type"]))
            elements.append(Spacer(1, 16))

        # Notes
        notes = data.get("notes", [])
        if notes:
            elements.append(Paragraph("Investigation Notes", self.styles["SectionHeader"]))
            for note in notes:
                elements.append(Paragraph(f"<b>{note.get('title', 'Note')}</b>", self.styles["BodyText2"]))
                elements.append(Paragraph(note.get("content", ""), self.styles["BodyText2"]))
                elements.append(Spacer(1, 8))

        elements.extend(self._add_footer(doc))
        doc.build(elements)
        return filepath
