import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Red Blood Cell and Bleeding Disorders"
BASE = {"subjectId": "pathology", "subjectTitle": "Pathology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(difficulty, prompt, answer, distractors, explanation):
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(difficulty)
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {"difficulty": difficulty, "prompt": prompt, "options": options, "answerIndex": 0, "answer": answer, "explanation": explanation}


def jumble(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    ("anemia-basics", "Anemia: Classification, Reticulocytes, and Morphology", [
        q("easy", "Anemia is best defined as:", "Reduced oxygen-carrying capacity of blood", ["Increased platelet count", "Increased leukocyte alkaline phosphatase", "Excess plasma fibrinogen"], "Anemia usually reflects reduced red cell mass or hemoglobin concentration."),
        q("easy", "Microcytic hypochromic anemia most often reflects defective:", "Hemoglobin synthesis", ["DNA synthesis", "Platelet adhesion", "Neutrophil migration"], "Iron deficiency and thalassemia produce small pale red cells by impairing hemoglobin production."),
        q("easy", "Macrocytic anemia commonly reflects defective:", "DNA synthesis", ["Globin chain polymerization", "Platelet aggregation", "Splenic filtration"], "Megaloblastic anemia produces large red cells due to impaired nuclear maturation."),
        q("moderate", "A high reticulocyte count in anemia suggests:", "Increased marrow response from blood loss or hemolysis", ["Marrow aplasia", "Severe iron lack without bleeding", "Pure renal failure"], "Reticulocytosis indicates that marrow is responding to red cell loss or destruction."),
        q("moderate", "A low reticulocyte count in anemia suggests:", "Reduced red cell production", ["Acute hemolysis only", "Massive splenic sequestration only", "Recent transfusion reaction only"], "Production failures such as marrow disease or nutrient deficiency often have inadequate reticulocytes."),
        q("moderate", "Anisocytosis means variation in red cell:", "Size", ["Color only", "Nuclear number", "Platelet granules"], "Anisocytosis is reflected by increased red cell distribution width."),
        q("moderate", "Poikilocytosis means variation in red cell:", "Shape", ["Count only", "Globin genotype only", "Platelet function"], "Poikilocytosis describes abnormal variation in erythrocyte shape."),
        q("high", "A patient with acute gastrointestinal bleeding develops anemia, and several days later the smear shows polychromasia with increased reticulocytes. Which marrow response explains the larger bluish circulating cells?", "Accelerated release of young red cells", ["Failure of erythropoietin secretion", "Defective heme synthesis", "Splenic destruction of platelets"], "Reticulocytes are young RNA-containing red cells released during a compensatory marrow response."),
        q("high", "A patient with fatigue has low hemoglobin, low MCV, pale red cells, and target cells. The pattern points away from pure DNA synthesis failure and toward abnormal hemoglobin accumulation. Which broad anemia category fits?", "Microcytic hypochromic anemia", ["Megaloblastic macrocytic anemia", "Aplastic normocytic anemia", "Immune thrombocytopenia"], "Microcytosis and hypochromia occur when hemoglobin synthesis is impaired."),
        q("high", "A patient has severe anemia with a very low reticulocyte count despite high erythropoietin levels. There is no bleeding or jaundice, and marrow examination shows markedly reduced erythroid precursors. Which mechanism is most likely?", "Inadequate red cell production", ["Compensated hemolysis", "Acute posthemorrhagic reticulocytosis", "Hypersplenic platelet pooling"], "Low reticulocytes in anemia indicate that marrow output is insufficient."),
    ]),
    ("iron-deficiency", "Iron Deficiency and Anemia of Chronic Inflammation", [
        q("easy", "The most common cause of anemia worldwide is:", "Iron deficiency", ["Vitamin B12 excess", "Hereditary spherocytosis", "Hemophilia A"], "Iron deficiency is the most common nutritional deficiency and anemia cause."),
        q("easy", "Iron deficiency anemia is typically:", "Microcytic and hypochromic", ["Macrocytic and hyperchromic", "Normocytic with spherocytes only", "Associated with giant platelets only"], "Reduced heme synthesis makes red cells small and pale."),
        q("easy", "Serum ferritin in uncomplicated iron deficiency is usually:", "Low", ["Very high", "Normal in every case", "Unmeasurable because ferritin is absent from humans"], "Ferritin reflects iron stores and falls in iron deficiency."),
        q("moderate", "Total iron-binding capacity in iron deficiency is usually:", "Increased", ["Decreased", "Always zero", "Unrelated to transferrin"], "The liver increases transferrin production when iron stores are low."),
        q("moderate", "Anemia of chronic inflammation is mediated largely by increased:", "Hepcidin", ["Intrinsic factor", "ADAMTS13", "Factor VIII"], "Hepcidin traps iron in macrophages and reduces intestinal absorption."),
        q("moderate", "Serum ferritin in anemia of chronic inflammation is usually:", "Normal or increased", ["Always absent", "Low in every case", "Only present after transfusion"], "Ferritin is an acute phase reactant and iron is stored rather than unavailable because stores are empty."),
        q("moderate", "Koilonychia is associated with:", "Iron deficiency", ["Hemophilia B", "TTP", "Vitamin K excess"], "Spoon nails are a classic physical finding in iron deficiency."),
        q("high", "A menstruating patient has fatigue, pica, koilonychia, low MCV, low serum iron, high TIBC, low transferrin saturation, and absent marrow iron stores. Which diagnosis best fits?", "Iron deficiency anemia", ["Anemia of chronic inflammation", "Beta-thalassemia minor", "Sideroblastic anemia"], "The combination of depleted stores and increased TIBC is typical of iron deficiency."),
        q("high", "A patient with rheumatoid arthritis has mild microcytic anemia, low serum iron, low TIBC, and increased ferritin. Iron is present in marrow macrophages but poorly available to erythroid precursors. Which mediator is central?", "Hepcidin", ["Erythropoietin excess", "Intrinsic factor antibody", "ADAMTS13 deficiency"], "Inflammation increases hepcidin, which blocks ferroportin-mediated iron release."),
        q("high", "An older man develops new iron deficiency anemia without obvious dietary restriction. The most important next concern is chronic occult blood loss from which source?", "Gastrointestinal tract malignancy or bleeding lesion", ["Thymic aplasia", "Pulmonary valve stenosis", "Congenital factor VIII deficiency"], "Iron deficiency in adult men or postmenopausal women should prompt evaluation for occult GI blood loss."),
    ]),
    ("megaloblastic", "Megaloblastic Anemias: Vitamin B12 and Folate", [
        q("easy", "Megaloblastic anemia is caused by impaired:", "DNA synthesis", ["Platelet adhesion", "Iron absorption only", "Globin polymerization"], "B12 and folate deficiencies impair thymidylate synthesis and nuclear maturation."),
        q("easy", "Pernicious anemia is caused by autoimmune loss of:", "Intrinsic factor-producing parietal cells", ["Splenic macrophages", "Platelet alpha granules", "ADAMTS13"], "Autoimmune gastritis destroys parietal cells and reduces intrinsic factor."),
        q("easy", "Neurologic deficits are classically associated with deficiency of:", "Vitamin B12", ["Folate", "Iron", "Vitamin K"], "B12 deficiency can cause subacute combined degeneration."),
        q("moderate", "Hypersegmented neutrophils are characteristic of:", "Megaloblastic anemia", ["Iron deficiency alone", "ITP", "Hemophilia A"], "Impaired DNA synthesis affects granulocyte nuclear maturation too."),
        q("moderate", "Both folate and vitamin B12 deficiency increase:", "Homocysteine", ["ADAMTS13", "Ferritin stores in every case", "Factor IX"], "Homocysteine rises in both folate and B12 deficiency."),
        q("moderate", "Methylmalonic acid is increased in:", "Vitamin B12 deficiency", ["Folate deficiency only", "Iron deficiency", "Anemia of chronic inflammation"], "Methylmalonic acid helps distinguish B12 deficiency from folate deficiency."),
        q("moderate", "Folate deficiency can be caused by:", "Increased requirement during pregnancy", ["Intrinsic factor antibody in every case", "JAK2 mutation", "Spectrin deficiency"], "Folate requirement rises in pregnancy and chronic hemolysis."),
        q("high", "A patient with autoimmune gastritis has macrocytic anemia, glossitis, hypersegmented neutrophils, low B12, increased methylmalonic acid, and posterior column neurologic findings. Which diagnosis is most likely?", "Pernicious anemia", ["Folate deficiency", "Iron deficiency anemia", "Anemia of chronic inflammation"], "Pernicious anemia causes B12 deficiency through intrinsic factor loss and can affect the nervous system."),
        q("high", "A pregnant patient with poor diet has macrocytic anemia and hypersegmented neutrophils but no neurologic deficits. Homocysteine is high and methylmalonic acid is normal. Which deficiency best explains this?", "Folate deficiency", ["Vitamin B12 deficiency", "Iron deficiency", "Glucose-6-phosphate dehydrogenase deficiency"], "Folate deficiency raises homocysteine without increasing methylmalonic acid or causing neurologic disease."),
        q("high", "A patient receives folate for macrocytic anemia caused by unrecognized B12 deficiency. Hemoglobin improves, but gait imbalance and paresthesias progress over months. What was masked by folate therapy?", "Neurologic injury from vitamin B12 deficiency", ["Iron overload", "Platelet adhesion defect", "Factor VIII deficiency"], "Folate can correct anemia while neurologic damage from B12 deficiency continues."),
    ]),
    ("hemolysis-membrane", "Hemolytic Anemias and Red Cell Membrane Defects", [
        q("easy", "Hemolytic anemia usually has increased:", "Reticulocytes", ["TIBC only", "Intrinsic factor", "Platelet count in every case"], "Marrow compensation produces reticulocytosis if production capacity is intact."),
        q("easy", "Extravascular hemolysis occurs mainly in:", "Spleen and liver macrophages", ["Renal tubules only", "Thymic cortex", "Platelet granules"], "Macrophages remove damaged or antibody-coated red cells."),
        q("easy", "Hereditary spherocytosis is most commonly due to defects in:", "Red cell membrane skeleton proteins", ["Factor VIII", "ADAMTS13", "Intrinsic factor"], "Spectrin, ankyrin, band 3, or protein 4.2 defects reduce membrane stability."),
        q("moderate", "The osmotic fragility test is increased in:", "Hereditary spherocytosis", ["Beta-thalassemia trait", "Iron deficiency anemia", "Hemophilia B"], "Spherocytes are less deformable and lyse more easily in hypotonic solutions."),
        q("moderate", "Splenectomy improves hereditary spherocytosis because it:", "Reduces destruction of spherocytes by splenic macrophages", ["Corrects the spectrin gene", "Increases factor VIII", "Restores intrinsic factor"], "Splenic removal decreases extravascular hemolysis but does not fix the membrane defect."),
        q("moderate", "Intravascular hemolysis can cause:", "Hemoglobinuria", ["Koilonychia only", "Mediastinal mass", "High platelet adhesion"], "Free hemoglobin filtered by kidneys darkens urine in intravascular hemolysis."),
        q("moderate", "Pigment gallstones in chronic hemolysis result from excess:", "Bilirubin production", ["Iron absorption blockade", "Factor IX activity", "Platelet aggregation"], "Heme breakdown increases unconjugated bilirubin and pigment stone risk."),
        q("high", "A child has anemia, jaundice, splenomegaly, pigment gallstones, increased MCHC, and many spherocytes on smear. Family members have similar findings. Which disorder is most likely?", "Hereditary spherocytosis", ["Autoimmune hemolytic anemia", "Iron deficiency anemia", "Beta-thalassemia major"], "Inherited membrane skeleton defects produce spherocytes and chronic extravascular hemolysis."),
        q("high", "A patient with hereditary spherocytosis undergoes splenectomy. Anemia improves and reticulocyte count falls, but spherocytes remain visible on the peripheral smear. Why do the abnormal cells persist?", "The membrane skeleton defect is intrinsic to red cells", ["The spleen creates the genetic mutation", "Iron deficiency has worsened", "Factor VIII is still absent"], "Splenectomy removes the main site of destruction but does not correct the inherited membrane abnormality."),
        q("high", "A patient develops dark urine, low haptoglobin, and hemoglobinemia after a mechanical valve damages red cells within the circulation. Which hemolysis pattern best explains these findings?", "Intravascular hemolysis", ["Extravascular splenic hemolysis", "Megaloblastic ineffective hematopoiesis", "Anemia of chronic inflammation"], "Intravascular red cell destruction releases free hemoglobin into plasma and urine."),
    ]),
    ("enzyme-immune-pnh", "Enzyme Defects, Immune Hemolysis, and PNH", [
        q("easy", "G6PD deficiency predisposes to hemolysis during:", "Oxidant stress", ["Vitamin B12 excess", "Factor VIII infusion", "Splenectomy only"], "G6PD protects red cells from oxidative injury by maintaining reduced glutathione."),
        q("easy", "Heinz bodies are composed of denatured:", "Hemoglobin", ["Fibrin", "Intrinsic factor", "ADAMTS13"], "Oxidized hemoglobin precipitates as Heinz bodies."),
        q("easy", "Warm autoimmune hemolytic anemia is usually mediated by:", "IgG", ["IgM only", "IgA only", "IgE only"], "IgG-coated red cells are removed mainly by splenic macrophages."),
        q("moderate", "Bite cells are formed when splenic macrophages remove:", "Heinz body inclusions", ["Auer rods", "Howell-Jolly bodies only", "Platelet plugs"], "Macrophages pluck out Heinz bodies, leaving bite cells."),
        q("moderate", "Cold agglutinin disease is usually mediated by:", "IgM against red cells", ["IgG against platelets", "IgA against endomysium", "IgE against mast cells"], "IgM binds red cells in cooler peripheral sites and fixes complement."),
        q("moderate", "Paroxysmal nocturnal hemoglobinuria results from mutation in:", "PIGA", ["HBB", "F8", "JAK2"], "PIGA mutation prevents synthesis of GPI anchors."),
        q("moderate", "PNH red cells are deficient in complement regulators:", "CD55 and CD59", ["CD15 and CD30", "CD5 and CD23", "CD10 and BCL6"], "Loss of GPI-linked CD55/CD59 makes cells complement-sensitive."),
        q("high", "A man develops episodic jaundice and dark urine after taking primaquine. Smear shows bite cells, and supravital stain would show Heinz bodies. Which enzyme defect is most likely?", "Glucose-6-phosphate dehydrogenase deficiency", ["Pyruvate kinase excess", "Spectrin deficiency", "Factor IX deficiency"], "G6PD deficiency causes oxidant-induced hemolysis with Heinz bodies and bite cells."),
        q("high", "A patient has anemia, jaundice, spherocytes, positive direct antiglobulin test for IgG, and splenomegaly. Hemolysis occurs mostly through Fc receptor-mediated removal by macrophages. Which diagnosis fits?", "Warm autoimmune hemolytic anemia", ["Cold agglutinin disease", "PNH", "G6PD deficiency"], "Warm AIHA is IgG-mediated extravascular hemolysis with positive Coombs test."),
        q("high", "A patient has recurrent morning hemoglobinuria, venous thrombosis, pancytopenia, and flow cytometry showing loss of GPI-linked CD55 and CD59 on blood cells. Which disorder is present?", "Paroxysmal nocturnal hemoglobinuria", ["Hereditary spherocytosis", "Sickle cell disease", "Immune thrombocytopenia"], "PNH causes complement-mediated intravascular hemolysis and thrombosis due to PIGA mutation."),
    ]),
    ("hemoglobinopathies", "Sickle Cell Disease and Thalassemias", [
        q("easy", "Sickle cell disease is caused by mutation in:", "Beta-globin", ["Alpha-spectrin", "Factor VIII", "Intrinsic factor"], "A point mutation in beta-globin produces hemoglobin S."),
        q("easy", "Sickling is promoted by:", "Deoxygenation", ["Hyperoxygenation", "High folate", "High platelet count"], "Deoxygenated hemoglobin S polymerizes and distorts red cells."),
        q("easy", "Thalassemias are caused by decreased synthesis of:", "Globin chains", ["Heme iron only", "Platelet granules", "Coagulation factors only"], "Alpha or beta globin chain production is reduced."),
        q("moderate", "A common early severe infection risk in sickle cell disease is due to:", "Functional asplenia", ["Intrinsic factor loss", "ADAMTS13 excess", "Factor V Leiden"], "Repeated splenic infarction impairs clearance of encapsulated organisms."),
        q("moderate", "Aplastic crisis in sickle cell disease is classically triggered by:", "Parvovirus B19 infection", ["EBV infection", "H. pylori", "HTLV-1"], "Parvovirus infects erythroid precursors and abruptly stops red cell production."),
        q("moderate", "Beta-thalassemia major usually presents with:", "Severe transfusion-dependent anemia in infancy", ["Mild asymptomatic adult anemia only", "Isolated thrombocytopenia", "Factor VIII deficiency"], "After fetal hemoglobin falls, absent beta-chain synthesis causes severe anemia."),
        q("moderate", "Alpha-thalassemia severity depends mainly on:", "Number of alpha-globin gene deletions", ["Amount of intrinsic factor", "Factor IX activity", "Platelet adhesion"], "Humans have four alpha-globin genes, and disease worsens as more are deleted."),
        q("high", "A child with sickle cell disease has painful vaso-occlusive crises, dactylitis, autosplenectomy, and increased risk of pneumococcal sepsis. Which molecular event initiates red cell sickling?", "Polymerization of deoxygenated hemoglobin S", ["Absent alpha-chain genes in all cells", "Autoantibodies to intrinsic factor", "Failure of platelet GPIb"], "Deoxygenated HbS polymerization distorts red cells and drives vaso-occlusion."),
        q("high", "An infant develops severe anemia, marrow expansion with frontal bossing, hepatosplenomegaly, target cells, and iron overload after repeated transfusions. Hemoglobin electrophoresis shows markedly reduced HbA. Which disease is most likely?", "Beta-thalassemia major", ["Beta-thalassemia minor", "Iron deficiency anemia", "Hereditary spherocytosis"], "Beta-thalassemia major causes severe ineffective erythropoiesis after HbF declines."),
        q("high", "A fetus develops hydrops fetalis because all four alpha-globin genes are deleted, causing inability to form normal fetal hemoglobin and accumulation of gamma-chain tetramers. Which condition is this?", "Hemoglobin Bart hydrops fetalis", ["Hemoglobin H disease", "Beta-thalassemia minor", "Sickle cell trait"], "Deletion of all four alpha-globin genes causes Hb Bart and fatal hydrops."),
    ]),
    ("marrow-failure", "Marrow Failure, Aplastic Anemia, and Polycythemia", [
        q("easy", "Aplastic anemia is characterized by:", "Pancytopenia with hypocellular fatty marrow", ["Isolated erythrocytosis", "High reticulocytosis", "Massive lymphadenopathy"], "Aplastic anemia reflects marrow stem cell failure."),
        q("easy", "Pure red cell aplasia affects mainly:", "Erythroid precursors", ["Megakaryocytes only", "Mature neutrophils only", "Thymic epithelial cells"], "Pure red cell aplasia selectively reduces red cell production."),
        q("easy", "Polycythemia means increased:", "Red cell mass", ["Platelet function only", "Coagulation factor consumption", "Intrinsic factor"], "Polycythemia is an expansion of circulating red cells."),
        q("moderate", "Fanconi anemia is associated with:", "Inherited DNA repair defect and marrow failure", ["Acquired factor VIII inhibitor only", "Vitamin K excess", "Splenic rupture only"], "Fanconi anemia causes congenital anomalies and predisposes to aplastic anemia and leukemia."),
        q("moderate", "Aplastic anemia often presents with:", "Anemia, infections, and bleeding", ["Hyperviscosity with high IgM", "Only painful lymph nodes", "Jaundice with high reticulocytes"], "Pancytopenia causes fatigue, infection risk, and thrombocytopenic bleeding."),
        q("moderate", "Secondary polycythemia usually has:", "Increased erythropoietin", ["Low erythropoietin", "Absent marrow erythroid cells", "Low oxygen affinity hemoglobin in every case"], "Hypoxia or EPO-secreting tumors raise erythropoietin."),
        q("moderate", "Polycythemia vera is usually associated with:", "JAK2 mutation and low erythropoietin", ["PIGA mutation and hemoglobinuria", "F8 mutation and bleeding", "HBB mutation and sickling"], "PV is a primary myeloproliferative neoplasm independent of high EPO."),
        q("high", "A patient exposed to benzene develops fatigue, recurrent infections, petechiae, pancytopenia, very low reticulocyte count, and a hypocellular marrow replaced by fat. Which diagnosis is most likely?", "Aplastic anemia", ["Myelophthisic anemia", "Autoimmune hemolytic anemia", "Iron deficiency anemia"], "Toxic stem cell injury can cause aplastic anemia with fatty marrow and pancytopenia."),
        q("high", "A patient living at high altitude has increased hemoglobin, increased erythropoietin, and otherwise normal leukocyte and platelet counts. The erythrocytosis improves with descent. Which category fits?", "Secondary polycythemia from hypoxia", ["Polycythemia vera", "Aplastic anemia", "Paroxysmal nocturnal hemoglobinuria"], "Hypoxia-driven EPO production causes secondary polycythemia."),
        q("high", "A patient has headache, pruritus after hot showers, splenomegaly, thrombosis, increased red cells, granulocytes, and platelets, plus low erythropoietin. Which primary marrow disorder best explains the findings?", "Polycythemia vera", ["Secondary polycythemia", "Pure red cell aplasia", "Megaloblastic anemia"], "PV is a JAK2-driven panmyelosis with low EPO and thrombotic risk."),
    ]),
    ("platelets", "Platelet Disorders and Immune Thrombocytopenia", [
        q("easy", "Thrombocytopenia usually causes:", "Petechiae and mucosal bleeding", ["Deep muscle hematomas only", "Lytic bone lesions", "Painful vaso-occlusion"], "Low platelet number causes primary hemostatic bleeding."),
        q("easy", "Immune thrombocytopenia is caused by autoantibodies against:", "Platelet membrane glycoproteins", ["Factor VIII", "Intrinsic factor", "Beta-globin"], "Antiplatelet antibodies promote splenic destruction."),
        q("easy", "Bernard-Soulier syndrome involves defective platelet:", "Adhesion", ["Coagulation factor synthesis", "Red cell membrane stability", "DNA synthesis"], "GPIb defects impair platelet binding to von Willebrand factor."),
        q("moderate", "Glanzmann thrombasthenia is caused by deficiency of:", "GPIIb/IIIa", ["GPIb", "Factor IX", "ADAMTS13"], "GPIIb/IIIa is needed for fibrinogen-mediated platelet aggregation."),
        q("moderate", "Bernard-Soulier syndrome is caused by deficiency of:", "GPIb", ["GPIIb/IIIa", "Factor VIII", "Protein C"], "GPIb binds vWF and mediates adhesion to subendothelium."),
        q("moderate", "Aspirin impairs platelet function by inhibiting:", "Cyclooxygenase and thromboxane A2 synthesis", ["ADAMTS13", "Intrinsic factor", "Spectrin"], "Aspirin irreversibly inhibits platelet COX, reducing thromboxane-dependent aggregation."),
        q("moderate", "Acute ITP in children often follows:", "Viral infection", ["Severe iron deficiency only", "BCR-ABL translocation", "Alpha-globin deletion"], "Childhood ITP is often self-limited after viral illness."),
        q("high", "A child develops petechiae and epistaxis two weeks after a viral illness. Platelet count is low, marrow megakaryocytes are increased, and coagulation tests are normal. Which diagnosis is most likely?", "Immune thrombocytopenia", ["Hemophilia A", "DIC", "Aplastic anemia"], "ITP causes isolated thrombocytopenia with compensatory megakaryocytic hyperplasia."),
        q("high", "A patient has lifelong mucocutaneous bleeding, giant platelets, thrombocytopenia, and failure of platelets to adhere to subendothelial von Willebrand factor. Which receptor is defective?", "GPIb", ["GPIIb/IIIa", "P2Y12", "Factor VIII"], "Bernard-Soulier syndrome is due to GPIb deficiency."),
        q("high", "A patient has normal platelet count but severe mucosal bleeding. Platelets fail to aggregate with ADP, collagen, or epinephrine because fibrinogen cannot bridge adjacent platelets. Which disorder is present?", "Glanzmann thrombasthenia", ["Bernard-Soulier syndrome", "Immune thrombocytopenia", "Hemophilia B"], "GPIIb/IIIa deficiency impairs platelet aggregation despite normal platelet count."),
    ]),
    ("coagulation-vwf", "Coagulation Disorders, von Willebrand Disease, and Hemophilia", [
        q("easy", "Hemophilia A is caused by deficiency of:", "Factor VIII", ["Factor IX", "von Willebrand factor only", "Platelet GPIb"], "Hemophilia A is an X-linked factor VIII deficiency."),
        q("easy", "Hemophilia B is caused by deficiency of:", "Factor IX", ["Factor VIII", "Factor XIII only", "ADAMTS13"], "Hemophilia B is Christmas disease."),
        q("easy", "von Willebrand disease primarily impairs platelet:", "Adhesion", ["Production in marrow", "Granule formation only", "Nuclear maturation"], "vWF bridges platelet GPIb to exposed collagen."),
        q("moderate", "von Willebrand factor also stabilizes:", "Factor VIII", ["Factor IX", "Protein C", "Thrombin only"], "Loss of vWF can secondarily reduce factor VIII levels."),
        q("moderate", "Hemophilia A typically causes:", "Deep tissue bleeding and hemarthroses", ["Only pinpoint petechiae", "Only iron deficiency", "Only splenomegaly"], "Coagulation factor defects produce secondary hemostatic bleeding."),
        q("moderate", "PTT is prolonged in:", "Hemophilia A", ["Isolated platelet adhesion defect only", "Iron deficiency", "Hereditary spherocytosis"], "Intrinsic pathway factor deficiency prolongs PTT."),
        q("moderate", "Vitamin K deficiency prolongs:", "PT and often PTT", ["Bleeding time only", "Reticulocyte count only", "Osmotic fragility"], "Vitamin K is needed for factors II, VII, IX, and X; PT is often affected first."),
        q("high", "A boy has recurrent hemarthroses, deep muscle hematomas, normal platelet count, normal bleeding time, and prolonged PTT corrected by mixing study. Which disorder is most likely?", "Hemophilia A", ["Immune thrombocytopenia", "von Willebrand disease", "Glanzmann thrombasthenia"], "Factor VIII deficiency causes intrinsic pathway bleeding with normal primary hemostasis."),
        q("high", "A patient has lifelong epistaxis and menorrhagia, prolonged bleeding time, mildly prolonged PTT, and reduced ristocetin-induced platelet aggregation. Which inherited bleeding disorder is most likely?", "von Willebrand disease", ["Hemophilia B", "Bernard-Soulier syndrome", "DIC"], "vWF disease causes mucosal bleeding from impaired adhesion and can reduce factor VIII."),
        q("high", "A newborn with biliary atresia develops bleeding with prolonged PT and PTT that corrects after vitamin K. Which biochemical requirement explains the coagulation defect?", "Gamma-carboxylation of vitamin K-dependent clotting factors", ["Hydroxylation of collagen", "Reduction of glutathione in red cells", "Assembly of spectrin tetramers"], "Vitamin K is needed for gamma-carboxylation of factors II, VII, IX, and X."),
    ]),
    ("dic-tma", "DIC, Thrombotic Microangiopathy, and Anticoagulant Disorders", [
        q("easy", "Disseminated intravascular coagulation involves widespread activation of:", "Coagulation", ["Intrinsic factor secretion", "Globin synthesis", "Platelet production only"], "DIC consumes platelets and clotting factors through systemic coagulation activation."),
        q("easy", "TTP is commonly caused by severe deficiency of:", "ADAMTS13", ["Factor VIII", "GPIb", "Intrinsic factor"], "ADAMTS13 cleaves large von Willebrand factor multimers."),
        q("easy", "HUS in children often follows infection with:", "Shiga toxin-producing E. coli", ["EBV", "HTLV-1", "H. pylori"], "Typical HUS follows diarrheal illness from Shiga toxin-producing bacteria."),
        q("moderate", "DIC laboratory findings usually include:", "Prolonged PT/PTT, low fibrinogen, thrombocytopenia, and high D-dimer", ["Normal PT/PTT with isolated low B12", "High fibrinogen and high platelets only", "Low ferritin and high TIBC"], "Consumption of clotting factors and fibrin breakdown define DIC labs."),
        q("moderate", "Schistocytes form because red cells are:", "Fragmented by fibrin strands or damaged microvasculature", ["Made without nuclei in marrow", "Filled with iron granules", "Coated with IgE"], "Microangiopathic hemolysis mechanically shears red cells."),
        q("moderate", "TTP classically causes:", "Thrombocytopenia and microangiopathic hemolytic anemia", ["Isolated factor VIII deficiency", "Pure iron deficiency", "Macrocytosis with neurologic deficits only"], "TTP produces platelet-rich microthrombi and RBC fragmentation."),
        q("moderate", "Heparin therapy is monitored mainly with:", "PTT", ["Bleeding time", "Reticulocyte count", "Osmotic fragility"], "Unfractionated heparin prolongs the intrinsic pathway measured by PTT."),
        q("high", "A septic patient develops oozing from venipuncture sites, thrombocytopenia, prolonged PT and PTT, low fibrinogen, elevated D-dimer, and schistocytes. Which hemostatic disorder is present?", "Disseminated intravascular coagulation", ["Immune thrombocytopenia", "Hemophilia A", "von Willebrand disease"], "Sepsis can trigger DIC with consumption of platelets and coagulation factors."),
        q("high", "A young adult has fever, confusion, renal dysfunction, thrombocytopenia, and microangiopathic hemolytic anemia. Coagulation tests are relatively normal, and ADAMTS13 activity is severely reduced. Which diagnosis fits?", "Thrombotic thrombocytopenic purpura", ["DIC", "Hemophilia B", "Immune thrombocytopenia"], "TTP causes platelet microthrombi from uncleaved vWF multimers without primary coagulation factor consumption."),
        q("high", "A child develops bloody diarrhea followed by acute kidney injury, thrombocytopenia, and schistocytes after eating undercooked meat. Coagulation tests are not diffusely consumed. Which syndrome is most likely?", "Hemolytic uremic syndrome", ["TTP from ADAMTS13 autoantibody", "DIC from sepsis", "Hemophilia A"], "Typical HUS follows Shiga toxin exposure and prominently injures renal microvasculature."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch14-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 14 questions, got {len(chapter_questions)}")
    topic_counts = Counter(q["topic"] for q in chapter_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in chapter_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in chapter_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    short_high = [q["id"] for q in chapter_questions if q["difficulty"] == "high" and len(q["prompt"].split()) < 24]
    if short_high:
        raise ValueError(f"High-level prompts too short: {short_high[:5]}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)
    total_removed = 0
    for data_path in DATA_PATHS:
        data = json.loads(data_path.read_text(encoding="utf-8-sig"))
        existing = data.get("questions", [])
        kept = [
            question for question in existing
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch14-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 14 questions")
    print(f"Removed {total_removed} existing Chapter 14 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 14 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
