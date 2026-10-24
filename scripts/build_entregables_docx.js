/**
 * COMPILADOR ESTILIZADO DE ENTREGABLES ACADÉMICOS UDEC (.MD -> .DOCX)
 * Genera:
 *  1. 01_Manual_Tecnico_HoneyMetrics_v2.docx (Estilo UDEC Azul + Bloques Código #333333 + Diccionario Minimalista)
 *  2. 02_Diccionario_Datos_HoneyMetrics_v2.docx (Estilo Diccionario Minimalista 5 Columnas + Control UDEC)
 *  3. 03_Manual_Usuario_HoneyMetrics_v2.docx (Estilo Editorial Dorado HoneyMetrics + Cajas Nota Crema/Oro + Control UDEC)
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageBreak, ImageRun, Header, Footer, PageNumber, VerticalAlign
} = require("docx");

// ---------------------------------------------------------------------------
// CONFIGURACIÓN DE RUTAS Y CONSTANTES DE ESTILO
// ---------------------------------------------------------------------------
const ENTREGABLES_DIR = path.resolve(__dirname, "../docs/entregables_profesor");
const LOGO_CANDIDATES = [
  path.resolve(__dirname, "../docs/images/logo_universidad.png"),
  "/media/sebas/Exdrive/Workspace/honeymetrics-backend/docs/images/logo_universidad.png",
];
const LOGO_PATH = LOGO_CANDIDATES.find((p) => fs.existsSync(p)) || null;

const FONT = "Arial";
const FONT_CODE = "Consolas";

// Paleta UDEC / Manual Técnico
const BLUE_UDEC = "2E74B5";
const DARK_CODE_BG = "333333";
const GRAY_BANNER = "808080";
const GRAY_HEADER_FILL = "EDEDED";

// Paleta Editorial Dorada / Manual de Usuario
const GOLD_TITLE = "7A6318";
const GOLD_ACCENT = "C5A028";
const GOLD_DARK = "5C4D17";
const NOTE_BG_CREAM = "F9F5E8";

// Bordes reutilizables
const B_BLACK_SOLID = { style: BorderStyle.SINGLE, size: 6, color: "000000" };
const B_GRAY_LIGHT = { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" };
const B_GOLD_SOLID = { style: BorderStyle.SINGLE, size: 12, color: GOLD_ACCENT };
const B_GOLD_THICK_LEFT = { style: BorderStyle.SINGLE, size: 24, color: GOLD_ACCENT };
const B_DASHED_PLACEHOLDER = { style: BorderStyle.DASHED, size: 8, color: "7F8C8D" };
const B_NONE = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };

const AUTHORS = [
  "Johan Sebastián Posada Beltrán",
  "Juan Pablo Fonseca Celis",
  "Manuel Alejandro Aldana Rincón",
];

// ---------------------------------------------------------------------------
// PARSER DE TEXTO INLINE (**negrita**, *cursiva*, `código`)
// ---------------------------------------------------------------------------
function parseInlineRuns(text, baseOpts = {}) {
  const runs = [];
  const tokenRegex = /(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g;
  let lastIdx = 0;
  let match;

  while ((match = tokenRegex.exec(text)) !== null) {
    if (match.index > lastIdx) {
      runs.push(
        new TextRun({
          text: text.slice(lastIdx, match.index),
          font: baseOpts.font || FONT,
          size: baseOpts.size || 21,
          bold: baseOpts.bold || false,
          italics: baseOpts.italics || false,
          color: baseOpts.color || "111111",
        })
      );
    }
    const token = match[0];
    if (token.startsWith("**") && token.endsWith("**")) {
      runs.push(
        new TextRun({
          text: token.slice(2, -2),
          font: baseOpts.font || FONT,
          size: baseOpts.size || 21,
          bold: true,
          color: baseOpts.color || "000000",
        })
      );
    } else if (token.startsWith("`") && token.endsWith("`")) {
      runs.push(
        new TextRun({
          text: token.slice(1, -1),
          font: FONT_CODE,
          size: (baseOpts.size || 21) - 2,
          bold: baseOpts.bold || false,
          color: baseOpts.codeColor || "1F4E79",
        })
      );
    } else if (token.startsWith("*") && token.endsWith("*")) {
      runs.push(
        new TextRun({
          text: token.slice(1, -1),
          font: baseOpts.font || FONT,
          size: baseOpts.size || 21,
          italics: true,
          color: baseOpts.color || "333333",
        })
      );
    }
    lastIdx = tokenRegex.lastIndex;
  }

  if (lastIdx < text.length) {
    runs.push(
      new TextRun({
        text: text.slice(lastIdx),
        font: baseOpts.font || FONT,
        size: baseOpts.size || 21,
        bold: baseOpts.bold || false,
        italics: baseOpts.italics || false,
        color: baseOpts.color || "111111",
      })
    );
  }

  return runs.length > 0
    ? runs
    : [new TextRun({ text: "", font: FONT, size: baseOpts.size || 21 })];
}

// ---------------------------------------------------------------------------
// COMPONENTES INSTITUCIONALES UDEC (Encabezado 3 Columnas, Portadas, Control)
// ---------------------------------------------------------------------------
function buildUdecBoxHeader({ docTitle, projectName = "HONEYMETRICS", dateStr = "2026-10-23", versionStr = "2.0.0" }) {
  const logoCellContent = [];
  if (LOGO_PATH) {
    logoCellContent.push(
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new ImageRun({
            type: "png",
            data: fs.readFileSync(LOGO_PATH),
            transformation: { width: 56, height: 68 },
          }),
        ],
      })
    );
  } else {
    logoCellContent.push(
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "UDEC", font: FONT, bold: true, size: 20, color: "1E5631" })],
      })
    );
  }

  return new Header({
    children: [
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [1750, 5210, 2400],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                width: { size: 1750, type: WidthType.DXA },
                rowSpan: 2,
                verticalAlign: VerticalAlign.CENTER,
                borders: { top: B_BLACK_SOLID, bottom: B_BLACK_SOLID, left: B_BLACK_SOLID, right: B_BLACK_SOLID },
                margins: { top: 80, bottom: 80, left: 80, right: 80 },
                children: logoCellContent,
              }),
              new TableCell({
                width: { size: 5210, type: WidthType.DXA },
                rowSpan: 2,
                verticalAlign: VerticalAlign.CENTER,
                borders: { top: B_BLACK_SOLID, bottom: B_BLACK_SOLID, left: B_BLACK_SOLID, right: B_BLACK_SOLID },
                children: [
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 40 },
                    children: [new TextRun({ text: docTitle.toUpperCase(), font: FONT, size: 22 })],
                  }),
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ text: projectName.toUpperCase(), font: FONT, size: 22 })],
                  }),
                ],
              }),
              new TableCell({
                width: { size: 2400, type: WidthType.DXA },
                verticalAlign: VerticalAlign.CENTER,
                borders: { top: B_BLACK_SOLID, bottom: B_BLACK_SOLID, left: B_BLACK_SOLID, right: B_BLACK_SOLID },
                margins: { top: 100, bottom: 100, left: 140, right: 100 },
                children: [
                  new Paragraph({
                    children: [new TextRun({ text: `Fecha: ${dateStr}`, font: FONT, size: 18 })],
                  }),
                ],
              }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({
                width: { size: 2400, type: WidthType.DXA },
                verticalAlign: VerticalAlign.CENTER,
                borders: { top: B_BLACK_SOLID, bottom: B_BLACK_SOLID, left: B_BLACK_SOLID, right: B_BLACK_SOLID },
                margins: { top: 100, bottom: 100, left: 140, right: 100 },
                children: [
                  new Paragraph({
                    children: [new TextRun({ text: `Versión: ${versionStr}`, font: FONT, size: 18 })],
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
      new Paragraph({ text: "", spacing: { after: 160 } }),
    ],
  });
}

function buildUserManualGoldHeader() {
  return new Header({
    children: [
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        border: { bottom: B_GOLD_SOLID },
        spacing: { after: 160 },
        children: [
          new TextRun({ text: "HoneyMetrics", font: FONT, bold: true, size: 19, color: GOLD_DARK }),
          new TextRun({ text: " • Manual de Usuario", font: FONT, size: 19, color: "666666" }),
        ],
      }),
    ],
  });
}

function buildSimpleFooter(isGold = false) {
  return new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        border: isGold ? { top: B_GOLD_SOLID } : undefined,
        spacing: { before: 120 },
        children: isGold
          ? [
              new TextRun({ text: "Página ", font: FONT, size: 18, color: "666666" }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, bold: true, size: 18, color: GOLD_DARK }),
              new TextRun({ text: " de ", font: FONT, size: 18, color: "666666" }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, bold: true, size: 18, color: GOLD_DARK }),
            ]
          : [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 21, color: "000000" })],
      }),
    ],
  });
}

function buildTechnicalCoverPage(docTitle) {
  return [
    new Paragraph({ text: "", spacing: { before: 3800 } }),
    new Paragraph({
      spacing: { after: 200 },
      children: [new TextRun({ text: docTitle.toUpperCase(), font: FONT, bold: true, size: 48, color: "000000" })],
    }),
    new Paragraph({
      spacing: { after: 1100 },
      children: [new TextRun({ text: "HONEYMETRICS", font: FONT, bold: true, size: 48, color: "000000" })],
    }),
    ...AUTHORS.map(
      (a) =>
        new Paragraph({
          spacing: { after: 160 },
          children: [new TextRun({ text: a, font: FONT, bold: true, size: 26, color: "000000" })],
        })
    ),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

function buildUserManualGoldCoverPage() {
  return [
    new Paragraph({ text: "", spacing: { before: 3400 } }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [new TextRun({ text: "— MANUAL DE USUARIO —", font: FONT, bold: true, size: 22, color: GOLD_TITLE })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [new TextRun({ text: "HoneyMetrics", font: FONT, bold: true, size: 64, color: GOLD_DARK })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 1400 },
      children: [
        new TextRun({
          text: "Plataforma de inteligencia de amenazas para equipos de ciberseguridad",
          font: FONT,
          size: 23,
          color: "666666",
        }),
      ],
    }),
    ...AUTHORS.map(
      (a) =>
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 120 },
          children: [new TextRun({ text: a, font: FONT, bold: true, size: 22, color: "333333" })],
        })
    ),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

function buildDataDictHeaderBlock() {
  return [
    new Paragraph({
      spacing: { after: 180 },
      children: [new TextRun({ text: "HoneyMetrics", font: "Georgia", size: 44, color: BLUE_UDEC })],
    }),
    ...AUTHORS.map(
      (a) =>
        new Paragraph({
          spacing: { after: 80 },
          children: [new TextRun({ text: a, font: "Georgia", size: 24, color: "111111" })],
        })
    ),
    new Paragraph({
      spacing: { before: 360, after: 240 },
      children: [
        new TextRun({ text: "DICCIONARIO DE DATOS DEL SISTEMA", font: FONT, size: 32, color: BLUE_UDEC }),
      ],
    }),
  ];
}

// Tablas oficiales REGISTRO DE CAMBIOS y CONTROL DEL DOCUMENTO (Pág. 4 del PDF)
function buildGovernanceBannerTable(bannerTitle, headers, widths, rowsData) {
  const totalW = widths.reduce((a, b) => a + b, 0);
  const paddedRows = [...rowsData];
  while (paddedRows.length < 3) {
    paddedRows.push(headers.map(() => ""));
  }

  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({
        tableHeader: true,
        children: [
          new TableCell({
            width: { size: totalW, type: WidthType.DXA },
            columnSpan: headers.length,
            shading: { fill: GRAY_BANNER, type: ShadingType.CLEAR, color: "auto" },
            borders: { top: B_GRAY_LIGHT, bottom: B_GRAY_LIGHT, left: B_GRAY_LIGHT, right: B_GRAY_LIGHT },
            margins: { top: 70, bottom: 70, left: 100, right: 100 },
            children: [
              new Paragraph({
                children: [new TextRun({ text: bannerTitle, font: FONT, bold: true, size: 20, color: "FFFFFF" })],
              }),
            ],
          }),
        ],
      }),
      new TableRow({
        tableHeader: true,
        children: headers.map((h, i) =>
          new TableCell({
            width: { size: widths[i], type: WidthType.DXA },
            shading: { fill: "F5F5F5", type: ShadingType.CLEAR, color: "auto" },
            borders: { top: B_GRAY_LIGHT, bottom: B_GRAY_LIGHT, left: B_GRAY_LIGHT, right: B_GRAY_LIGHT },
            margins: { top: 70, bottom: 70, left: 100, right: 100 },
            children: [
              new Paragraph({
                children: [new TextRun({ text: h.replace(/\*\*/g, ""), font: FONT, bold: true, size: 19 })],
              }),
            ],
          })
        ),
      }),
      ...paddedRows.map(
        (r) =>
          new TableRow({
            cantSplit: true,
            children: r.map((val, i) =>
              new TableCell({
                width: { size: widths[i], type: WidthType.DXA },
                borders: { top: B_GRAY_LIGHT, bottom: B_GRAY_LIGHT, left: B_GRAY_LIGHT, right: B_GRAY_LIGHT },
                margins: { top: 80, bottom: 80, left: 100, right: 100 },
                children: [
                  new Paragraph({
                    children: [new TextRun({ text: val || " ", font: FONT, size: 19 })],
                  }),
                ],
              })
            ),
          })
      ),
    ],
  });
}

// ---------------------------------------------------------------------------
// BLOQUES ESPECIALIZADOS: CÓDIGO OSCURO (#333333), DICCIONARIO, NOTAS Y FIGURAS
// ---------------------------------------------------------------------------
function buildDarkCodeTable(codeLines) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [
      new TableRow({
        cantSplit: false,
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: DARK_CODE_BG, type: ShadingType.CLEAR, color: "auto" },
            borders: { top: B_NONE, bottom: B_NONE, left: B_NONE, right: B_NONE },
            margins: { top: 140, bottom: 140, left: 180, right: 180 },
            children: codeLines.map((line) => {
              const trimmed = line.trim();
              const isComment = trimmed.startsWith("#") || trimmed.startsWith("--");
              return new Paragraph({
                spacing: { line: 240, after: 20 },
                children: [
                  new TextRun({
                    text: line.length > 0 ? line : " ",
                    font: FONT_CODE,
                    size: 18,
                    italics: isComment,
                    color: isComment ? "A6A6A6" : "F8F8F2",
                  }),
                ],
              });
            }),
          }),
        ],
      }),
    ],
  });
}

// Tabla minimalista de 5 columnas sin bordes verticales (idéntica al PDF de Diccionario)
function buildMinimalistDictionaryTable(headers, rows) {
  const colWidths = [1850, 1450, 1450, 1000, 3610];
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({
        tableHeader: true,
        cantSplit: true,
        children: headers.map((h, i) =>
          new TableCell({
            width: { size: colWidths[i], type: WidthType.DXA },
            borders: { top: B_NONE, bottom: B_BLACK_SOLID, left: B_NONE, right: B_NONE },
            margins: { top: 90, bottom: 90, left: 70, right: 70 },
            children: [
              new Paragraph({
                children: [new TextRun({ text: h.replace(/\*\*/g, ""), font: FONT, bold: true, size: 19 })],
              }),
            ],
          })
        ),
      }),
      ...rows.map(
        (r) =>
          new TableRow({
            cantSplit: true,
            children: r.map((cellText, i) =>
              new TableCell({
                width: { size: colWidths[i], type: WidthType.DXA },
                borders: { top: B_BLACK_SOLID, bottom: B_BLACK_SOLID, left: B_NONE, right: B_NONE },
                margins: { top: 100, bottom: 100, left: 70, right: 70 },
                children: [
                  new Paragraph({
                    spacing: { line: 250 },
                    children: parseInlineRuns(cellText, { size: 19, codeColor: "000000" }),
                  }),
                ],
              })
            ),
          })
      ),
    ],
  });
}

// Tabla general con bordes limpios y cabecera sombreada
function buildStandardGridTable(headers, rows, isGoldTheme = false) {
  const totalW = 9360;
  const colCount = headers.length;
  let colWidths;
  if (colCount === 2) colWidths = [2800, 6560];
  else if (colCount === 3) colWidths = [2300, 2100, 4960];
  else if (colCount === 4) colWidths = [1800, 2500, 2500, 2560];
  else colWidths = headers.map(() => Math.floor(totalW / colCount));

  const headerFill = isGoldTheme ? "F4ECD6" : GRAY_HEADER_FILL;

  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({
        tableHeader: true,
        cantSplit: true,
        children: headers.map((h, i) =>
          new TableCell({
            width: { size: colWidths[i], type: WidthType.DXA },
            shading: { fill: headerFill, type: ShadingType.CLEAR, color: "auto" },
            borders: { top: B_BLACK_SOLID, bottom: B_BLACK_SOLID, left: B_BLACK_SOLID, right: B_BLACK_SOLID },
            margins: { top: 80, bottom: 80, left: 90, right: 90 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: h.replace(/\*\*/g, ""),
                    font: FONT,
                    bold: true,
                    size: 19,
                    color: isGoldTheme ? GOLD_DARK : "000000",
                  }),
                ],
              }),
            ],
          })
        ),
      }),
      ...rows.map(
        (r) =>
          new TableRow({
            cantSplit: true,
            children: r.map((cellText, i) =>
              new TableCell({
                width: { size: colWidths[i] || Math.floor(totalW / colCount), type: WidthType.DXA },
                borders: { top: B_GRAY_LIGHT, bottom: B_GRAY_LIGHT, left: B_GRAY_LIGHT, right: B_GRAY_LIGHT },
                margins: { top: 75, bottom: 75, left: 90, right: 90 },
                children: [
                  new Paragraph({
                    spacing: { line: 245 },
                    children: parseInlineRuns(cellText, { size: 18 }),
                  }),
                ],
              })
            ),
          })
      ),
    ],
  });
}

function buildGoldNoteBox(noteText) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [
      new TableRow({
        cantSplit: true,
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: NOTE_BG_CREAM, type: ShadingType.CLEAR, color: "auto" },
            borders: { top: B_NONE, bottom: B_NONE, right: B_NONE, left: B_GOLD_THICK_LEFT },
            margins: { top: 100, bottom: 100, left: 160, right: 140 },
            children: [
              new Paragraph({
                spacing: { line: 250 },
                children: parseInlineRuns(noteText, { size: 19, color: "333333" }),
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

const SCREENSHOTS_DIR = path.resolve(__dirname, "../docs/assets/screenshots");

function getImageDimensions(imgPath) {
  if (imgPath.includes("mobile") || imgPath.includes("390")) {
    return { width: 220, height: 476 };
  }
  return { width: 540, height: 338 };
}

function buildRealImageParagraph(imgPath) {
  const dims = getImageDimensions(imgPath);
  const imgBuffer = fs.readFileSync(imgPath);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 180, after: 120 },
    children: [
      new ImageRun({
        type: "png",
        data: imgBuffer,
        transformation: dims,
      }),
    ],
  });
}

function resolvePlaceholderToImage(placeholderText, nextLine) {
  const combined = (placeholderText + " " + (nextLine || "")).toLowerCase();

  if (combined.includes("figura 1b") || combined.includes("móvil") || combined.includes("mobile")) {
    return path.join(SCREENSHOTS_DIR, "fig01b_mobile_landing.png");
  }
  if (combined.includes("figura 1") || combined.includes("inicio de sesión") || combined.includes("formulario de acceso")) {
    return path.join(SCREENSHOTS_DIR, "fig01_login.png");
  }
  if (combined.includes("figura 2") || combined.includes("mfa") || combined.includes("código qr") || combined.includes("enrolamiento")) {
    return path.join(SCREENSHOTS_DIR, "fig02_mfa_enrolamiento.png");
  }
  if (combined.includes("figura 3") || combined.includes("recuperación") || combined.includes("redefinición") || combined.includes("olvidó")) {
    return path.join(SCREENSHOTS_DIR, "fig03_recuperacion_clave.png");
  }
  if (combined.includes("figura 4") || combined.includes("preferencias") || combined.includes("fortaleza") || combined.includes("cambio de contraseña")) {
    return path.join(SCREENSHOTS_DIR, "fig07_admin_usuarios_roles.png");
  }
  if (combined.includes("figura 5") || combined.includes("telegram") || combined.includes("userinfobot")) {
    return path.join(SCREENSHOTS_DIR, "fig01b_mobile_landing.png");
  }
  if (combined.includes("figura 6") || combined.includes("dashboard") || combined.includes("kpis") || combined.includes("panorámica")) {
    return path.join(SCREENSHOTS_DIR, "fig04_dashboard_cti.png");
  }
  if (combined.includes("figura 7") || combined.includes("threat center") || combined.includes("ioc") || combined.includes("indicadores")) {
    return path.join(SCREENSHOTS_DIR, "fig05_threat_center_ioc.png");
  }
  if (combined.includes("figura 8") || combined.includes("solicitud") || combined.includes("extracciones") || combined.includes("historial de solicitudes")) {
    return path.join(SCREENSHOTS_DIR, "fig06_exportacion_logs_modal.png");
  }
  if (combined.includes("figura 9") || combined.includes("aprobación") || combined.includes("gobernanza móvil") || combined.includes("notificación")) {
    return path.join(SCREENSHOTS_DIR, "fig09_analista_logs_pdf.png");
  }
  if (combined.includes("figura 10") || combined.includes("consultor") || combined.includes("bóveda")) {
    return path.join(SCREENSHOTS_DIR, "fig08_consultor_cti_boveda.png");
  }
  if (combined.includes("figura 11") || combined.includes("directivo") || combined.includes("resumen")) {
    return path.join(SCREENSHOTS_DIR, "fig10_directivo_resumen.png");
  }
  return null;
}

function buildFigurePlaceholderBox(placeholderText) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [
      new TableRow({
        cantSplit: true,
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: "F8FAFC", type: ShadingType.CLEAR, color: "auto" },
            borders: {
              top: B_DASHED_PLACEHOLDER,
              bottom: B_DASHED_PLACEHOLDER,
              left: B_DASHED_PLACEHOLDER,
              right: B_DASHED_PLACEHOLDER,
            },
            margins: { top: 280, bottom: 280, left: 200, right: 200 },
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({
                    text: `🖼️ ${placeholderText}`,
                    font: FONT,
                    bold: true,
                    size: 19,
                    color: BLUE_UDEC,
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

// ---------------------------------------------------------------------------
// MOTOR PARSER DE MARKDOWN A ELEMENTOS DOCX
// ---------------------------------------------------------------------------
function convertMarkdownToDocxElements(mdContent, mode = "technical") {
  const isGold = mode === "user";
  const lines = mdContent.replace(/\r\n/g, "\n").split("\n");
  const elements = [];

  let i = 0;
  let currentSection = "";

  while (i < lines.length) {
    const rawLine = lines[i];
    const line = rawLine.trim();

    // Ignorar anclas HTML sueltas o líneas vacías
    if (!line || line.startsWith("<a id=") || line === "---") {
      i++;
      continue;
    }

    // Saltar el H1 inicial del archivo (ya está en la portada)
    if (i < 5 && line.startsWith("# ")) {
      i++;
      continue;
    }

    // Bloques de código ``` o ~~~
    if (line.startsWith("```") || line.startsWith("~~~")) {
      const fence = line.slice(0, 3);
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith(fence)) {
        codeLines.push(lines[i]);
        i++;
      }
      i++; // saltar cierre de fence
      elements.push(buildDarkCodeTable(codeLines));
      elements.push(new Paragraph({ text: "", spacing: { after: 140 } }));
      continue;
    }

    // Tablas Markdown | ... |
    if (line.startsWith("|")) {
      const tableLines = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        tableLines.push(lines[i].trim());
        i++;
      }
      if (tableLines.length >= 2) {
        const parseRow = (rStr) =>
          rStr
            .replace(/^\|/, "")
            .replace(/\|$/, "")
            .split("|")
            .map((c) => c.trim());

        const headers = parseRow(tableLines[0]);
        const dataRows = tableLines
          .slice(2)
          .filter((l) => !/^\|?[\s:-]+\|/.test(l))
          .map(parseRow);

        const firstHeader = (headers[0] || "").toLowerCase();

        // Omitir la tabla de metadatos de portada (ya renderizada en la Portada y Encabezado UDEC)
        if (firstHeader.includes("identificación") || firstHeader.includes("campo institucional") || firstHeader === "campo") {
          continue;
        }

        if (currentSection.includes("REGISTRO DE CAMBIOS")) {
          elements.push(buildGovernanceBannerTable("REGISTRO DE CAMBIOS", headers, [1600, 2400, 5360], dataRows));
          elements.push(new Paragraph({ text: "", spacing: { after: 280 } }));
        } else if (currentSection.includes("CONTROL DEL DOCUMENTO")) {
          elements.push(buildGovernanceBannerTable("CONTROL DEL DOCUMENTO", headers, [1400, 3360, 2300, 2300], dataRows));
          elements.push(new Paragraph({ children: [new PageBreak()] }));
        } else if (firstHeader.includes("nombre del campo")) {
          elements.push(buildMinimalistDictionaryTable(headers, dataRows));
          elements.push(new Paragraph({ text: "", spacing: { after: 220 } }));
        } else {
          elements.push(buildStandardGridTable(headers, dataRows, isGold));
          elements.push(new Paragraph({ text: "", spacing: { after: 200 } }));
        }
      }
      continue;
    }

    // Omitir etiquetas de video HTML para el documento Word
    if (line.startsWith("<video")) {
      while (i < lines.length && !lines[i].includes("</video>")) {
        i++;
      }
      i++;
      continue;
    }

    // Imágenes estándar de Markdown: ![Alt](path)
    const imgMatch = line.match(/^!\[(.*?)\]\((.*?)\)/);
    if (imgMatch) {
      const altText = imgMatch[1];
      let imgPath = imgMatch[2];
      if (!path.isAbsolute(imgPath)) {
        const candidates = [
          path.resolve("/media/sebas/Exdrive/Workspace/honeymetrics-backend/docs", imgPath),
          path.resolve(SCREENSHOTS_DIR, path.basename(imgPath)),
          path.resolve(ENTREGABLES_DIR, imgPath)
        ];
        for (const c of candidates) {
          if (fs.existsSync(c)) {
            imgPath = c;
            break;
          }
        }
      }
      if (fs.existsSync(imgPath)) {
        elements.push(buildRealImageParagraph(imgPath));
      } else {
        elements.push(buildFigurePlaceholderBox(altText));
      }
      i++;
      continue;
    }

    // Marcadores de Figuras StarUML o Capturas
    if (line.startsWith("[FIGURA PENDIENTE:") || line.startsWith("[CAPTURA PENDIENTE:") || line.startsWith("[Captura ")) {
      const placeholderText = line.slice(1, -1);
      const nextLine = lines[i + 1] || "";
      const resolvedImg = resolvePlaceholderToImage(placeholderText, nextLine);
      if (resolvedImg && fs.existsSync(resolvedImg)) {
        elements.push(buildRealImageParagraph(resolvedImg));
      } else {
        elements.push(buildFigurePlaceholderBox(placeholderText));
      }
      elements.push(new Paragraph({ text: "", spacing: { after: 80 } }));
      i++;
      continue;
    }

    // Títulos H1 / H2 / H3 / H4
    const headingMatch = line.match(/^(#{1,4})\s+(.*)$/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      const titleText = headingMatch[2].trim();
      currentSection = titleText.toUpperCase();

      // Los títulos REGISTRO DE CAMBIOS y CONTROL DEL DOCUMENTO ya van dentro del banner gris de su tabla
      if (currentSection === "REGISTRO DE CAMBIOS" || currentSection === "CONTROL DEL DOCUMENTO") {
        i++;
        continue;
      }

      if (level === 2 && titleText.toLowerCase() === "índice") {
        elements.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 120, after: 240 },
            children: [
              new TextRun({
                text: "TABLA DE CONTENIDO",
                font: FONT,
                bold: true,
                size: 24,
                color: isGold ? GOLD_TITLE : BLUE_UDEC,
              }),
            ],
          })
        );
        i++;
        continue;
      }

      if (level <= 2) {
        elements.push(
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            keepNext: true,
            border: isGold ? { bottom: B_GOLD_SOLID } : undefined,
            spacing: { before: 340, after: 180 },
            children: [
              new TextRun({
                text: titleText.toUpperCase(),
                font: FONT,
                bold: true,
                size: 30,
                color: isGold ? GOLD_TITLE : BLUE_UDEC,
              }),
            ],
          })
        );
      } else if (level === 3) {
        const isTableTitle = titleText.startsWith("Tabla:");
        elements.push(
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            keepNext: true,
            border: isGold ? { left: B_GOLD_THICK_LEFT } : undefined,
            indent: isGold ? { left: 140 } : undefined,
            spacing: { before: 280, after: 120 },
            children: [
              new TextRun({
                text: isTableTitle ? titleText.replace(/`/g, "") : titleText,
                font: FONT,
                bold: !isTableTitle,
                size: isTableTitle ? 28 : 24,
                color: isTableTitle ? "000000" : isGold ? GOLD_TITLE : BLUE_UDEC,
              }),
            ],
          })
        );
      } else {
        elements.push(
          new Paragraph({
            heading: HeadingLevel.HEADING_3,
            keepNext: true,
            spacing: { before: 200, after: 100 },
            children: [
              new TextRun({
                text: titleText,
                font: FONT,
                bold: true,
                size: 22,
                color: isGold ? GOLD_DARK : "1F4E79",
              }),
            ],
          })
        );
      }
      i++;
      continue;
    }

    // Notas y Blockquotes (> ... o ⚡ Nota:)
    if (line.startsWith("> ") || line.startsWith("⚡ Nota:")) {
      const cleanNote = line.replace(/^>\s*/, "");
      elements.push(buildGoldNoteBox(cleanNote));
      elements.push(new Paragraph({ text: "", spacing: { after: 140 } }));
      i++;
      continue;
    }

    // Listas con viñetas (- o * )
    if (/^[-*]\s+/.test(line)) {
      const itemText = line.replace(/^[-*]\s+/, "").replace(/\[([^\]]+)\]\(#[^)]+\)/g, "$1");
      elements.push(
        new Paragraph({
          spacing: { line: 276, after: 100 },
          indent: { left: 540, hanging: 260 },
          children: [
            new TextRun({ text: "•  ", font: FONT, bold: true, size: 21, color: isGold ? GOLD_ACCENT : BLUE_UDEC }),
            ...parseInlineRuns(itemText, { size: 21 }),
          ],
        })
      );
      i++;
      continue;
    }

    // Listas numeradas (1. , 2. )
    const numMatch = line.match(/^(\d+)\.\s+(.*)$/);
    if (numMatch) {
      elements.push(
        new Paragraph({
          spacing: { line: 276, after: 100 },
          indent: { left: 540, hanging: 300 },
          children: [
            new TextRun({ text: `${numMatch[1]}. `, font: FONT, bold: true, size: 21, color: isGold ? GOLD_DARK : "000000" }),
            ...parseInlineRuns(numMatch[2], { size: 21 }),
          ],
        })
      );
      i++;
      continue;
    }

    // Párrafo normal o pie de figura (*Figura X...*)
    const isCaption = line.startsWith("*Figura ") && line.endsWith("*");
    elements.push(
      new Paragraph({
        alignment: isCaption ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { line: 280, after: 160 },
        children: parseInlineRuns(line, { size: isCaption ? 19 : 21 }),
      })
    );
    i++;
  }

  return elements;
}

// ---------------------------------------------------------------------------
// ENSAMBLADOR DE LOS 3 DOCUMENTOS DOCX
// ---------------------------------------------------------------------------
async function compileAllDeliverables() {
  const deliverables = [
    {
      mdFile: "01_Manual_Tecnico_HoneyMetrics_v2.md",
      docxFile: "01_Manual_Tecnico_HoneyMetrics_v2.docx",
      docTitle: "MANUAL TÉCNICO",
      mode: "technical",
    },
    {
      mdFile: "02_Diccionario_Datos_HoneyMetrics_v2.md",
      docxFile: "02_Diccionario_Datos_HoneyMetrics_v2.docx",
      docTitle: "DICCIONARIO DE DATOS DEL SISTEMA",
      mode: "dictionary",
    },
    {
      mdFile: "03_Manual_Usuario_HoneyMetrics_v2.md",
      docxFile: "03_Manual_Usuario_HoneyMetrics_v2.docx",
      docTitle: "MANUAL DE USUARIO",
      mode: "user",
    },
    {
      mdFile: "04_Manual_Tecnico_Frontend_HoneyMetrics_v2.md",
      docxFile: "04_Manual_Tecnico_Frontend_HoneyMetrics_v2.docx",
      docTitle: "MANUAL TÉCNICO FRONTEND",
      mode: "technical",
    },
  ];

  for (const item of deliverables) {
    const mdPath = path.join(ENTREGABLES_DIR, item.mdFile);
    if (!fs.existsSync(mdPath)) {
      console.error(`No se encontró: ${mdPath}`);
      continue;
    }

    const mdContent = fs.readFileSync(mdPath, "utf-8");
    const bodyElements = convertMarkdownToDocxElements(mdContent, item.mode);

    let coverElements = [];
    if (item.mode === "technical") {
      coverElements = buildTechnicalCoverPage(item.docTitle);
    } else if (item.mode === "user") {
      coverElements = buildUserManualGoldCoverPage();
    } else {
      coverElements = buildDataDictHeaderBlock();
    }

    const headerObj =
      item.mode === "user"
        ? buildUserManualGoldHeader()
        : buildUdecBoxHeader({
            docTitle: item.docTitle,
            projectName: "HONEYMETRICS",
            dateStr: "2026-10-23",
            versionStr: "2.0.0",
          });

    const doc = new Document({
      creator: "Johan Sebastián Posada Beltrán",
      title: `${item.docTitle} — HoneyMetrics v2.0`,
      sections: [
        {
          properties: {
            titlePage: item.mode !== "dictionary",
            page: {
              size: { width: 12240, height: 15840 }, // Carta (Letter)
              margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
            },
          },
          headers: {
            first: new Header({ children: [] }),
            default: headerObj,
          },
          footers: {
            first: new Footer({ children: [] }),
            default: buildSimpleFooter(item.mode === "user"),
          },
          children: [...coverElements, ...bodyElements],
        },
      ],
    });

    const outPath = path.join(ENTREGABLES_DIR, item.docxFile);
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outPath, buffer);
    console.log(`✅ Generado con éxito: ${outPath} (${(buffer.length / 1024).toFixed(1)} KB)`);
  }
}

compileAllDeliverables().catch((err) => {
  console.error(err);
  process.exit(1);
});
