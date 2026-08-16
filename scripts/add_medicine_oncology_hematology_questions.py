import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Oncology and Hematology"
CHAPTER_ORDER = 4
SOURCE_PDF = "medicine 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("Neoplastic Disorders", [
        q("Which feature best separates a malignant tumor from a benign tumor?", "Invasion with potential for metastasis", ["Slow growth alone", "Presence of a capsule", "Uniform cell size"], "Malignancy is defined by invasive behavior and capacity for spread."),
        q("A 58-year-old smoker has weight loss, hemoptysis and a hilar mass. Which initial tissue diagnosis approach is most appropriate?", "Bronchoscopy with biopsy if the lesion is endobronchial or central", ["Empiric chemotherapy without histology", "Repeat chest x-ray after one year", "Therapeutic anticoagulation"], "Cancer treatment generally requires histologic confirmation and staging.", True),
        q("Match the marker with the malignancy: AFP is most associated with", "Hepatocellular carcinoma and nonseminomatous germ cell tumors", ["Multiple myeloma only", "Chronic lymphocytic leukemia", "Papillary thyroid carcinoma"], "AFP can support diagnosis and monitoring in HCC and yolk sac/nonseminomatous germ cell tumors."),
        q("What does tumor staging primarily describe?", "Anatomic extent of disease", ["Cellular differentiation only", "Chemotherapy sensitivity", "Inherited risk alone"], "Stage summarizes tumor size/local extension, nodal disease and metastasis."),
        q("A woman with breast cancer has back pain, hypercalcemia and lytic vertebral lesions. The most likely explanation is", "Bone metastases with osteolysis", ["Vitamin D deficiency only", "Acute leukemia transformation", "Iron overload"], "Breast cancer commonly metastasizes to bone and can cause hypercalcemia.", True),
        q("Which statement about paraneoplastic syndromes is correct?", "They are remote effects of cancer not directly caused by local tumor invasion", ["They require visible metastasis", "They are always due to infection", "They prove the tumor is benign"], "Paraneoplastic syndromes arise from tumor-secreted hormones, cytokines or immune cross-reactivity."),
        q("Small-cell lung cancer is classically associated with which paraneoplastic endocrine syndrome?", "SIADH", ["Primary hypothyroidism", "Addison disease from adrenal autoimmunity", "Pseudohypoparathyroidism"], "Small-cell lung cancer may produce ADH, causing hyponatremia."),
        q("A patient starting chemotherapy for bulky lymphoma develops hyperkalemia, hyperphosphatemia, hypocalcemia and acute kidney injury. Name the emergency.", "Tumor lysis syndrome", ["Superior vena cava syndrome", "Carcinoid syndrome", "Nephrotic syndrome"], "Rapid tumor breakdown releases intracellular potassium, phosphate and nucleic acids.", True),
        q("Which cancer screening principle is most important before population screening is adopted?", "The test should reduce morbidity or mortality in the target population", ["The test should detect every benign lesion", "False positives should be ignored", "Screening should begin at birth for all cancers"], "Screening must show meaningful outcome benefit and acceptable harms."),
        q("Choose the best pair: chronic hepatitis B infection increases risk of", "Hepatocellular carcinoma", ["Glioblastoma", "Osteosarcoma", "Basal cell carcinoma"], "HBV promotes chronic hepatic injury and oncogenic pathways leading to HCC."),
        q("A man with facial swelling, distended neck veins and dyspnea has a right upper mediastinal mass. What syndrome is this?", "Superior vena cava syndrome", ["Horner syndrome only", "Tumor lysis syndrome", "Carpal tunnel syndrome"], "Obstruction of SVC venous return causes head-neck swelling and venous distension.", True),
        q("Which molecular change directly activates a growth-promoting oncogene?", "Point mutation in RAS", ["Loss of both RB alleles only", "Germline BRCA1 deletion only", "Reduced telomerase in tumor cells"], "RAS gain-of-function mutations drive proliferative signaling."),
        q("A patient with colon cancer has mismatch repair deficiency. Which hereditary syndrome should be considered?", "Lynch syndrome", ["Li-Fraumeni syndrome", "MEN 2B", "Von Hippel-Lindau disease"], "Lynch syndrome is due to inherited mismatch repair defects and causes microsatellite instability.", True),
        q("Which treatment intent is palliative rather than curative?", "Radiotherapy to painful bone metastasis to relieve symptoms", ["Adjuvant chemotherapy after resected colon cancer", "Surgery for localized appendiceal tumor", "Definitive chemoradiation for localized lymphoma"], "Palliative treatment focuses on symptom relief and quality of life."),
        q("A patient with advanced cancer develops new confusion, constipation, polyuria and calcium 13.5 mg/dL. What is the immediate management priority?", "Treat severe hypercalcemia with IV fluids and antiresorptive therapy", ["Give oral iron", "Start high-calcium diet", "Delay treatment until biopsy"], "Malignancy-associated hypercalcemia can be life-threatening and requires urgent correction.", True),
    ]),
    ("Hematopoietic Disorders", [
        q("Microcytic anemia most commonly results from", "Iron deficiency", ["Vitamin B12 deficiency", "Aplastic anemia", "Acute hemolysis only"], "Iron deficiency is the commonest cause of microcytic hypochromic anemia."),
        q("A 35-year-old woman has fatigue, pica, low ferritin and high TIBC. Which diagnosis fits best?", "Iron deficiency anemia", ["Anemia of chronic inflammation", "Hereditary spherocytosis", "Polycythemia vera"], "Low ferritin with high TIBC strongly supports iron deficiency.", True),
        q("Which lab pattern favors anemia of chronic inflammation over iron deficiency?", "Low serum iron with normal or high ferritin", ["Low ferritin with high TIBC", "High reticulocyte count with schistocytes", "Macro-ovalocytes with hypersegmented neutrophils"], "Ferritin is an acute-phase reactant and iron is sequestered in inflammatory states.", True),
        q("Vitamin B12 deficiency may cause neurologic disease because it impairs", "Myelin maintenance in dorsal columns and corticospinal tracts", ["Platelet adhesion only", "Globin chain synthesis only", "Neutrophil migration only"], "B12 deficiency can cause subacute combined degeneration."),
        q("A vegan patient has paresthesias, macrocytosis and hypersegmented neutrophils. What should be checked or treated?", "Vitamin B12 deficiency", ["Isolated iron overload", "Essential thrombocythemia", "Acute blood loss only"], "Dietary deficiency can cause megaloblastic anemia with neurologic symptoms.", True),
        q("Reticulocytosis in anemia usually indicates", "Increased marrow response to blood loss or hemolysis", ["Marrow aplasia", "Absent erythropoietin effect", "Pure iron deficiency without treatment"], "Reticulocytes rise when marrow responds appropriately to red cell loss or destruction."),
        q("Schistocytes on peripheral smear point toward", "Microangiopathic hemolysis", ["Simple iron deficiency only", "Thalassemia trait only", "B12 deficiency only"], "Fragmented RBCs arise from mechanical shearing in small vessels."),
        q("A patient has anemia, thrombocytopenia, renal injury and schistocytes after bloody diarrhea. Which condition is likely?", "Hemolytic uremic syndrome", ["Hereditary elliptocytosis", "Multiple myeloma only", "Immune thrombocytopenia"], "HUS causes microangiopathic hemolysis, thrombocytopenia and kidney injury.", True),
        q("Which finding suggests hemolysis?", "High indirect bilirubin with elevated LDH and low haptoglobin", ["High ferritin alone", "Low MCV alone", "Normal reticulocytes in all cases"], "Hemolysis releases LDH, consumes haptoglobin and raises unconjugated bilirubin."),
        q("Multiple myeloma classically causes the CRAB features. What does B represent?", "Bone lesions", ["Bleeding time", "Basophilia", "Bilirubin rise"], "CRAB means hyperCalcemia, Renal dysfunction, Anemia and Bone lesions."),
        q("An older adult has back pain, anemia, renal dysfunction and an M spike. Which test helps confirm clonal plasma cells?", "Bone marrow examination", ["D-dimer alone", "Sweat chloride test", "Skin prick test"], "Myeloma diagnosis uses monoclonal protein assessment plus marrow/plasma cell criteria.", True),
        q("Which leukemia is associated with Auer rods and risk of DIC?", "Acute promyelocytic leukemia", ["Chronic lymphocytic leukemia", "Hairy cell leukemia", "Adult T-cell leukemia only"], "APL has abnormal promyelocytes and can trigger severe coagulopathy."),
        q("Philadelphia chromosome produces which fusion gene?", "BCR-ABL1", ["PML-RARA", "JAK2-V617F", "MYD88-L265P"], "t(9;22) creates BCR-ABL1 tyrosine kinase, classically in CML."),
        q("A patient has massive splenomegaly, leukocytosis with left shift and low leukocyte alkaline phosphatase. Which diagnosis is most likely?", "Chronic myeloid leukemia", ["Leukemoid reaction", "Iron deficiency anemia", "Immune thrombocytopenia"], "CML causes granulocytic proliferation, splenomegaly and BCR-ABL1 positivity.", True),
        q("Pancytopenia with hypocellular marrow is most consistent with", "Aplastic anemia", ["Polycythemia vera", "Essential thrombocythemia", "Iron deficiency alone"], "Aplastic anemia is marrow failure with reduced hematopoietic cells across lineages."),
    ]),
    ("Disorders of Hemostasis", [
        q("Primary hemostasis depends most directly on", "Platelet adhesion, activation and aggregation", ["Fibrin cross-linking only", "Red cell deformability", "Albumin synthesis"], "Platelets form the initial plug at sites of vascular injury."),
        q("A child has recurrent epistaxis, petechiae and isolated thrombocytopenia after viral illness. Which diagnosis is likely?", "Immune thrombocytopenia", ["Hemophilia A", "Factor XIII deficiency", "Vitamin K deficiency"], "ITP commonly presents with mucocutaneous bleeding and low platelets.", True),
        q("Which bleeding pattern is typical of platelet disorders?", "Petechiae and mucosal bleeding", ["Deep muscle hematomas only", "Hemarthroses as the dominant feature", "Delayed umbilical stump bleeding only"], "Platelet defects cause superficial skin and mucosal bleeding."),
        q("Which bleeding pattern is typical of coagulation factor deficiency?", "Deep tissue bleeding and hemarthrosis", ["Tiny petechiae only", "Isolated gum bleeding after brushing", "No postoperative bleeding"], "Coagulation factor defects cause deep, delayed or joint bleeding."),
        q("A boy has recurrent hemarthroses, normal platelet count and prolonged aPTT. What is the likely disorder?", "Hemophilia A or B", ["Immune thrombocytopenia", "Thrombotic thrombocytopenic purpura", "Bernard-Soulier syndrome"], "Hemophilia causes intrinsic pathway prolongation with deep bleeding.", True),
        q("von Willebrand factor normally helps platelets adhere to", "Subendothelial collagen through platelet GPIb", ["Albumin through GPIIb/IIIa", "Red cells through spectrin", "Fibrinogen through factor XII"], "vWF bridges exposed collagen to platelet GPIb."),
        q("A woman has lifelong heavy menstrual bleeding, easy bruising and prolonged bleeding after dental extraction. Which test abnormality may be present?", "Prolonged bleeding time with possible prolonged aPTT", ["Isolated prolonged PT only", "High platelet count always", "Absent fibrinogen in every case"], "vWD causes mucocutaneous bleeding and may reduce factor VIII, prolonging aPTT.", True),
        q("Warfarin therapy is monitored primarily with", "PT/INR", ["Bleeding time", "Thrombin time only", "Platelet aggregation study only"], "Warfarin reduces vitamin K-dependent factors and prolongs PT/INR."),
        q("Unfractionated heparin therapy is commonly monitored with", "aPTT", ["Serum ferritin", "Direct bilirubin", "MCV"], "Heparin potentiates antithrombin and prolongs intrinsic pathway clotting tests."),
        q("A hospitalized patient on heparin develops a platelet fall and new thrombosis after 7 days. What is the concern?", "Heparin-induced thrombocytopenia", ["Simple dilutional anemia", "Vitamin B12 deficiency", "Warfarin skin necrosis before warfarin"], "HIT is immune-mediated platelet activation causing thrombocytopenia and thrombosis.", True),
        q("Disseminated intravascular coagulation usually shows", "Prolonged PT and aPTT, thrombocytopenia, low fibrinogen and high D-dimer", ["Normal D-dimer always", "High fibrinogen with normal PT", "Isolated high platelets"], "DIC consumes platelets and clotting factors while generating fibrin degradation products."),
        q("A septic patient bleeds from venipuncture sites with low platelets, prolonged PT/aPTT and high D-dimer. Diagnosis?", "Disseminated intravascular coagulation", ["Immune thrombocytopenia only", "Hemophilia carrier state", "Essential thrombocythemia"], "Sepsis-triggered systemic coagulation activation can cause DIC.", True),
        q("Vitamin K deficiency first prolongs which routine coagulation test?", "PT", ["Bleeding time", "Eosinophil count", "Reticulocyte index"], "Factor VII has a short half-life, so PT rises early in vitamin K deficiency."),
        q("Which inherited thrombophilia is due to resistance to activated protein C?", "Factor V Leiden", ["Hemophilia A", "Glanzmann thrombasthenia", "Wiskott-Aldrich syndrome"], "Factor V Leiden mutation prevents normal inactivation by activated protein C."),
        q("A young woman has recurrent unprovoked venous thrombosis and miscarriages with prolonged aPTT. Which disorder should be suspected?", "Antiphospholipid syndrome", ["von Willebrand disease", "Iron deficiency", "Bernard-Soulier syndrome"], "Antiphospholipid antibodies can prolong phospholipid-based tests while causing thrombosis and pregnancy loss.", True),
    ]),
]


def build_questions():
    questions = []
    for topic_order, (topic, rows) in enumerate(TOPICS, 1):
        if len(rows) != 15:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 15")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 6:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 6")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"medicine-oncology-hematology-{topic_slug}-{question_order:02d}",
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "chapterTitle": CHAPTER,
                "chapterOrder": CHAPTER_ORDER,
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "source": "ai",
                "sourcePdf": SOURCE_PDF,
                "imageUrls": [],
                **row,
            })
    return questions


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    questions = build_questions()
    data["questions"] = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("chapterTitle") == CHAPTER)
    ] + questions
    if len(questions) != 45:
        raise AssertionError(f"Expected 45 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 45:
        raise AssertionError("Duplicate oncology/hematology question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 45 Oncology and Hematology questions.")


if __name__ == "__main__":
    main()
