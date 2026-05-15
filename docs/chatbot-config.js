(function (global) {
  'use strict';

  const PROGRAMS = {
    atitlan_recicla: {
      id: 'atitlan_recicla',
      name: 'Atitlán Recicla',
      shortName: 'AR',
      aliases: [
        'atitlan recicla', 'atitlán recicla', 'cooperativa atitlan recicla',
        'cooperativa atitlán recicla', 'cooperativa', 'ar', 'reciclaje',
        'recicla', 'atitlan recilca', 'atitlan reclica', 'cooperatva',
        'atitlan reciclar', 'lideresas', 'materiales reciclables', 'reciclado',
        'recoleccion materiales', 'recolección materiales'
      ]
    },
    conservando_atitlan: {
      id: 'conservando_atitlan',
      name: 'Conservando Atitlán',
      shortName: 'CA',
      aliases: [
        'conservando atitlan', 'conservando atitlán', 'ca',
        'conservacion', 'conservación', 'aceite', 'jabones',
        'aceite usado', 'conservado', 'conservando',
        'recoleccion aceite', 'recolección aceite', 'agua protegida'
      ]
    },
    educando_para_conservar: {
      id: 'educando_para_conservar',
      name: 'Educando para Conservar',
      shortName: 'EPC',
      aliases: [
        'educando para conservar', 'epc', 'educacion', 'educación',
        'educando', 'escuelas', 'docentes', 'estudiantes', 'pedagogico',
        'pedagógico', 'educativo', 'centros educativos', 'colegios',
        'niños', 'jovenes', 'jóvenes', 'programa educativo'
      ]
    },
    fortalecimiento_municipal: {
      id: 'fortalecimiento_municipal',
      name: 'Fortalecimiento Municipal',
      shortName: 'FM',
      aliases: [
        'fortalecimiento municipal', 'fm', 'municipal', 'municipalidad',
        'municipalidades', 'municipios', 'fortalecimiento', 'capacitaciones',
        'pirdes', 'pird', 'capacitacion', 'capacitación', 'gobiernos locales',
        'asistencias', 'reuniones', 'estudios municipales'
      ]
    },
    reforestacion: {
      id: 'reforestacion',
      name: 'Reforestando Atitlán',
      shortName: 'RA',
      aliases: [
        'reforestacion', 'reforestación', 'reforestando atitlan',
        'reforestando atitlán', 'ra', 'reforestar', 'reforestando',
        'arboles', 'árboles', 'plantas', 'vivero', 'bosque',
        'hectareas', 'hectáreas', 'hectareas monitoreadas',
        'area intervenida', 'área intervenida',
        'especies nativas', 'plantas nativas'
      ]
    },
    siembra_tul: {
      id: 'siembra_tul',
      name: 'Siembra de Tul',
      shortName: 'ST',
      aliases: [
        'tul', 'siembra de tul', 'siembra tul', 'siembras de tul',
        'macollas', 'macolla', 'metros lineales', 'jornadas de siembra',
        'restauracion tul', 'restauración tul', 'vegetacion lacustre',
        'vegetación lacustre', 'tular', 'litoral lago', 'st',
        'programa tul', 'tules'
      ]
    }
  };

  const APP = {
    id: 'aala-dashboard-chatbot',
    name: 'Asistente AALA',
    subtitle: 'Datos actualizados del dashboard',
    emptyState: 'Todavía no hay datos cargados para responder.',
    loadingLabel: 'Buscando en los datos...',
    errorLabel: 'No pude cargar la información en este momento. Intenta recargar la página.',
    placeholder: 'Pregunta sobre resultados, metas, alertas, comparaciones...',
    inputMaxLength: 500,
    historyLimit: 30,
    suggestionsLimit: 8
  };

  const DATA = {
    latestByDefault: true,
    includeDetailsByDefault: true,
    includeIndicatorsByDefault: true,
    includeMetadataByDefault: true,
    maxRowsPerCollection: 200,
    maxSearchResults: 25,
    refreshMode: 'manual_reload',
    dataSourceRoot: './data'
  };

  const UX = {
    defaultScope: 'all_programs',
    allowFreeText: true,
    allowOffTopicRedirect: true,
    showSuggestedQuestions: true,
    showSourcePeriod: true,
    showProgramChip: true,
    useLocalDraftPersistence: false,
    autoFocusInput: false,
    enterToSend: true,
    clearInputOnSend: true
  };

  const MODEL = {
    mode: 'ai_backend',
    backendEnabled: true,
    endpoint: 'https://aala-chatbo.sgeograficaaala.workers.dev',
    timeoutMs: 30000,
    temperature: 0.3,
    maxTokens: 1024
  };

  const RESPONSE_POLICY = {
    language: 'es',
    requireGroundingInData: true,
    requireProgramMentionWhenRelevant: true,
    requirePeriodMentionWhenRelevant: true,
    preferLatestPeriod: true,
    allowComparisonsAcrossPrograms: true,
    answerUnknownsClearly: true,
    declineWhenNoData: true,
    offTopicBehavior: 'redirect_to_dashboard_scope',
    forbiddenClaims: [
      'inventar cifras',
      'inventar metas',
      'afirmar datos que no aparezcan en los csv',
      'responder como si hubiera leido fuentes externas'
    ]
  };

  const INTENTS = {
    resumen: [
      'resumen', 'resume', 'resumir', 'sintesis', 'sintesis',
      'panorama', 'overview', 'analisis', 'analisis', 'analizar',
      'estado', 'estado general', 'situacion', 'situacion',
      'como va', 'como van', 'como esta', 'como estan',
      'que tal va', 'que tal estan', 'cuentame', 'dime sobre', 'dime de',
      'completo', 'detalle', 'detallado', 'informe', 'reporte',
      'resultado', 'resultados', 'balance', 'desempeno',
      'como le fue', 'como les fue', 'que paso', 'que pasa',
      'cuales son', 'que tiene', 'que muestra', 'que dice',
      'explicame', 'explicar', 'contame', 'cuéntame'
    ],
    comparacion: [
      'comparar', 'comparacion', 'comparacion', 'versus', 'vs',
      'diferencia', 'diferencias', 'frente a', 'contra',
      'mejor', 'peor', 'cual es mejor', 'cual va mejor',
      'comparame', 'comparame', 'entre programas', 'todos los programas',
      'cual esta mejor', 'cual esta peor', 'ranking'
    ],
    ultimo_mes: [
      'ultimo mes', 'ultimo mes', 'mes mas reciente', 'mes mas reciente',
      'ultimo periodo', 'ultimo periodo', 'periodo mas reciente',
      'mas reciente', 'reciente', 'actual', 'hoy', 'ahora', 'vigente'
    ],
    indicadores: [
      'indicador', 'indicadores', 'meta', 'metas', 'avance',
      'cumplimiento', 'porcentaje', 'kpi', 'objetivo', 'objetivos',
      'llegaron', 'alcanzaron', 'cumplieron', 'lograron',
      'cuanto llevan', 'cuanto llevan', 'como van las metas',
      'que porcentaje', 'cuanto falta', 'cuanto lograron'
    ],
    tendencia: [
      'tendencia', 'evolucion', 'evolucion', 'cambio', 'historico',
      'historico', 'comparado con', 'mes anterior', 'vs mes anterior',
      'subio', 'subio', 'bajo', 'bajo', 'aumento', 'aumento',
      'disminuyo', 'disminuyo', 'crecio', 'cayo', 'mejoro', 'empeoro',
      'progreso', 'retroceso', 'subi', 'baj'
    ],
    alerta: [
      'alerta', 'alertas', 'riesgo', 'riesgos', 'bajo meta',
      'rezago', 'problema', 'problemas', 'preocupacion', 'preocupacion',
      'rojo', 'amarillo', 'semaforo', 'semaforo',
      'que esta mal', 'que va mal', 'donde hay problemas',
      'que hay que mejorar', 'no esta llegando', 'atrasado', 'atrasados',
      'debajo', 'por debajo', 'incumplimiento', 'no cumple', 'no cumplieron',
      'fallando', 'falla', 'critico', 'critica'
    ],
    territorio: [
      'municipio', 'municipios', 'territorio', 'territorios',
      'zona', 'zonas', 'sector', 'sectores', 'tema', 'temas',
      'material', 'materiales', 'comunidad', 'comunidades',
      'donde', 'en que municipio', 'por zona', 'por sector',
      'por municipio', 'por material', 'desagregado', 'desglose'
    ]
  };

  const SUGGESTED_QUESTIONS = [
    {
      id: 'q-global-resumen',
      text: 'Resumen de todos los programas',
      scope: 'all_programs',
      programId: null,
      intent: 'resumen'
    },
    {
      id: 'q-global-alertas',
      text: '¿Qué indicadores están en alerta?',
      scope: 'all_programs',
      programId: null,
      intent: 'alerta'
    },
    {
      id: 'q-ar-resumen',
      text: '¿Cómo va Atitlán Recicla?',
      scope: 'program',
      programId: 'atitlan_recicla',
      intent: 'resumen'
    },
    {
      id: 'q-ca-resumen',
      text: '¿Cómo va Conservando Atitlán?',
      scope: 'program',
      programId: 'conservando_atitlan',
      intent: 'resumen'
    },
    {
      id: 'q-epc-resumen',
      text: '¿Cómo va Educando para Conservar?',
      scope: 'program',
      programId: 'educando_para_conservar',
      intent: 'resumen'
    },
    {
      id: 'q-fm-resumen',
      text: '¿Cómo va Fortalecimiento Municipal?',
      scope: 'program',
      programId: 'fortalecimiento_municipal',
      intent: 'resumen'
    },
    {
      id: 'q-refo-resumen',
      text: '¿Cómo va Reforestando Atitlán?',
      scope: 'program',
      programId: 'reforestacion',
      intent: 'resumen'
    },
    {
      id: 'q-tul-resumen',
      text: '¿Cómo va Siembra de Tul?',
      scope: 'program',
      programId: 'siembra_tul',
      intent: 'resumen'
    },
    {
      id: 'q-global-comparacion',
      text: 'Comparar todos los programas',
      scope: 'all_programs',
      programId: null,
      intent: 'comparacion'
    }
  ];

  const FALLBACKS = {
    noData: 'No encontré información en el dashboard para responder eso con confianza. Puedes preguntarme por resultados, metas, alertas o tendencias de cualquiera de nuestros 6 programas.',
    offTopic: 'Solo puedo ayudarte con datos de los programas de AALA: resultados, metas, indicadores y avances del dashboard. ¿Sobre qué programa quieres saber?',
    ambiguous: 'Puedo explicarlo mejor si me dices por qué programa, indicador o mes quieres preguntar. ¿Empezamos por alguno?',
    stale: 'Mis datos vienen de los datos publicados más recientemente en el dashboard.'
  };

  function stripAccents(value) {
    return String(value || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  }

  function normalizeText(value) {
    return stripAccents(value)
      .toLowerCase()
      .replace(/[_|/]+/g, ' ')
      .replace(/[^a-z0-9áéíóúüñ\s.-]/gi, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function resolveProgramFromText(text) {
    const normalized = normalizeText(text);
    if (!normalized) return null;
    for (const program of Object.values(PROGRAMS)) {
      if (normalizeText(program.name) === normalized) return program.id;
      if (program.aliases.some((alias) => normalized.includes(normalizeText(alias)))) return program.id;
    }
    return null;
  }

  function detectIntents(text) {
    const normalized = normalizeText(text);
    const matches = [];
    Object.entries(INTENTS).forEach(([intent, words]) => {
      if (words.some((word) => normalized.includes(normalizeText(word)))) matches.push(intent);
    });
    return matches;
  }

  function getProgramLabel(programId) {
    return PROGRAMS[programId]?.name || null;
  }

  function getSuggestedQuestions(programId = null) {
    if (!programId) return SUGGESTED_QUESTIONS.slice(0, APP.suggestionsLimit);
    const scoped = SUGGESTED_QUESTIONS.filter((item) => !item.programId || item.programId === programId);
    return scoped.slice(0, APP.suggestionsLimit);
  }

  function buildSystemInstruction() {
    const programList = Object.values(PROGRAMS).map((p) => `• ${p.name} (id: ${p.id})`).join('\n');
    return `Eres el Asistente de Datos de la Asociación Amigos del Lago de Atitlán (AALA). Tu única función es analizar y explicar los datos reales de los programas de AALA que se te proporcionan en el contexto.

═══════════════════════════════
REGLAS ABSOLUTAS — NUNCA VIOLAR
═══════════════════════════════
1. SOLO usas datos del contexto que recibes. Jamás inventas, estimas ni asumes cifras.
2. Si un campo vale 0 o está vacío para un período, ese período NO tiene datos reales. No lo presentes como resultado.
3. Nunca uses la fecha de hoy para inferir qué período es el más reciente. Lo determinas leyendo los datos del contexto.
4. Si no hay información suficiente en el contexto para responder, di: "No tengo datos suficientes para responder eso."
5. Sin emojis. Tono frío, directo y profesional.

═══════════════════════════════
PROGRAMAS DISPONIBLES
═══════════════════════════════
${programList}

═══════════════════════════════
CÓMO ANALIZAR Y RESPONDER
═══════════════════════════════
• Tono: frío, profesional, directo. Sin saludos efusivos ni frases de relleno. Ve al dato.
• Cifras: números clave en negrita. Incluye unidades (qq, Q, litros, árboles, ha, metros, macollas).
• Período: menciona siempre el mes al que corresponden los datos que citas.
• Alertas: cuando un indicador está por debajo de su meta, dilo con el valor real vs la meta.
• Tendencias: si tienes datos de varios meses, compara y señala si subió, bajó o se mantuvo.
• Siembra de Tul: sus indicadores son jornadas, metros lineales de tul sembrado, macollas establecidas y municipios atendidos.

═══════════════════════════════
FORMATO DE RESPUESTA
═══════════════════════════════
• Markdown: **negrita** para cifras clave, guiones para listas.
• Máximo 4 párrafos o una lista corta. Conciso pero completo.
• Pregunta simple (un indicador, un mes): 2-3 líneas máximo.
• Pregunta compleja (resumen global, comparación): más detalle, sin repetir.
• Nunca empieces con "Claro que sí" ni frases de relleno. Ve directo al dato.`;
  }

  function clone(value) {
    if (typeof structuredClone === 'function') return structuredClone(value);
    return JSON.parse(JSON.stringify(value));
  }

  global.ChatbotConfig = {
    APP: clone(APP),
    DATA: clone(DATA),
    UX: clone(UX),
    MODEL: clone(MODEL),
    PROGRAMS: clone(PROGRAMS),
    INTENTS: clone(INTENTS),
    RESPONSE_POLICY: clone(RESPONSE_POLICY),
    SUGGESTED_QUESTIONS: clone(SUGGESTED_QUESTIONS),
    FALLBACKS: clone(FALLBACKS),
    normalizeText,
    resolveProgramFromText,
    detectIntents,
    getProgramLabel,
    getSuggestedQuestions,
    buildSystemInstruction,
    getState() {
      return {
        app: clone(APP),
        data: clone(DATA),
        ux: clone(UX),
        model: clone(MODEL),
        programs: clone(PROGRAMS),
        suggestedQuestions: clone(SUGGESTED_QUESTIONS)
      };
    }
  };
})(window);
