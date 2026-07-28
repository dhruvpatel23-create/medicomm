import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Diseases of Infancy and Childhood"
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
    ("anomalies", "Congenital Anomalies: Definitions and Patterns", [
        q("easy", "A malformation is best defined as:", "A primary intrinsic error of morphogenesis", ["Secondary destruction of a previously normal structure", "Fetal compression by abnormal mechanical forces", "A localized overgrowth of mature native tissue"], "Malformations reflect an intrinsically abnormal developmental process."),
        q("easy", "A disruption is caused by:", "Secondary destruction of a previously normal developing tissue", ["An inherited primary error of organ formation", "Normal fetal growth", "Postnatal tumor metastasis"], "Disruptions arise from extrinsic injury to tissue that began development normally."),
        q("easy", "A deformation results from:", "Extrinsic mechanical forces altering fetal form", ["A clonal malignant tumor", "Antibody-mediated hemolysis", "Surfactant excess"], "Deformations are caused by biomechanical forces such as uterine constraint."),
        q("moderate", "Amniotic bands are a classic cause of:", "Disruptions", ["Malformations", "Hamartomas", "Immune hydrops"], "Amniotic bands can encircle and destroy previously normal fetal parts."),
        q("moderate", "Uterine constraint is a common cause of:", "Deformations", ["Chromosomal nondisjunction", "Neuroblastoma", "Wilms tumor"], "Constraint compresses the fetus and alters shape or position."),
        q("moderate", "A sequence means:", "A cascade of anomalies initiated by one primary defect", ["Multiple unrelated defects from separate causes", "A benign tumor of native tissue", "A malignant embryonal neoplasm"], "A sequence is a chain reaction from a single initiating abnormality."),
        q("moderate", "A syndrome is:", "A recognized pattern of anomalies with a common cause", ["A single isolated deformation", "Any birth injury", "A tumor marker"], "Syndromes group anomalies with a shared etiology."),
        q("high", "A neonate has renal agenesis, oligohydramnios, flattened facies, limb positioning defects, and pulmonary hypoplasia. The lung and limb abnormalities follow from reduced amniotic fluid caused by the kidney defect. Which pattern best describes this?", "Sequence", ["Syndrome", "Disruption", "Hamartoma"], "Potter sequence is a cascade initiated by oligohydramnios from renal/urinary abnormalities."),
        q("high", "A fetus develops a constricting ring and distal limb amputation after rupture of the amnion. The limb originally formed normally, and the event does not imply increased recurrence risk in future pregnancies. Which developmental error is this?", "Disruption", ["Malformation", "Deformation", "Metaplasia"], "Amniotic band disruption is extrinsic destruction of normal tissue and is not heritable."),
        q("high", "A breech fetus in a small uterus develops clubfeet and hip dislocation without intrinsic abnormality of limb patterning. The abnormality reflects compression during growth rather than abnormal organogenesis. Which category fits?", "Deformation", ["Disruption", "Malformation", "Neoplasm"], "Deformations arise from mechanical constraint acting on the developing fetus."),
    ]),
    ("teratogens", "Teratogens, Timing, and Multifactorial Inheritance", [
        q("easy", "Peak susceptibility to teratogenesis occurs during:", "Organogenesis", ["Late adulthood", "The neonatal period", "After puberty"], "The third to ninth weeks are most vulnerable because organs are forming."),
        q("easy", "Periconceptional folic acid reduces risk of:", "Neural tube defects", ["Neuroblastoma", "Rh hydrops", "Retinopathy of prematurity"], "Folic acid supplementation prevents many neural tube defects."),
        q("easy", "Fetal alcohol syndrome is caused by maternal exposure to:", "Ethanol", ["Retinoic acid deficiency only", "Lead after birth", "Oxygen therapy"], "Alcohol is a teratogen causing growth, facial, and CNS abnormalities."),
        q("moderate", "Retinoic acid embryopathy is associated with:", "CNS, cardiac, and craniofacial defects", ["Only fetal anemia", "Only surfactant deficiency", "Only adrenal tumors"], "Isotretinoin exposure can disrupt developmental signaling."),
        q("moderate", "Valproic acid teratogenicity is linked to disruption of:", "HOX gene expression", ["LDL receptor recycling", "Surfactant secretion", "Rh antibody formation"], "Valproate affects developmental transcription programs including HOX genes."),
        q("moderate", "Maternal diabetes increases risk of:", "Cardiac anomalies and neural tube defects", ["Only cystic hygroma", "Only neuroblastoma regression", "Only hydrops from ABO incompatibility"], "Diabetic embryopathy causes major congenital anomalies and macrosomia."),
        q("moderate", "Multifactorial inheritance involves:", "Multiple genes of small effect plus environmental factors", ["Only one dominant gene", "Only mitochondrial DNA", "Only postnatal infection"], "Common malformations such as cleft lip/palate and neural tube defects are often multifactorial."),
        q("high", "A pregnant patient takes isotretinoin for acne during early organogenesis. The infant has craniofacial defects, cardiac anomalies, and CNS malformations. Which concept best explains the timing and pattern of injury?", "Teratogenic disruption of developmental signaling during organogenesis", ["Mechanical deformation late in gestation", "Immune hydrops from Rh incompatibility", "Postnatal vitamin deficiency"], "Retinoic acid exposure during organogenesis causes predictable embryopathy."),
        q("high", "A woman with poorly controlled diabetes delivers a macrosomic infant with cardiac malformation and neural tube defect. The fetus had hyperinsulinemia and abnormal development despite modern antenatal care. Which maternal condition is the key teratogenic setting?", "Maternal diabetes mellitus", ["Maternal phenylketonuria only", "Rh sensitization", "Placenta previa"], "Maternal hyperglycemia is linked to diabetic embryopathy and fetal macrosomia."),
        q("high", "A population has frequent neural tube defects, but rates fall dramatically after folic acid supplementation before conception. The responsible genes are not eliminated, yet environmental modification prevents many cases. Which inheritance model is illustrated?", "Multifactorial inheritance", ["Autosomal recessive inheritance", "Mitochondrial inheritance", "Genomic imprinting"], "Multifactorial malformations reflect gene-environment interactions."),
    ]),
    ("prematurity-fgr", "Prematurity and Fetal Growth Restriction", [
        q("easy", "Prematurity is defined as birth before:", "37 weeks of gestation", ["28 weeks only", "40 weeks", "42 weeks"], "Preterm birth occurs before 37 completed weeks."),
        q("easy", "Low birth weight is commonly defined as birth weight less than:", "2500 g", ["500 g", "4000 g", "5000 g"], "Infants under 2500 g are low birth weight."),
        q("easy", "Small-for-gestational-age infants are:", "Undergrown for their gestational age", ["Always premature", "Always macrosomic", "Always hydropic"], "SGA refers to growth restriction relative to gestational age."),
        q("moderate", "The most common maternal mechanism causing FGR is:", "Reduced uteroplacental blood flow", ["Excess surfactant", "Rh IgM crossing placenta", "MYCN amplification"], "Maternal vascular disease often decreases placental perfusion."),
        q("moderate", "Preeclampsia can cause FGR by:", "Impairing placental blood flow", ["Increasing fetal insulin only", "Preventing TORCH infection", "Increasing surfactant"], "Maternal vascular disease reduces uteroplacental perfusion."),
        q("moderate", "Symmetric FGR is more suggestive of:", "Fetal chromosomal abnormality or congenital infection", ["Late placental insufficiency only", "Maternal obesity", "Cesarean delivery"], "Early intrinsic fetal problems affect all organs proportionately."),
        q("moderate", "Asymmetric FGR is commonly related to:", "Uteroplacental insufficiency later in gestation", ["Triploidy in every case", "Rh antibody hemolysis", "Congenital neuroblastoma"], "Late placental insufficiency preferentially spares brain growth."),
        q("high", "A fetus has proportionately small head, trunk, and limbs, with ultrasound malformations and suspected congenital infection. All organ systems are similarly affected rather than brain-sparing. Which pattern best describes this growth restriction?", "Symmetric fetal growth restriction", ["Asymmetric fetal growth restriction", "Macrosomia", "Hydrops fetalis"], "Intrinsic fetal causes early in development produce symmetric/proportionate FGR."),
        q("high", "A hypertensive mother has placental infarcts and delivers an infant with low weight but relatively preserved head circumference compared with abdominal size. The growth problem developed in the third trimester under reduced placental perfusion. Which pattern is likely?", "Asymmetric fetal growth restriction", ["Symmetric FGR from trisomy", "Fetal macrosomia", "Prematurity without growth restriction"], "Late uteroplacental insufficiency causes brain-sparing asymmetric FGR."),
        q("high", "A term newborn weighs under 2500 g but has mature gestational features. The clinical issue is undergrowth rather than immaturity, and causes include maternal vascular disease, congenital infection, and placental pathology. Which term applies?", "Fetal growth restriction", ["Prematurity", "Respiratory distress syndrome", "Sudden infant death syndrome"], "FGR/SGA infants are small for gestational age even if born at term."),
    ]),
    ("rds", "Neonatal Respiratory Distress Syndrome and Pulmonary Complications", [
        q("easy", "Neonatal respiratory distress syndrome is caused primarily by deficiency of:", "Surfactant", ["Hemoglobin", "Albumin", "IgG"], "RDS reflects pulmonary immaturity and surfactant deficiency."),
        q("easy", "RDS is also called:", "Hyaline membrane disease", ["Hydrops fetalis", "Necrotizing enterocolitis", "Bronchopneumonia"], "Proteinaceous hyaline membranes line alveoli in fatal RDS."),
        q("easy", "Surfactant is produced by:", "Type II pneumocytes", ["Type I pneumocytes", "Alveolar macrophages only", "Endothelial cells only"], "Type II pneumocytes synthesize surfactant."),
        q("moderate", "Surfactant deficiency causes:", "Increased alveolar surface tension and atelectasis", ["Excess alveolar expansion", "Renal dysgenesis", "Erythroblastosis"], "Without surfactant, alveoli collapse during expiration."),
        q("moderate", "Infants of diabetic mothers have increased RDS risk because insulin:", "Suppresses surfactant synthesis", ["Destroys alveolar macrophages", "Causes Rh sensitization", "Increases VEGF in retina"], "Fetal hyperinsulinemia counteracts corticosteroid-driven surfactant production."),
        q("moderate", "Antenatal corticosteroids reduce RDS by:", "Promoting fetal lung maturation and surfactant production", ["Blocking all labor", "Preventing NEC directly", "Removing IgG"], "Steroids accelerate type II pneumocyte maturation."),
        q("moderate", "Retinopathy of prematurity is related to abnormal regulation of:", "VEGF during oxygen therapy and relative hypoxia", ["RhD antigen", "MYCN", "WT1"], "Hyperoxia suppresses VEGF; later rebound promotes neovascularization."),
        q("high", "A 28-week premature infant develops tachypnea, grunting, hypoxemia, and diffuse atelectasis shortly after birth. Autopsy would show collapsed alveoli lined by fibrin-rich hyaline membranes. Which pathogenic defect is central?", "Surfactant deficiency from pulmonary immaturity", ["IgG-mediated fetal hemolysis", "Amniotic band disruption", "MYCN amplification"], "Prematurity causes inadequate surfactant, increasing surface tension and alveolar collapse."),
        q("high", "A preterm infant treated with high oxygen later develops retinal neovascularization. During hyperoxia VEGF fell and vessels regressed; after return to lower oxygen tension, VEGF rebounded and drove abnormal vessel growth. Which complication is this?", "Retinopathy of prematurity", ["Bronchopulmonary sequestration", "Hyaline membrane disease", "Necrotizing enterocolitis"], "ROP has a two-phase VEGF-mediated pathogenesis."),
        q("high", "A very premature infant survives RDS but later has large simplified alveoli, dysmorphic capillaries, and arrested septation after oxygen, ventilation, inflammation, and vascular maldevelopment. Which chronic lung disease is described?", "Bronchopulmonary dysplasia", ["Pulmonary hypoplasia from oligohydramnios", "Cystic fibrosis", "Meconium ileus"], "BPD reflects disrupted alveolar development in premature lungs."),
    ]),
    ("nec", "Necrotizing Enterocolitis and Complications of Prematurity", [
        q("easy", "Necrotizing enterocolitis is most common in:", "Premature infants", ["Adolescents", "Elderly smokers", "Adults with obesity"], "NEC incidence rises as gestational age decreases."),
        q("easy", "NEC primarily affects the:", "Intestine", ["Retina", "Adrenal medulla", "Kidney blastema"], "NEC is necrotizing inflammation of neonatal bowel."),
        q("easy", "Very-low-birth-weight means birth weight less than:", "1500 g", ["2500 g", "3500 g", "5000 g"], "VLBW infants weigh under 1500 g."),
        q("moderate", "NEC pathogenesis involves immature gut plus:", "Microbial colonization and inflammatory injury", ["MYCN amplification", "Rh IgG only", "Retinoic acid excess only"], "Immaturity, feeding, colonization, and inflammation contribute to NEC."),
        q("moderate", "A radiographic clue to NEC is:", "Pneumatosis intestinalis", ["Dense metaphyseal lines", "Apple-green birefringence", "Owl-eye inclusions"], "Gas in the bowel wall is a classic NEC finding."),
        q("moderate", "Premature infants are at increased risk of intraventricular hemorrhage because of fragility of:", "Germinal matrix vessels", ["Ciliary zonules", "Renal blastema", "Amniotic bands"], "The germinal matrix is vascular and vulnerable in preterm infants."),
        q("moderate", "Patent ductus arteriosus is a complication associated with:", "Prematurity", ["Maternal Rh negativity only", "Neuroblastoma", "Teratoma"], "Premature infants often fail to close the ductus arteriosus."),
        q("high", "A very-low-birth-weight premature infant develops abdominal distention, bloody stools, sepsis, and radiographic gas within the intestinal wall after enteral feeding. The disease reflects immature mucosal defenses, bacterial colonization, and exaggerated inflammation. Which condition is most likely?", "Necrotizing enterocolitis", ["Hirschsprung disease", "Meconium ileus", "Pyloric stenosis"], "NEC is a life-threatening bowel necrosis of premature infants."),
        q("high", "A 30-week infant suddenly deteriorates with apnea and a bulging fontanelle. Cranial ultrasound shows bleeding near the lateral ventricles arising from fragile vessels in a highly cellular periventricular region. Which complication is present?", "Germinal matrix intraventricular hemorrhage", ["Retinopathy of prematurity", "Immune hydrops", "Wilms tumor"], "Prematurity predisposes to germinal matrix hemorrhage."),
        q("high", "A premature infant recovers from surfactant-deficiency RDS but later has PDA, NEC, and intraventricular hemorrhage. These complications cluster because several organ systems remain structurally and functionally immature. What unifying risk factor is central?", "Prematurity", ["Maternal ABO incompatibility", "Fetal macrosomia", "Neural crest tumor"], "Prematurity underlies multiple neonatal complications."),
    ]),
    ("hydrops", "Fetal Hydrops and Hemolytic Disease of the Newborn", [
        q("easy", "Fetal hydrops means:", "Accumulation of edema fluid in the fetus", ["Premature closure of ductus", "A renal embryonal tumor", "A skin hemangioma"], "Hydrops refers to generalized or localized fetal edema."),
        q("easy", "Classic immune hydrops is caused by:", "Maternal antibodies against fetal red cells", ["Surfactant deficiency", "Amniotic bands", "Valproate exposure"], "Immune hydrops is hemolytic disease from blood group incompatibility."),
        q("easy", "The major Rh antigen causing severe disease is:", "D antigen", ["A antigen", "B antigen", "Lewis antigen"], "RhD is the main cause of clinically significant Rh incompatibility."),
        q("moderate", "Rh disease is uncommon in a first pregnancy because initial antibodies are mainly:", "IgM", ["IgG", "IgA", "IgE"], "IgM does not cross the placenta effectively."),
        q("moderate", "Severe fetal anemia causes hydrops partly by causing:", "High-output cardiac failure", ["Surfactant excess", "MYCN amplification", "Low VEGF"], "Anemia and hypoxia lead to cardiac failure and edema."),
        q("moderate", "ABO incompatibility can protect against Rh sensitization because fetal RBCs are:", "Cleared rapidly by maternal IgM anti-A or anti-B", ["Converted to platelets", "Unable to enter maternal blood", "Made Rh negative"], "Rapid removal of fetal cells reduces RhD immunization."),
        q("moderate", "Prophylaxis for Rh incompatibility uses:", "Anti-D immunoglobulin", ["Surfactant", "Folic acid only", "Retinoic acid"], "Anti-D prevents maternal sensitization to fetal RhD cells."),
        q("high", "An Rh-negative mother has an Rh-positive fetus in a second pregnancy. Maternal IgG crosses the placenta, destroys fetal RBCs, and causes severe anemia with generalized edema and extramedullary hematopoiesis. Which disorder is present?", "Immune hydrops fetalis", ["Nonimmune hydrops from cardiac malformation", "Necrotizing enterocolitis", "RDS"], "Rh IgG-mediated hemolysis causes erythroblastosis fetalis and hydrops."),
        q("high", "A fetus has generalized edema, pleural effusions, and ascites, but the mother is not Rh sensitized and direct antiglobulin testing does not support immune hemolysis. Cardiac malformation and chromosomal disease are considered. Which category applies?", "Nonimmune hydrops", ["Immune hydrops", "Kwashiorkor", "SIDS"], "Most hydrops is now nonimmune and has diverse cardiac, chromosomal, infectious, or hematologic causes."),
        q("high", "A mother receives anti-D immunoglobulin after delivery of an Rh-positive infant. The administered antibody clears fetal Rh-positive red cells before her immune system mounts a durable response. What is the preventive goal?", "Prevent maternal Rh sensitization", ["Treat neonatal RDS", "Induce fetal macrosomia", "Prevent Wilms tumor"], "Anti-D prophylaxis prevents future IgG-mediated hemolytic disease."),
    ]),
    ("perinatal-infection", "Perinatal and Congenital Infections", [
        q("easy", "The TORCH group includes:", "Toxoplasma, other agents, rubella, CMV, and herpes", ["Tumors, oxygen, retinoids, carbon monoxide, hydrops", "Teratoma, obesity, rickets, cholera, HSV", "Thymus, ovary, retina, colon, heart"], "TORCH is a mnemonic for important congenital infections."),
        q("easy", "Cytomegalovirus is a common cause of:", "Congenital infection", ["Sacrococcygeal teratoma", "Fetal alcohol syndrome", "RDS"], "CMV is a frequent congenital viral infection."),
        q("easy", "Congenital rubella can cause:", "Cataracts, deafness, and cardiac defects", ["MYCN amplification", "Hyaline membranes only", "Hydatid cyst"], "Rubella embryopathy classically affects eyes, ears, and heart."),
        q("moderate", "Congenital CMV often produces:", "Periventricular calcifications", ["Posterior mediastinal mass", "Triphasic renal tumor", "Pneumatosis intestinalis"], "CMV can cause periventricular calcifications and neurologic injury."),
        q("moderate", "Congenital toxoplasmosis is associated with:", "Chorioretinitis and intracranial calcifications", ["Hyaline membranes", "Retinoblastoma", "Basophilic stippling"], "Toxoplasma affects eye and CNS."),
        q("moderate", "Congenital syphilis may cause:", "Saber shins and Hutchinson teeth", ["Homer-Wright rosettes", "Triphasic nephroblastoma", "Retinopathy from oxygen"], "Treponema pallidum can cause late congenital stigmata."),
        q("moderate", "Fetal infections can cause FGR because they:", "Intrinsically impair fetal growth", ["Increase surfactant", "Prevent placental inflammation", "Cause only macrosomia"], "Congenital infections are fetal causes of symmetric growth restriction."),
        q("high", "A newborn has microcephaly, seizures, hepatosplenomegaly, jaundice, and periventricular calcifications. Viral inclusions may be found in infected tissues, and infection is often clinically silent in the mother. Which congenital infection is most likely?", "Cytomegalovirus", ["Rubella", "Toxoplasmosis", "HSV-2"], "CMV is a common congenital infection with periventricular calcifications."),
        q("high", "An infant has chorioretinitis, hydrocephalus, and diffuse intracranial calcifications after maternal exposure to cat feces or undercooked meat during pregnancy. Which organism is responsible?", "Toxoplasma gondii", ["Cytomegalovirus", "Rubella virus", "Treponema pallidum"], "Congenital toxoplasmosis causes chorioretinitis, hydrocephalus, and intracranial calcifications."),
        q("high", "A child develops sensorineural deafness, cataracts, and patent ductus arteriosus after maternal infection early in pregnancy. The timing during organogenesis explains the structural defects. Which congenital infection is classic?", "Rubella", ["CMV", "Parvovirus B19", "Listeria"], "Congenital rubella causes cataracts, deafness, and cardiac anomalies."),
    ]),
    ("sids", "Sudden Infant Death and Unexpected Infant Death", [
        q("easy", "SIDS is sudden death of an infant that remains unexplained after:", "Complete investigation including autopsy", ["Only physical examination", "Only family history", "Only chest x-ray"], "SIDS is a diagnosis of exclusion after full investigation."),
        q("easy", "The strongest modifiable risk factor for SIDS is:", "Prone sleeping position", ["High folate intake", "Breastfeeding", "Back sleeping"], "Back-to-sleep campaigns reduced SIDS."),
        q("easy", "Maternal smoking is associated with increased risk of:", "SIDS", ["Wilms tumor only", "Teratoma only", "Rh sensitization only"], "Prenatal and postnatal smoke exposure increase SIDS risk."),
        q("moderate", "SIDS most often occurs during:", "Sleep", ["Feeding only", "Delivery only", "Adolescence"], "SIDS typically occurs during sleep in apparently healthy infants."),
        q("moderate", "A proposed vulnerability in SIDS involves abnormal control of:", "Arousal and cardiorespiratory responses", ["Nephrogenesis", "Retinoid signaling only", "MYCN repair"], "Brainstem serotonergic/arousal abnormalities are implicated."),
        q("moderate", "Unsafe sleep environments increase SIDS risk by promoting:", "Rebreathing or asphyxial stress", ["Surfactant synthesis", "Anti-D sensitization", "Tumor regression"], "Soft bedding and prone sleep can impair ventilation."),
        q("moderate", "Some sudden unexpected infant deaths are explained by:", "Inborn errors of metabolism", ["Allergic rhinitis", "Adult atherosclerosis", "Scurvy"], "Fatty acid oxidation defects account for a subset of SUID."),
        q("high", "A 3-month-old infant is found dead during sleep. Autopsy, death-scene investigation, and clinical history reveal no cause. The infant slept prone on soft bedding and had prenatal smoke exposure. Which diagnosis is most appropriate?", "Sudden infant death syndrome", ["Immune hydrops", "RDS", "Congenital rubella"], "SIDS is unexplained infant death after investigation, with prone sleep and smoke exposure as risks."),
        q("high", "An infant has sudden unexpected death during a minor illness. Molecular testing reveals a fatty acid oxidation enzyme defect that prevented adequate energy production during fasting stress. Which broader category does this case represent?", "Explained sudden unexpected infant death due to metabolic disease", ["Classic unexplained SIDS", "Immune hydrops", "Necrotizing enterocolitis"], "Some SUIDs are explained by inherited metabolic defects."),
        q("high", "Public health campaigns advising supine sleep markedly reduce infant deaths without changing congenital anomaly rates. The intervention changes the sleep environment and reduces rebreathing/asphyxial stress in vulnerable infants. Which risk factor was directly modified?", "Prone sleeping position", ["Rh incompatibility", "Prematurity itself", "MYCN amplification"], "The back-to-sleep intervention targets prone positioning."),
    ]),
    ("tumorlike", "Tumorlike Lesions and Benign Tumors of Childhood", [
        q("easy", "A heterotopia is:", "Normal tissue in an abnormal location", ["Malignant neuroblastoma", "Diffuse fetal edema", "Surfactant deficiency"], "Heterotopia/choristoma is misplaced normal tissue."),
        q("easy", "A hamartoma is:", "Focal overgrowth of mature native tissue", ["A metastatic carcinoma", "An immune hemolysis", "A teratogenic drug"], "Hamartomas are disorganized overgrowths native to the organ."),
        q("easy", "The most common tumors of infancy are:", "Hemangiomas", ["Glioblastomas", "Colon carcinomas", "Lung carcinomas"], "Infantile hemangiomas are very common benign vascular tumors."),
        q("moderate", "Infantile hemangiomas often:", "Spontaneously regress", ["Always metastasize", "Always require nephrectomy", "Cause Rh hydrops"], "Many grow early and involute over time."),
        q("moderate", "Port-wine stains are considered:", "Vascular ectasias/malformations", ["Wilms tumors", "Teratomas", "Neuroblastomas"], "Flat vascular lesions are often malformations rather than true neoplasms."),
        q("moderate", "Congenital-infantile fibrosarcoma often contains:", "ETV6-NTRK3 fusion", ["MYCN amplification only", "WT1 deletion only", "RhD antigen"], "This translocation is a useful diagnostic marker."),
        q("moderate", "Despite adult-like histology, congenital-infantile fibrosarcoma usually has:", "Excellent prognosis", ["Uniformly fatal course", "Mandatory renal origin", "No translocation"], "Infantile fibrosarcoma behaves better than adult fibrosarcoma."),
        q("high", "A red-blue facial mass appears in infancy, enlarges with the child, then begins to involute. Histology shows benign capillary vascular channels without malignant atypia. Which lesion best fits?", "Infantile hemangioma", ["Angiosarcoma", "Wilms tumor", "Neuroblastoma"], "Infantile hemangiomas are common benign vascular lesions that may regress."),
        q("high", "A gastric submucosal nodule in a child contains well-organized pancreatic acini and ducts. The tissue is normal microscopically but misplaced. Which tumorlike lesion is this?", "Heterotopia", ["Hamartoma", "Teratoma", "Fibrosarcoma"], "Heterotopia is normal tissue in an abnormal site."),
        q("high", "An infant has a cellular spindle-cell soft tissue tumor resembling adult fibrosarcoma, but testing reveals t(12;15) with ETV6-NTRK3 fusion. The expected clinical behavior is much better than its histology suggests. Which tumor is this?", "Congenital-infantile fibrosarcoma", ["Rhabdomyosarcoma", "Neuroblastoma", "Wilms tumor"], "Infantile fibrosarcoma has ETV6-NTRK3 and excellent prognosis."),
    ]),
    ("neuroblastoma", "Neuroblastoma and Neural Crest Tumors", [
        q("easy", "Neuroblastoma arises from:", "Neural crest-derived sympathetic tissue", ["Renal blastema", "Germ cells", "Mature vascular endothelium"], "Neuroblastoma is an embryonal tumor of sympathetic nervous system lineage."),
        q("easy", "The most common site of childhood neuroblastoma is:", "Adrenal medulla", ["Renal cortex", "Sacrococcygeal region", "Liver"], "About 40% arise in adrenal medulla."),
        q("easy", "Homer-Wright pseudorosettes contain tumor cells around:", "Neuropil", ["Blood vessels", "Mucin", "Keratin pearls"], "Neuroblastoma rosettes surround fibrillary neuritic material."),
        q("moderate", "A poor prognostic marker in neuroblastoma is:", "MYCN amplification", ["Hyperdiploidy in infants", "Spontaneous maturation", "Low stage"], "MYCN amplification is associated with aggressive disease."),
        q("moderate", "Neuroblastomas may secrete catecholamines causing increased urinary:", "VMA and HVA", ["AFP and beta-hCG", "Albumin and glucose", "Anti-D IgG"], "Catecholamine metabolites aid diagnosis."),
        q("moderate", "Better prognosis in neuroblastoma is associated with:", "Hyperdiploidy", ["Near-diploid complex karyotype", "MYCN amplification", "1p deletion"], "Hyperdiploidy often indicates favorable biology."),
        q("moderate", "Ganglioneuroma represents:", "Mature neural tumor differentiation", ["Immune hydrops", "RDS", "NEC"], "Maturation of neuroblastic tumors can produce ganglioneuroma."),
        q("high", "A 2-year-old has an adrenal mass crossing the midline, elevated urinary VMA/HVA, small round blue cells in neuropil, and Homer-Wright pseudorosettes. Which tumor is most likely?", "Neuroblastoma", ["Wilms tumor", "Sacrococcygeal teratoma", "Infantile hemangioma"], "Neuroblastoma is a catecholamine-producing adrenal/sympathetic small round blue cell tumor."),
        q("high", "A neuroblastoma in an infant is hyperdiploid and localized, while another tumor in an older child is near diploid with MYCN amplification and 1p deletion. Which tumor has the worse prognosis?", "The near-diploid tumor with MYCN amplification", ["The hyperdiploid localized tumor", "Both are equally benign", "Neither can metastasize"], "MYCN amplification and segmental chromosomal abnormalities indicate aggressive disease."),
        q("high", "A small adrenal neuroblastoma focus is discovered incidentally at autopsy in an infant; many such silent lesions regress, leaving fibrosis or calcification. Which unusual feature of neuroblastoma is illustrated?", "Capacity for spontaneous regression or maturation", ["Obligate progression to carcinoma", "Origin from renal blastema", "Dependence on Rh antibodies"], "Some neuroblastomas regress or mature, especially in infancy."),
    ]),
    ("wilms", "Wilms Tumor and Other Childhood Tumors", [
        q("easy", "Wilms tumor is also called:", "Nephroblastoma", ["Neuroblastoma", "Retinoblastoma", "Hepatoblastoma"], "Wilms tumor is an embryonal renal tumor."),
        q("easy", "Wilms tumor arises in the:", "Kidney", ["Adrenal medulla", "Retina", "Sacrococcygeal region"], "Wilms tumor is the common childhood kidney tumor."),
        q("easy", "The classic Wilms tumor pattern is:", "Triphasic blastemal, epithelial, and stromal elements", ["Only mature fat", "Only vascular channels", "Only trophoblastic tissue"], "Wilms tumor recapitulates nephrogenesis."),
        q("moderate", "Anaplasia in Wilms tumor is associated with:", "TP53 mutations and poorer response to therapy", ["Better prognosis", "Surfactant deficiency", "Rh incompatibility"], "Anaplasia correlates with p53 loss and chemoresistance."),
        q("moderate", "WT1 is located on chromosome:", "11p13", ["13q14", "17p13", "15q11"], "WT1 at 11p13 is involved in Wilms tumor predisposition."),
        q("moderate", "WAGR syndrome includes Wilms tumor with:", "Aniridia, genitourinary anomalies, and intellectual disability", ["Ataxia, telangiectasia, and immunodeficiency", "Webbed neck and coarctation", "Macroglossia and omphalocele only"], "WAGR is due to 11p13 deletions involving WT1 and PAX6."),
        q("moderate", "Sacrococcygeal teratomas are the most common:", "Teratomas of childhood", ["Kidney tumors", "Neural crest tumors", "Vascular tumors"], "Sacrococcygeal teratomas account for many childhood teratomas."),
        q("high", "A 3-year-old has a large unilateral renal mass. Histology shows blastemal blue cells, primitive tubules/glomeruloid structures, and fibroblastic stroma. Which tumor is most likely?", "Wilms tumor", ["Neuroblastoma", "Congenital mesoblastic nephroma", "Rhabdomyosarcoma"], "Wilms tumor classically has triphasic blastemal, epithelial, and stromal elements."),
        q("high", "A child with aniridia, genitourinary malformations, intellectual disability, and a renal embryonal tumor has a deletion involving WT1 and PAX6. Which syndrome is present?", "WAGR syndrome", ["Beckwith-Wiedemann syndrome", "Li-Fraumeni syndrome", "Down syndrome"], "WAGR combines Wilms tumor, aniridia, GU anomalies, and intellectual disability."),
        q("high", "A Wilms tumor shows large hyperchromatic pleomorphic nuclei and abnormal multipolar mitoses. Molecular testing reveals TP53 mutation, and the tumor is less responsive to chemotherapy. Which histologic feature is present?", "Anaplasia", ["Maturation", "Heterotopia", "Caseation"], "Anaplasia in Wilms tumor indicates adverse prognosis and p53 loss."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if slug == "tumorlike":
            continue
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch10-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 10 questions, got {len(chapter_questions)}")
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
    kept = [question for question in existing if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch10-"))]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Removed {len(existing) - len(kept)} existing Chapter 10 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 10 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
