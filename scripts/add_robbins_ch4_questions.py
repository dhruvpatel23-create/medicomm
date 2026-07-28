import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Hemodynamic Disorders, Thromboembolic Disease, and Shock"

BASE = {
    "subjectId": "pathology",
    "subjectTitle": "Pathology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "imageUrls": [],
}


def q(difficulty, prompt, answer, distractors, explanation):
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(f"Bad options for prompt: {prompt}")
    return {
        "difficulty": difficulty,
        "prompt": prompt,
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
    }


def jumble_answer_position(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    if len(distractors) != 3:
        raise ValueError(f"Cannot jumble options for {question.get('id', question['prompt'])}")
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    (
        "edema",
        "Edema and Effusions",
        [
            q("easy", "Edema is best defined as:", "Excess fluid in interstitial tissues or serous cavities", ["A localized collection of pus", "Coagulative necrosis from ischemia", "Platelet adhesion to exposed collagen"], "Edema is abnormal fluid accumulation outside vascular spaces, either in tissues or body cavities."),
            q("easy", "A transudate is typically:", "Protein-poor fluid caused by hydrostatic or oncotic imbalance", ["Protein-rich fluid caused by inflammation", "A clot made of platelets and fibrin", "A collection of neutrophils and necrotic debris"], "Transudates arise from noninflammatory pressure changes and have low protein and few cells."),
            q("easy", "An exudate is usually produced by:", "Inflammation with increased vascular permeability", ["Purely reduced plasma oncotic pressure", "Uncomplicated venous stasis without leakage", "Normal lymphatic drainage"], "Inflammatory endothelial leakage permits proteins and cells to enter extravascular spaces."),
            q("moderate", "Generalized edema due to congestive heart failure is mainly driven by:", "Increased hydrostatic pressure", ["Decreased capillary permeability", "Excess fibrinolysis", "Platelet aggregation"], "Venous congestion increases hydrostatic pressure, pushing fluid out of vessels."),
            q("moderate", "Nephrotic syndrome causes edema primarily through:", "Reduced plasma oncotic pressure from albumin loss", ["Excess tissue factor release", "Increased platelet adhesion", "Arteriolar vasoconstriction only"], "Heavy proteinuria lowers plasma albumin and oncotic pressure, favoring fluid movement into tissues."),
            q("moderate", "Lymphatic obstruction causes edema because it:", "Prevents removal of interstitial fluid and proteins", ["Increases antithrombin activity", "Activates protein C", "Converts fibrin into fibrinogen"], "Blocked lymphatics impair return of extravascular fluid and proteins to the circulation."),
            q("moderate", "Pulmonary edema is clinically dangerous because it can:", "Impair gas exchange in alveolar spaces", ["Increase platelet count", "Prevent all inflammatory responses", "Convert red infarcts into white infarcts"], "Fluid in alveoli increases diffusion distance and can cause hypoxemia."),
            q("very high", "Pitting edema occurs when pressure on swollen subcutaneous tissue:", "Displaces interstitial fluid and leaves a temporary depression", ["Fragments a thrombus into emboli", "Produces a fibrinous exudate", "Activates factor XII"], "Mobile interstitial fluid can be pushed aside, creating a transient pit."),
            q("very high", "Brain edema is especially dangerous because:", "The skull limits expansion and raised pressure can compromise perfusion or cause herniation", ["Brain tissue has abundant collateral lymphatics", "It always remains limited to subcutaneous tissue", "It prevents ischemic injury"], "Intracranial swelling in a closed space can raise pressure and injure vital centers."),
            q("very high", "Which combination most strongly favors transudative edema?", "Increased hydrostatic pressure with reduced plasma oncotic pressure", ["Bacterial infection with neutrophil exudation", "Endothelial necrosis with fibrin leakage", "Abscess formation with liquefactive debris"], "Transudates reflect pressure imbalance, particularly elevated hydrostatic or decreased oncotic pressure."),
        ],
    ),
    (
        "congestion",
        "Hyperemia, Congestion, and Hemorrhage",
        [
            q("easy", "Hyperemia is:", "An active process caused by arteriolar dilation and increased inflow", ["A passive process from impaired venous outflow", "A platelet-rich thrombus", "A fibrinous pericardial exudate"], "Hyperemia is active vascular dilation, such as in exercise or inflammation."),
            q("easy", "Congestion is:", "A passive process caused by impaired venous outflow", ["Active arteriolar dilation", "Primary platelet aggregation", "Coagulation factor deficiency"], "Congestion results from venous obstruction or heart failure and produces cyanotic, blood-filled tissues."),
            q("easy", "Petechiae are best described as:", "Minute 1- to 2-mm hemorrhages", ["Large 1- to 2-cm bruises", "Localized collections of pus", "Organized arterial thrombi"], "Petechiae are tiny hemorrhages often linked to platelet defects or thrombocytopenia."),
            q("moderate", "Chronic passive congestion of the lung commonly produces:", "Hemosiderin-laden macrophages", ["Caseating granulomas", "Liquefactive abscesses", "Lines of Zahn"], "Repeated capillary rupture in congested lungs leaves iron pigment in macrophages."),
            q("moderate", "A nutmeg liver is associated with:", "Chronic passive hepatic congestion", ["Fat embolism", "Primary hemostatic failure", "Air embolism"], "Right-sided heart failure can cause centrilobular congestion and a mottled liver appearance."),
            q("moderate", "Purpura are larger than petechiae and measure at least about:", "3 mm", ["0.1 mm", "20 cm", "1 meter"], "Purpura are hemorrhages larger than petechiae; ecchymoses are larger bruises."),
            q("moderate", "Ecchymoses are commonly called:", "Bruises", ["Abscesses", "Vegetations", "Infarcts"], "Ecchymoses are larger subcutaneous hemorrhages, typically 1 to 2 cm."),
            q("very high", "The color change in an old bruise from blue-red to green-brown mainly reflects:", "Hemoglobin breakdown and hemosiderin/bilirubin pigment formation", ["Immediate fibrin polymerization", "Platelet degranulation only", "Complement activation"], "Extravasated red cells are degraded, generating pigments that alter the bruise color."),
            q("very high", "A hematoma is:", "A localized mass of extravasated blood", ["A sterile transudate", "A platelet receptor deficiency", "A bland embolus"], "A hematoma is blood accumulated within tissues, sometimes forming a palpable mass."),
            q("very high", "Why can a small intracranial hemorrhage be fatal while a larger subcutaneous hemorrhage may not be?", "The rigid skull permits pressure rise and compression of vital brain tissue", ["Subcutaneous tissues cannot recycle iron", "Brain hemorrhage never triggers inflammation", "Skin has no vascular supply"], "Location matters; intracranial bleeding can raise pressure and cause herniation or perfusion failure."),
        ],
    ),
    (
        "hemostasis",
        "Normal Hemostasis",
        [
            q("easy", "The first immediate response to vascular injury is usually:", "Transient arteriolar vasoconstriction", ["Permanent venous thrombosis", "Fibroblast scar formation", "Systemic septic shock"], "Neurogenic reflexes and endothelin cause brief vasoconstriction that reduces blood loss."),
            q("easy", "Primary hemostasis produces:", "A platelet plug", ["A mature collagen scar", "A pulmonary embolus", "A liquefactive infarct"], "Primary hemostasis depends on platelet adhesion, activation, and aggregation."),
            q("easy", "Secondary hemostasis stabilizes the platelet plug mainly by forming:", "Fibrin", ["Albumin", "Hemosiderin", "Bilirubin"], "The coagulation cascade generates thrombin, which converts fibrinogen to fibrin."),
            q("moderate", "Platelet adhesion to subendothelial matrix is mediated largely by:", "GpIb binding von Willebrand factor", ["GpIIb/IIIa binding albumin", "Protein C binding factor V", "C5a binding collagen"], "vWF bridges exposed matrix and platelet GpIb, allowing adhesion under flow."),
            q("moderate", "Platelet aggregation is mediated mainly by:", "GpIIb/IIIa binding fibrinogen bridges between platelets", ["GpIb binding plasmin", "TFPI binding fibrin", "Antithrombin binding collagen"], "Activated GpIIb/IIIa binds fibrinogen, linking adjacent platelets."),
            q("moderate", "Dense granules of platelets contain important mediators such as:", "ADP and calcium", ["Type I collagen and elastin", "C3b and C5b-9", "Insulin and glucagon"], "Dense granules release ADP and calcium, which support platelet activation and coagulation."),
            q("moderate", "Aspirin impairs platelet function by inhibiting synthesis of:", "Thromboxane A2", ["Von Willebrand factor", "Protein S", "Tissue factor pathway inhibitor"], "Aspirin blocks platelet cyclooxygenase, reducing TxA2-mediated aggregation."),
            q("very high", "Bernard-Soulier syndrome causes bleeding because of defective:", "Platelet GpIb", ["Platelet GpIIb/IIIa", "Factor V Leiden", "Protein C activation"], "GpIb deficiency impairs platelet adhesion to vWF."),
            q("very high", "Glanzmann thrombasthenia is caused by deficiency of:", "GpIIb/IIIa", ["GpIb", "Factor XII", "Antithrombin"], "Loss of GpIIb/IIIa prevents fibrinogen-mediated platelet aggregation."),
            q("very high", "Thrombin is central to hemostasis because it:", "Converts fibrinogen to fibrin and activates platelets", ["Only dissolves fibrin clots", "Only inhibits platelet aggregation", "Only causes lymphatic obstruction"], "Thrombin amplifies coagulation, activates platelets, and generates fibrin."),
        ],
    ),
    (
        "coagulation",
        "Platelets, Coagulation Factors, and Anticoagulant Mechanisms",
        [
            q("easy", "The prothrombin time primarily screens the:", "Extrinsic pathway and common pathway", ["Intrinsic pathway only", "Platelet adhesion pathway", "Fibrinolytic pathway only"], "PT assesses factors VII, X, V, II, and fibrinogen."),
            q("easy", "The partial thromboplastin time primarily screens the:", "Intrinsic pathway and common pathway", ["Extrinsic pathway only", "Platelet dense granules", "Lymphatic drainage"], "PTT assesses factors XII, XI, IX, VIII, X, V, II, and fibrinogen."),
            q("easy", "Vitamin K is needed for gamma-carboxylation of:", "Factors II, VII, IX, and X", ["Factors I, V, VIII, and XIII only", "vWF and GpIb", "Albumin and fibrinogen only"], "Vitamin K-dependent carboxylation allows calcium binding by several coagulation factors."),
            q("moderate", "The most important in vivo initiator of coagulation after injury is:", "Tissue factor with factor VIIa", ["Factor XII activation alone", "Albumin leakage", "Platelet serotonin release only"], "Tissue factor exposed or expressed at injury sites complexes with VIIa to initiate coagulation."),
            q("moderate", "Plasmin limits clot size by:", "Degrading fibrin", ["Activating GpIIb/IIIa", "Producing thromboxane A2", "Synthesizing vWF"], "Plasmin is the major fibrinolytic enzyme and breaks down fibrin polymers."),
            q("moderate", "Tissue plasminogen activator acts by:", "Converting plasminogen to plasmin", ["Converting fibrinogen to fibrin", "Activating platelets through PAR-1", "Blocking protein C"], "t-PA promotes fibrinolysis by generating plasmin."),
            q("moderate", "Antithrombin inhibits thrombin and several clotting factors, and its activity is enhanced by:", "Heparin-like molecules and therapeutic heparin", ["Aspirin", "Thromboxane A2", "Serotonin"], "Heparin accelerates antithrombin activity against thrombin and factors including Xa."),
            q("very high", "Thrombomodulin on intact endothelium changes thrombin activity by:", "Promoting protein C activation", ["Increasing platelet aggregation", "Blocking t-PA release", "Activating factor VII directly"], "Thrombin bound to thrombomodulin activates protein C, which inhibits Va and VIIIa with protein S."),
            q("very high", "Activated protein C with protein S inhibits:", "Factors Va and VIIIa", ["GpIb and vWF", "Fibrin and plasmin", "ADP and serotonin"], "The protein C/S system is an endothelial anticoagulant mechanism that turns off key cofactors."),
            q("very high", "Tissue factor pathway inhibitor limits coagulation by inhibiting:", "Tissue factor-factor VIIa complexes", ["GpIIb/IIIa-fibrinogen binding", "Plasminogen activation", "Platelet dense granule release"], "TFPI restrains the tissue factor pathway, helping confine coagulation to the injury site."),
        ],
    ),
    (
        "bleeding",
        "Hemorrhagic Disorders",
        [
            q("easy", "Defects of primary hemostasis most often cause:", "Petechiae and mucosal bleeding", ["Deep muscle hematomas only", "Pulmonary thromboembolism", "White infarcts"], "Platelet/vWF problems commonly present with skin and mucosal bleeding."),
            q("easy", "Defects of secondary hemostasis most often cause:", "Deep soft tissue bleeding and hemarthroses", ["Only tiny petechiae", "Pulmonary edema", "Nutmeg liver"], "Coagulation factor deficiencies tend to cause deeper bleeding into muscles and joints."),
            q("easy", "Hemarthrosis is especially characteristic of:", "Hemophilia", ["Thrombocytopenia alone", "Pulmonary congestion", "Fat embolism"], "Severe factor VIII or IX deficiency classically causes recurrent joint bleeding."),
            q("moderate", "A patient with thrombocytopenia is at particular risk for:", "Petechiae and potentially fatal intracerebral hemorrhage", ["Caseous granulomas", "Red infarcts only", "Air embolism after diving"], "Very low platelet counts impair primary hemostasis and can cause serious bleeding."),
            q("moderate", "Aspirin can produce a mild bleeding tendency because it:", "Impairs platelet thromboxane A2 synthesis", ["Activates factor X", "Increases protein C", "Raises fibrinogen cross-linking"], "Platelets cannot resynthesize cyclooxygenase, so aspirin reduces platelet aggregation."),
            q("moderate", "Uremia causes bleeding mainly by:", "Altering platelet function", ["Producing factor V Leiden", "Increasing tissue factor", "Creating septic emboli"], "Renal failure can impair platelet function and primary hemostasis."),
            q("moderate", "Scurvy may cause purpura and ecchymoses because:", "Defective collagen weakens small vessel walls", ["It increases platelet aggregation", "It creates factor VIII excess", "It causes pulmonary emboli"], "Vitamin C deficiency impairs collagen synthesis, increasing vascular fragility."),
            q("very high", "Palpable purpura most strongly suggests:", "Small-vessel inflammation or vascular wall injury", ["Pure factor VIII deficiency", "Simple transudative edema", "Normal platelet plug formation"], "Vasculitis and vessel wall disorders can cause palpable purpuric lesions."),
            q("very high", "Rapid loss of more than about 20% of blood volume can lead to:", "Hemorrhagic hypovolemic shock", ["Primary hyperemia", "Nephrotic edema", "Fat embolism syndrome"], "Large acute blood loss reduces effective circulating volume and tissue perfusion."),
            q("very high", "Chronic external blood loss most characteristically causes:", "Iron deficiency anemia", ["Hemochromatosis", "Polycythemia vera", "Thrombotic thrombocytopenic purpura"], "Repeated loss of red cells and iron, such as GI or menstrual bleeding, depletes iron stores."),
        ],
    ),
    (
        "thrombosis",
        "Thrombosis and Virchow Triad",
        [
            q("easy", "Virchow triad consists of endothelial injury, abnormal blood flow, and:", "Hypercoagulability", ["Hypoalbuminemia", "Lymphatic obstruction", "Reduced oncotic pressure"], "These three factors are the major contributors to pathologic thrombosis."),
            q("easy", "Arterial thrombi are typically rich in:", "Platelets", ["Bile pigment", "Serous fluid", "Air bubbles"], "High-shear arterial thrombi depend strongly on platelet adhesion and activation."),
            q("easy", "Venous thrombi are typically:", "Red cell-rich and associated with stasis", ["Always sterile gas bubbles", "Composed only of platelets", "Confined to lymphatics"], "Slow venous flow promotes coagulation and traps red cells, forming red thrombi."),
            q("moderate", "Lines of Zahn indicate:", "Antemortem thrombus formation in flowing blood", ["Postmortem clot only", "Pure edema fluid", "Fat embolism"], "Alternating pale platelet/fibrin and dark red cell layers form only when blood is flowing."),
            q("moderate", "Endothelial injury promotes thrombosis by:", "Exposing vWF and tissue factor", ["Increasing albumin synthesis", "Reducing all platelet adhesion", "Activating t-PA only"], "Injury exposes prothrombotic matrix and tissue factor, triggering platelets and coagulation."),
            q("moderate", "Stasis promotes thrombosis partly because it:", "Prevents dilution and washout of activated clotting factors", ["Increases lymphatic drainage", "Blocks all platelet adhesion", "Raises plasma oncotic pressure"], "Stasis keeps activated factors near the vessel wall and brings platelets into contact with endothelium."),
            q("moderate", "Turbulence promotes arterial thrombosis by:", "Causing endothelial dysfunction and local pockets of stasis", ["Increasing protein C activation only", "Preventing platelet contact with endothelium", "Lowering blood viscosity"], "Disturbed flow injures/activates endothelium and disrupts laminar flow."),
            q("very high", "Factor V Leiden causes hypercoagulability because factor V becomes resistant to:", "Activated protein C", ["Antithrombin", "Plasmin", "Aspirin"], "The Leiden mutation impairs APC-mediated inactivation of factor Va."),
            q("very high", "Antiphospholipid antibody syndrome is paradoxically associated clinically with:", "Thrombosis despite prolonged phospholipid-dependent clotting tests in vitro", ["Only severe mucosal bleeding", "Only transudative edema", "Only platelet absence"], "Antiphospholipid antibodies may prolong PTT assays yet cause arterial/venous thrombosis and pregnancy morbidity."),
            q("very high", "Mural thrombi are thrombi that:", "Form on the wall of a heart chamber or large vessel", ["Float freely in lymphatic channels", "Occur only after death", "Are composed only of air"], "Mural thrombi are attached to endocardial or vascular walls, often after MI or in aneurysms."),
        ],
    ),
    (
        "fate-dic",
        "Fate and Clinical Consequences of Thrombi, including DIC",
        [
            q("easy", "Propagation of a thrombus means:", "Accumulation of more platelets and fibrin", ["Complete enzymatic dissolution", "Replacement by normal endothelium immediately", "Transformation into edema"], "A thrombus may enlarge by additional platelet and fibrin deposition."),
            q("easy", "Embolization means a thrombus:", "Detaches and travels to another vascular site", ["Becomes a bruise", "Turns into pus", "Raises plasma oncotic pressure"], "Fragments of thrombi can travel and lodge downstream as emboli."),
            q("easy", "Thrombus dissolution is most likely when:", "Fibrinolysis occurs early in a recent thrombus", ["A thrombus is old and densely organized", "All plasmin is inhibited", "The thrombus calcifies"], "Recent thrombi may be removed by fibrinolytic activity."),
            q("moderate", "Organization of a thrombus involves:", "Ingrowth of endothelial cells, smooth muscle cells, and fibroblasts", ["Pure conversion to air", "Immediate disappearance without repair", "Transformation into a transudate"], "Older thrombi may be incorporated into the vessel wall by repair tissue."),
            q("moderate", "Recanalization refers to:", "Formation of channels through an organized thrombus", ["Complete obstruction by a fresh embolus", "Albumin leakage into tissue", "Platelet receptor activation"], "Channels may restore limited blood flow across an organized thrombus."),
            q("moderate", "The most important clinical consequence of venous thrombosis is often:", "Pulmonary embolism", ["Brain liquefaction without emboli", "Serous inflammation", "Keloid formation"], "Deep venous thrombi can embolize through the right heart to pulmonary arteries."),
            q("moderate", "The most important clinical consequence of arterial thrombosis is often:", "Downstream tissue infarction", ["Generalized pitting edema only", "Iron deficiency anemia only", "Transudate formation"], "Arterial thrombi can occlude blood supply to organs such as heart, brain, or bowel."),
            q("very high", "Disseminated intravascular coagulation is best described as:", "Widespread microvascular thrombosis with consumption of platelets and coagulation factors", ["A single organized mural thrombus", "A localized bruise from trauma", "Pure platelet adhesion without fibrin"], "DIC consumes clotting components while forming microthrombi, causing both thrombosis and bleeding."),
            q("very high", "A classic trigger of DIC is:", "Obstetric complications, sepsis, or advanced malignancy", ["Simple pitting edema", "Mild hyperemia after exercise", "Uncomplicated aspirin use"], "DIC is secondary to disorders that strongly activate coagulation systemically."),
            q("very high", "Bleeding in DIC occurs mainly because:", "Platelets and coagulation factors are consumed and fibrinolysis is activated", ["There is no thrombin generation", "All vessels become lymphatics", "Only red cells are consumed"], "DIC paradoxically causes hemorrhage because hemostatic elements are depleted during widespread clotting."),
        ],
    ),
    (
        "embolism",
        "Embolism",
        [
            q("easy", "An embolus is:", "A detached intravascular solid, liquid, or gas mass carried by blood", ["A fixed bruise in subcutaneous tissue", "A low-protein edema fluid", "A platelet receptor"], "Emboli travel through blood and lodge at distant sites."),
            q("easy", "Most pulmonary emboli arise from:", "Deep veins of the lower limbs", ["Left atrial mural thrombi only", "Carotid atherosclerotic plaques", "Pulmonary alveoli"], "Deep venous thrombi are the common source of pulmonary thromboembolism."),
            q("easy", "Systemic arterial emboli most commonly lodge in:", "Lower extremities and brain", ["Only pulmonary arteries", "Only lymph nodes", "Only alveolar spaces"], "Systemic emboli travel through arterial circulation and often affect legs, brain, bowel, kidney, or spleen."),
            q("moderate", "A saddle pulmonary embolus lodges at:", "The bifurcation of the main pulmonary artery", ["A superficial skin capillary", "The hepatic sinusoids", "The renal pelvis"], "Large emboli can straddle the pulmonary artery bifurcation and cause sudden death."),
            q("moderate", "Small recurrent pulmonary emboli may cause:", "Pulmonary hypertension", ["Nephrotic syndrome", "Keloids", "Vitamin K deficiency"], "Repeated embolic obstruction can increase pulmonary vascular resistance."),
            q("moderate", "Fat embolism syndrome classically follows:", "Long bone fractures or soft tissue trauma", ["Pure dehydration", "Aspirin ingestion", "Chronic passive liver congestion"], "Marrow fat can enter torn vessels after skeletal trauma."),
            q("moderate", "The classic triad of fat embolism syndrome includes respiratory distress, neurologic symptoms, and:", "Petechial rash", ["Hemarthrosis", "Keloid scar", "Nutmeg liver"], "Fat embolism syndrome presents with pulmonary insufficiency, neurologic signs, anemia/thrombocytopenia, and petechiae."),
            q("very high", "Air embolism in divers is related to:", "Gas bubbles coming out of solution during rapid decompression", ["vWF deficiency", "Factor V Leiden", "Albumin loss in urine"], "Decompression can form nitrogen bubbles that obstruct vessels and injure tissue."),
            q("very high", "Caisson disease is another name for:", "Decompression sickness", ["DIC", "Nephrotic syndrome", "Hemophilia A"], "Caisson disease occurs when dissolved gases form bubbles during decompression."),
            q("very high", "Amniotic fluid embolism is dangerous because it can cause:", "Sudden respiratory distress, shock, seizures, and DIC", ["Only mild pitting ankle edema", "Only chronic iron deficiency", "Only platelet adhesion defects"], "Entry of amniotic fluid into maternal circulation can trigger pulmonary dysfunction, shock, and consumptive coagulopathy."),
        ],
    ),
    (
        "infarction",
        "Infarction",
        [
            q("easy", "An infarct is:", "An area of ischemic necrosis", ["A platelet granule", "A low-protein effusion", "A bruise only"], "Infarction is tissue necrosis caused by loss of blood supply or venous drainage."),
            q("easy", "Most infarcts are caused by:", "Thrombotic or embolic arterial occlusion", ["Simple hyperemia", "Normal lymphatic drainage", "Increased oncotic pressure"], "Arterial occlusion by thrombi or emboli is the most common cause."),
            q("easy", "White infarcts usually occur in:", "Solid organs with end-arterial circulation", ["Loose spongy tissues with dual blood supply", "Venous occlusion of ovary", "Pulmonary tissue after venous congestion"], "Pale infarcts occur in compact tissues where arterial inflow is blocked and little blood can enter."),
            q("moderate", "Red infarcts are likely with:", "Venous occlusion or tissues with dual blood supply", ["End-arterial occlusion in compact kidney only", "Pure platelet adhesion without occlusion", "Reduced plasma oncotic pressure"], "Hemorrhagic infarcts occur when blood can enter necrotic tissue or when venous drainage is blocked."),
            q("moderate", "Pulmonary infarcts are often red because the lung:", "Has dual blood supply and spongy parenchyma", ["Has no blood supply", "Cannot hemorrhage", "Always undergoes caseous necrosis"], "Bronchial and pulmonary arterial supplies and loose tissue architecture favor hemorrhagic infarction."),
            q("moderate", "The dominant histologic pattern in most non-brain infarcts is:", "Coagulative necrosis", ["Liquefactive necrosis", "Caseous necrosis", "Fat necrosis"], "Ischemia usually produces coagulative necrosis except in the brain."),
            q("moderate", "Brain infarction characteristically produces:", "Liquefactive necrosis", ["Coagulative necrosis with firm scar at once", "Caseous granuloma", "Serous exudate"], "CNS ischemic injury causes liquefactive necrosis."),
            q("very high", "Whether vascular occlusion causes infarction depends strongly on:", "Collateral supply, rate of occlusion, tissue susceptibility, and oxygen content", ["Only platelet count", "Only skin temperature", "Only lymphatic drainage"], "Robbins emphasizes these determinants of infarct development."),
            q("very high", "A septic infarct means:", "The infarct is infected or seeded by microbes", ["The infarct is always pale and sterile", "The infarct is caused only by albumin loss", "The infarct is a postmortem clot"], "Septic emboli can seed organisms into infarcted tissue and form abscesses."),
            q("very high", "Microscopic evidence of necrosis after vascular occlusion may be absent for the first:", "Several hours", ["Several months", "Several years", "Exactly 30 days"], "Histologic necrosis typically requires hours to become apparent after ischemic injury."),
        ],
    ),
    (
        "shock",
        "Shock",
        [
            q("easy", "Shock is best defined as:", "Systemic tissue hypoperfusion from reduced cardiac output or effective circulating volume", ["Localized edema from lymphatic obstruction", "A platelet plug at an injury site", "A small mucosal hemorrhage"], "Shock is circulatory failure that causes cellular hypoxia and organ dysfunction."),
            q("easy", "The three major types of shock are:", "Cardiogenic, hypovolemic, and septic", ["Serous, fibrinous, and purulent", "Red, white, and septic infarcts", "Primary, secondary, and tertiary hemostasis"], "Robbins emphasizes cardiogenic, hypovolemic, and septic shock as major categories."),
            q("easy", "Cardiogenic shock can be caused by:", "Myocardial infarction", ["Mild ankle edema only", "GpIb deficiency", "Vitamin C deficiency"], "Pump failure after MI can reduce cardiac output and perfusion."),
            q("moderate", "Hypovolemic shock can result from:", "Severe hemorrhage or fluid loss", ["Increased cardiac contractility", "Minor hyperemia", "Normal plasma volume"], "Loss of blood or plasma volume reduces effective circulating volume."),
            q("moderate", "Early septic shock may show warm, flushed skin because of:", "Peripheral vasodilation", ["Pure peripheral vasoconstriction", "Increased oncotic pressure", "Platelet absence"], "Unlike hypovolemic/cardiogenic shock, early sepsis often causes vasodilation."),
            q("moderate", "A key feature of septic shock pathogenesis is:", "Dysregulated host response with endothelial activation, vasodilation, leakage, and DIC", ["Only loss of albumin in urine", "Only failure of platelet adhesion", "Only chronic passive congestion"], "Septic shock is driven by inflammatory mediators, endothelial dysfunction, coagulation activation, and metabolic abnormalities."),
            q("moderate", "The initial nonprogressive stage of shock maintains perfusion through:", "Compensatory neurohumoral mechanisms", ["Immediate lysosomal rupture", "Complete arteriolar paralysis", "Universal DIC"], "Baroreflexes, catecholamines, ADH, and RAAS help preserve blood pressure and vital organ flow."),
            q("very high", "The progressive stage of shock is characterized by:", "Tissue hypoperfusion with lactic acidosis and worsening circulatory failure", ["Complete recovery without intervention", "Only local platelet aggregation", "Improved aerobic metabolism"], "Persistent hypoxia shifts metabolism to anaerobic glycolysis, causing lactic acidosis and vasomotor failure."),
            q("very high", "Irreversible shock means:", "Cellular injury is so severe that survival is impossible even if hemodynamics are corrected", ["The patient has only mild hypotension", "All organs regenerate fully", "Only the skin is affected"], "Late shock produces severe cellular and organ injury that cannot be reversed by restoring pressure alone."),
            q("very high", "Septic shock commonly causes microvascular thrombosis because inflammatory cytokines:", "Increase tissue factor, reduce anticoagulants, and increase PAI-1", ["Increase thrombomodulin and t-PA only", "Block all thrombin generation", "Prevent endothelial activation"], "Sepsis promotes coagulation and inhibits fibrinolysis, leading to DIC and tissue ischemia."),
        ],
    ),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch4-{slug}-{index}", "topic": topic, **data}
            jumble_answer_position(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(ch4_questions, all_questions=None):
    if len(ch4_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 4 questions, got {len(ch4_questions)}")
    topic_counts = Counter(q["topic"] for q in ch4_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "very high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in ch4_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in ch4_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    ch4_questions = build_questions()
    validate(ch4_questions)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
    existing = data.get("questions", [])
    kept = [
        question
        for question in existing
        if not (
            question.get("chapterTitle") == CHAPTER
            or str(question.get("id", "")).startswith("robbins-ch4-")
        )
    ]
    data["questions"] = kept + ch4_questions
    validate(ch4_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Removed {len(existing) - len(kept)} existing Chapter 4 questions")
    print(f"Added {len(ch4_questions)} Robbins Chapter 4 questions")
    for topic, count in Counter(q["topic"] for q in ch4_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
