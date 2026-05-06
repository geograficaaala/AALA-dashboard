from __future__ import annotations
from pathlib import Path
import unicodedata
import pandas as pd

PROGRAM_ID = "fortalecimiento_municipal"
PROGRAM_NAME = "Fortalecimiento municipal"

RAW_DIR = Path("data_raw/fortalecimiento_municipal")
OUT_DIR = Path("data_processed/fortalecimiento_municipal")
DOCS_DIR = Path("docs/data/fortalecimiento_municipal")
OUT_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

MONTH_NAMES_ES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

PRIMARY_METAS = {
    "municipios_capacitacion_nucleo": 15.0,
    "personas_capacitadas_nucleo": 75.0,
    "asistencias_priorizadas_proxy": 3.0,
    "estudios_rs_comercial_mercados": 2.0,
    "pirdes_implementados": 5.0,
    "reuniones_codema": 10.0,
    "mesas_tecnicas_departamentales": 2.0,
}

INDICATOR_LABELS = {
    "municipios_capacitacion_nucleo": ("Municipios alcanzados por capacitaciones núcleo", "municipios", "primario"),
    "personas_capacitadas_nucleo": ("Personas capacitadas en temas núcleo", "personas", "primario"),
    "asistencias_priorizadas_proxy": ("Asistencias técnicas priorizadas de agua y saneamiento (proxy operativo)", "proyectos", "primario"),
    "estudios_rs_comercial_mercados": ("Estudios de residuos sólidos sector comercial / mercados finalizados", "estudios", "primario"),
    "pirdes_implementados": ("PIRDES implementados", "municipios", "primario"),
    "reuniones_codema": ("Reuniones del eje de agua y saneamiento / CODEMA", "reuniones", "primario"),
    "mesas_tecnicas_departamentales": ("Mesas técnicas departamentales de agua y saneamiento", "mesas", "primario"),
    "eventos_capacitacion_total": ("Eventos de capacitación", "eventos", "complementario"),
    "personas_capacitadas_total": ("Personas capacitadas totales", "personas", "complementario"),
    "tecnicos_capacitados_total": ("Técnicos capacitados", "personas", "complementario"),
    "operarios_capacitados_total": ("Operarios capacitados", "personas", "complementario"),
    "otro_personal_capacitado_total": ("Otro personal capacitado", "personas", "complementario"),
    "asistencias_nuevas_total": ("Asistencias nuevas totales", "asistencias", "complementario"),
    "estudios_finalizados_total": ("Estudios finalizados totales", "estudios", "complementario"),
    "reuniones_totales": ("Reuniones totales", "reuniones", "complementario"),
    "mesas_tecnicas_municipales": ("Mesas técnicas municipales", "mesas", "complementario"),
}

CORE_THEME_ALIAS_RULES = [
    ("SNIP · Sistema Nacional de Inversión Pública", ["snip", "inversion publica", "inversión pública", "sistema nacional de inversion publica", "sistema nacional de inversión pública"]),
    ("SIG · Sistemas de Información Geográfica", ["sig", "informacion geografica", "información geográfica", "geografica", "geográfica", "gis", "cartografia", "cartografía", "georrefer"]),
    ("Recolección digital de datos", ["recoleccion digital", "recolección digital", "levantamiento digital", "captura digital", "kobo", "encuesta digital", "datos digitales"]),
    ("Cumplimiento legal ambiental y saneamiento", ["cumplimiento legal", "legal ambiental", "saneamiento ambiental", "agua y saneamiento", "ambiental", "normativa ambiental"]),
]

CANONICAL_CORE_THEMES = {label for label, _ in CORE_THEME_ALIAS_RULES}

WATER_SANITATION_SECTORS = {
    "Alcantarillado",
    "Tratamiento de aguas residuales",
    "Desechos sólidos",
    "Agua potable",
}

PRIMARY_INDICATOR_ORDER = [
    "municipios_capacitacion_nucleo",
    "personas_capacitadas_nucleo",
    "asistencias_priorizadas_proxy",
    "estudios_rs_comercial_mercados",
    "pirdes_implementados",
    "reuniones_codema",
    "mesas_tecnicas_departamentales",
]

MODULE_FILE_MAP = {
    "capacitaciones": "capacitaciones_raw.csv",
    "asistencias": "asistencias_raw.csv",
    "estudios": "estudios_raw.csv",
    "pirdes": "pirdes_raw.csv",
    "reuniones": "reuniones_raw.csv",
}


# ─────────────────────────────────────────────
# Nueva arquitectura validada por coordinador
# ─────────────────────────────────────────────

VALIDATED_SUMMARY_RAW = "indicadores_resumen_validado_raw.csv"
PROGRAM_CARD_RAW = "programa_card_raw.csv"

VALIDATED_SUMMARY_COLUMNS = [
    "indicador_id",
    "dashboard",
    "indicador",
    "valor_validado",
    "meta",
    "unidad",
    "criterio_de_conteo",
]

PROGRAM_CARD_COLUMNS = [
    "programa_id",
    "indicador_id",
    "label",
    "valor_acumulado",
    "meta_anual",
    "unidad",
    "pct_avance",
    "orden",
    "estado",
]

DEFAULT_VALIDATED_INDICATORS = [
    {
        "indicador_id": "FM_GEN_01",
        "dashboard": "index_general",
        "indicador": "Municipalidades con capacidad instalada",
        "valor_validado": 0,
        "meta": 15,
        "unidad": "municipalidades",
        "criterio_de_conteo": "Solo municipios con capacidad instalada confirmada.",
    },
    {
        "indicador_id": "FM_GEN_02",
        "dashboard": "index_general",
        "indicador": "Estudios de caracterización de desechos y residuos sólidos y/o aguas residuales",
        "valor_validado": 0,
        "meta": 6,
        "unidad": "estudios",
        "criterio_de_conteo": "Solo estudios confirmados con clave única validada.",
    },
    {
        "indicador_id": "FM_GEN_03",
        "dashboard": "index_general",
        "indicador": "PIRDES Municipales",
        "valor_validado": 0,
        "meta": 5,
        "unidad": "planes integrales",
        "criterio_de_conteo": "Solo PIRDES confirmados con clave única validada.",
    },
    {
        "indicador_id": "FM_GEN_04",
        "dashboard": "index_general",
        "indicador": "Asistencias técnicas municipales en aguas residuales",
        "valor_validado": 0,
        "meta": 20,
        "unidad": "asistencias técnicas",
        "criterio_de_conteo": "Solo asistencias confirmadas como aguas residuales.",
    },
    {
        "indicador_id": "FM_SPEC_01",
        "dashboard": "index_especifico",
        "indicador": "Personal municipal capacitado por eje temático",
        "valor_validado": 0,
        "meta": 4,
        "unidad": "ejes cumplidos",
        "criterio_de_conteo": "Registros confirmados para capacitación por eje.",
    },
    {
        "indicador_id": "FM_SPEC_02",
        "dashboard": "index_especifico",
        "indicador": "Estudios de caracterización finalizados",
        "valor_validado": 0,
        "meta": 6,
        "unidad": "estudios",
        "criterio_de_conteo": "Estudios confirmados para el tablero específico.",
    },
    {
        "indicador_id": "FM_SPEC_03",
        "dashboard": "index_especifico",
        "indicador": "PIRDES finalizados / implementados",
        "valor_validado": 0,
        "meta": 5,
        "unidad": "PIRDES",
        "criterio_de_conteo": "PIRDES confirmados para el tablero específico.",
    },
    {
        "indicador_id": "FM_SPEC_04",
        "dashboard": "index_especifico",
        "indicador": "Reuniones CODEMA / eje agua y saneamiento",
        "valor_validado": 0,
        "meta": 10,
        "unidad": "reuniones",
        "criterio_de_conteo": "Reuniones CODEMA confirmadas.",
    },
    {
        "indicador_id": "FM_SPEC_05",
        "dashboard": "index_especifico",
        "indicador": "Asistencias técnicas municipales en aguas residuales",
        "valor_validado": 0,
        "meta": 20,
        "unidad": "asistencias técnicas",
        "criterio_de_conteo": "Asistencias confirmadas para el tablero específico.",
    },
    {
        "indicador_id": "FM_SPEC_06",
        "dashboard": "index_especifico",
        "indicador": "Municipalidades con avance hacia capacidad instalada",
        "valor_validado": 0,
        "meta": 15,
        "unidad": "municipalidades",
        "criterio_de_conteo": "Municipios con avance confirmado hacia capacidad instalada.",
    },
]

GENERAL_ORDER = {
    "FM_GEN_01": 1,
    "FM_GEN_02": 2,
    "FM_GEN_03": 3,
    "FM_GEN_04": 4,
}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, dtype=str).fillna("")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def parse_bool(value) -> bool:
    if value is None:
        return False
    s = str(value).strip().lower()
    return s in {"sí", "si", "true", "1", "yes", "y", "x", "verdadero"}


def parse_number(value):
    if value is None:
        return pd.NA
    s = str(value).strip().replace(" ", "")
    if s == "" or s.lower() in {"nan", "na", "n/a", "-"}:
        return pd.NA
    try:
        if "," in s and "." in s:
            if s.rfind(".") > s.rfind(","):
                s = s.replace(",", "")
            else:
                s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".")
        return float(s)
    except ValueError:
        return pd.NA


def parse_date_any(value):
    if value is None:
        return pd.NaT
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "na", "n/a"}:
        return pd.NaT

    num = parse_number(s)
    if pd.notna(num):
        try:
            n = float(num)
            if n > 20000:
                return pd.Timestamp("1899-12-30") + pd.to_timedelta(n, unit="D")
        except Exception:
            pass

    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        dt = pd.to_datetime(s, errors="coerce")
        if pd.notna(dt):
            return dt

    dt = pd.to_datetime(s, errors="coerce", dayfirst=True)
    if pd.notna(dt):
        return dt
    dt = pd.to_datetime(s, errors="coerce", dayfirst=False)
    if pd.notna(dt):
        return dt
    return pd.NaT


def normalize_text(value) -> str:
    return " ".join(str(value).strip().split()) if value is not None else ""


def slug_text(value) -> str:
    text = normalize_text(value).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text


def month_name(month_num: int) -> str:
    return MONTH_NAMES_ES.get(int(month_num), f"Mes {month_num}")


def safe_sum(series) -> float:
    if series is None:
        return 0.0
    return float(pd.to_numeric(series, errors="coerce").fillna(0).sum())


def semaforo_from_pct(pct) -> str:
    if pd.isna(pct) or pct == 0:
        return "muted"
    if pct >= 1:
        return "green"
    if pct >= 0.85:
        return "yellow"
    return "red"


def extract_yes_columns(df: pd.DataFrame, prefix: str) -> list[str]:
    return [c for c in df.columns if str(c).startswith(prefix)]


def ensure_base_fields(df: pd.DataFrame, module_name: str) -> pd.DataFrame:
    df = df.copy()
    if "row_number" not in df.columns:
        df["row_number"] = range(1, len(df) + 1)
    df["module_name"] = module_name
    df["fecha"] = df.get("Fecha *", "").apply(parse_date_any)
    df["anio"] = df["fecha"].dt.year.astype("Int64")
    df["mes_num"] = df["fecha"].dt.month.astype("Int64")
    df["periodo"] = df["fecha"].dt.to_period("M").astype(str)
    df["mes_nombre"] = df["mes_num"].apply(lambda x: month_name(int(x)) if pd.notna(x) else "")
    df["estado_fila_norm"] = df.get("Estado fila", "").astype(str).str.strip().str.upper()
    return df


def classify_core_theme(*texts) -> list[str]:
    combined = " | ".join(normalize_text(t) for t in texts if normalize_text(t))
    combined_slug = slug_text(combined)
    hits = []
    for label, keywords in CORE_THEME_ALIAS_RULES:
        if any(keyword in combined_slug for keyword in keywords):
            hits.append(label)
    return list(dict.fromkeys(hits))


def coalesce_numeric(*values) -> float:
    for value in values:
        num = parse_number(value)
        if pd.notna(num):
            return float(num)
    return 0.0


def split_pipe_values(value: str) -> list[str]:
    if value is None:
        return []
    return [x.strip() for x in str(value).split(" | ") if x.strip()]


def build_capacitaciones() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = read_csv(RAW_DIR / MODULE_FILE_MAP["capacitaciones"])
    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    df = ensure_base_fields(df, "capacitaciones")
    muni_cols = extract_yes_columns(df, "Mun: ")
    tema_cols = extract_yes_columns(df, "Tema: ")

    df["participantes_totales"] = df.apply(
        lambda r: coalesce_numeric(
            r.get("Participantes totales *", ""),
            r.get("Subtotal categorías", ""),
        ),
        axis=1,
    )
    df["n_tecnicos"] = df.get("N° técnicos", "").apply(parse_number)
    df["n_operarios"] = df.get("N° operarios", "").apply(parse_number)
    df["n_otro_personal"] = df.get("N° otro personal", "").apply(parse_number)

    df["municipios_list"] = (
        df[muni_cols].apply(
            lambda row: [col.replace("Mun: ", "") for col, v in row.items() if parse_bool(v)],
            axis=1,
        ) if muni_cols else [[] for _ in range(len(df))]
    )

    df["temas_seleccionados"] = (
        df[tema_cols].apply(
            lambda row: [col.replace("Tema: ", "") for col, v in row.items() if parse_bool(v)],
            axis=1,
        ) if tema_cols else [[] for _ in range(len(df))]
    )

    def infer_dashboard_themes(row) -> list[str]:
        selected = row["temas_seleccionados"]
        inferred = classify_core_theme(
            row.get("Tipo de actividad *", ""),
            row.get("Observaciones", ""),
            " | ".join(selected),
        )
        clean_selected = [normalize_text(x) for x in selected if normalize_text(x)]
        if inferred:
            return list(dict.fromkeys(inferred + clean_selected))
        activity = normalize_text(row.get("Tipo de actividad *", ""))
        if clean_selected:
            return clean_selected
        if activity:
            return [activity]
        return []

    df["temas_dashboard"] = df.apply(infer_dashboard_themes, axis=1)
    df["temas_nucleo"] = df.apply(
        lambda r: classify_core_theme(
            r.get("Tipo de actividad *", ""),
            r.get("Observaciones", ""),
            " | ".join(r["temas_seleccionados"]),
        ),
        axis=1,
    )
    df["has_core_theme"] = df["temas_nucleo"].apply(lambda xs: len(xs) > 0)

    people_total = pd.to_numeric(df["participantes_totales"], errors="coerce").fillna(0)
    disaggregated_total = (
        pd.to_numeric(df["n_tecnicos"], errors="coerce").fillna(0)
        + pd.to_numeric(df["n_operarios"], errors="coerce").fillna(0)
        + pd.to_numeric(df["n_otro_personal"], errors="coerce").fillna(0)
    )
    has_people = people_total.gt(0) | disaggregated_total.gt(0)
    has_substance = (
        df.get("Tipo de actividad *", "").astype(str).str.strip().ne("")
        | df.get("Instituciones participantes", "").astype(str).str.strip().ne("")
        | df.get("Observaciones", "").astype(str).str.strip().ne("")
    )

    df["row_has_minimum_data"] = df["fecha"].notna() & has_people & has_substance
    df["row_alert_municipio_missing"] = df["row_has_minimum_data"] & df["has_core_theme"] & df["municipios_list"].apply(len).eq(0)
    df["row_alert_estado_incompleto"] = df["estado_fila_norm"].eq("INCOMPLETA")
    df["registro_valido"] = df["row_has_minimum_data"]

    detail = df[
        [
            "row_number",
            "module_name",
            "fecha",
            "anio",
            "mes_num",
            "mes_nombre",
            "periodo",
            "registro_valido",
            "estado_fila_norm",
            "row_alert_municipio_missing",
            "row_alert_estado_incompleto",
        ]
    ].copy()
    detail["modalidad"] = df.get("Modalidad *", "").astype(str)
    detail["tipo_actividad"] = df.get("Tipo de actividad *", "").astype(str)
    detail["participantes_totales"] = people_total
    detail["n_tecnicos"] = df["n_tecnicos"]
    detail["n_operarios"] = df["n_operarios"]
    detail["n_otro_personal"] = df["n_otro_personal"]
    detail["instituciones_participantes"] = df.get("Instituciones participantes", "").astype(str)
    detail["observaciones"] = df.get("Observaciones", "").astype(str)
    detail["municipios"] = df["municipios_list"].apply(lambda xs: " | ".join(xs))
    detail["temas"] = df["temas_dashboard"].apply(lambda xs: " | ".join(xs))
    detail["temas_nucleo"] = df["temas_nucleo"].apply(lambda xs: " | ".join(xs))
    detail["has_core_theme"] = df["has_core_theme"]

    tema_rows = []
    muni_rows = []

    valid = df[df["registro_valido"]].copy()
    for _, row in valid.iterrows():
        themes_for_row = row["temas_dashboard"] or row["temas_nucleo"]
        if not themes_for_row:
            themes_for_row = [normalize_text(row.get("Tipo de actividad *", ""))] if normalize_text(row.get("Tipo de actividad *", "")) else []
        for tema in themes_for_row:
            tema_rows.append(
                {
                    "programa_id": PROGRAM_ID,
                    "periodo": row["periodo"],
                    "anio": row["anio"],
                    "mes_num": row["mes_num"],
                    "mes_nombre": row["mes_nombre"],
                    "tema": tema,
                    "es_tema_nucleo": tema in CANONICAL_CORE_THEMES,
                    "eventos": 1,
                    "personas": float(row["participantes_totales"] or 0),
                }
            )
        for municipio in row["municipios_list"]:
            muni_rows.append(
                {
                    "programa_id": PROGRAM_ID,
                    "periodo": row["periodo"],
                    "anio": row["anio"],
                    "mes_num": row["mes_num"],
                    "mes_nombre": row["mes_nombre"],
                    "municipio": municipio,
                    "eventos": 1,
                    "capacitacion_nucleo": bool(row["has_core_theme"]),
                }
            )

    tema_df = pd.DataFrame(tema_rows)
    if not tema_df.empty:
        tema_df = tema_df.groupby(
            ["programa_id", "periodo", "anio", "mes_num", "mes_nombre", "tema", "es_tema_nucleo"],
            dropna=False,
            as_index=False,
        )[["eventos", "personas"]].sum()

    muni_df = pd.DataFrame(muni_rows)
    if not muni_df.empty:
        muni_df = muni_df.groupby(
            ["programa_id", "periodo", "anio", "mes_num", "mes_nombre", "municipio", "capacitacion_nucleo"],
            dropna=False,
            as_index=False,
        )["eventos"].sum()

    return detail, tema_df, muni_df


def build_asistencias() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_csv(RAW_DIR / MODULE_FILE_MAP["asistencias"])
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = ensure_base_fields(df, "asistencias")
    sector_cols = extract_yes_columns(df, "Sector: ")

    df["nueva_asistencia_auto"] = pd.to_numeric(df.get("Nueva asistencia (auto)", "").apply(parse_number), errors="coerce").fillna(0)
    df["es_nueva_asistencia"] = df.get("¿Cuenta como nueva asistencia? *", "").apply(parse_bool) | df["nueva_asistencia_auto"].gt(0)
    df["sectores"] = (
        df[sector_cols].apply(
            lambda row: [col.replace("Sector: ", "") for col, v in row.items() if parse_bool(v)],
            axis=1,
        ) if sector_cols else [[] for _ in range(len(df))]
    )

    df["row_has_minimum_data"] = (
        df["fecha"].notna()
        & df.get("Municipio *", "").astype(str).str.strip().ne("")
        & (
            df.get("Código corto del proyecto *", "").astype(str).str.strip().ne("")
            | df.get("Nombre corto del proyecto", "").astype(str).str.strip().ne("")
            | df.get("Tipo de asistencia / actividad *", "").astype(str).str.strip().ne("")
            | df.get("Resultado o avance del mes", "").astype(str).str.strip().ne("")
        )
    )
    df["registro_valido"] = df["row_has_minimum_data"]
    df["row_alert_estado_incompleto"] = df["estado_fila_norm"].eq("INCOMPLETA")

    codede_cols = [c for c in df.columns if "CODEDE" in str(c).upper()]
    codede_flag = df[codede_cols[0]].apply(parse_bool) if codede_cols else pd.Series(False, index=df.index)

    line_slug = df.get("Línea / enfoque *", "").astype(str).apply(slug_text)
    type_slug = df.get("Tipo de asistencia / actividad *", "").astype(str).apply(slug_text)

    df["proxy_priorizada_agua_saneamiento"] = (
        df["es_nueva_asistencia"]
        & (
            df["sectores"].apply(lambda xs: any(s in WATER_SANITATION_SECTORS for s in xs))
            | line_slug.str.contains("agua|saneamiento|residuos|alcantarillado|tratamiento", regex=True, na=False)
            | type_slug.str.contains("agua|saneamiento|residuos|alcantarillado|tratamiento", regex=True, na=False)
        )
    )
    df["cuenta_indicador_asistencia"] = codede_flag | df["proxy_priorizada_agua_saneamiento"]

    detail = df[
        ["row_number", "module_name", "fecha", "anio", "mes_num", "mes_nombre", "periodo", "registro_valido", "estado_fila_norm", "row_alert_estado_incompleto"]
    ].copy()
    detail["municipio"] = df.get("Municipio *", "").astype(str)
    detail["proyecto_codigo"] = df.get("Código corto del proyecto *", "").astype(str)
    detail["proyecto_nombre"] = df.get("Nombre corto del proyecto", "").astype(str)
    detail["tipo_asistencia"] = df.get("Tipo de asistencia / actividad *", "").astype(str)
    detail["linea_enfoque"] = df.get("Línea / enfoque *", "").astype(str)
    detail["es_nueva_asistencia"] = df["es_nueva_asistencia"]
    detail["cuenta_indicador_asistencia"] = df["cuenta_indicador_asistencia"]
    detail["sectores"] = df["sectores"].apply(lambda xs: " | ".join(xs))
    detail["resultado_mes"] = df.get("Resultado o avance del mes", "").astype(str)
    detail["observaciones"] = df.get("Observaciones", "").astype(str)

    sector_rows = []
    valid = df[df["registro_valido"]].copy()
    for _, row in valid.iterrows():
        sectors = row["sectores"] if row["sectores"] else ["Sin sector marcado"]
        for sector in sectors:
            sector_rows.append(
                {
                    "programa_id": PROGRAM_ID,
                    "periodo": row["periodo"],
                    "anio": row["anio"],
                    "mes_num": row["mes_num"],
                    "mes_nombre": row["mes_nombre"],
                    "sector": sector,
                    "actividades": 1,
                    "nuevas_asistencias": int(bool(row["es_nueva_asistencia"])),
                    "asistencia_indicador": int(bool(row["cuenta_indicador_asistencia"])),
                }
            )

    sector_df = pd.DataFrame(sector_rows)
    if not sector_df.empty:
        sector_df = sector_df.groupby(
            ["programa_id", "periodo", "anio", "mes_num", "mes_nombre", "sector"],
            dropna=False,
            as_index=False,
        )[["actividades", "nuevas_asistencias", "asistencia_indicador"]].sum()

    return detail, sector_df


def build_estudios() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_csv(RAW_DIR / MODULE_FILE_MAP["estudios"])
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = ensure_base_fields(df, "estudios")
    sector_cols = extract_yes_columns(df, "Sector: ")

    df["nuevo_finalizado_auto"] = pd.to_numeric(df.get("Nuevo estudio finalizado (auto)", "").apply(parse_number), errors="coerce").fillna(0)
    status_slug = df.get("Estado del estudio *", "").astype(str).apply(slug_text)
    df["se_finalizo_mes"] = (
        df.get("¿Se finalizó este mes? *", "").apply(parse_bool)
        | df["nuevo_finalizado_auto"].gt(0)
        | status_slug.str.contains("final", na=False)
    )
    df["sectores"] = (
        df[sector_cols].apply(
            lambda row: [col.replace("Sector: ", "") for col, v in row.items() if parse_bool(v)],
            axis=1,
        ) if sector_cols else [[] for _ in range(len(df))]
    )

    df["row_has_minimum_data"] = (
        df["fecha"].notna()
        & df.get("Municipio *", "").astype(str).str.strip().ne("")
        & (
            df.get("Tipo de estudio *", "").astype(str).str.strip().ne("")
            | df.get("Estado del estudio *", "").astype(str).str.strip().ne("")
            | df.get("Observaciones", "").astype(str).str.strip().ne("")
        )
    )
    df["registro_valido"] = df["row_has_minimum_data"]
    df["row_alert_estado_incompleto"] = df["estado_fila_norm"].eq("INCOMPLETA")
    df["study_key"] = (
        df.get("Municipio *", "").astype(str).str.strip()
        + "||"
        + df.get("Tipo de estudio *", "").astype(str).str.strip()
        + "||"
        + df["sectores"].apply(lambda xs: "|".join(sorted(xs)))
    )
    study_type_slug = df.get("Tipo de estudio *", "").astype(str).apply(slug_text)
    df["is_rs_comercial_mercados"] = (
        study_type_slug.str.contains("residuos", na=False)
        & df["sectores"].apply(lambda xs: any(x in {"Comercial", "Mercados"} for x in xs))
    )
    df["cuenta_indicador_estudio"] = df["is_rs_comercial_mercados"] & df["se_finalizo_mes"]

    detail = df[
        ["row_number", "module_name", "fecha", "anio", "mes_num", "mes_nombre", "periodo", "registro_valido", "estado_fila_norm", "row_alert_estado_incompleto"]
    ].copy()
    detail["municipio"] = df.get("Municipio *", "").astype(str)
    detail["tipo_estudio"] = df.get("Tipo de estudio *", "").astype(str)
    detail["estado_estudio"] = df.get("Estado del estudio *", "").astype(str)
    detail["se_finalizo_mes"] = df["se_finalizo_mes"]
    detail["es_rs_comercial_mercados"] = df["is_rs_comercial_mercados"]
    detail["cuenta_indicador_estudio"] = df["cuenta_indicador_estudio"]
    detail["sectores"] = df["sectores"].apply(lambda xs: " | ".join(xs))
    detail["instituciones_apoyo"] = df.get("Instituciones de apoyo", "").astype(str)
    detail["observaciones"] = df.get("Observaciones", "").astype(str)

    sector_rows = []
    valid = df[df["registro_valido"]].copy()
    for _, row in valid.iterrows():
        sectors = row["sectores"] if row["sectores"] else ["Sin sector marcado"]
        for sector in sectors:
            sector_rows.append(
                {
                    "programa_id": PROGRAM_ID,
                    "periodo": row["periodo"],
                    "anio": row["anio"],
                    "mes_num": row["mes_num"],
                    "mes_nombre": row["mes_nombre"],
                    "sector": sector,
                    "estudios": 1,
                    "estudios_finalizados": int(bool(row["se_finalizo_mes"])),
                    "estudios_rs_comercial_mercados": int(bool(row["is_rs_comercial_mercados"] and row["se_finalizo_mes"])),
                }
            )

    sector_df = pd.DataFrame(sector_rows)
    if not sector_df.empty:
        sector_df = sector_df.groupby(
            ["programa_id", "periodo", "anio", "mes_num", "mes_nombre", "sector"],
            dropna=False,
            as_index=False,
        )[["estudios", "estudios_finalizados", "estudios_rs_comercial_mercados"]].sum()

    return detail, sector_df


def build_pirdes() -> pd.DataFrame:
    df = read_csv(RAW_DIR / MODULE_FILE_MAP["pirdes"])
    if df.empty:
        return pd.DataFrame()

    df = ensure_base_fields(df, "pirdes")

    df["pirdes_auto"] = pd.to_numeric(df.get("PIRDES implementado (auto)", "").apply(parse_number), errors="coerce").fillna(0)
    state_slug = df.get("Estado del PIRDES *", "").astype(str).apply(slug_text)
    df["implementado_mes"] = (
        df.get("¿Implementado este mes? *", "").apply(parse_bool)
        | df["pirdes_auto"].gt(0)
        | state_slug.str.contains("implement", na=False)
    )
    df["participantes_totales"] = df.get("Participantes totales", "").apply(parse_number)
    df["n_tecnicos"] = df.get("N° técnicos", "").apply(parse_number)
    df["n_operarios"] = df.get("N° operarios", "").apply(parse_number)
    df["row_has_minimum_data"] = (
        df["fecha"].notna()
        & df.get("Municipio *", "").astype(str).str.strip().ne("")
        & (
            df.get("Estado del PIRDES *", "").astype(str).str.strip().ne("")
            | pd.to_numeric(df["participantes_totales"], errors="coerce").fillna(0).gt(0)
            | df.get("Observaciones", "").astype(str).str.strip().ne("")
        )
    )
    df["registro_valido"] = df["row_has_minimum_data"]
    df["row_alert_estado_incompleto"] = df["estado_fila_norm"].eq("INCOMPLETA")

    detail = df[
        ["row_number", "module_name", "fecha", "anio", "mes_num", "mes_nombre", "periodo", "registro_valido", "estado_fila_norm", "row_alert_estado_incompleto"]
    ].copy()
    detail["municipio"] = df.get("Municipio *", "").astype(str)
    detail["estado_pirdes"] = df.get("Estado del PIRDES *", "").astype(str)
    detail["implementado_mes"] = df["implementado_mes"]
    detail["participantes_totales"] = df["participantes_totales"]
    detail["n_tecnicos"] = df["n_tecnicos"]
    detail["n_operarios"] = df["n_operarios"]
    detail["requiere_seguimiento"] = df.get("¿Requiere seguimiento adicional? *", "").astype(str)
    detail["observaciones"] = df.get("Observaciones", "").astype(str)

    return detail


def normalize_reunion_type(value: str) -> str:
    raw = normalize_text(value)
    slug = slug_text(raw)
    if "codema" in slug:
        return "Eje de agua y saneamiento / CODEMA"
    if "mesa tecnica departamental" in slug:
        return "Mesa técnica departamental de agua y saneamiento"
    if "mesa tecnica municipal" in slug or "reunion tecnica con municipio" in slug:
        return "Mesa técnica municipal"
    return raw


def build_reuniones() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_csv(RAW_DIR / MODULE_FILE_MAP["reuniones"])
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = ensure_base_fields(df, "reuniones")
    muni_cols = extract_yes_columns(df, "Mun: ")

    df["municipios_list"] = (
        df[muni_cols].apply(
            lambda row: [col.replace("Mun: ", "") for col, v in row.items() if parse_bool(v)],
            axis=1,
        ) if muni_cols else [[] for _ in range(len(df))]
    )

    df["tipo_reunion"] = df.get("Tipo de reunión / espacio *", "").astype(str).apply(normalize_reunion_type)
    df["is_codema"] = df["tipo_reunion"].eq("Eje de agua y saneamiento / CODEMA")
    df["is_mesa_dep"] = df["tipo_reunion"].eq("Mesa técnica departamental de agua y saneamiento")
    df["is_mesa_municipal"] = df["tipo_reunion"].eq("Mesa técnica municipal")

    df["row_has_minimum_data"] = (
        df["fecha"].notna()
        & (
            df["tipo_reunion"].ne("")
            | df.get("Tema principal", "").astype(str).str.strip().ne("")
            | df.get("Instituciones participantes", "").astype(str).str.strip().ne("")
            | df.get("Acuerdos principales", "").astype(str).str.strip().ne("")
        )
    )
    df["registro_valido"] = df["row_has_minimum_data"]
    df["row_alert_estado_incompleto"] = df["estado_fila_norm"].eq("INCOMPLETA")

    detail = df[
        ["row_number", "module_name", "fecha", "anio", "mes_num", "mes_nombre", "periodo", "registro_valido", "estado_fila_norm", "row_alert_estado_incompleto"]
    ].copy()
    detail["tipo_reunion"] = df["tipo_reunion"]
    detail["tema_principal"] = df.get("Tema principal", "").astype(str)
    detail["instituciones_participantes"] = df.get("Instituciones participantes", "").astype(str)
    detail["acuerdos_principales"] = df.get("Acuerdos principales", "").astype(str)
    detail["is_codema"] = df["is_codema"]
    detail["is_mesa_dep"] = df["is_mesa_dep"]
    detail["is_mesa_municipal"] = df["is_mesa_municipal"]
    detail["municipios"] = df["municipios_list"].apply(lambda xs: " | ".join(xs))

    type_df = (
        detail[detail["registro_valido"]]
        .groupby(["periodo", "anio", "mes_num", "mes_nombre", "tipo_reunion"], dropna=False, as_index=False)
        .size()
        .rename(columns={"size": "reuniones"})
    )
    if not type_df.empty:
        type_df.insert(0, "programa_id", PROGRAM_ID)

    return detail, type_df


def compute_periods(*frames) -> pd.DataFrame:
    periods = []
    for df in frames:
        if df is None or df.empty or "fecha" not in df.columns:
            continue
        subset = df[df["fecha"].notna()][["fecha"]].copy()
        if subset.empty:
            continue
        periods.append(subset)
    if not periods:
        return pd.DataFrame(columns=["periodo", "anio", "mes_num", "mes_nombre"])
    all_dates = pd.concat(periods, ignore_index=True)
    out = pd.DataFrame({"fecha": pd.to_datetime(all_dates["fecha"])})
    out["periodo"] = out["fecha"].dt.to_period("M").astype(str)
    out["anio"] = out["fecha"].dt.year.astype(int)
    out["mes_num"] = out["fecha"].dt.month.astype(int)
    out["mes_nombre"] = out["mes_num"].map(MONTH_NAMES_ES)
    out = out[["periodo", "anio", "mes_num", "mes_nombre"]].drop_duplicates().sort_values(["anio", "mes_num"]).reset_index(drop=True)
    return out


def unique_first_period(detail: pd.DataFrame, key_col: str, flag_col: str) -> pd.Series:
    if detail.empty:
        return pd.Series(dtype="object")
    subset = detail[(detail["registro_valido"]) & (detail[flag_col])].copy()
    if subset.empty:
        return pd.Series(dtype="object")
    subset = subset.sort_values(["fecha", "row_number"])
    return subset.groupby(key_col, as_index=True)["periodo"].first()


def build_indicator_rows(
    periods: pd.DataFrame,
    cap_detail: pd.DataFrame,
    cap_tema_df: pd.DataFrame,
    cap_muni_df: pd.DataFrame,
    asis_detail: pd.DataFrame,
    est_detail: pd.DataFrame,
    pirdes_detail: pd.DataFrame,
    reu_detail: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows_total = []
    rows_ind = []

    cap_valid = cap_detail[cap_detail["registro_valido"]].copy()
    asis_valid = asis_detail[asis_detail["registro_valido"]].copy()
    est_valid = est_detail[est_detail["registro_valido"]].copy()
    pirdes_valid = pirdes_detail[pirdes_detail["registro_valido"]].copy()
    reu_valid = reu_detail[reu_detail["registro_valido"]].copy()

    asis_detail = asis_detail.copy()
    asis_detail["project_key"] = (
        asis_detail["proyecto_codigo"].astype(str).str.strip()
        + "||"
        + asis_detail["municipio"].astype(str).str.strip()
    )
    est_detail = est_detail.copy()
    est_detail["study_key"] = (
        est_detail["municipio"].astype(str).str.strip()
        + "||"
        + est_detail["tipo_estudio"].astype(str).str.strip()
        + "||"
        + est_detail["sectores"].astype(str).str.strip()
    )
    pirdes_detail = pirdes_detail.copy()
    pirdes_detail["pirdes_key"] = pirdes_detail["municipio"].astype(str).str.strip()

    first_asis = unique_first_period(asis_detail, "project_key", "cuenta_indicador_asistencia")
    first_study_primary = unique_first_period(est_detail, "study_key", "cuenta_indicador_estudio")
    first_study_any = unique_first_period(est_detail, "study_key", "se_finalizo_mes")
    first_pirdes = unique_first_period(pirdes_detail, "pirdes_key", "implementado_mes")

    for _, p in periods.iterrows():
        periodo = p["periodo"]
        anio = int(p["anio"])
        mes_num = int(p["mes_num"])
        mes_nombre = p["mes_nombre"]

        cap_month = cap_valid[cap_valid["periodo"] == periodo]
        cap_upto = cap_valid[cap_valid["periodo"] <= periodo]

        cap_month_core = cap_month[cap_month["has_core_theme"]]
        cap_upto_core = cap_upto[cap_upto["has_core_theme"]]

        municipios_cap_mes = set()
        for value in cap_month_core["municipios"]:
            municipios_cap_mes.update(split_pipe_values(value))

        municipios_cap_acum = set()
        for value in cap_upto_core["municipios"]:
            municipios_cap_acum.update(split_pipe_values(value))

        temas_nucleo_mes = cap_tema_df[(cap_tema_df["periodo"] == periodo) & (cap_tema_df["es_tema_nucleo"])]
        reuniones_mes = reu_valid[reu_valid["periodo"] == periodo]
        reuniones_upto = reu_valid[reu_valid["periodo"] <= periodo]

        metrics = {
            "municipios_capacitacion_nucleo": {
                "valor_mes": float(len(municipios_cap_mes)),
                "valor_acumulado": float(len(municipios_cap_acum)),
            },
            "personas_capacitadas_nucleo": {
                "valor_mes": safe_sum(cap_month_core["participantes_totales"]),
                "valor_acumulado": safe_sum(cap_upto_core["participantes_totales"]),
            },
            "asistencias_priorizadas_proxy": {
                "valor_mes": float((first_asis == periodo).sum()),
                "valor_acumulado": float((first_asis <= periodo).sum()),
            },
            "estudios_rs_comercial_mercados": {
                "valor_mes": float((first_study_primary == periodo).sum()),
                "valor_acumulado": float((first_study_primary <= periodo).sum()),
            },
            "pirdes_implementados": {
                "valor_mes": float((first_pirdes == periodo).sum()),
                "valor_acumulado": float((first_pirdes <= periodo).sum()),
            },
            "reuniones_codema": {
                "valor_mes": float(reuniones_mes["is_codema"].fillna(False).sum()),
                "valor_acumulado": float(reuniones_upto["is_codema"].fillna(False).sum()),
            },
            "mesas_tecnicas_departamentales": {
                "valor_mes": float(reuniones_mes["is_mesa_dep"].fillna(False).sum()),
                "valor_acumulado": float(reuniones_upto["is_mesa_dep"].fillna(False).sum()),
            },
            "eventos_capacitacion_total": {
                "valor_mes": float(len(cap_month)),
                "valor_acumulado": float(len(cap_upto)),
            },
            "personas_capacitadas_total": {
                "valor_mes": safe_sum(cap_month["participantes_totales"]),
                "valor_acumulado": safe_sum(cap_upto["participantes_totales"]),
            },
            "tecnicos_capacitados_total": {
                "valor_mes": safe_sum(cap_month["n_tecnicos"]),
                "valor_acumulado": safe_sum(cap_upto["n_tecnicos"]),
            },
            "operarios_capacitados_total": {
                "valor_mes": safe_sum(cap_month["n_operarios"]),
                "valor_acumulado": safe_sum(cap_upto["n_operarios"]),
            },
            "otro_personal_capacitado_total": {
                "valor_mes": safe_sum(cap_month["n_otro_personal"]),
                "valor_acumulado": safe_sum(cap_upto["n_otro_personal"]),
            },
            "asistencias_nuevas_total": {
                "valor_mes": float(asis_valid[asis_valid["periodo"] == periodo]["es_nueva_asistencia"].fillna(False).sum()),
                "valor_acumulado": float(asis_valid[asis_valid["periodo"] <= periodo]["es_nueva_asistencia"].fillna(False).sum()),
            },
            "estudios_finalizados_total": {
                "valor_mes": float((first_study_any == periodo).sum()),
                "valor_acumulado": float((first_study_any <= periodo).sum()),
            },
            "reuniones_totales": {
                "valor_mes": float(len(reuniones_mes)),
                "valor_acumulado": float(len(reuniones_upto)),
            },
            "mesas_tecnicas_municipales": {
                "valor_mes": float(reuniones_mes["is_mesa_municipal"].fillna(False).sum()),
                "valor_acumulado": float(reuniones_upto["is_mesa_municipal"].fillna(False).sum()),
            },
        }

        row_total = {
            "programa_id": PROGRAM_ID,
            "programa_nombre": PROGRAM_NAME,
            "periodo": periodo,
            "anio": anio,
            "mes_num": mes_num,
            "mes_nombre": mes_nombre,
            "cohorte_mes_indice": mes_num,
            "fecha_min_periodo": periodo + "-01",
            "fecha_max_periodo": pd.Period(periodo).to_timestamp(how="end").date().isoformat(),
            "eventos_capacitacion_mes": metrics["eventos_capacitacion_total"]["valor_mes"],
            "eventos_capacitacion_acum": metrics["eventos_capacitacion_total"]["valor_acumulado"],
            "municipios_capacitacion_nucleo_mes": metrics["municipios_capacitacion_nucleo"]["valor_mes"],
            "municipios_capacitacion_nucleo_acum": metrics["municipios_capacitacion_nucleo"]["valor_acumulado"],
            "personas_capacitadas_nucleo_mes": metrics["personas_capacitadas_nucleo"]["valor_mes"],
            "personas_capacitadas_nucleo_acum": metrics["personas_capacitadas_nucleo"]["valor_acumulado"],
            "personas_capacitadas_total_mes": metrics["personas_capacitadas_total"]["valor_mes"],
            "personas_capacitadas_total_acum": metrics["personas_capacitadas_total"]["valor_acumulado"],
            "tecnicos_capacitados_mes": metrics["tecnicos_capacitados_total"]["valor_mes"],
            "tecnicos_capacitados_acum": metrics["tecnicos_capacitados_total"]["valor_acumulado"],
            "operarios_capacitados_mes": metrics["operarios_capacitados_total"]["valor_mes"],
            "operarios_capacitados_acum": metrics["operarios_capacitados_total"]["valor_acumulado"],
            "otro_personal_capacitado_mes": metrics["otro_personal_capacitado_total"]["valor_mes"],
            "otro_personal_capacitado_acum": metrics["otro_personal_capacitado_total"]["valor_acumulado"],
            "temas_nucleo_cubiertos_mes": float(temas_nucleo_mes["tema"].nunique()) if not temas_nucleo_mes.empty else 0.0,
            "asistencias_priorizadas_proxy_mes": metrics["asistencias_priorizadas_proxy"]["valor_mes"],
            "asistencias_priorizadas_proxy_acum": metrics["asistencias_priorizadas_proxy"]["valor_acumulado"],
            "asistencias_nuevas_total_mes": metrics["asistencias_nuevas_total"]["valor_mes"],
            "asistencias_nuevas_total_acum": metrics["asistencias_nuevas_total"]["valor_acumulado"],
            "estudios_rs_comercial_mercados_mes": metrics["estudios_rs_comercial_mercados"]["valor_mes"],
            "estudios_rs_comercial_mercados_acum": metrics["estudios_rs_comercial_mercados"]["valor_acumulado"],
            "estudios_finalizados_total_mes": metrics["estudios_finalizados_total"]["valor_mes"],
            "estudios_finalizados_total_acum": metrics["estudios_finalizados_total"]["valor_acumulado"],
            "pirdes_implementados_mes": metrics["pirdes_implementados"]["valor_mes"],
            "pirdes_implementados_acum": metrics["pirdes_implementados"]["valor_acumulado"],
            "reuniones_codema_mes": metrics["reuniones_codema"]["valor_mes"],
            "reuniones_codema_acum": metrics["reuniones_codema"]["valor_acumulado"],
            "mesas_tecnicas_departamentales_mes": metrics["mesas_tecnicas_departamentales"]["valor_mes"],
            "mesas_tecnicas_departamentales_acum": metrics["mesas_tecnicas_departamentales"]["valor_acumulado"],
            "mesas_tecnicas_municipales_mes": metrics["mesas_tecnicas_municipales"]["valor_mes"],
            "mesas_tecnicas_municipales_acum": metrics["mesas_tecnicas_municipales"]["valor_acumulado"],
            "reuniones_totales_mes": metrics["reuniones_totales"]["valor_mes"],
            "reuniones_totales_acum": metrics["reuniones_totales"]["valor_acumulado"],
        }
        rows_total.append(row_total)

        for indicator_id, metric in metrics.items():
            label, unit, category = INDICATOR_LABELS[indicator_id]
            meta_anual = PRIMARY_METAS.get(indicator_id)
            meta_cohorte = (meta_anual * mes_num / 12.0) if meta_anual is not None else pd.NA
            pct_cohorte = (
                metric["valor_acumulado"] / meta_cohorte
                if meta_anual is not None and pd.notna(meta_cohorte) and meta_cohorte != 0
                else pd.NA
            )
            pct_anual = (
                metric["valor_acumulado"] / meta_anual
                if meta_anual is not None and pd.notna(meta_anual) and meta_anual != 0
                else pd.NA
            )
            rows_ind.append(
                {
                    "programa_id": PROGRAM_ID,
                    "programa_nombre": PROGRAM_NAME,
                    "periodo": periodo,
                    "anio": anio,
                    "mes_num": mes_num,
                    "mes_nombre": mes_nombre,
                    "indicador_id": indicator_id,
                    "indicador_nombre": label,
                    "categoria": category,
                    "orden_dashboard": (PRIMARY_INDICATOR_ORDER.index(indicator_id) + 1) if indicator_id in PRIMARY_INDICATOR_ORDER else 100,
                    "unidad": unit,
                    "valor_mes": metric["valor_mes"],
                    "valor_acumulado": metric["valor_acumulado"],
                    "meta_anual": meta_anual,
                    "meta_cohorte": meta_cohorte,
                    "pct_meta_anual": pct_anual,
                    "pct_cohorte": pct_cohorte,
                    "semaforo": semaforo_from_pct(pct_cohorte) if category == "primario" else "",
                }
            )

    return pd.DataFrame(rows_total), pd.DataFrame(rows_ind)


def build_quality_table(
    periods: pd.DataFrame,
    cap_detail: pd.DataFrame,
    asis_detail: pd.DataFrame,
    est_detail: pd.DataFrame,
    pirdes_detail: pd.DataFrame,
    reu_detail: pd.DataFrame,
) -> pd.DataFrame:
    quality_rows = []
    module_frames = {
        "capacitaciones": cap_detail,
        "asistencias": asis_detail,
        "estudios": est_detail,
        "pirdes": pirdes_detail,
        "reuniones": reu_detail,
    }

    for _, p in periods.iterrows():
        periodo = p["periodo"]
        for module_name, detail in module_frames.items():
            if detail.empty:
                continue
            month = detail[detail["periodo"] == periodo].copy()
            quality_rows.append(
                {
                    "programa_id": PROGRAM_ID,
                    "periodo": periodo,
                    "anio": p["anio"],
                    "mes_num": p["mes_num"],
                    "mes_nombre": p["mes_nombre"],
                    "modulo": module_name,
                    "filas_con_fecha": int(month["fecha"].notna().sum()),
                    "filas_validas": int(month["registro_valido"].fillna(False).sum()),
                    "filas_estado_incompleto": int((month["estado_fila_norm"] == "INCOMPLETA").sum()) if "estado_fila_norm" in month.columns else 0,
                    "filas_alerta_municipio_missing": int(month.get("row_alert_municipio_missing", pd.Series(dtype=bool)).fillna(False).sum()),
                }
            )
    return pd.DataFrame(quality_rows)



def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def number_or_zero(value) -> float:
    num = parse_number(value)
    if pd.isna(num):
        return 0.0
    return float(num)


def estado_from_pct_public(pct: float) -> str:
    if pct >= 1:
        return "cumplido"
    if pct >= 0.70:
        return "alto"
    if pct >= 0.35:
        return "medio"
    if pct > 0:
        return "bajo"
    return "sin_avance"


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]


def build_default_validated_summary() -> pd.DataFrame:
    return pd.DataFrame(DEFAULT_VALIDATED_INDICATORS, columns=VALIDATED_SUMMARY_COLUMNS)


def build_validated_summary() -> pd.DataFrame:
    """
    Lee la salida del Apps Script:
    data_raw/fortalecimiento_municipal/indicadores_resumen_validado_raw.csv

    Si no existe o viene vacía, genera una estructura segura con los indicadores en 0.
    """
    path = RAW_DIR / VALIDATED_SUMMARY_RAW

    if not path.exists():
        return build_default_validated_summary()

    df = read_csv(path)
    df = clean_column_names(df)

    if df.empty:
        return build_default_validated_summary()

    df = ensure_columns(df, VALIDATED_SUMMARY_COLUMNS)

    df["indicador_id"] = df["indicador_id"].astype(str).str.strip()
    df["dashboard"] = df["dashboard"].astype(str).str.strip()
    df["indicador"] = df["indicador"].astype(str).str.strip()
    df["unidad"] = df["unidad"].astype(str).str.strip()
    df["criterio_de_conteo"] = df["criterio_de_conteo"].astype(str).str.strip()

    df["valor_validado"] = df["valor_validado"].apply(number_or_zero)
    df["meta"] = df["meta"].apply(number_or_zero)

    # Si por alguna razón el Apps Script no devolvió todos los indicadores,
    # se completan con defaults sin inventar avance.
    defaults = build_default_validated_summary()
    existing_ids = set(df["indicador_id"].astype(str))

    missing = defaults[~defaults["indicador_id"].isin(existing_ids)].copy()

    if not missing.empty:
        df = pd.concat([df, missing], ignore_index=True)

    return df[VALIDATED_SUMMARY_COLUMNS]


def read_program_card_raw() -> pd.DataFrame:
    """
    Lee programa_card_raw.csv si el Apps Script ya lo generó.
    Si no existe o está vacío, devuelve DataFrame vacío.
    """
    path = RAW_DIR / PROGRAM_CARD_RAW

    if not path.exists():
        return pd.DataFrame(columns=PROGRAM_CARD_COLUMNS)

    df = read_csv(path)
    df = clean_column_names(df)

    if df.empty:
        return pd.DataFrame(columns=PROGRAM_CARD_COLUMNS)

    df = ensure_columns(df, PROGRAM_CARD_COLUMNS)

    df["programa_id"] = df["programa_id"].astype(str).str.strip()
    df["indicador_id"] = df["indicador_id"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip()
    df["unidad"] = df["unidad"].astype(str).str.strip()
    df["estado"] = df["estado"].astype(str).str.strip()

    df["valor_acumulado"] = df["valor_acumulado"].apply(number_or_zero)
    df["meta_anual"] = df["meta_anual"].apply(number_or_zero)
    df["pct_avance"] = df["pct_avance"].apply(number_or_zero)
    df["orden"] = df["orden"].apply(number_or_zero)

    return df[PROGRAM_CARD_COLUMNS]


def build_program_card_from_summary(summary: pd.DataFrame) -> pd.DataFrame:
    """
    Construye programa_card.csv desde 99_Indicadores_Resumen
    cuando Apps Script no haya generado programa_card todavía.
    """
    df = summary.copy()
    df = df[df["dashboard"].astype(str).str.strip().eq("index_general")].copy()

    if df.empty:
        return pd.DataFrame(columns=PROGRAM_CARD_COLUMNS)

    rows = []

    for _, row in df.iterrows():
        indicador_id = str(row.get("indicador_id", "")).strip()
        valor = number_or_zero(row.get("valor_validado", 0))
        meta = number_or_zero(row.get("meta", 0))
        pct = min(valor / meta, 1.0) if meta > 0 else 0.0

        rows.append(
            {
                "programa_id": PROGRAM_ID,
                "indicador_id": indicador_id,
                "label": str(row.get("indicador", "")).strip(),
                "valor_acumulado": valor,
                "meta_anual": meta,
                "unidad": str(row.get("unidad", "")).strip(),
                "pct_avance": pct,
                "orden": GENERAL_ORDER.get(indicador_id, 99),
                "estado": estado_from_pct_public(pct),
            }
        )

    out = pd.DataFrame(rows, columns=PROGRAM_CARD_COLUMNS)
    out = out.sort_values(["orden", "indicador_id"]).reset_index(drop=True)

    return out


def build_program_card(summary: pd.DataFrame) -> pd.DataFrame:
    """
    Prioridad:
    1. Si existe programa_card_raw.csv con filas reales, usa ese archivo.
    2. Si no, genera programa_card.csv desde indicadores_resumen_validado_raw.csv.
    """
    card_raw = read_program_card_raw()

    if not card_raw.empty:
        card_raw = card_raw.copy()

        # Asegura consistencia de estado y porcentaje.
        card_raw["pct_avance"] = card_raw.apply(
            lambda r: min(
                number_or_zero(r.get("valor_acumulado", 0)) / number_or_zero(r.get("meta_anual", 0)),
                1.0,
            )
            if number_or_zero(r.get("meta_anual", 0)) > 0
            else 0.0,
            axis=1,
        )

        card_raw["estado"] = card_raw["pct_avance"].apply(estado_from_pct_public)
        card_raw["orden"] = card_raw.apply(
            lambda r: GENERAL_ORDER.get(str(r.get("indicador_id", "")).strip(), number_or_zero(r.get("orden", 99))),
            axis=1,
        )

        return card_raw[PROGRAM_CARD_COLUMNS].sort_values(["orden", "indicador_id"]).reset_index(drop=True)

    return build_program_card_from_summary(summary)


def build_validated_compat_indicators(summary: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el resumen validado a un formato cercano a institucional_indicadores.csv,
    sin sustituir aún la lógica vieja del dashboard específico.

    Este archivo nuevo sirve para el siguiente paso:
    docs/data/fortalecimiento_municipal/institucional_indicadores_validado.csv
    """
    rows = []

    for _, row in summary.iterrows():
        valor = number_or_zero(row.get("valor_validado", 0))
        meta = number_or_zero(row.get("meta", 0))
        pct = valor / meta if meta > 0 else 0.0

        rows.append(
            {
                "programa_id": PROGRAM_ID,
                "programa_nombre": PROGRAM_NAME,
                "periodo": "validado",
                "anio": "",
                "mes_num": "",
                "mes_nombre": "",
                "indicador_id": str(row.get("indicador_id", "")).strip(),
                "indicador_nombre": str(row.get("indicador", "")).strip(),
                "categoria": str(row.get("dashboard", "")).strip(),
                "orden_dashboard": GENERAL_ORDER.get(str(row.get("indicador_id", "")).strip(), 100),
                "unidad": str(row.get("unidad", "")).strip(),
                "valor_mes": valor,
                "valor_acumulado": valor,
                "meta_anual": meta,
                "meta_cohorte": meta,
                "pct_meta_anual": pct,
                "pct_cohorte": pct,
                "semaforo": semaforo_from_pct(pct),
                "criterio_de_conteo": str(row.get("criterio_de_conteo", "")).strip(),
            }
        )

    return pd.DataFrame(rows)

def write_csv(df: pd.DataFrame, filename: str):
    out_path = OUT_DIR / filename
    doc_path = DOCS_DIR / filename
    df.to_csv(out_path, index=False)
    df.to_csv(doc_path, index=False)


def main():
    cap_detail, cap_tema_df, cap_muni_df = build_capacitaciones()
    asis_detail, asis_sector_df = build_asistencias()
    est_detail, est_sector_df = build_estudios()
    pirdes_detail = build_pirdes()
    reu_detail, reu_type_df = build_reuniones()

    periods = compute_periods(cap_detail, asis_detail, est_detail, pirdes_detail, reu_detail)
    total_mes, institucional = build_indicator_rows(
        periods=periods,
        cap_detail=cap_detail,
        cap_tema_df=cap_tema_df,
        cap_muni_df=cap_muni_df,
        asis_detail=asis_detail,
        est_detail=est_detail,
        pirdes_detail=pirdes_detail,
        reu_detail=reu_detail,
    )
    calidad = build_quality_table(periods, cap_detail, asis_detail, est_detail, pirdes_detail, reu_detail)

    metadata = pd.DataFrame(
        [
            {
                "programa_id": PROGRAM_ID,
                "programa_nombre": PROGRAM_NAME,
                "periodos_detectados": " | ".join(periods["periodo"].tolist()),
                "fecha_min_global": str(periods["periodo"].min()) if not periods.empty else "",
                "fecha_max_global": str(periods["periodo"].max()) if not periods.empty else "",
                "usa_encabezado_como_fuente_periodo": False,
                "nota_asistencias_codede": "Indicador publicado como proxy operativo mientras no exista columna explícita CODEDE en el sheet.",
                "nota_capacitaciones": "Estado fila e INCOMPLETA solo alertan calidad; no excluyen KPIs si la fila sí trae evidencia operativa mínima.",
                "nota_temas_nucleo": "Los temas núcleo se homologan desde Tema:, Tipo de actividad y Observaciones para no depender de nombres literales.",
            }
        ]
    )

    # ─────────────────────────────────────────────
    # Nueva capa validada por coordinador
    # ─────────────────────────────────────────────
    resumen_validado = build_validated_summary()
    programa_card = build_program_card(resumen_validado)
    institucional_validado = build_validated_compat_indicators(resumen_validado)

    outputs = {
        "detalle_capacitaciones.csv": cap_detail,
        "detalle_asistencias.csv": asis_detail,
        "detalle_estudios.csv": est_detail,
        "detalle_pirdes.csv": pirdes_detail,
        "detalle_reuniones.csv": reu_detail,
        "capacitaciones_tema_mes.csv": cap_tema_df,
        "capacitaciones_municipio_mes.csv": cap_muni_df,
        "asistencias_sector_mes.csv": asis_sector_df,
        "estudios_sector_mes.csv": est_sector_df,
        "reuniones_tipo_mes.csv": reu_type_df,
        "calidad_datos_mes.csv": calidad,
        "total_mes.csv": total_mes,
        "institucional_indicadores.csv": institucional.sort_values(["periodo", "orden_dashboard", "indicador_id"]),
        "metadata_publicacion.csv": metadata,
        "indicadores_resumen_validado.csv": resumen_validado,
        "programa_card.csv": programa_card,
        "institucional_indicadores_validado.csv": institucional_validado,
    }

    for filename, df in outputs.items():
        if df is None:
            df = pd.DataFrame()
        write_csv(df, filename)
        print(f"Generado: {filename} ({len(df)} filas)")

    print("Transformación de Fortalecimiento municipal completada.")


if __name__ == "__main__":
    main()
