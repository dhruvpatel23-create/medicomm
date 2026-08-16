import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Immune-Mediated, Inflammatory, and Rheumatologic Disorders"
CHAPTER_ORDER = 11
SOURCE_PDF = "medicine 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False, page=None):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
        "sourcePdfPageStart": page,
        "sourcePdfPageEnd": page,
    }


TOPICS = [
    ("Immune System, Immunodeficiency and Allergy", [
        q("In Medicine 1 chapter 342, CD4 T cells are described as T lymphocytes that participate in adaptive immunity and help B cells make", "Antibody", ["Bile", "Renin", "Surfactant"], "The immune system glossary defines CD4 T cells as helper cells for adaptive immunity and antibody production.", page=2451),
        q("CD8 T cells are the cytotoxic T-cell subset that destroys tumor cells and cells infected with", "Intracellular pathogens", ["Extracellular sodium", "Urate crystals only", "Thyroid hormone"], "Chapter 342 identifies CD8 T cells as cytotoxic lymphocytes against tumor cells and cells infected with intracellular pathogens.", page=2451),
        q("Complement is a cascading series of plasma enzymes and effector proteins that lyses pathogens or targets them for", "Phagocytosis", ["Gluconeogenesis", "Ventilation", "Bilirubin conjugation"], "Medicine 1 defines complement as helping lyse pathogens and target them to phagocytes.", page=2451),
        q("A patient with endotoxin exposure develops overwhelming cytokine release and shock. In chapter 342, this is linked to massive LPS signaling through", "TLR4", ["HLA-B27", "BTK", "CysLT1"], "The innate immunity section states that massive LPS signaling through TLR4 leads to cytokine release mediating LPS-induced shock.", True, page=2454),
        q("NK cells are activated by contact with cells that lack expression of", "MHC class I", ["IgA", "C-reactive protein", "Uric acid"], "Chapter 343 notes that NK cells are activated by cells lacking MHC class I and inhibited by cells expressing it.", page=2484),
        q("HLA-B27 is very highly associated with ankylosing spondylitis and", "Reactive arthritis", ["X-linked agammaglobulinemia", "Mastocytosis", "Celiac crisis only"], "Medicine 1 describes HLA-B27 association with ankylosing spondylitis, reactive arthritis, undifferentiated spondyloarthropathy and recurrent anterior uveitis.", page=2487),
        q("A newborn screened for severe combined immunodeficiency has low T-cell receptor excision circles. The screening test measures", "TREC", ["INR", "DLCO", "BISAP"], "Chapter 344 describes T-cell receptor excision circle quantification on a Guthrie card as a reliable newborn screening test for SCID.", True, page=2493),
        q("The most frequent SCID phenotype, absence of both T and NK cells, results from deficiency of the common gamma-chain receptor or", "JAK3", ["BTK", "HLA-B27", "C5a"], "Medicine 1 states that the common gamma-chain receptor or JAK3 deficiency produces the common T- and NK-cell absent SCID phenotype.", page=2493),
        q("A boy has recurrent bacterial infections with profound B-cell deficiency and absent BTK expression in monocytes. The best diagnosis is", "X-linked agammaglobulinemia", ["Giant cell arteritis", "Osteoarthritis", "Behcet syndrome"], "Chapter 344 states that most agammaglobulinemia is caused by BTK mutations on the X chromosome, with BTK testing by intracellular immunofluorescence.", True, page=2496),
        q("A patient with anaphylaxis should receive a self-injectable prescription for", "Epinephrine", ["Allopurinol", "Warfarin", "Methotrexate"], "Medicine 1 recommends self-injectable epinephrine for most patients at increased risk of anaphylaxis.", True, page=2510),
    ]),
    ("Systemic Autoimmune and Vasculitic Disorders", [
        q("A central feature of the immune system is mounting responses to harmful foreign material while avoiding damage to", "Self", ["Calcium", "Albumin", "Insulin"], "Chapter 348 opens by emphasizing immune defense against foreign material while avoiding damage to self.", page=2510),
        q("Excess B cell activating factor can impair B-cell tolerance and lead to", "Autoimmunity", ["Achalasia", "Gout", "Aortic stenosis"], "The autoimmunity chapter states that excess BAFF can impair B-cell tolerance and promote autoimmunity.", page=2512),
        q("Negative selection of autoreactive T cells in the thymus requires expression of the", "AIRE gene", ["BTK gene", "PKD1 gene", "VHL gene"], "Medicine 1 notes that thymic negative selection of autoreactive T cells requires autoimmune regulator, AIRE.", page=2512),
        q("A young woman with SLE risk factors has strong type I interferon gene-expression activity. Which pathway is described as especially characteristic in SLE?", "Interferon production", ["Bile acid transport", "Urea recycling", "Surfactant secretion"], "Chapter 349 highlights interferon production as the most characteristic gene-expression pattern in SLE patients.", True, page=2516),
        q("The most frequent hematologic manifestation of systemic lupus erythematosus is", "Normochromic normocytic anemia", ["Polycythemia", "Eosinophilic leukemia", "Isolated macrocytosis from B12 excess"], "Medicine 1 states that anemia, usually normochromic normocytic and reflecting chronic illness, is the most frequent hematologic manifestation of SLE.", page=2522),
        q("A patient with SLE flare develops diffuse abdominal pain from suspected intestinal vasculitis. Which short-term therapy is recommended for control?", "High-dose glucocorticoids", ["No therapy because vasculitis is benign", "Oral iron only", "Beta blocker monotherapy"], "Chapter 349 notes that intestinal vasculitis in SLE can be life-threatening and recommends aggressive immunosuppression with high-dose glucocorticoids for short-term control.", True, page=2522),
        q("Laboratory criteria for antiphospholipid syndrome include lupus anticoagulant, anticardiolipin and", "Anti-beta2 glycoprotein I antibodies", ["Anti-mitochondrial antibodies only", "Anti-centromere only", "Anti-HMGCR only"], "The APS chapter lists LA, anticardiolipin and anti-beta2 glycoprotein I antibodies at significant titers on two occasions 12 weeks apart.", page=2527),
        q("After a first thrombotic event in antiphospholipid syndrome, Medicine 1 recommends lifelong", "Warfarin", ["Acetaminophen", "Inhaled salbutamol", "Pancreatic enzymes"], "The APS treatment section recommends lifelong warfarin after the first thrombotic event.", True, page=2527),
        q("Diffuse cutaneous systemic sclerosis is associated with early interstitial lung disease and acute", "Renal involvement", ["Appendicitis", "Migraine", "Otitis externa"], "Chapter 353 contrasts diffuse cutaneous SSc, in which ILD and acute renal involvement develop relatively early, with limited cutaneous SSc.", page=2546),
        q("A patient older than 50 has new headache, fever, anemia and very high ESR. Which vasculitis is classically described by this complex?", "Giant cell arteritis", ["Reactive arthritis", "Fibromyalgia", "X-linked agammaglobulinemia"], "Medicine 1 describes giant cell arteritis as fever, anemia, high ESR and headache in a patient older than 50 years.", True, page=2584),
    ]),
    ("Musculoskeletal, Joint and Crystal Disorders", [
        q("Medicine 1 chapter 363 lists urgent red-flag musculoskeletal diagnoses including septic arthritis, acute crystal-induced arthritis and", "Fracture", ["Dry mouth", "Urticaria", "Rhinitis"], "The musculoskeletal approach chapter identifies septic arthritis, crystal arthritis and fracture as red-flag diagnoses requiring prompt diagnosis.", page=2614),
        q("Acute monarticular inflammatory arthritis often requires", "Arthrocentesis", ["Bronchoscopy", "ERCP", "Lumbar sympathectomy"], "Chapter 363 states that acute monarticular inflammatory arthritis may require arthrocentesis, especially when infection is suspected.", page=2617),
        q("Low-titer positive rheumatoid factor and ANA may be seen in up to 15% of", "Elderly patients", ["Newborns only", "Patients after appendectomy only", "Patients with asthma only"], "The geriatric rheumatology section warns that low-titer RF and ANA may be seen in up to 15% of elderly patients.", page=2617),
        q("An elderly patient has a hot swollen single knee with fever. Which step is most important to avoid missing septic arthritis or gout?", "Prompt arthrocentesis", ["Reassurance without evaluation", "Capsule endoscopy", "Spirometry"], "Medicine 1 treats acute monarticular inflammatory arthritis as a red flag requiring arthrocentesis when infection is possible.", True, page=2617),
        q("MRI or ultrasound best confirms suspected tear or tendinitis of the", "Rotator cuff", ["Mitral valve", "Pancreatic duct", "Renal artery"], "The shoulder pain section states that rotator cuff tendinitis or tear is best confirmed by MRI or ultrasound.", page=2620),
        q("The goals of osteoarthritis treatment are to alleviate pain and minimize loss of", "Physical function", ["Hepatic bile flow", "Alveolar ventilation", "Renal erythropoietin"], "Chapter 364 states that OA treatment aims to alleviate pain and minimize loss of physical function.", page=2629),
        q("A patient with knee osteoarthritis has pain when walking down hills. The simplest useful nonpharmacologic approach is to avoid activities that", "Precipitate pain", ["Improve sleep", "Reduce urate", "Increase saliva"], "Medicine 1 notes that avoiding pain-provoking activities may eliminate symptoms in OA.", True, page=2629),
        q("Acute arthritis is the most common early clinical manifestation of", "Gout", ["IgG4-related disease", "Sjogren syndrome", "Relapsing polychondritis"], "Chapter 365 states that acute arthritis is the most common early clinical manifestation of gout.", page=2632),
        q("A patient wakes at night with dramatic pain, swelling, warmth and redness of the first metatarsophalangeal joint. Which diagnosis is most likely?", "Acute gouty arthritis", ["Fibromyalgia", "Scleroderma renal crisis", "Anaphylaxis"], "Medicine 1 describes acute gout as often beginning at night with dramatic pain and swelling, commonly involving the first MTP joint.", True, page=2632),
        q("A middle-aged patient has widespread pain without inflammatory arthritis, and drug therapy is considered. Which listed fibromyalgia drug is FDA-approved in the table?", "Duloxetine", ["Allopurinol", "Warfarin", "Penicillin V"], "Medicine 1 table 366-3 lists duloxetine, milnacipran and pregabalin as FDA-approved pharmacologic agents for fibromyalgia.", True, page=2639),
    ]),
]


def build_questions():
    questions = []
    for topic_order, (topic, rows) in enumerate(TOPICS, 1):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 4:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 4")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"medicine-immune-rheumatologic-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 30:
        raise AssertionError(f"Expected 30 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 30:
        raise AssertionError("Duplicate immune/rheumatologic question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 30 book-based Immune-Mediated, Inflammatory, and Rheumatologic Disorders questions.")


if __name__ == "__main__":
    main()
