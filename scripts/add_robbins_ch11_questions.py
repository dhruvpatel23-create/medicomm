import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Blood Vessels"
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
    ("vascular-wall", "Vascular Wall, Endothelial Cells, and Smooth Muscle Cells", [
        q("easy", "Which vascular layer is directly exposed to flowing blood and normally provides an antithrombotic surface?", "Intima", ["Media", "Adventitia", "External elastic lamina"], "The intima contains endothelium and subendothelial connective tissue."),
        q("easy", "Which endothelial products normally promote vasodilation and inhibit platelet activation?", "Nitric oxide and prostacyclin", ["Endothelin and thromboxane A2", "Collagen and tissue factor", "C5a and leukotriene B4"], "NO and prostacyclin maintain flow by relaxing smooth muscle and limiting platelet activation."),
        q("easy", "The principal contractile cells of the tunica media are:", "Smooth muscle cells", ["Macrophages", "Plasma cells", "Megakaryocytes"], "Smooth muscle cells regulate vascular tone and respond to injury."),
        q("moderate", "During acute inflammation, endothelial activation is important because it:", "Increases leukocyte adhesion and creates a more procoagulant surface", ["Prevents cytokine signaling", "Eliminates all platelet binding", "Converts arteries into veins"], "Activated endothelium expresses adhesion molecules and favors leukocyte recruitment and thrombosis."),
        q("moderate", "Restenosis after angioplasty is mainly driven by:", "Smooth muscle migration, proliferation, and matrix synthesis", ["Neutrophilic abscess formation", "Amyloid deposition", "Viral cytopathic effect"], "Vascular injury stimulates intimal smooth muscle proliferation and extracellular matrix deposition."),
        q("moderate", "Vasa vasorum are most important in large vessels because they:", "Supply the outer media and adventitia", ["Drain lymph from capillaries only", "Prevent all aneurysm formation", "Form venous valves"], "Large vessels are too thick to be nourished entirely by diffusion from the lumen."),
        q("moderate", "Loss of endothelial nitric oxide bioavailability favors which combination of changes?", "Vasoconstriction, platelet adhesion, and inflammation", ["Universal vasodilation and plaque regression", "Absent leukocyte recruitment", "Immediate lymphatic obstruction"], "Endothelial dysfunction promotes abnormal tone, thrombosis, and inflammatory recruitment."),
        q("high", "A diabetic smoker has coronary arteries with impaired vasodilation, increased endothelial adhesion molecule expression, and platelet activation before severe luminal narrowing is present. Which early abnormality best links these risk factors to later plaque formation?", "Endothelial dysfunction", ["Medial calcific sclerosis", "Leukocytoclastic vasculitis", "Venous valve incompetence"], "Atherosclerotic risk factors dysregulate endothelium, enabling lipid entry, inflammation, and thrombosis-prone behavior."),
        q("high", "Months after balloon angioplasty, a coronary segment narrows again. Histology shows intimal smooth muscle proliferation with abundant extracellular matrix but no necrotizing vasculitis. Which process explains this restenosis?", "Intimal hyperplasia after vascular injury", ["Caseating granulomatous arteritis", "Primary lymphedema", "Berry aneurysm rupture"], "Restenosis is a repair response caused by smooth muscle migration/proliferation and matrix deposition."),
        q("high", "Tertiary syphilis damages the small vessels that nourish the thoracic aortic wall. The aortic media becomes ischemic and scarred, predisposing to ascending aortic dilation. Which structure is primarily injured?", "Vasa vasorum", ["Venous valves", "Capillary basement membrane", "Cardiac conduction fibers"], "Obliterative endarteritis of vasa vasorum causes medial ischemia and thoracic aneurysm."),
    ]),
    ("atherogenesis", "Atherosclerosis: Risk Factors and Pathogenesis", [
        q("easy", "Atherosclerosis primarily affects which vessels?", "Large and medium-sized arteries", ["Postcapillary venules", "Lymphatic channels", "Pulmonary capillaries only"], "Atherosclerosis is an intimal disease of elastic and muscular arteries."),
        q("easy", "The earliest visible lesion of atherosclerosis is the:", "Fatty streak", ["Complicated plaque", "Berry aneurysm", "Organizing thrombus"], "Fatty streaks are intimal collections of lipid-laden foam cells."),
        q("easy", "Which lipoprotein is most directly implicated in atheroma formation?", "LDL", ["Albumin", "IgM", "Fibrinogen"], "LDL enters the intima, becomes modified, and drives foam cell formation."),
        q("moderate", "Foam cells in atherosclerotic lesions are mainly:", "Macrophages and smooth muscle cells that have ingested lipid", ["Eosinophils with Charcot-Leyden crystals", "Megakaryocytes with platelet granules", "Mast cells with IgE"], "Macrophages and smooth muscle cells can accumulate lipid and become foam cells."),
        q("moderate", "Oxidized LDL promotes atherogenesis because it is:", "Proinflammatory and taken up by scavenger receptors", ["Cleared only by regulated LDL receptors", "Protective against monocyte recruitment", "Able to dissolve fibrous caps"], "Modified LDL stimulates inflammation and is ingested by macrophage scavenger receptors."),
        q("moderate", "Which plaque is least likely to rupture?", "A plaque with a thick fibrous cap and smaller lipid core", ["A plaque with a thin inflamed cap", "A plaque with abundant macrophages at the shoulder", "A plaque with a large necrotic lipid core"], "Thick collagen-rich caps are more stable than thin inflamed caps."),
        q("moderate", "The major modifiable risk factors for atherosclerosis include:", "Hyperlipidemia, hypertension, smoking, and diabetes", ["Age, sex, and family history only", "ABO blood group only", "Height and hair color"], "These factors injure endothelium or alter lipid and inflammatory responses."),
        q("high", "A man dies suddenly from coronary thrombosis. Autopsy shows a plaque with a large necrotic core, many macrophages at the shoulder, and a very thin fibrous cap that has ruptured. Which feature made this plaque vulnerable?", "Thin inflamed fibrous cap over a large lipid core", ["Dense medial calcification without luminal narrowing", "A thick collagen-rich cap", "A pure fatty streak without necrosis"], "Vulnerable plaques have thin caps, lipid-rich cores, and abundant inflammation."),
        q("high", "A macrophage in the arterial intima keeps taking up modified LDL despite becoming cholesterol-rich. The responsible uptake pathway is not down-regulated by intracellular cholesterol. Which receptor class explains this?", "Scavenger receptors", ["Insulin receptors", "Beta-adrenergic receptors", "T-cell receptors"], "Scavenger receptors internalize modified LDL without normal feedback suppression."),
        q("high", "After aortic catheterization, a patient develops blue toes and renal dysfunction. Biopsy of a small artery shows elongated empty clefts surrounded by inflammation. Which atherosclerotic complication is most likely?", "Cholesterol atheroembolism", ["Septic embolism from endocarditis", "Fat embolism after fracture", "Air embolism from diving"], "Disrupted plaques can release cholesterol crystals that leave needle-shaped clefts in tissue."),
    ]),
    ("plaque-complications", "Atherosclerotic Plaque Complications and Clinical Consequences", [
        q("easy", "Rupture of an atherosclerotic plaque most directly predisposes to:", "Thrombosis", ["Lymphangioma", "Thymoma", "Pure transudative edema"], "Rupture exposes thrombogenic material and may cause acute occlusive thrombosis."),
        q("easy", "Atherosclerosis of the abdominal aorta commonly predisposes to:", "Abdominal aortic aneurysm", ["Acute rheumatic fever", "Sarcoidosis", "Primary immunodeficiency"], "Severe aortic atherosclerosis weakens the media and favors aneurysm formation."),
        q("easy", "Stable angina usually reflects:", "Fixed coronary atherosclerotic narrowing", ["Acute myocarditis", "Right atrial myxoma only", "Pulmonary embolism only"], "Stable plaques limit flow during increased myocardial demand."),
        q("moderate", "Hemorrhage into an atherosclerotic plaque can worsen ischemia by:", "Expanding plaque volume and narrowing the lumen", ["Removing all lipid", "Repairing the fibrous cap", "Creating venous valves"], "Bleeding from plaque neovessels or cap disruption can abruptly enlarge a plaque."),
        q("moderate", "Renal artery atherosclerosis may produce hypertension by:", "Activating the renin-angiotensin system", ["Causing IgE-mediated mast cell degranulation", "Blocking lymphatic drainage only", "Increasing pulmonary surfactant"], "Reduced renal perfusion stimulates renin release."),
        q("moderate", "Critical coronary stenosis usually becomes symptomatic because it:", "Limits flow during exertion or increased demand", ["Prevents all thrombosis", "Causes only venous congestion", "Excludes ischemia"], "A fixed severe narrowing causes demand-related ischemia."),
        q("moderate", "Which change makes an atherosclerotic plaque 'complicated'?", "Surface rupture with superimposed thrombus", ["Normal overlying endothelium", "Absence of calcification", "Complete lack of inflammation"], "Complicated plaques show rupture, ulceration, hemorrhage, thrombosis, or calcification."),
        q("high", "A patient develops predictable chest pain when climbing stairs. Angiography shows a stable coronary plaque causing severe fixed narrowing, but no acute plaque rupture. Which clinical syndrome is best explained?", "Stable angina from chronic critical stenosis", ["Unstable angina from acute plaque change", "Myocarditis", "Cardiac tamponade"], "Fixed stenosis causes reproducible ischemia during stress."),
        q("high", "A carotid plaque ulcerates and sends embolic material into the cerebral circulation, causing transient unilateral weakness. There is no primary intracerebral hemorrhage. Which mechanism best explains the event?", "Atheroembolism or thromboembolism from an ulcerated plaque", ["Hypertensive Charcot-Bouchard rupture", "Venous varix rupture", "Lymphatic obstruction"], "Ulcerated plaques can generate emboli that cause TIA or ischemic stroke."),
        q("high", "An older man with severe aortic atherosclerosis has a pulsatile abdominal mass. Imaging shows a dilated infrarenal aorta with mural thrombus. Which pathologic process is central?", "Atherosclerotic abdominal aortic aneurysm formation", ["Takayasu arteritis of the arch", "Cystic medial degeneration of the ascending aorta", "Kawasaki coronary aneurysm"], "Most AAAs are infrarenal, atherosclerosis-associated, and often contain mural thrombus."),
    ]),
    ("hypertension", "Hypertension and Hypertensive Vascular Disease", [
        q("easy", "Benign hypertension classically causes:", "Hyaline arteriolosclerosis", ["Capillary hemangioma", "Caseating arteritis", "Cavernous lymphangioma"], "Chronic hypertension causes plasma protein leakage and smooth muscle wall thickening."),
        q("easy", "Malignant hypertension classically causes:", "Hyperplastic arteriolosclerosis", ["Fatty streaks only", "Venous varices", "Lymphangitis"], "Severe hypertension produces onion-skin arteriolar thickening."),
        q("easy", "Charcot-Bouchard microaneurysms are associated with:", "Long-standing hypertension", ["Vitamin C deficiency", "CMV infection", "Hyper-IgM syndrome"], "Hypertension weakens small penetrating brain arteries."),
        q("moderate", "Hyaline arteriolosclerosis in diabetes is promoted by:", "Endothelial injury and plasma protein leakage into arteriolar walls", ["IgE-mediated degranulation", "Direct fungal invasion", "Reed-Sternberg cells"], "Diabetes and hypertension both cause homogeneous hyaline arteriolar thickening."),
        q("moderate", "The microscopic 'onion-skin' lesion of malignant hypertension is due to:", "Concentric smooth muscle proliferation and basement membrane duplication", ["Noncaseating granulomas", "Foam cell fatty streaks only", "Large cavernous vascular spaces"], "Hyperplastic arteriolosclerosis has laminated concentric arteriolar thickening."),
        q("moderate", "Fibrinoid necrosis in malignant hypertension reflects:", "Acute severe arteriolar wall injury with plasma protein deposition", ["Benign medial calcification", "Pure venous dilation", "AL amyloid deposition"], "Severe pressure damages endothelium and vessel walls."),
        q("moderate", "The kidney in benign nephrosclerosis typically shows:", "Finely granular cortical scarring", ["Large hydatid cysts", "Diffuse purulent abscesses", "Medullary thyroid tissue"], "Chronic arteriolar narrowing causes ischemic renal scarring."),
        q("high", "A patient with BP 245/145 mm Hg develops headache, renal failure, papilledema, and retinal hemorrhages. Renal arterioles show onion-skin lesions with areas of fibrinoid necrosis. Which diagnosis best fits?", "Malignant hypertension with hyperplastic arteriolosclerosis", ["Benign nephrosclerosis only", "Polyarteritis nodosa", "Atherosclerotic aneurysm"], "Malignant hypertension causes acute vascular injury with hyperplastic arteriolosclerosis and necrotizing arteriolitis."),
        q("high", "A long-standing diabetic patient has renal arterioles with homogeneous eosinophilic wall thickening and luminal narrowing. Similar lesions are common in chronic hypertension. Which lesion is present?", "Hyaline arteriolosclerosis", ["Hyperplastic arteriolosclerosis", "Leukocytoclastic vasculitis", "Cystic medial degeneration"], "Hyaline arteriolosclerosis is seen in diabetes and benign hypertension."),
        q("high", "A hypertensive patient dies of hemorrhage in the basal ganglia. Autopsy reveals rupture of tiny aneurysmal dilations in penetrating arteries rather than a saccular aneurysm at the circle of Willis. Which lesion is implicated?", "Charcot-Bouchard microaneurysm", ["Berry aneurysm", "Mycotic aneurysm", "Aortic dissection"], "Long-standing hypertension can produce microaneurysms in small penetrating cerebral vessels."),
    ]),
    ("aneurysm-dissection", "Aneurysms and Aortic Dissection", [
        q("easy", "An aneurysm is best defined as:", "Localized abnormal dilation of a blood vessel or heart wall", ["Complete thrombotic occlusion", "Inflammation of lymphatics", "Transient vasospasm only"], "Aneurysms are permanent abnormal dilations due to wall weakness."),
        q("easy", "A true aneurysm involves:", "All layers of the vessel wall", ["Only extravascular hematoma", "Only the intima", "Only lymphatics"], "True aneurysms include intact but thinned arterial wall layers."),
        q("easy", "A false aneurysm is also called a:", "Pseudoaneurysm", ["Fatty streak", "Capillary hemangioma", "Varix"], "A pseudoaneurysm is a contained vascular wall defect communicating with the lumen."),
        q("moderate", "Atherosclerotic abdominal aortic aneurysms classically occur:", "Below the renal arteries", ["Only in the aortic root", "In the pulmonary trunk", "In cerebral cortical veins"], "AAAs usually occur in the infrarenal abdominal aorta."),
        q("moderate", "Aortic dissection begins when blood enters the media through:", "An intimal tear", ["A venous valve", "A lymphatic channel", "A capillary hemangioma"], "An intimal tear permits blood to dissect through the media."),
        q("moderate", "The most important risk factor for aortic dissection in older adults is:", "Hypertension", ["IgE allergy", "Iron deficiency", "Low HDL alone"], "Hypertension is the major risk factor for dissection."),
        q("moderate", "Marfan syndrome predisposes to aortic dissection because of:", "Medial degeneration with elastic tissue fragmentation", ["Immune complex vasculitis", "Endotoxin shock", "Venous thrombosis"], "Connective tissue weakness causes medial degeneration and wall fragility."),
        q("high", "A 68-year-old smoker has a 6.2-cm infrarenal abdominal aortic aneurysm with mural thrombus. The media is thinned beneath severe atherosclerosis. What is the most feared acute complication?", "Rupture with life-threatening hemorrhage", ["Hyperacute transplant rejection", "Primary Raynaud phenomenon", "Pulmonary valve stenosis"], "Large AAAs can rupture into the retroperitoneum or peritoneal cavity."),
        q("high", "A hypertensive man suddenly develops tearing chest pain radiating to the back. Blood tracks through the aortic media, creating a false channel for several centimeters. Which event initiated the lesion?", "Intimal tear with medial dissection by blood", ["Rupture of venous valve cusps", "Pyogenic abscess in the adventitia", "Endothelial IgE cross-linking"], "Aortic dissection is blood dissecting through the media after intimal disruption."),
        q("high", "A patient with tertiary syphilis develops dilation of the ascending thoracic aorta and aortic valve ring. Histology shows obliterative endarteritis of small vessels in the aortic wall with medial scarring. Which mechanism caused the aneurysm?", "Ischemic medial injury from vasa vasorum endarteritis", ["Direct LDL deposition in capillaries", "Autoantibodies against acetylcholine receptors", "Thromboangiitis of digital arteries"], "Syphilitic aortitis injures vasa vasorum, producing medial ischemia and thoracic aneurysm."),
    ]),
    ("large-vessel-vasculitis", "Large-Vessel Vasculitis", [
        q("easy", "Giant cell arteritis most often occurs in:", "Older adults", ["Infants", "Adolescents only", "Newborns"], "Giant cell arteritis is typically a disease of patients older than 50 years."),
        q("easy", "Takayasu arteritis is classically associated with:", "Weak upper-extremity pulses", ["Painless temporal headache in elderly only", "Palpable purpura only", "Blue toe after catheterization"], "Takayasu arteritis can narrow aortic arch branches, causing pulseless disease."),
        q("easy", "The vessel commonly biopsied in suspected giant cell arteritis is the:", "Temporal artery", ["Splenic vein", "Pulmonary capillary", "Thoracic duct"], "Temporal artery biopsy may show granulomatous inflammation."),
        q("moderate", "Giant cell arteritis can cause sudden blindness by involving the:", "Ophthalmic artery or its branches", ["Portal vein", "Renal vein", "Lymphatic duct"], "Ocular ischemia is a feared complication requiring urgent therapy."),
        q("moderate", "Both giant cell arteritis and Takayasu arteritis are characterized by:", "Granulomatous inflammation of large arteries", ["IgA immune complex deposition only", "Neutrophilic venulitis only", "HHV-8 spindle cells"], "Both are granulomatous large-vessel vasculitides."),
        q("moderate", "Takayasu arteritis most commonly involves the:", "Aortic arch and great vessel branches", ["Digital veins", "Coronary venules", "Capillary loops only"], "Aortic arch branch stenosis explains pulse deficits and blood pressure differences."),
        q("moderate", "Jaw claudication in giant cell arteritis reflects:", "Ischemia of muscles supplied by inflamed cranial arteries", ["Temporomandibular infection only", "IgE-mediated edema", "Venous thrombosis"], "Cranial arterial narrowing can cause pain while chewing."),
        q("high", "A 72-year-old has new headache, scalp tenderness, jaw claudication, high ESR, and visual blurring. Biopsy shows granulomatous inflammation with fragmentation of the internal elastic lamina. Which diagnosis is most likely?", "Giant cell arteritis", ["Takayasu arteritis", "Kawasaki disease", "Microscopic polyangiitis"], "Giant cell arteritis affects older adults and branches of carotid arteries."),
        q("high", "A 24-year-old woman has diminished radial pulses, arm claudication, ocular symptoms, and different blood pressures in the two arms. Imaging shows narrowing of aortic arch branches. Which vasculitis best fits?", "Takayasu arteritis", ["Giant cell arteritis", "Polyarteritis nodosa", "IgA vasculitis"], "Takayasu arteritis is granulomatous inflammation of the aorta and major branches in younger patients."),
        q("high", "An elderly patient with suspected temporal arteritis is started on high-dose corticosteroids before biopsy results return. What complication is this urgent treatment intended to prevent?", "Irreversible ischemic blindness", ["Abdominal aortic rupture", "Pulmonary embolism", "Mycotic aneurysm"], "Visual loss from arterial occlusion can be sudden and permanent in giant cell arteritis."),
    ]),
    ("medium-vessel-vasculitis", "Medium-Vessel Vasculitis", [
        q("easy", "Polyarteritis nodosa primarily affects:", "Medium-sized muscular arteries", ["Postcapillary venules only", "Lymphatic sinuses", "Capillaries only"], "PAN is a necrotizing arteritis of medium-sized arteries."),
        q("easy", "Kawasaki disease is most important because it can cause:", "Coronary artery aneurysms", ["Temporal artery blindness", "Renal vein thrombosis", "Esophageal varices"], "Kawasaki disease can damage coronary arteries in children."),
        q("easy", "Thromboangiitis obliterans is strongly linked to:", "Cigarette smoking", ["Hypervitaminosis A", "Congenital rubella", "Asbestos"], "Buerger disease occurs in smokers and affects extremity vessels."),
        q("moderate", "Classic polyarteritis nodosa characteristically spares the:", "Pulmonary circulation", ["Renal arteries", "Mesenteric arteries", "Coronary arteries"], "PAN often involves renal, visceral, and coronary arteries but not pulmonary arteries."),
        q("moderate", "Polyarteritis nodosa has been associated with infection by:", "Hepatitis B virus", ["HHV-8", "Parvovirus B19 only", "Rhinovirus"], "Some PAN cases are linked to immune complexes containing HBV antigens."),
        q("moderate", "The acute mucocutaneous syndrome with fever, conjunctivitis, oral erythema, rash, and cervical lymphadenopathy in a child suggests:", "Kawasaki disease", ["Takayasu arteritis", "Giant cell arteritis", "Buerger disease"], "Kawasaki disease is also called mucocutaneous lymph node syndrome."),
        q("moderate", "Thromboangiitis obliterans typically affects:", "Small and medium arteries of extremities", ["Aortic root only", "Pulmonary trunk", "Temporal artery only"], "Buerger disease causes segmental thrombosing inflammation of extremity vessels."),
        q("high", "A middle-aged patient has fever, weight loss, abdominal pain, hypertension, renal infarcts, and aneurysmal nodularity in renal and mesenteric arteries. Lung vessels are spared. Which diagnosis best fits?", "Polyarteritis nodosa", ["Microscopic polyangiitis", "Giant cell arteritis", "Granulomatosis with polyangiitis"], "PAN is a necrotizing medium-vessel vasculitis with renal/visceral involvement and pulmonary sparing."),
        q("high", "A 3-year-old child has persistent fever, conjunctival injection, strawberry tongue, erythema of palms and soles, desquamation, and cervical lymphadenopathy. Weeks later, echocardiography detects coronary aneurysms. Which disease is most likely?", "Kawasaki disease", ["IgA vasculitis", "Takayasu arteritis", "Polyarteritis nodosa"], "Kawasaki disease affects children and can produce coronary arteritis with aneurysms."),
        q("high", "A young heavy smoker has severe pain in fingers and toes, superficial nodular phlebitis, and segmental thrombosing inflammation containing microabscesses in small and medium arteries. Symptoms improve only with smoking cessation. Which disease is present?", "Thromboangiitis obliterans", ["Raynaud disease", "Atherosclerotic AAA", "Microscopic polyangiitis"], "Buerger disease is a smoking-associated thrombosing vasculitis of extremity vessels."),
    ]),
    ("small-vessel-vasculitis", "Small-Vessel Vasculitis and ANCA-Associated Disease", [
        q("easy", "Granulomatosis with polyangiitis is classically associated with:", "PR3-ANCA", ["Anti-GBM only", "Anti-dsDNA only", "IgE to pollen"], "PR3-ANCA/c-ANCA is strongly associated with GPA."),
        q("easy", "Microscopic polyangiitis is commonly associated with:", "MPO-ANCA", ["BCR-ABL", "PML-RARA", "Anti-centromere"], "MPO-ANCA/p-ANCA is common in microscopic polyangiitis."),
        q("easy", "IgA vasculitis was formerly called:", "Henoch-Schonlein purpura", ["Buerger disease", "Kawasaki disease", "Pulseless disease"], "IgA vasculitis causes purpura, arthralgia, abdominal pain, and renal disease."),
        q("moderate", "Granulomatosis with polyangiitis commonly involves:", "Upper airway, lungs, and kidneys", ["Skin only", "Thyroid only", "Bone marrow only"], "GPA causes necrotizing granulomas and small-vessel vasculitis in these sites."),
        q("moderate", "Microscopic polyangiitis differs from polyarteritis nodosa because it:", "Involves capillaries, venules, and arterioles and often causes glomerulonephritis", ["Always spares kidneys", "Only affects the aorta", "Produces coronary aneurysms in children"], "MPA is a small-vessel vasculitis and may cause pulmonary capillaritis and GN."),
        q("moderate", "Eosinophilic granulomatosis with polyangiitis is strongly associated with:", "Asthma and eosinophilia", ["Temporal headache", "Smoking-associated digital ischemia", "Portal hypertension"], "EGPA features asthma, eosinophilia, and necrotizing vasculitis."),
        q("moderate", "Leukocytoclastic vasculitis refers to:", "Neutrophilic small-vessel inflammation with nuclear debris", ["Pure lymphoid malignancy", "Smooth muscle hamartoma", "Medial calcification"], "Fragmented neutrophils create leukocytoclasia in small vessel walls."),
        q("high", "A patient has chronic sinusitis, otitis media, cavitary lung nodules, hematuria, and crescentic glomerulonephritis. Biopsy shows necrotizing granulomatous inflammation and vasculitis. Which antibody is most expected?", "PR3-ANCA", ["Anti-mitochondrial antibody", "Anti-acetylcholine receptor", "Anti-D immunoglobulin"], "GPA is associated with PR3-ANCA and necrotizing granulomatous respiratory disease."),
        q("high", "A patient develops pulmonary hemorrhage and rapidly progressive glomerulonephritis. Biopsy shows necrotizing small-vessel vasculitis without granulomas or immune deposits. MPO-ANCA is positive. Which diagnosis best fits?", "Microscopic polyangiitis", ["Granulomatosis with polyangiitis", "Kawasaki disease", "Giant cell arteritis"], "MPA is a pauci-immune ANCA-associated small-vessel vasculitis without granulomatous inflammation."),
        q("high", "A child develops palpable purpura on the legs, colicky abdominal pain, arthralgia, and hematuria after an upper respiratory infection. Vessel walls and glomeruli show IgA deposition. Which mechanism is central?", "IgA immune complex-mediated small-vessel vasculitis", ["PR3-ANCA granulomatous vasculitis", "Smoking-induced thrombotic arteritis", "Atherosclerotic plaque rupture"], "IgA vasculitis is an immune complex small-vessel vasculitis involving skin, gut, joints, and kidneys."),
    ]),
    ("raynaud-fmd", "Raynaud Phenomenon, Fibromuscular Dysplasia, and Other Noninflammatory Disorders", [
        q("easy", "Raynaud phenomenon is caused by episodic vasospasm of:", "Digital arteries and arterioles", ["Pulmonary veins", "Aortic vasa vasorum", "Thoracic duct"], "Raynaud causes color changes in fingers or toes after cold or stress."),
        q("easy", "Primary Raynaud phenomenon is also called:", "Raynaud disease", ["Buerger disease", "Kawasaki disease", "Takayasu disease"], "Primary Raynaud occurs without an associated disease."),
        q("easy", "Fibromuscular dysplasia most often affects:", "Renal and carotid arteries", ["Pulmonary capillaries", "Splenic veins", "Lymphatic vessels only"], "Renal artery involvement may cause secondary hypertension."),
        q("moderate", "Secondary Raynaud phenomenon can be associated with:", "Systemic sclerosis", ["Acute appendicitis", "Iron deficiency alone", "Simple obesity"], "Connective tissue diseases can cause structural vascular disease with Raynaud symptoms."),
        q("moderate", "The angiographic pattern classically associated with fibromuscular dysplasia is:", "String-of-beads appearance", ["Tree-in-bud appearance", "Honeycomb lung", "Apple-green birefringence"], "Alternating stenosis and dilation creates a beaded appearance."),
        q("moderate", "Medial calcific sclerosis is characterized by:", "Calcification of muscular artery media without significant luminal narrowing", ["Necrotizing granulomas", "Acute platelet thrombi", "IgA immune deposits"], "Monckeberg sclerosis is often an incidental radiologic finding."),
        q("moderate", "Fibromuscular dysplasia is best described as:", "Noninflammatory, nonatherosclerotic arterial wall thickening", ["ANCA-associated necrotizing vasculitis", "Atherosclerotic lipid plaque", "Bacterial endarteritis"], "FMD is a noninflammatory stenosing disease of medium-sized arteries."),
        q("high", "A young woman has severe hypertension. Renal angiography shows alternating stenotic and dilated segments of the renal artery, but there is no lipid plaque, vasculitis, or thrombus. Which diagnosis is most likely?", "Fibromuscular dysplasia", ["Polyarteritis nodosa", "Atherosclerotic renal artery stenosis", "Takayasu arteritis"], "FMD causes renal artery stenosis in young women and has a string-of-beads appearance."),
        q("high", "A patient’s fingers turn white, then blue, then red after cold exposure. Nailfold capillaries are normal and no autoimmune disease is found. Which diagnosis best fits?", "Primary Raynaud phenomenon", ["Secondary Raynaud from systemic sclerosis", "Thromboangiitis obliterans", "Cholesterol embolization"], "Primary Raynaud is functional vasospasm without an associated structural disease."),
        q("high", "An elderly patient has pipe-stem calcification of muscular arteries on radiograph, but distal pulses are preserved and the lumen is not significantly narrowed. Which vascular change is present?", "Medial calcific sclerosis", ["Hyaline arteriolosclerosis", "Atherosclerotic critical stenosis", "Hyperplastic arteriolosclerosis"], "Monckeberg medial calcific sclerosis calcifies the media but usually does not obstruct flow."),
    ]),
    ("veins-lymphatics", "Veins, Varices, Thrombophlebitis, and Lymphatics", [
        q("easy", "Varicose veins result primarily from:", "Venous valve incompetence and chronic dilation", ["Arterial granulomas", "Capillary tumors", "Lymph node infarction"], "Valve failure causes venous pooling and dilation."),
        q("easy", "Deep venous thrombosis is clinically important mainly because it can lead to:", "Pulmonary embolism", ["Temporal arteritis", "Aortic stenosis", "Hydatid disease"], "Leg DVT can embolize to pulmonary arteries."),
        q("easy", "Lymphedema is edema caused by impaired:", "Lymphatic drainage", ["Arterial vasospasm", "Coronary thrombosis", "Aortic dissection"], "Lymphatic obstruction causes protein-rich interstitial fluid accumulation."),
        q("moderate", "Esophageal varices most often develop because of:", "Portal hypertension", ["Primary Raynaud disease", "Renal artery fibromuscular dysplasia", "Pulmonary stenosis"], "Portal hypertension diverts blood through portosystemic collaterals."),
        q("moderate", "Migratory thrombophlebitis is also known as:", "Trousseau syndrome", ["Kawasaki disease", "Goodpasture syndrome", "Dressler syndrome"], "Trousseau syndrome may accompany visceral malignancy."),
        q("moderate", "Chronic venous insufficiency can cause:", "Stasis dermatitis and leg ulcers", ["Pulmonary granulomas", "Temporal artery blindness", "Coronary aneurysms"], "Sustained venous hypertension injures skin and subcutaneous tissues."),
        q("moderate", "Elephantiasis is most often caused worldwide by:", "Filarial lymphatic obstruction", ["Atherosclerotic plaque rupture", "ANCA vasculitis", "Medial calcification"], "Filarial infection can obstruct lymphatics and cause massive lymphedema."),
        q("high", "A cirrhotic patient vomits large amounts of blood. Endoscopy shows dilated tortuous submucosal veins at the gastroesophageal junction. Which hemodynamic abnormality produced these vessels?", "Portal hypertension with portosystemic collateral formation", ["Systemic hypertension with arteriolosclerosis", "Pulmonary hypertension with cor pulmonale", "Renal artery stenosis"], "Esophageal varices form when portal pressure is diverted to systemic venous channels."),
        q("high", "A patient with pancreatic adenocarcinoma develops recurrent tender superficial venous thromboses that appear in different sites over several months. Which vascular complication is this?", "Migratory thrombophlebitis", ["Primary Raynaud phenomenon", "Takayasu arteritis", "Lymphangioma"], "Mucin-producing cancers can cause a hypercoagulable state with Trousseau syndrome."),
        q("high", "After axillary lymph node dissection and radiation therapy for breast cancer, a patient’s arm becomes chronically swollen with thickened skin and recurrent infections. Which process explains the swelling?", "Secondary lymphedema from lymphatic obstruction", ["Deep venous thrombosis with pulmonary embolism", "Fibromuscular dysplasia", "Arteriolar hyalinosis"], "Surgery and radiation can obstruct lymphatic drainage and produce chronic lymphedema."),
    ]),
    ("vascular-tumors", "Vascular Tumors and Malformations", [
        q("easy", "The most common benign tumor of infancy is:", "Hemangioma", ["Angiosarcoma", "Kaposi sarcoma", "Lymphoma"], "Infantile hemangiomas are common benign vascular tumors."),
        q("easy", "Pyogenic granuloma is best classified as a:", "Lobular capillary hemangioma", ["True bacterial abscess", "Necrotizing arteritis", "Venous thrombus"], "Despite its name, pyogenic granuloma is a capillary proliferation."),
        q("easy", "Angiosarcoma is a malignant tumor of:", "Endothelial cells", ["Smooth muscle cells only", "Lymphoid follicles", "Adipocytes"], "Angiosarcoma is an aggressive endothelial malignancy."),
        q("moderate", "Cavernous hemangiomas are composed of:", "Large dilated vascular channels", ["Small lymphoid follicles", "Atheromatous lipid cores", "Granulomatous arterial walls"], "Cavernous hemangiomas have large blood-filled spaces."),
        q("moderate", "Kaposi sarcoma is associated with infection by:", "HHV-8", ["EBV only", "HPV only", "HBV only"], "Human herpesvirus 8 is required for Kaposi sarcoma."),
        q("moderate", "Bacillary angiomatosis is caused by:", "Bartonella species", ["Candida albicans", "Mycobacterium tuberculosis", "Treponema pallidum"], "Bartonella causes vascular proliferations, especially in immunocompromised patients."),
        q("moderate", "Lymphangiomas are best considered:", "Benign lymphatic malformations", ["Malignant endothelial sarcomas", "Atherosclerotic plaques", "Organizing thrombi"], "Lymphangiomas are developmental lymphatic lesions, often in children."),
        q("high", "An AIDS patient develops multiple violaceous skin plaques. Biopsy shows spindle cells, slit-like vascular spaces, extravasated red cells, and hemosiderin. Which viral association is required for this tumor?", "HHV-8 infection", ["CMV infection", "Parvovirus B19 infection", "Hepatitis A infection"], "Kaposi sarcoma is an HHV-8-associated vascular neoplasm."),
        q("high", "A pregnant patient develops a rapidly growing, red, pedunculated gingival lesion that bleeds easily. Histology shows lobular proliferation of capillaries in an edematous stroma. Which lesion is most likely?", "Pyogenic granuloma", ["Angiosarcoma", "Cavernous lymphangioma", "Atherosclerotic plaque"], "Pyogenic granuloma is a reactive lobular capillary hemangioma and may occur during pregnancy."),
        q("high", "A worker exposed to vinyl chloride develops a hemorrhagic malignant liver tumor composed of atypical endothelial cells forming irregular vascular channels. Which tumor is most likely?", "Hepatic angiosarcoma", ["Capillary hemangioma", "Bacillary angiomatosis", "Glomus tumor"], "Vinyl chloride, arsenic, and thorotrast exposure are linked to hepatic angiosarcoma."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if slug == "plaque-complications":
            continue
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch11-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 11 questions, got {len(chapter_questions)}")
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
    data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
    existing = data.get("questions", [])
    discarded_titles = {
        "Blood Vessels",
        "The Heart",
        "Diseases of White Blood Cells, Lymph Nodes, Spleen, and Thymus",
    }
    discarded_prefixes = ("robbins-ch11-", "robbins-ch12-", "robbins-ch13-")
    kept = [
        question for question in existing
        if not (question.get("chapterTitle") in discarded_titles or str(question.get("id", "")).startswith(discarded_prefixes))
    ]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Removed {len(existing) - len(kept)} existing Chapter 11-13 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 11 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
