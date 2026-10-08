// Reference titles, not a claim that a particular edition was retrieved.
const books = {
  anatomy: ["B. D. Chaurasia's Human Anatomy", "Inderbir Singh's Human Embryology", "Inderbir Singh's Textbook of Human Histology"],
  physiology: ["Guyton and Hall Textbook of Medical Physiology"],
  biochemistry: ["Vasudevan's Textbook of Biochemistry for Medical Students"],
  pharmacology: ["K. D. Tripathi's Essentials of Medical Pharmacology"],
  pathology: ["Robbins and Cotran Pathologic Basis of Disease", "Harsh Mohan's Textbook of Pathology"],
  microbiology: ["Apurba S. Sastry and Sandhya Bhat's Essentials of Medical Microbiology"],
  "forensic medicine and toxicology": ["K. S. Narayan Reddy and O. P. Murty's The Essentials of Forensic Medicine and Toxicology"],
  "community medicine": ["Park's Textbook of Preventive and Social Medicine"],
  ophthalmology: ["A. K. Khurana's Comprehensive Ophthalmology"],
  ent: ["P. L. Dhingra and Shruti Dhingra's Diseases of Ear, Nose and Throat & Head and Neck Surgery"],
  "general medicine": ["Davidson's Principles and Practice of Medicine"],
  "general surgery": ["Bailey & Love's Short Practice of Surgery"],
  orthopedics: ["J. Maheshwari and Vikram A. Mhaskar's Essential Orthopaedics"],
  "obstetrics and gynaecology": ["D. C. Dutta's Textbook of Obstetrics", "D. C. Dutta's Textbook of Gynecology"],
  pediatrics: ["Ghai Essential Pediatrics"],
};

export function theoryTextbooks(subjectTitle) {
  return books[String(subjectTitle).trim().toLowerCase()] ?? [];
}

export function buildTheoryTextbookInstructions(subjectTitle) {
  const titles = theoryTextbooks(subjectTitle);
  return [
    "Base the corrected model answer on standard undergraduate medical textbooks used in Indian MBBS teaching, in Indian university/professional examination answer format only. Write an original synthesis of textbook knowledge, never a reproduced passage. Do not use coaching-note shorthand, chatty explanations, or USMLE-style discussion.",
    titles.length ? `Use the relevant textbook(s) from this approved list: ${JSON.stringify(titles)}.` : "Select established subject-specific undergraduate textbooks used in India; never invent a textbook title.",
    "Use a brief definition/introduction where relevant, then logically ordered descriptive headings and complete exam points covering each requested part. Include relevant classification, mechanisms, features, investigations, management, applied significance or labelled-diagram guidance only as appropriate to the question. Scale depth to short-note versus long-answer format and marks. Do not include feedback about the student's performance inside the model answer.",
    "Return textbookSources with one to three entries identifying the textbook basis of this answer: book (the exact approved title) and topic (the relevant topic covered by the answer). Select only relevant books, not the whole list. These are general textbook references based on your knowledge: no full textbook has been supplied or retrieved. Do not claim you consulted a book or verified a chapter, edition, quotation, page number, or URL. Do not invent those details. If a detail cannot be supported confidently, explicitly flag the uncertainty rather than inventing a citation or a medical fact.",
  ].join("\n\n");
}

export function textbookSourceSchema(subjectTitle) {
  const titles = theoryTextbooks(subjectTitle);
  return { type: "array", minItems: 1, maxItems: 3, items: {
    type: "object", required: ["book", "topic"], properties: {
      book: { type: "string", ...(titles.length ? { enum: titles } : {}) },
      topic: { type: "string" },
    },
  } };
}

export function normalizeTextbookSources(value, subjectTitle) {
  const titles = theoryTextbooks(subjectTitle);
  if (!Array.isArray(value) || value.length < 1 || value.length > 3) throw new Error("The AI examiner did not identify its textbook references. Please try again.");
  const sources = value.map(source => ({ book: String(source?.book ?? "").trim(), topic: String(source?.topic ?? "").trim() }));
  if (sources.some(source => source.book.length < 5 || source.book.length > 200 || source.topic.length < 3 || source.topic.length > 300
    || (titles.length && !titles.includes(source.book))) || new Set(sources.map(source => source.book)).size !== sources.length) {
    throw new Error("The AI examiner returned invalid textbook references. Please try again.");
  }
  return sources;
}
