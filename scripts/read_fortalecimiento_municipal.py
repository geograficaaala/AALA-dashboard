import json
import os
from pathlib import Path

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

RAW_DIR = Path("data_raw/fortalecimiento_municipal")
RAW_DIR.mkdir(parents=True, exist_ok=True)


TAB_CONFIG = {
    # ─────────────────────────────────────────────
    # Hojas base originales
    # ─────────────────────────────────────────────
    "encabezado_raw.csv": {
        "sheet": "01_Encabezado",
        "range": "A4:C30",
        "mode": "fixed_header",
        "header": ["campo", "valor", "nota"],
        "optional": False,
    },
    "modulos_raw.csv": {
        "sheet": "02_Modulos",
        "range": "A4:C30",
        "mode": "fixed_header",
        "header": ["modulo", "activo_este_mes", "nota"],
        "optional": False,
    },
    "capacitaciones_raw.csv": {
        "sheet": "03_Capacitaciones",
        "range": "A2:AZ1200",
        "mode": "first_row_header",
        "optional": False,
    },
    "asistencias_raw.csv": {
        "sheet": "04_Asistencias",
        "range": "A2:AZ1200",
        "mode": "first_row_header",
        "optional": False,
    },
    "estudios_raw.csv": {
        "sheet": "05_Estudios",
        "range": "A2:AZ1200",
        "mode": "first_row_header",
        "optional": False,
    },
    "pirdes_raw.csv": {
        "sheet": "06_PIRDES",
        "range": "A2:AZ1200",
        "mode": "first_row_header",
        "optional": False,
    },
    "reuniones_raw.csv": {
        "sheet": "07_Reuniones",
        "range": "A2:AZ1200",
        "mode": "first_row_header",
        "optional": False,
    },

    # ─────────────────────────────────────────────
    # Nuevas hojas de validación
    # Fila 1 = título
    # Fila 2 = encabezados
    # Fila 3+ = datos
    # Por eso se leen desde A2
    # ─────────────────────────────────────────────
    "capacitaciones_validacion_raw.csv": {
        "sheet": "03_Capacitaciones_VALIDACION",
        "range": "A2:AZ1500",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "fecha",
            "municipio",
            "descripcion",
            "eje_validado",
            "cuenta_index_especifico",
            "cuenta_index_general",
            "indicador_destino",
            "estado_validacion",
            "nivel_avance",
            "motivo_no_cuenta",
            "evidencia_usada",
            "observacion_coordinador",
        ],
    },
    "asistencias_validacion_raw.csv": {
        "sheet": "04_Asistencias_VALIDACION",
        "range": "A2:AZ1500",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "fecha",
            "municipio",
            "descripcion",
            "sector_validado",
            "tipo_asistencia_validada",
            "cuenta_index_especifico",
            "cuenta_index_general",
            "indicador_destino",
            "estado_validacion",
            "nivel_avance",
            "clave_unica_validada",
            "motivo_no_cuenta",
            "evidencia_usada",
            "observacion_coordinador",
        ],
    },
    "estudios_validacion_raw.csv": {
        "sheet": "05_Estudios_VALIDACION",
        "range": "A2:AZ1500",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "fecha",
            "municipio",
            "descripcion",
            "tipo_estudio_validado",
            "sector_validado",
            "estado_estudio_validado",
            "cuenta_index_especifico",
            "cuenta_index_general",
            "indicador_destino",
            "estado_validacion",
            "nivel_avance",
            "clave_unica_validada",
            "motivo_no_cuenta",
            "evidencia_usada",
            "observacion_coordinador",
        ],
    },
    "pirdes_validacion_raw.csv": {
        "sheet": "06_PIRDES_VALIDACION",
        "range": "A2:AZ1500",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "fecha",
            "municipio",
            "descripcion",
            "estado_pirdes_validado",
            "cuenta_index_especifico",
            "cuenta_index_general",
            "indicador_destino",
            "estado_validacion",
            "nivel_avance",
            "clave_unica_validada",
            "motivo_no_cuenta",
            "evidencia_usada",
            "observacion_coordinador",
        ],
    },
    "reuniones_validacion_raw.csv": {
        "sheet": "07_Reuniones_VALIDACION",
        "range": "A2:AZ1500",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "fecha",
            "municipio",
            "descripcion",
            "tipo_reunion_validado",
            "cuenta_index_especifico",
            "cuenta_index_general",
            "indicador_destino",
            "estado_validacion",
            "nivel_avance",
            "clave_unica_validada",
            "motivo_no_cuenta",
            "evidencia_usada",
            "observacion_coordinador",
        ],
    },
    "capacidad_instalada_validacion_raw.csv": {
        "sheet": "08_Capacidad_Instalada_VALIDACION",
        "sheet_aliases": [
            "08_Capacidad_Instalada_VALIDACI",
            "08_Capacidad_Instalada_VALIDAC",
        ],
        "range": "A2:AZ1500",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "municipio",
            "SNIP_validado",
            "SIG_validado",
            "recoleccion_digital_validada",
            "cumplimiento_legal_validado",
            "estado_capacidad_instalada",
            "cuenta_index_general",
            "indicador_destino",
            "estado_validacion",
            "fecha_validacion",
            "responsable_validacion",
            "evidencia_usada",
            "observacion_coordinador",
        ],
    },

    # ─────────────────────────────────────────────
    # Salidas creadas por Apps Script
    # ─────────────────────────────────────────────
    "indicadores_resumen_validado_raw.csv": {
        "sheet": "99_Indicadores_Resumen",
        "range": "A1:Z200",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "indicador_id",
            "dashboard",
            "indicador",
            "valor_validado",
            "meta",
            "unidad",
            "criterio_de_conteo",
        ],
    },
    "programa_card_raw.csv": {
        "sheet": "programa_card",
        "range": "A1:Z200",
        "mode": "first_row_header",
        "optional": True,
        "empty_header": [
            "programa_id",
            "indicador_id",
            "label",
            "valor_acumulado",
            "meta_anual",
            "unidad",
            "pct_avance",
            "orden",
            "estado",
        ],
    },
}


def get_service():
    creds_info = json.loads(os.environ["GOOGLE_CREDS_JSON"])
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def quote_sheet_name(sheet_name: str) -> str:
    safe_name = sheet_name.replace("'", "''")
    return f"'{safe_name}'"


def build_range(sheet_name: str, cell_range: str) -> str:
    return f"{quote_sheet_name(sheet_name)}!{cell_range}"


def get_sheet_names(service, spreadsheet_id: str) -> list[str]:
    result = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, fields="sheets.properties.title")
        .execute()
    )
    return [
        sheet["properties"]["title"]
        for sheet in result.get("sheets", [])
        if "properties" in sheet and "title" in sheet["properties"]
    ]


def resolve_sheet_name(cfg: dict, available_sheets: list[str]) -> str | None:
    preferred = cfg["sheet"]
    aliases = cfg.get("sheet_aliases", [])

    candidates = [preferred] + aliases

    for candidate in candidates:
        if candidate in available_sheets:
            return candidate

    normalized_available = {normalize_text(name): name for name in available_sheets}

    for candidate in candidates:
        normalized_candidate = normalize_text(candidate)
        if normalized_candidate in normalized_available:
            return normalized_available[normalized_candidate]

    return None


def read_range(service, spreadsheet_id: str, range_name: str):
    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueRenderOption="UNFORMATTED_VALUE",
            dateTimeRenderOption="SERIAL_NUMBER",
        )
        .execute()
    )
    return result.get("values", [])


def normalize_text(value) -> str:
    return str(value or "").strip().lower()


def normalize_headers(raw_headers):
    seen = {}
    headers = []

    for i, value in enumerate(raw_headers, start=1):
        name = str(value).strip() if value is not None else ""

        if not name:
            name = f"col_{i}"

        count = seen.get(name, 0) + 1
        seen[name] = count

        headers.append(name if count == 1 else f"{name}__{count}")

    return headers


def write_empty_csv(output_path: Path, header: list[str] | None = None) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(columns=header or []).to_csv(output_path, index=False)
    return 0


def save_rows(rows, output_path: Path, mode: str, fixed_header=None, empty_header=None):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        return write_empty_csv(output_path, empty_header or fixed_header)

    if mode == "fixed_header":
        headers = fixed_header or ["col_1", "col_2", "col_3"]
        data = rows

    elif mode == "first_row_header":
        headers = normalize_headers(rows[0])
        data = rows[1:]

    else:
        raise ValueError(f"Modo no soportado: {mode}")

    max_cols = max(len(headers), max((len(r) for r in data), default=0))

    if len(headers) < max_cols:
        headers = headers + [
            f"col_{i}"
            for i in range(len(headers) + 1, max_cols + 1)
        ]

    normalized = []

    for row in data:
        row = ["" if v is None else str(v) for v in row]

        if len(row) < max_cols:
            row += [""] * (max_cols - len(row))
        elif len(row) > max_cols:
            row = row[:max_cols]

        normalized.append(row)

    df = pd.DataFrame(normalized, columns=headers)

    # Evita filas completamente vacías.
    if not df.empty:
        df = df.dropna(how="all")
        df = df.loc[~(df.astype(str).apply(lambda col: col.str.strip()).eq("").all(axis=1))]

    df.to_csv(output_path, index=False)
    return len(df)


def main():
    service = get_service()
    spreadsheet_id = os.environ["SHEET_ID_FORTALECIMIENTO_MUNICIPAL"]

    available_sheets = get_sheet_names(service, spreadsheet_id)

    manifest = {
        "spreadsheet_id": spreadsheet_id,
        "available_sheets": available_sheets,
        "files": [],
        "warnings": [],
    }

    for filename, cfg in TAB_CONFIG.items():
        output = RAW_DIR / filename

        resolved_sheet = resolve_sheet_name(cfg, available_sheets)

        if not resolved_sheet:
            message = f"No se encontró la hoja '{cfg['sheet']}' para {filename}."

            if cfg.get("optional", False):
                count = write_empty_csv(output, cfg.get("empty_header") or cfg.get("header"))
                manifest["warnings"].append(message)
                manifest["files"].append(
                    {
                        "filename": filename,
                        "sheet": cfg["sheet"],
                        "resolved_sheet": None,
                        "range": None,
                        "rows_saved": count,
                        "status": "missing_optional_sheet",
                    }
                )
                print(f"[AVISO] {message} CSV vacío creado.")
                continue

            raise RuntimeError(message)

        range_name = build_range(resolved_sheet, cfg["range"])

        try:
            rows = read_range(service, spreadsheet_id, range_name)

        except HttpError as exc:
            message = f"No se pudo leer rango {range_name}: {exc}"

            if cfg.get("optional", False):
                count = write_empty_csv(output, cfg.get("empty_header") or cfg.get("header"))
                manifest["warnings"].append(message)
                manifest["files"].append(
                    {
                        "filename": filename,
                        "sheet": cfg["sheet"],
                        "resolved_sheet": resolved_sheet,
                        "range": range_name,
                        "rows_saved": count,
                        "status": "read_error_optional_sheet",
                    }
                )
                print(f"[AVISO] {message} CSV vacío creado.")
                continue

            raise

        count = save_rows(
            rows,
            output,
            mode=cfg["mode"],
            fixed_header=cfg.get("header"),
            empty_header=cfg.get("empty_header"),
        )

        manifest["files"].append(
            {
                "filename": filename,
                "sheet": cfg["sheet"],
                "resolved_sheet": resolved_sheet,
                "range": range_name,
                "rows_saved": count,
                "status": "ok",
            }
        )

        print(f"{filename}: {count} filas guardadas desde {range_name}")

    (RAW_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Lectura de Google Sheets completada.")


if __name__ == "__main__":
    main()
