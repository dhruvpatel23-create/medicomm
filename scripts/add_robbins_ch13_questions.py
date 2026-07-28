import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Diseases of White Blood Cells, Lymph Nodes, Spleen, and Thymus"
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
    ("normal-reactive", "Normal Leukocyte Responses and Reactive Lymphadenitis", [
        q("easy", "Leukocytosis means:", "Increased white blood cell count", ["Decreased platelet count", "Increased red cell mass", "Absent lymph nodes"], "Leukocytosis is an elevation in circulating leukocytes."),
        q("easy", "Neutrophilia is most often associated with:", "Acute bacterial infection", ["Allergic asthma only", "Viral mononucleosis only", "Plasma cell myeloma"], "Bacterial infections commonly cause increased neutrophils."),
        q("easy", "Eosinophilia is classically associated with:", "Allergic disease and parasitic infection", ["Iron deficiency only", "Aortic stenosis", "Vitamin K deficiency"], "Eosinophils respond to allergic disorders and helminthic parasites."),
        q("moderate", "A leukemoid reaction is best described as:", "Marked reactive leukocytosis that can mimic leukemia", ["A malignant plasma cell tumor", "A congenital thymic cyst", "A lymphoma of Reed-Sternberg cells"], "Severe infection or stress can produce very high reactive WBC counts."),
        q("moderate", "Reactive follicular hyperplasia primarily reflects activation of:", "B-cell follicles and germinal centers", ["Medullary thymic epithelium", "Splenic red pulp cords only", "Bone marrow megakaryocytes"], "Follicular hyperplasia expands secondary follicles after antigenic stimulation."),
        q("moderate", "Paracortical hyperplasia in a lymph node usually reflects expansion of:", "T-cell zones", ["B-cell mantle zones only", "Splenic sinusoids", "Thymic Hassall corpuscles"], "The paracortex is a T-cell-rich region."),
        q("moderate", "Sinus histiocytosis in lymph nodes is often seen in:", "Nodes draining cancers or inflammatory lesions", ["Acute myeloid leukemia only", "Pure red cell aplasia", "Aplastic anemia only"], "Macrophages expand in nodal sinuses in response to draining antigens or tumor products."),
        q("high", "A child with a painful enlarged cervical node after pharyngitis has preserved nodal architecture with large reactive germinal centers containing tingible-body macrophages. Which diagnosis is most likely?", "Reactive follicular hyperplasia", ["Follicular lymphoma", "Classical Hodgkin lymphoma", "Metastatic carcinoma"], "Reactive follicles retain polarity, macrophages, and overall nodal architecture."),
        q("high", "A patient with severe bacterial pneumonia has WBC count of 55,000/uL with toxic granulation and left shift, but leukocyte alkaline phosphatase is high and BCR-ABL testing is negative. Which process best fits?", "Leukemoid reaction", ["Chronic myeloid leukemia", "Acute lymphoblastic leukemia", "Multiple myeloma"], "Leukemoid reaction is reactive neutrophilia and must be separated from CML."),
        q("high", "A lymph node from a patient with viral infection shows expanded paracortical areas filled with immunoblasts, while follicles are not the dominant abnormality. Which immune compartment is mainly activated?", "T-cell paracortex", ["B-cell follicle only", "Splenic red pulp", "Bone marrow plasma cells"], "Viral infections commonly produce paracortical T-cell hyperplasia."),
    ]),
    ("benign-wbc", "Nonneoplastic Leukocyte Disorders and Leukopenia", [
        q("easy", "Neutropenia predisposes most strongly to:", "Bacterial and fungal infections", ["Atherosclerosis", "Gallstones", "Renal calculi"], "Neutrophils are central for defense against bacteria and fungi."),
        q("easy", "Agranulocytosis refers to severe deficiency of:", "Granulocytes, especially neutrophils", ["Platelets only", "Red cells only", "Plasma proteins"], "Agranulocytosis is a severe neutropenic state."),
        q("easy", "Infectious mononucleosis is most commonly caused by:", "Epstein-Barr virus", ["Parvovirus B19", "Hepatitis C virus", "HTLV-1"], "EBV infects B cells and produces a reactive T-cell response."),
        q("moderate", "The atypical lymphocytes in infectious mononucleosis are mainly:", "Reactive CD8+ T cells", ["Malignant B lymphoblasts", "Neoplastic plasma cells", "Reed-Sternberg cells"], "CD8+ T cells expand in response to EBV-infected B cells."),
        q("moderate", "The classic serologic test for infectious mononucleosis detects:", "Heterophile antibodies", ["Anti-dsDNA antibodies", "BCR-ABL transcripts", "Anti-centromere antibodies"], "Heterophile antibodies are detected by Monospot-type tests."),
        q("moderate", "Lymphopenia is a characteristic feature of:", "Advanced HIV infection", ["Essential thrombocythemia", "Polycythemia vera", "Burkitt lymphoma only"], "HIV progressively depletes CD4+ T lymphocytes."),
        q("moderate", "Drug-induced marrow suppression can produce neutropenia by:", "Reducing granulocyte production in bone marrow", ["Increasing lymph node follicles", "Causing splenic infarction only", "Activating BCR-ABL kinase"], "Many drugs can suppress myeloid precursors."),
        q("high", "A teenager has fever, sore throat, generalized lymphadenopathy, splenomegaly, and atypical lymphocytosis. The abnormal blood cells are large reactive T cells responding to infected B cells. Which infection is most likely?", "Epstein-Barr virus infectious mononucleosis", ["Acute HIV only", "Cytomegalovirus colitis", "HTLV-1 adult T-cell leukemia"], "EBV mononucleosis causes atypical CD8+ T-cell lymphocytosis and lymphoid hyperplasia."),
        q("high", "A patient taking an antithyroid drug develops fever, painful oral ulcers, and an absolute neutrophil count under 500/uL. Bone marrow shows marked reduction in granulocytic precursors. Which disorder is present?", "Drug-induced agranulocytosis", ["Leukemoid reaction", "Eosinophilic leukemia", "Classical Hodgkin lymphoma"], "Severe neutropenia can follow idiosyncratic drug toxicity and causes mucosal infections."),
        q("high", "A person with untreated HIV has recurrent opportunistic infections and very low CD4+ T-cell count. The total white cell count may be low rather than high. Which leukocyte abnormality is central?", "Lymphopenia from T-cell depletion", ["Reactive neutrophilia", "Eosinophilia from parasites", "Basophilia from CML"], "HIV targets helper T cells and causes progressive lymphopenia."),
    ]),
    ("acute-leukemias", "Acute Leukemias: ALL and AML", [
        q("easy", "Acute leukemia is defined by accumulation of immature:", "Blasts", ["Mature plasma cells", "Reactive macrophages", "Tingible-body macrophages"], "Acute leukemias are neoplasms of immature hematopoietic progenitors."),
        q("easy", "Acute lymphoblastic leukemia is most common in:", "Children", ["Elderly smokers only", "Newborns only", "Middle-aged women only"], "ALL is the most common cancer of childhood."),
        q("easy", "Auer rods are characteristic of:", "Acute myeloid leukemia", ["Acute lymphoblastic leukemia", "Chronic lymphocytic leukemia", "Follicular lymphoma"], "Auer rods are needle-like azurophilic granules in myeloid blasts."),
        q("moderate", "TdT positivity supports a diagnosis of:", "Lymphoblastic leukemia or lymphoma", ["Mature plasma cell neoplasm", "Hairy cell leukemia", "Classical Hodgkin lymphoma"], "TdT is a marker of immature lymphoid cells."),
        q("moderate", "AML with t(15;17) produces:", "Acute promyelocytic leukemia", ["Burkitt lymphoma", "CML blast crisis", "Mantle cell lymphoma"], "PML-RARA fusion blocks promyelocyte differentiation."),
        q("moderate", "Acute promyelocytic leukemia is especially associated with:", "Disseminated intravascular coagulation", ["Hypercalcemia only", "Cold agglutinin disease", "Pure red cell aplasia"], "Granule contents from promyelocytes can trigger DIC."),
        q("moderate", "ALL often presents with bone pain because of:", "Marrow expansion by lymphoblasts", ["Splenic red pulp fibrosis only", "Valve vegetations", "Amyloid deposition"], "Rapid marrow replacement can cause bone pain and cytopenias."),
        q("high", "A 4-year-old has fatigue, bruising, bone pain, lymphadenopathy, and marrow packed with TdT-positive lymphoblasts. The blasts express CD10 and B-cell markers. Which diagnosis is most likely?", "B-acute lymphoblastic leukemia", ["Acute promyelocytic leukemia", "Chronic myeloid leukemia", "Multiple myeloma"], "Childhood B-ALL commonly expresses TdT, CD10, and B-cell markers."),
        q("high", "An adult develops gingival infiltration, anemia, thrombocytopenia, and circulating blasts containing Auer rods after weeks of fatigue and infections. Flow cytometry shows myeloid markers. Which disease is present?", "Acute myeloid leukemia", ["Acute lymphoblastic leukemia", "CLL/SLL", "Hodgkin lymphoma"], "Auer rods and myeloid markers support AML."),
        q("high", "A patient with AML has abnormal promyelocytes, severe bleeding, laboratory evidence of DIC, and t(15;17). Therapy with all-trans retinoic acid is chosen because it overcomes which problem?", "Blocked differentiation caused by PML-RARA", ["BCR-ABL kinase activation", "Cyclin D1 overexpression", "MYC-driven germinal center proliferation"], "ATRA releases the differentiation block in acute promyelocytic leukemia."),
    ]),
    ("mpn-mds", "Myeloproliferative Neoplasms and Myelodysplastic Syndromes", [
        q("easy", "Chronic myeloid leukemia is driven by:", "BCR-ABL fusion tyrosine kinase", ["PML-RARA fusion", "MYC translocation", "Cyclin D1 translocation"], "CML is defined by the Philadelphia chromosome t(9;22)."),
        q("easy", "Polycythemia vera is characterized by increased:", "Red cell mass", ["Only lymph nodes", "Only plasma cells", "Only thymic epithelium"], "PV is a myeloproliferative neoplasm dominated by erythrocytosis."),
        q("easy", "Essential thrombocythemia primarily causes increased:", "Platelets", ["Neutrophil apoptosis", "T-cell depletion", "Reed-Sternberg cells"], "ET is a clonal megakaryocytic proliferation with thrombocytosis."),
        q("moderate", "Most polycythemia vera cases have mutation in:", "JAK2", ["RET", "RB1", "NF1"], "JAK2 mutations activate cytokine signaling in PV and other MPNs."),
        q("moderate", "Primary myelofibrosis commonly causes:", "Marrow fibrosis with extramedullary hematopoiesis", ["Pure lymph node follicular hyperplasia", "Thymic epithelial tumor only", "Isolated neutropenia"], "Fibrogenic cytokines from abnormal megakaryocytes scar the marrow."),
        q("moderate", "Myelodysplastic syndromes are characterized by:", "Ineffective hematopoiesis with dysplasia and cytopenias", ["Reactive leukocytosis only", "Benign germinal centers", "Pure thymic aplasia"], "MDS causes cytopenias despite cellular marrow due to ineffective maturation."),
        q("moderate", "A low leukocyte alkaline phosphatase score supports:", "Chronic myeloid leukemia over leukemoid reaction", ["Reactive neutrophilia over CML", "Infectious mononucleosis", "Hodgkin lymphoma"], "CML classically has low LAP, unlike reactive neutrophilia."),
        q("high", "A patient has marked leukocytosis with left-shifted granulocytes at all maturation stages, basophilia, splenomegaly, low LAP score, and t(9;22). Which neoplasm is most likely?", "Chronic myeloid leukemia", ["Leukemoid reaction", "Acute promyelocytic leukemia", "Hairy cell leukemia"], "BCR-ABL-positive CML produces granulocytic proliferation and basophilia."),
        q("high", "A patient has pruritus after hot baths, plethora, splenomegaly, recurrent thrombosis, very high hematocrit, low erythropoietin, and JAK2 mutation. Which myeloproliferative neoplasm fits best?", "Polycythemia vera", ["Secondary polycythemia", "Essential thrombocythemia", "Myelodysplastic syndrome"], "PV is a JAK2-driven clonal erythrocytosis with low EPO."),
        q("high", "An older patient has anemia, teardrop red cells, massive splenomegaly, dry tap on marrow aspiration, and atypical megakaryocytes releasing fibrogenic cytokines. Which diagnosis is most likely?", "Primary myelofibrosis", ["CML chronic phase", "Acute lymphoblastic leukemia", "Reactive lymphadenitis"], "Primary myelofibrosis causes marrow scarring and extramedullary hematopoiesis."),
    ]),
    ("cll-hairy", "Mature Leukemias: CLL/SLL and Hairy Cell Leukemia", [
        q("easy", "CLL/SLL is a neoplasm of mature:", "B cells", ["Neutrophils", "Megakaryocytes", "Thymic epithelial cells"], "CLL/SLL is the most common adult leukemia in many populations and is of B-cell lineage."),
        q("easy", "Smudge cells are commonly seen in:", "Chronic lymphocytic leukemia", ["Acute promyelocytic leukemia", "Burkitt lymphoma", "Multiple myeloma"], "Fragile CLL cells rupture during smear preparation, forming smudge cells."),
        q("easy", "Hairy cell leukemia is classically associated with:", "Splenomegaly", ["Massive thymoma", "Mediastinal germ cell tumor", "Aortic dissection"], "Hairy cell leukemia often produces splenic red pulp expansion."),
        q("moderate", "CLL/SLL cells commonly express:", "CD5 and CD23", ["CD10 and BCL6", "CD30 and CD15", "CD138 and MUM1 only"], "CLL/SLL has a characteristic CD5-positive mature B-cell phenotype with CD23."),
        q("moderate", "A common immune complication of CLL/SLL is:", "Autoimmune hemolytic anemia", ["DIC in every patient", "Hyperviscosity from IgM only", "Eosinophilic myocarditis"], "CLL can disrupt immune tolerance and cause autoimmune cytopenias."),
        q("moderate", "Hairy cell leukemia cells are classically positive for:", "TRAP", ["TdT", "MPO only", "Cyclin D1 only"], "Tartrate-resistant acid phosphatase is a classic marker of hairy cell leukemia."),
        q("moderate", "Hairy cell leukemia often causes dry tap because of:", "Marrow fibrosis", ["Purely fatty marrow", "Absent spleen", "Reactive follicular hyperplasia"], "Reticulin fibrosis can make marrow aspiration difficult."),
        q("high", "An elderly patient has persistent lymphocytosis, generalized lymphadenopathy, hypogammaglobulinemia, and fragile lymphocytes forming smudge cells on smear. Flow cytometry shows CD5+ CD23+ B cells. Which diagnosis fits?", "CLL/SLL", ["Mantle cell lymphoma", "Acute lymphoblastic leukemia", "Hairy cell leukemia"], "CLL/SLL is a mature CD5+ CD23+ B-cell neoplasm with smudge cells."),
        q("high", "A patient with previously indolent CLL develops rapidly enlarging lymph nodes, fever, weight loss, rising LDH, and biopsy shows diffuse large B-cell lymphoma. Which transformation has occurred?", "Richter transformation", ["Blast crisis of CML", "Leukemoid reaction", "Myeloid metaplasia"], "CLL can transform to an aggressive large B-cell lymphoma."),
        q("high", "A middle-aged man has pancytopenia, massive splenomegaly without prominent lymphadenopathy, dry tap marrow, and B cells with circumferential cytoplasmic projections. Which neoplasm is most likely?", "Hairy cell leukemia", ["CLL/SLL", "Follicular lymphoma", "Plasma cell myeloma"], "Hairy cell leukemia has hairy projections, splenomegaly, pancytopenia, and marrow fibrosis."),
    ]),
    ("nhl-small-b", "Small B-Cell Non-Hodgkin Lymphomas", [
        q("easy", "Follicular lymphoma is a neoplasm of:", "Germinal center B cells", ["Thymic epithelial cells", "Neutrophil precursors", "Megakaryocytes"], "Follicular lymphoma resembles germinal center B cells."),
        q("easy", "Follicular lymphoma commonly has translocation involving:", "BCL2", ["PML-RARA", "BCR-ABL", "ALK"], "t(14;18) places BCL2 under immunoglobulin enhancer control."),
        q("easy", "Mantle cell lymphoma commonly overexpresses:", "Cyclin D1", ["TdT", "E-cadherin", "Factor VIII"], "t(11;14) drives cyclin D1 overexpression."),
        q("moderate", "The t(14;18) translocation promotes lymphoma by:", "Preventing apoptosis through BCL2 overexpression", ["Activating retinoic acid receptor", "Creating BCR-ABL kinase", "Deleting all immunoglobulin genes"], "BCL2 survival signaling allows abnormal germinal center B cells to persist."),
        q("moderate", "Mantle cell lymphoma typically expresses:", "CD5 and cyclin D1", ["CD15 and CD30", "CD10 and TdT only", "CD138 and kappa only"], "Mantle cell lymphoma is a CD5+ mature B-cell lymphoma with cyclin D1."),
        q("moderate", "Extranodal marginal zone lymphoma of MALT type is linked to:", "Chronic inflammation", ["Acute hemorrhage", "Vitamin C excess", "Aortic stenosis"], "Persistent antigenic stimulation can drive MALT lymphoma."),
        q("moderate", "Gastric MALT lymphoma is associated with:", "Helicobacter pylori infection", ["EBV in every case", "HTLV-1", "Parvovirus B19"], "H. pylori-driven chronic gastritis can lead to MALT lymphoma."),
        q("high", "A middle-aged adult has generalized painless lymphadenopathy. Node biopsy shows back-to-back follicles lacking tingible-body macrophages, and tumor cells overexpress BCL2 due to t(14;18). Which lymphoma is most likely?", "Follicular lymphoma", ["Reactive follicular hyperplasia", "Mantle cell lymphoma", "Classical Hodgkin lymphoma"], "Neoplastic follicles lack normal polarity and express antiapoptotic BCL2."),
        q("high", "An older man has generalized lymphadenopathy, splenomegaly, marrow involvement, and lymphoma cells expressing CD5, cyclin D1, and t(11;14). The clinical course is aggressive. Which lymphoma is present?", "Mantle cell lymphoma", ["CLL/SLL", "Follicular lymphoma", "Burkitt lymphoma"], "Mantle cell lymphoma is driven by CCND1-IGH translocation."),
        q("high", "A patient with chronic H. pylori gastritis develops a low-grade extranodal B-cell lymphoma in the stomach that may regress after antibiotic eradication. Which lymphoma is this?", "Extranodal marginal zone lymphoma of MALT", ["Diffuse large B-cell lymphoma", "Mantle cell lymphoma", "Lymphoblastic lymphoma"], "Early gastric MALT lymphoma can be antigen-dependent and responsive to H. pylori eradication."),
    ]),
    ("aggressive-b-t", "Aggressive B-Cell and T-Cell Lymphomas", [
        q("easy", "Diffuse large B-cell lymphoma is usually:", "An aggressive lymphoma of large B cells", ["A benign reactive node", "A thymic epithelial tumor", "A platelet disorder"], "DLBCL is a common aggressive mature B-cell lymphoma."),
        q("easy", "Burkitt lymphoma is strongly associated with activation of:", "MYC", ["BCL2", "PML-RARA", "JAK2"], "Burkitt lymphoma has MYC translocation, often t(8;14)."),
        q("easy", "Adult T-cell leukemia/lymphoma is associated with:", "HTLV-1", ["HHV-8", "H. pylori", "Parvovirus B19"], "HTLV-1 is the cause of adult T-cell leukemia/lymphoma."),
        q("moderate", "The classic microscopic pattern of Burkitt lymphoma is:", "Starry-sky appearance", ["Lacunar cells in bands of fibrosis", "Auer rods", "Dry tap fibrosis"], "Macrophages among rapidly proliferating tumor cells create the starry-sky pattern."),
        q("moderate", "Endemic Burkitt lymphoma often involves the:", "Jaw", ["Thymus only", "Spleen red pulp only", "Aortic root"], "African endemic Burkitt lymphoma commonly presents as jaw or facial bone masses."),
        q("moderate", "Anaplastic large cell lymphoma often expresses:", "CD30", ["CD15 only", "CD138 only", "MPO only"], "ALCL is a T-cell lymphoma with strong CD30 expression."),
        q("moderate", "Mycosis fungoides is a lymphoma primarily involving:", "Skin", ["Bone marrow only", "Thymic medulla", "Splenic white pulp only"], "Mycosis fungoides is a cutaneous T-cell lymphoma."),
        q("high", "A child has a rapidly enlarging jaw mass. Biopsy shows sheets of medium-sized lymphoid cells with many mitoses and tingible-body macrophages. Cytogenetics reveals t(8;14). Which lymphoma is most likely?", "Burkitt lymphoma", ["Follicular lymphoma", "Mantle cell lymphoma", "CLL/SLL"], "Burkitt lymphoma is a MYC-driven tumor with very high proliferation."),
        q("high", "An adult has a rapidly growing extranodal mass composed of large CD20+ B cells. The disease is clinically aggressive but potentially curable with combination chemotherapy. Which lymphoma is most likely?", "Diffuse large B-cell lymphoma", ["Small lymphocytic lymphoma", "MALT lymphoma", "Hairy cell leukemia"], "DLBCL is an aggressive large B-cell lymphoma that may arise de novo or by transformation."),
        q("high", "A patient from an HTLV-1 endemic region has leukemia, skin lesions, lytic bone lesions, hypercalcemia, and malignant CD4+ T cells with multilobated nuclei. Which diagnosis fits best?", "Adult T-cell leukemia/lymphoma", ["Sezary syndrome", "Burkitt lymphoma", "Classical Hodgkin lymphoma"], "HTLV-1 causes adult T-cell leukemia/lymphoma with hypercalcemia and skin involvement."),
    ]),
    ("hodgkin", "Hodgkin Lymphoma", [
        q("easy", "The diagnostic malignant cell of classical Hodgkin lymphoma is the:", "Reed-Sternberg cell", ["Auer rod-bearing blast", "Plasma cell", "Hairy cell"], "Classical Hodgkin lymphoma requires Reed-Sternberg cells in an inflammatory background."),
        q("easy", "Classical Reed-Sternberg cells commonly express:", "CD15 and CD30", ["CD5 and CD23", "CD10 and BCL2", "CD138 and CD56"], "CD15 and CD30 are typical immunophenotypic markers."),
        q("easy", "Hodgkin lymphoma usually spreads by:", "Contiguous nodal spread", ["Random leukemic dissemination first", "Transplacental spread", "Direct arterial invasion only"], "HL often spreads in an orderly fashion to adjacent nodal groups."),
        q("moderate", "Nodular sclerosis Hodgkin lymphoma is characterized by:", "Lacunar cells and broad collagen bands", ["Starry-sky pattern", "Cyclin D1 overexpression", "Dry tap fibrosis"], "Nodular sclerosis has lacunar variant RS cells and fibrous bands."),
        q("moderate", "Mixed cellularity Hodgkin lymphoma is commonly associated with:", "EBV infection", ["H. pylori in every case", "BCR-ABL", "JAK2 mutation"], "EBV is often present in mixed cellularity HL."),
        q("moderate", "Lymphocyte-rich Hodgkin lymphoma generally has:", "Many background lymphocytes and relatively few RS cells", ["No lymphocytes", "Only plasma cells", "Only neutrophils"], "This subtype has abundant reactive lymphocytes."),
        q("moderate", "Lymphocyte depletion Hodgkin lymphoma is associated with:", "Older age or immunodeficiency and poorer prognosis", ["Best prognosis in all patients", "Exclusive childhood disease", "H. pylori gastritis"], "Lymphocyte-depleted HL is uncommon and aggressive."),
        q("high", "A young woman has a mediastinal mass. Lymph node biopsy shows nodules divided by broad collagen bands and large cells with folded multilobed nuclei sitting in clear spaces. Which subtype is most likely?", "Nodular sclerosis classical Hodgkin lymphoma", ["Mixed cellularity Hodgkin lymphoma", "Nodular lymphocyte-predominant Hodgkin lymphoma", "Burkitt lymphoma"], "Nodular sclerosis HL often affects young women and mediastinal nodes."),
        q("high", "A patient has painless cervical lymphadenopathy. Biopsy shows scattered binucleate cells with prominent eosinophilic nucleoli in a mixed inflammatory background. The tumor cells are CD15+ and CD30+. Which disease is present?", "Classical Hodgkin lymphoma", ["Diffuse large B-cell lymphoma", "Reactive lymphadenitis", "Mantle cell lymphoma"], "Reed-Sternberg cells with CD15/CD30 expression define classical HL."),
        q("high", "A man has a localized peripheral lymph node with nodular architecture and popcorn cells expressing B-cell markers but lacking CD15 and CD30. Which Hodgkin lymphoma variant is most likely?", "Nodular lymphocyte-predominant Hodgkin lymphoma", ["Nodular sclerosis classical Hodgkin lymphoma", "Lymphocyte-depleted classical Hodgkin lymphoma", "Burkitt lymphoma"], "NLPHL has L&H popcorn cells and a B-cell immunophenotype."),
    ]),
    ("plasma-cell", "Plasma Cell Neoplasms and Related Disorders", [
        q("easy", "Multiple myeloma is a malignant proliferation of:", "Plasma cells", ["Neutrophils", "T lymphoblasts", "Thymic epithelial cells"], "Myeloma is a plasma cell neoplasm producing monoclonal immunoglobulin."),
        q("easy", "The classic urine protein in multiple myeloma is:", "Bence Jones protein", ["Albumin only", "Hemoglobin A", "Fibrinogen"], "Bence Jones proteins are free immunoglobulin light chains."),
        q("easy", "Multiple myeloma commonly causes bone lesions that are:", "Lytic punched-out lesions", ["Purely sclerotic in every case", "Cartilage-capped exostoses", "Caseating granulomas"], "Myeloma activates osteoclasts and suppresses osteoblasts."),
        q("moderate", "A common cause of renal failure in myeloma is:", "Light chain cast nephropathy", ["Membranous nephropathy only", "IgA vasculitis only", "Uric acid stones only"], "Filtered light chains injure tubules and form casts."),
        q("moderate", "A monoclonal spike on serum protein electrophoresis indicates:", "Monoclonal immunoglobulin production", ["Polyclonal infection only", "Platelet fragmentation", "Acute hemolysis"], "An M spike reflects a clonal plasma cell or B-cell process."),
        q("moderate", "Waldenstrom macroglobulinemia produces excess:", "IgM", ["IgA only", "IgE only", "IgD only"], "Lymphoplasmacytic lymphoma often secretes monoclonal IgM."),
        q("moderate", "Hyperviscosity syndrome is especially associated with:", "Waldenstrom macroglobulinemia", ["Iron deficiency anemia", "Reactive follicular hyperplasia", "Drug neutropenia"], "Large pentameric IgM can markedly increase serum viscosity."),
        q("high", "An older adult has back pain, anemia, recurrent infections, hypercalcemia, renal dysfunction, and punched-out skull lesions. Marrow shows sheets of clonal plasma cells. Which diagnosis is most likely?", "Multiple myeloma", ["Waldenstrom macroglobulinemia", "CLL/SLL", "Hodgkin lymphoma"], "CRAB features and clonal marrow plasma cells support multiple myeloma."),
        q("high", "A patient has mucosal bleeding, visual blurring, neurologic symptoms, lymphoplasmacytic marrow infiltrate, and a large IgM M spike without punched-out bone lesions. Which disorder best fits?", "Waldenstrom macroglobulinemia", ["Multiple myeloma", "Solitary plasmacytoma", "Primary myelofibrosis"], "IgM hyperviscosity with lymphoplasmacytic lymphoma indicates Waldenstrom macroglobulinemia."),
        q("high", "A patient has a small serum M spike but no lytic bone lesions, anemia, renal failure, hypercalcemia, or marrow plasmacytosis sufficient for myeloma. The lesion may progress over years. Which diagnosis is most appropriate?", "Monoclonal gammopathy of undetermined significance", ["Symptomatic multiple myeloma", "Burkitt lymphoma", "Acute myeloid leukemia"], "MGUS is an asymptomatic monoclonal gammopathy with risk of progression."),
    ]),
    ("spleen-thymus", "Spleen and Thymus Disorders", [
        q("easy", "The spleen removes old red cells primarily in the:", "Red pulp", ["White pulp follicles only", "Thymic cortex", "Bone marrow sinusoids only"], "Splenic red pulp filters blood and removes senescent cells."),
        q("easy", "The spleen helps defend especially against:", "Encapsulated bacteria", ["Dermatophytes only", "Helminths only", "Prions only"], "Splenic macrophages and antibodies are important for clearing encapsulated organisms."),
        q("easy", "Thymomas are tumors of:", "Thymic epithelial cells", ["Mature neutrophils", "Splenic macrophages", "Plasma cells"], "Thymoma is an epithelial neoplasm with admixed nonneoplastic lymphocytes."),
        q("moderate", "Asplenia increases risk of sepsis by:", "Impaired clearance of opsonized encapsulated organisms", ["Increased thymic selection", "Reduced red cell production only", "Excess eosinophils"], "The spleen filters blood-borne encapsulated bacteria."),
        q("moderate", "Howell-Jolly bodies are seen after:", "Splenectomy or functional asplenia", ["Thymoma resection only", "Acute appendicitis", "Pure iron deficiency"], "Nuclear remnants persist in RBCs when splenic filtering is absent."),
        q("moderate", "Thymoma is classically associated with:", "Myasthenia gravis", ["Polycythemia vera", "Burkitt lymphoma", "Hairy cell leukemia"], "Autoimmune disease, especially myasthenia gravis, can accompany thymoma."),
        q("moderate", "Hypersplenism can cause:", "Cytopenias from sequestration and destruction", ["Hypercalcemia from bone lysis", "Mediastinal compression only", "IgM hyperviscosity"], "An enlarged spleen can trap and destroy blood cells."),
        q("high", "A child without a spleen develops overwhelming sepsis due to Streptococcus pneumoniae despite previously normal neutrophil counts. Peripheral smear shows Howell-Jolly bodies. Which immune function was most impaired?", "Filtering blood-borne encapsulated bacteria", ["T-cell maturation in thymic cortex", "Granulocyte production in marrow", "IgE-mediated mast cell activation"], "Asplenia compromises clearance of encapsulated organisms."),
        q("high", "A patient has ptosis and fatigable weakness. Imaging shows an anterior mediastinal mass composed of thymic epithelial cells with many benign immature T cells. Which tumor is most likely?", "Thymoma", ["Hodgkin lymphoma", "Mediastinal seminoma", "Metastatic carcinoma"], "Thymoma is an anterior mediastinal epithelial tumor associated with myasthenia gravis."),
        q("high", "A patient with portal hypertension has massive splenomegaly, anemia, leukopenia, and thrombocytopenia. Bone marrow is cellular, suggesting peripheral sequestration rather than production failure. Which mechanism explains the cytopenias?", "Hypersplenism", ["Aplastic anemia", "Acute leukemia", "Pure red cell aplasia"], "Hypersplenism causes cytopenias by pooling and increased destruction in an enlarged spleen."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch13-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 13 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch13-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 13 questions")
    print(f"Removed {total_removed} existing Chapter 13 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 13 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
