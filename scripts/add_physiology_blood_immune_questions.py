import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Blood and Immune System"
CHAPTER_ORDER = 6
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 107
SOURCE_PAGE_END = 184

BASE = {
    "subjectId": "physiology",
    "subjectTitle": "Physiology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": SOURCE_PDF,
    "sourcePdfPageStart": SOURCE_PAGE_START,
    "sourcePdfPageEnd": SOURCE_PAGE_END,
    "chapterOrder": CHAPTER_ORDER,
    "imageUrls": [],
}


def q(prompt, answer, wrong, explanation, clinical=False, difficulty="moderate"):
    return {
        "prompt": prompt,
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("plasma-proteins", "Plasma and Plasma Proteins", 1, [
        q("What is plasma?", "Fluid part of blood containing clotting factors", ["Blood without fibrinogen", "Packed red cells only", "Lymph inside lymph nodes"], "Plasma is the fluid part of blood; serum is plasma after clotting factors, especially fibrinogen, are removed."),
        q("Serum differs from plasma mainly because serum lacks:", "Fibrinogen and clotting factors", ["Albumin only", "Globulins only", "Electrolytes",], "Serum is obtained after clotting and therefore lacks fibrinogen and several clotting factors."),
        q("Which plasma protein is most important for maintaining colloid osmotic pressure?", "Albumin", ["Fibrinogen", "Prothrombin", "Gamma globulin"], "Albumin is the major plasma protein fraction and is chiefly responsible for plasma oncotic pressure."),
        q("A patient with severe hypoalbuminaemia develops pedal edema. Which function is lost?", "Maintenance of plasma oncotic pressure", ["Oxygen transport", "Platelet plug formation", "ABO agglutination"], "Low albumin lowers colloid osmotic pressure, favoring movement of fluid into tissues.", True),
        q("Which plasma protein fraction contains most antibodies?", "Gamma globulins", ["Albumin", "Fibrinogen", "Prothrombin"], "Immunoglobulins are present in the globulin fraction, especially gamma globulins."),
        q("Which plasma protein is converted to fibrin during coagulation?", "Fibrinogen", ["Albumin", "Ceruloplasmin", "Transferrin"], "Fibrinogen is converted into fibrin during the final stage of clot formation."),
        q("Most plasma proteins are synthesized mainly in the:", "Liver", ["Kidney", "Spleen", "Bone marrow"], "The chapter states that most plasma proteins are synthesized in the liver; immunoglobulins are an exception."),
        q("A patient with unconjugated bilirubin excess depends on plasma transport before hepatic uptake. Which plasma protein carries bilirubin, fatty acids and many drugs?", "Albumin", ["Fibrinogen", "Prothrombin", "IgE"], "Albumin has important transport functions for several poorly soluble substances.", True),
        q("A patient with advanced liver disease has edema and bleeding tendency. Which combined plasma protein defect explains this best?", "Reduced albumin and clotting factor synthesis", ["Excess RBC production", "Excess platelet production", "Increased ABO antigens"], "Liver disease can reduce albumin and clotting protein synthesis, causing edema and coagulation defects.", True),
        q("Which dietary factor most directly supports synthesis of plasma proteins?", "Adequate protein intake", ["Low oxygen tension only", "High bilirubin", "ABO incompatibility"], "Dietary proteins are listed among factors affecting plasma protein synthesis."),
    ]),
    ("red-cells-anaemias", "Red Blood Cells and Anaemias", 2, [
        q("Normal mature red blood cells are best described as:", "Biconcave non-nucleated discs", ["Nucleated spherical cells", "Granular leukocytes", "Fragments of megakaryocytes"], "RBCs are biconcave discs and lack nuclei, improving deformability and gas transport."),
        q("What is packed cell volume also called?", "Haematocrit", ["Colour index", "ESR", "MCHC"], "Packed cell volume is the haematocrit: the fraction of blood volume occupied by RBCs."),
        q("Which index reflects average volume of a red blood cell?", "Mean corpuscular volume", ["MCHC", "Colour index", "Bleeding time"], "MCV denotes the average red cell volume."),
        q("An increased ESR is clinically useful because it often indicates:", "Inflammation or tissue disease activity", ["Specific ABO group", "Exact haemoglobin genotype", "Platelet count only"], "ESR has clinical significance as a nonspecific marker that rises in several inflammatory and disease states.", True),
        q("Which hormone chiefly regulates erythropoiesis?", "Erythropoietin", ["Thrombopoietin", "Insulin", "Calcitonin"], "Erythropoietin is the main regulator of red cell formation."),
        q("Deficiency of vitamin B12 or folic acid classically causes:", "Megaloblastic anaemia", ["Iron deficiency anaemia", "Haemophilia", "Leukemoid reaction"], "Vitamin B12 and folate are special maturation factors; deficiency causes megaloblastic anaemia.", True),
        q("Iron deficiency anaemia is typically classified morphologically as:", "Microcytic hypochromic anaemia", ["Macrocytic hyperchromic anaemia", "Normocytic polycythaemia", "Thrombocytopenia"], "Iron deficiency impairs haemoglobinization, producing small pale RBCs.", True),
        q("The usual life span of an RBC is about:", "120 days", ["7 days", "10 hours", "1 year"], "Human RBCs circulate for about 120 days before removal."),
        q("Unconjugated bilirubin formation is mainly related to breakdown of:", "Haemoglobin from old RBCs", ["Albumin", "Platelets", "Fibrin"], "Bilirubin is formed during haem breakdown after destruction of senescent RBCs."),
        q("Physiological jaundice of newborn is related mainly to immature handling of:", "Bilirubin", ["Albumin", "Sodium", "ABO antigens"], "The chapter discusses neonatal physiological jaundice under bilirubin and jaundice mechanisms.", True),
    ]),
    ("white-blood-cells", "White Blood Cells", 3, [
        q("Which cells are granulocytes?", "Neutrophils, eosinophils and basophils", ["Lymphocytes and monocytes only", "RBCs and platelets", "Megakaryocytes only"], "WBCs are divided into granulocytes and agranulocytes; neutrophils, eosinophils and basophils are granulocytes."),
        q("Which WBC is most important in acute bacterial phagocytosis?", "Neutrophil", ["Eosinophil", "Basophil", "Erythrocyte"], "Neutrophils are key phagocytic cells and rise in many acute bacterial infections.", True),
        q("Which WBC commonly increases in allergic disorders and parasitic infestations?", "Eosinophil", ["Neutrophil", "Monocyte", "Platelet"], "Eosinophilia is classically associated with allergy and parasitic disease.", True),
        q("Basophils and mast cells are especially associated with release of:", "Histamine and heparin", ["Haemoglobin", "Erythropoietin", "Fibrin"], "Basophils contain mediators such as histamine and heparin and are related to allergic responses."),
        q("Which cells become macrophages in tissues?", "Monocytes", ["Eosinophils", "Basophils", "Reticulocytes"], "Monocytes enter tissues and form macrophages in the monocyte-macrophage system."),
        q("Which WBC is central to acquired immunity?", "Lymphocyte", ["RBC", "Platelet", "Reticulocyte"], "Lymphocytes, including B and T cells, mediate acquired immune responses."),
        q("Leucocytosis means:", "Increase in total WBC count", ["Decrease in WBC count", "Increase in RBC fragility", "Low platelet count"], "Leucocytosis is an increase in white blood cell count."),
        q("Leucopenia means:", "Decrease in WBC count", ["Increase in WBC count", "Increase in ESR", "Agglutination of RBCs"], "Leucopenia is a decrease in total white blood cell count."),
        q("A patient on chemotherapy develops low neutrophil count and recurrent infections. The relevant abnormality is:", "Neutropenia", ["Eosinophilia", "Polycythaemia", "Thrombocytosis"], "Neutropenia reduces antibacterial defense and predisposes to infection.", True),
        q("Which factors regulate leucopoiesis prominently?", "Cytokines", ["ABO agglutinins", "Bilirubin", "Albumin only"], "The chapter highlights cytokines in regulation of leucopoiesis."),
    ]),
    ("immune-mechanisms", "Immune Mechanisms", 4, [
        q("Innate immunity is best described as:", "Inborn nonspecific defense", ["Antibody from vaccination only", "Transferred maternal IgG only", "ABO agglutination"], "Innate immunity consists of nonspecific mechanisms present from birth."),
        q("Active acquired immunity develops when:", "The body produces its own immune response", ["Ready-made antibodies are transferred", "RBCs sediment faster", "Albumin falls"], "Active immunity is produced by the host after antigen exposure or vaccination."),
        q("Passive immunity is produced by:", "Transfer of ready-made antibodies", ["Formation of memory cells by infection", "Direct platelet adhesion", "Fibrin formation"], "Passive immunity results from receiving preformed antibodies, naturally or artificially."),
        q("Vaccination is an example of:", "Artificial active immunity", ["Natural passive immunity", "Artificial passive immunity only", "Innate immunity"], "Vaccination exposes the immune system to antigen and induces active immunity.", True),
        q("Maternal antibody crossing to fetus is an example of:", "Natural passive immunity", ["Artificial active immunity", "Autoimmunity", "Hypersensitivity"], "Maternal antibodies provide natural passive immunity to the fetus/newborn.", True),
        q("Which molecule class is antibody?", "Immunoglobulin", ["Albumin", "Fibrinogen", "Haemoglobin"], "Antibodies are immunoglobulins made of heavy and light chains."),
        q("Humoral immunity mainly depends on:", "B lymphocytes and antibodies", ["Platelet plugs", "RBC membrane proteins", "Smooth muscle calcium"], "Humoral immune response involves B cell activation and antibody production."),
        q("Cell-mediated immunity mainly depends on:", "T lymphocytes", ["RBCs", "Fibrinogen", "Albumin"], "Cellular immune response is mediated by T lymphocytes, including cytotoxic and helper T cells."),
        q("Loss of tolerance to self-antigens may lead to:", "Autoimmunity", ["Physiological jaundice", "Isotonicity", "Rouleaux only"], "Autoimmunity occurs when tolerance mechanisms fail and immune attack is directed against self.", True),
        q("HLA tissue typing is especially important in:", "Transplant matching", ["ESR measurement", "Haemoglobin synthesis", "Osmotic fragility testing"], "Histocompatibility antigens and HLA typing are important for graft/transplant compatibility.", True),
    ]),
    ("platelets-haemostasis", "Platelets, Haemostasis and Blood Coagulation", 5, [
        q("Platelets are derived from:", "Megakaryocytes", ["Neutrophils", "Reticulocytes", "Plasma cells"], "Platelets are cytoplasmic fragments produced from megakaryocytes."),
        q("The normal platelet count is approximately:", "150,000-400,000 per microlitre", ["4,000-11,000 per microlitre", "5 million per microlitre", "120 per microlitre"], "The chapter gives the normal platelet count in the usual range of about 1.5-4 lakh per microlitre."),
        q("The first event in haemostasis after vascular injury is:", "Vasoconstriction", ["Fibrinolysis", "ABO grouping", "Erythropoiesis"], "Haemostasis begins with vasoconstriction, followed by platelet plug and coagulation."),
        q("Temporary haemostatic plug formation mainly depends on:", "Platelet adhesion and aggregation", ["Albumin synthesis", "RBC destruction", "Bilirubin conjugation"], "Platelets adhere and aggregate to form the temporary haemostatic plug."),
        q("The definitive haemostatic plug is stabilized by:", "Fibrin", ["Albumin", "IgE", "Oxyhaemoglobin"], "Coagulation forms fibrin, which stabilizes the platelet plug."),
        q("Vitamin K is required for normal synthesis of several clotting factors in the:", "Liver", ["Spleen", "Thymus", "Kidney tubule only"], "Vitamin K supports hepatic synthesis/activation of vitamin K dependent clotting factors.", True),
        q("Haemophilia A is due to deficiency of:", "Factor VIII", ["Factor IX", "Platelets", "Albumin"], "The chapter lists haemophilia A as factor VIII deficiency.", True),
        q("Haemophilia B is due to deficiency of:", "Factor IX", ["Factor VIII", "Fibrinogen only", "Vitamin B12"], "Haemophilia B is Christmas disease due to factor IX deficiency."),
        q("Heparin acts physiologically as a/an:", "Anticoagulant", ["Agglutinin", "Oxygen carrier", "Erythropoietic hormone"], "Heparin is listed among circulating/endogenous anticoagulants."),
        q("A patient has low platelets with petechiae and prolonged bleeding time. The likely category is:", "Platelet disorder", ["ABO incompatibility only", "Megaloblastic anaemia only", "Hyperalbuminaemia"], "Platelet disorders cause purpura/petechiae and abnormal primary haemostasis.", True),
    ]),
    ("blood-groups-transfusion", "Blood Groups and Blood Transfusion", 6, [
        q("In ABO blood grouping, agglutinogens are present on:", "RBC membrane", ["Plasma albumin", "Platelet granules", "Neutrophil nucleus"], "A and B agglutinogens are antigens present on RBC surfaces."),
        q("Agglutinins in ABO grouping are present in:", "Plasma", ["RBC membrane", "Haemoglobin", "Bone marrow only"], "Anti-A and anti-B agglutinins are antibodies found in plasma."),
        q("Landsteiner law states that if an agglutinogen is present on RBCs, the corresponding agglutinin is:", "Absent from plasma", ["Always present in plasma", "Present on platelets", "Converted to fibrin"], "Landsteiner law describes reciprocal presence of ABO antigens and antibodies."),
        q("A person with blood group O has which ABO antigens on RBCs?", "Neither A nor B", ["A only", "B only", "Both A and B"], "Group O RBCs lack A and B agglutinogens."),
        q("A person with blood group AB has which ABO antibodies in plasma?", "Neither anti-A nor anti-B", ["Anti-A only", "Anti-B only", "Both anti-A and anti-B"], "Group AB individuals have both A and B antigens and lack anti-A/anti-B antibodies."),
        q("The most important Rh antigen in clinical practice is:", "D antigen", ["A antigen", "B antigen", "H antigen"], "Rh grouping is chiefly concerned with the D antigen."),
        q("Haemolytic disease of newborn due to Rh incompatibility usually occurs when:", "Rh-negative mother carries Rh-positive fetus", ["Rh-positive mother carries Rh-negative fetus", "Both mother and fetus are Rh-negative", "Both are group O"], "Rh-negative mother can become immunized against fetal Rh-positive cells and affect later Rh-positive babies.", True),
        q("Prevention of Rh haemolytic disease of newborn uses:", "Anti-D immunoglobulin", ["Albumin infusion", "Heparin", "Vitamin B12"], "Anti-D prophylaxis prevents maternal sensitization to Rh-positive fetal RBCs.", True),
        q("The safest approach before transfusion is to perform:", "Blood grouping and cross-matching", ["ESR alone", "Osmotic fragility alone", "DLC only"], "Compatibility testing, including grouping and crossmatching, reduces transfusion reactions.", True),
        q("Fever, chills, haemolysis or shock after incompatible blood transfusion are examples of:", "Transfusion hazards", ["Normal active immunity", "Physiological jaundice only", "Platelet production"], "The chapter discusses hazards of transfusion, including reactions from incompatibility.", True),
    ]),
]


def build_questions():
    questions = []
    for slug, topic, topic_order, rows in TOPICS:
        for index, row in enumerate(rows, 1):
            shift = (topic_order + index) % 4
            options = row["options"][shift:] + row["options"][:shift]
            answer = row["answer"]
            questions.append({
                **BASE,
                **row,
                "id": f"physiology-blood-immune-{slug}-{index:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "options": options,
                "answerIndex": options.index(answer),
                "answer": answer,
            })
    return questions


def validate(questions):
    if len(TOPICS) != 6 or len(questions) != 60:
        raise ValueError("Expected 6 topics and 60 questions")
    if len({q["id"] for q in questions}) != 60:
        raise ValueError("Duplicate ids")
    for _, topic, _, _ in TOPICS:
        topic_questions = [q for q in questions if q["topic"] == topic]
        if len(topic_questions) != 10:
            raise ValueError(f"{topic} must have 10 questions")
        if sum("clinical" in q.get("tags", []) for q in topic_questions) < 3:
            raise ValueError(f"{topic} must have at least 3 clinical questions")
    for question in questions:
        if question["answer"] != question["options"][question["answerIndex"]]:
            raise ValueError(f"Bad answer mapping: {question['id']}")


def update_file(path, questions):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ids = {q["id"] for q in questions}
    data["questions"] = [q for q in data.get("questions", []) if q.get("id") not in ids] + questions
    data["questions"].sort(key=lambda item: item.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    questions = build_questions()
    validate(questions)
    for path in DATA_PATHS:
        update_file(path, questions)
        print(f"Added {len(questions)} physiology questions to {path}.")
    for _, topic, _, _ in TOPICS:
        print(f"- {topic}: 10 questions")


if __name__ == "__main__":
    main()
