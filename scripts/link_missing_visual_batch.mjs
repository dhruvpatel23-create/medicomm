import fs from "node:fs";

const assignments = {
  "ini-cet-2021-biochemistry-q009": "Michaelis-Menten kinetics graph restored; hyperbolic velocity curve, Vmax, half-Vmax, and Km relationships preserved.",
  "ini-cet-2022-biochemistry-q012": "Competitive-inhibition Lineweaver-Burk plot restored; shared Vmax intercept and increased apparent Km preserved.",
  "neet-pg-2020-pharmacology-q018": "Graded dose-response graph restored; parallel A, B, and C curves with equal efficacy and left-to-right potency order preserved.",
  "neet-pg-2021-pharmacology-q006": "Clinical angioedema image restored; characteristic lip and lower-face swelling preserved.",
  "aiims-2018-pathology-q008": "Asbestosis lung micrograph restored; interstitial fibrosis and diagnostic ferruginous bodies preserved.",
  "neet-pg-2019-pathology-q003": "Prussian-blue liver micrograph restored; hepatocellular iron deposits and hepatic architecture preserved.",
  "ini-cet-2022-pathology-q036": "CLL peripheral smear restored; mature lymphocytosis and diagnostic smudge cells preserved.",
  "neet-pg-2024-pathology-q020": "Aortic-dissection histology restored; intimal tear, medial separation, and blood-filled false channel preserved.",
  "neet-pg-2024-pathology-q030": "Advanced asbestosis lung micrograph restored; diffuse fibrosis and ferruginous bodies preserved.",
  "neet-pg-2024-pathology-q031": "Classical Hodgkin lymphoma micrograph restored; Reed-Sternberg owl-eye morphology and mixed inflammatory background preserved.",
  "aiims-2020-microbiology-q021": "Aseptic-meningitis clinical composite restored; non-hemorrhagic rash and characteristic CSF findings preserved.",
  "aiims-2020-microbiology-q023": "Zika transplacental-transmission diagram restored; Aedes vector, placental passage, and microcephaly relationship preserved.",
  "ini-cet-2021-microbiology-q006": "Ziehl-Neelsen sputum smear restored; bright acid-fast bacilli on a blue counterstained background preserved.",
  "ini-cet-2021-microbiology-q007": "Actinomyces sulfur-granule microscopy restored; central colony, radiating filaments, clubs, and neutrophils preserved.",
  "ini-cet-2022-microbiology-q012": "Fungal cell-envelope diagram restored; mannoprotein, beta-glucan, chitin, membrane, and ergosterol order preserved.",
  "ini-cet-2022-microbiology-q029": "Falciparum-malaria smear restored; delicate ring forms and double-dot headphone morphology preserved.",
  "ini-cet-2022-microbiology-q037": "Modified acid-fast Nocardia microscopy restored; weakly acid-fast branching beaded filaments preserved.",
};

const files = [
  "data/practice-question-bank.json",
  "public/practice-question-bank.json",
  "dist/practice-question-bank.json",
];

for (const file of files) {
  const database = JSON.parse(fs.readFileSync(file, "utf8"));
  const questions = database.subjects.flatMap((subject) => subject.questions ?? []);
  for (const [questionId, assetNote] of Object.entries(assignments)) {
    const question = questions.find((item) => item.id === questionId);
    if (!question) throw new Error(`${questionId} not found in ${file}`);
    const url = `/uploads/medicomm-atlas-${questionId}.png`;
    question.imageUrls = [url];
    question.images = [url];
    question.assetNote = `${assetNote} Subtle medicomm watermark lower-left.`;
  }
  fs.writeFileSync(file, `${JSON.stringify(database, null, 2)}\n`);
}

console.log(`Linked ${Object.keys(assignments).length} visuals across ${files.length} question banks.`);
