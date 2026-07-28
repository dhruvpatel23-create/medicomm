import { readFileSync } from "node:fs";

const DATA_PATHS = ["runtime-data/users.json", "data/users.json"];

const EXPECTED_CHAPTERS_BY_SUBJECT = {
  anatomy: [
    "General Anatomy",
    "Upper Limb",
    "Lower Limb",
    "Thorax",
    "Abdomen",
    "Head and Neck",
    "Brain",
  ],
  biochemistry: [
    "Chemical Basis of Life",
    "General Metabolism",
    "Clinical and Applied Biochemistry",
    "Nutrition",
    "Molecular Biology",
  ],
  "community-medicine": [
    "Principles of Epidemiology and Epidemiological Methods",
    "Screening for Disease",
    "Epidemiology of Communicable Diseases",
    "Epidemiology of Chronic Non-Communicable Diseases and Conditions",
    "Health Programmes in India",
    "Demography and Family Planning",
    "Preventive Medicine in Obstetrics, Paediatrics and Geriatrics",
    "Nutrition and Health",
    "Medicine and Social Sciences",
    "Environment and Health",
    "Hospital Waste Management",
    "Disaster Management",
    "Occupational Health",
    "Genetics and Health",
    "Mental Health",
    "Health Information and Basic Medical Statistics",
    "Communication for Health Education",
    "Health Planning and Management",
    "Health Care of the Community",
  ],
  microbiology: [
    "General Microbiology",
    "Immunology",
    "Hospital Infection Control",
    "Bloodstream and Cardiovascular System Infections",
    "Central Nervous System Infections",
    "Respiratory Tract Infections",
    "Gastrointestinal (GI) Infections",
    "Hepatobiliary System Infections",
    "Urogenital Tract Infections",
    "Skin, Soft Tissue and Musculoskeletal System Infections",
    "Miscellaneous Infective Syndromes",
  ],
  pathology: [
    "The Cell as a Unit of Health and Disease",
    "Cell Injury, Cell Death, and Adaptations",
    "Inflammation and Repair",
    "Hemodynamic Disorders, Thromboembolic Disease, and Shock",
    "Genetic Disorders",
    "Diseases of the Immune System",
    "Neoplasia",
    "Infectious Diseases",
    "Environmental and Nutritional Diseases",
    "Diseases of Infancy and Childhood",
    "Blood Vessels",
    "The Heart",
    "Diseases of White Blood Cells, Lymph Nodes, Spleen, and Thymus",
    "Red Blood Cell and Bleeding Disorders",
    "The Lung",
    "Head and Neck",
    "The Gastrointestinal Tract",
    "Liver and Gallbladder",
    "The Pancreas",
    "The Kidney",
    "The Lower Urinary Tract and Male Genital System",
    "The Female Genital Tract",
    "The Breast",
    "The Endocrine System",
    "The Skin",
    "Bones, Joints, and Soft Tissue Tumors",
    "Peripheral Nerves and Skeletal Muscles",
    "The Central Nervous System",
    "The Eye",
  ],
  pharmacology: [
    "General Principles",
    "Neuropharmacology",
    "Modulation of Pulmonary, Renal, and Cardiovascular",
    "Inflammation, Immunomodulation, and Hematopoiesis",
    "Endocrine Pharmacology",
    "Gastrointestinal Pharmacology",
    "Chemotherapy of Infectious Diseases",
    "Pharmacotherapy of Neoplastic Disease",
    "Special Systems Pharmacology",
  ],
  physiology: [
    "The Cell Physiology",
    "Transport Through Cell Membrane",
    "Membrane Potential",
    "Genetics",
    "Nerve Muscle Physiology",
    "Blood and Immune System",
    "Cardiovascular System",
    "Respiratory System",
    "Excretory System",
    "Gastrointestinal System",
    "Endocrinal System",
    "Reproductive System",
    "Nervous System",
    "Special Senses",
    "Specialised Integrative Physiology",
  ],
};

const expectedOrdersBySubject = new Map(
  Object.entries(EXPECTED_CHAPTERS_BY_SUBJECT).map(([subjectId, chapters]) => [
    subjectId,
    new Map(chapters.map((title, index) => [title, index + 1])),
  ]),
);

function addMapSet(map, key, value) {
  map.set(key, map.get(key) ?? new Set());
  map.get(key).add(value);
}

function summarizeDirectory(data, subjectId) {
  const chapters = new Map();
  for (const question of data.questions ?? []) {
    if (question.subjectId !== subjectId) continue;
    const chapterTitle = question.chapterTitle;
    const topic = question.topic;
    if (!chapterTitle || !topic) continue;

    chapters.set(chapterTitle, chapters.get(chapterTitle) ?? {
      chapterOrders: new Set(),
      topics: new Map(),
    });

    const chapter = chapters.get(chapterTitle);
    chapter.chapterOrders.add(question.chapterOrder);
    addMapSet(chapter.topics, topic, question.topicOrder);
  }
  return chapters;
}

function numericSetValues(values) {
  return [...values].map(Number).filter(Number.isFinite);
}

function checkDuplicateOrders(entries, label, report) {
  const orders = entries.map(([, order]) => order).sort((left, right) => left - right);
  const duplicateOrders = orders.filter((order, index) => orders.indexOf(order) !== index);

  if (duplicateOrders.length) {
    report.push(`  Duplicate ${label} order values: ${[...new Set(duplicateOrders)].join(", ")}`);
  }
}

let failed = false;

for (const dataPath of DATA_PATHS) {
  const data = JSON.parse(readFileSync(dataPath, "utf8").replace(/^\uFEFF/, ""));

  for (const [subjectId, expectedOrder] of expectedOrdersBySubject) {
    const report = [];
    const chapters = summarizeDirectory(data, subjectId);
    const expectedTitles = EXPECTED_CHAPTERS_BY_SUBJECT[subjectId];
    const actualTitles = [...chapters.keys()];
    const unexpected = actualTitles.filter((title) => !expectedOrder.has(title));
    const orderedChapters = [];

    if (!actualTitles.length) {
      report.push("  No chapters found for this subject.");
    }

    for (const [title, chapter] of chapters) {
      const chapterOrders = numericSetValues(chapter.chapterOrders);
      if (chapterOrders.length !== 1) {
        report.push(`  ${title}: chapterOrder must be one stable number, found ${[...chapter.chapterOrders].join(", ")}`);
        continue;
      }

      orderedChapters.push([title, chapterOrders[0]]);
      const expectedChapterOrder = expectedOrder.get(title);
      if (expectedChapterOrder && chapterOrders[0] !== expectedChapterOrder) {
        report.push(`  ${title}: chapterOrder ${chapterOrders[0]}, expected ${expectedChapterOrder}`);
      }

      const orderedTopics = [];
      for (const [topic, topicOrders] of chapter.topics) {
        const numericTopicOrders = numericSetValues(topicOrders);
        if (numericTopicOrders.length !== 1) {
          report.push(`  ${title} / ${topic}: topicOrder must be one stable number, found ${[...topicOrders].join(", ")}`);
          continue;
        }
        orderedTopics.push([topic, numericTopicOrders[0]]);
      }
      checkDuplicateOrders(orderedTopics, `${title} topic`, report);
    }

    checkDuplicateOrders(orderedChapters, `${subjectId} chapter`, report);

    const actualSequence = orderedChapters
      .sort((left, right) => left[1] - right[1] || left[0].localeCompare(right[0]))
      .map(([title]) => title)
      .filter((title) => expectedOrder.has(title));
    const expectedSubset = expectedTitles.filter((title) => actualSequence.includes(title));
    const sequenceMatches = actualSequence.every((title, index) => title === expectedSubset[index]);

    if (unexpected.length) report.push(`  Unexpected chapters: ${unexpected.join("; ")}`);
    if (!sequenceMatches) {
      report.push("  Actual chapter sequence:");
      orderedChapters
        .sort((left, right) => left[1] - right[1] || left[0].localeCompare(right[0]))
        .forEach(([title, order]) => report.push(`    ${order}. ${title}`));
    }

    if (report.length) {
      failed = true;
      console.error(`${subjectId} directory order check failed for ${dataPath}`);
      report.forEach((line) => console.error(line));
    } else {
      console.log(`${subjectId} directory order is locked for ${dataPath}.`);
    }
  }
}

if (failed) process.exit(1);
