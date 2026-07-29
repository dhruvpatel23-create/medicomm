import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "forensic-medicine"
SUBJECT_TITLE = "Forensic Medicine"
SOURCE_PDF = "fmt1"


def q(prompt, answer, wrong, explanation, clinical=False):
    options = [answer, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {
        "prompt": prompt,
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "moderate" if not clinical else "high",
        "tags": ["clinical"] if clinical else [],
    }


LEGAL_TOPICS = [
    ("courts-law", "Courts, Legal Procedure and Medical Evidence", [
        ("A summons in court is legally used to", "Compel attendance of a witness", ["Arrest a convicted person", "Certify cause of death", "Register a medical council complaint"], "A summons is a court order requiring attendance or production of documents."),
        ("A subpoena duces tecum requires a doctor to", "Produce records or documents in court", ["Perform an autopsy", "Issue a birth certificate", "Give expert evidence without records"], "Duces tecum specifically means bringing relevant documents or records."),
        ("A dying declaration is admissible because it relates to", "The cause or circumstances of the declarant's death", ["Any civil dispute", "Routine medical negligence only", "A witness's character certificate"], "A dying declaration is an exception to hearsay when death is in question."),
        ("A conscious burns patient tells the magistrate that her husband poured kerosene and lit the match. She dies next day. The statement is best treated as", "Dying declaration", ["Hostile testimony", "Privileged communication", "Conduct money"], "A statement about the circumstances causing death is a dying declaration if the maker later dies.", True),
        ("Expert medical evidence is primarily", "Opinion evidence based on specialized knowledge", ["Direct eyewitness evidence only", "A police confession", "A judicial sentence"], "Experts assist the court by interpreting technical facts within their field."),
        ("A hostile witness is one who", "Gives evidence adverse to the party who called the witness", ["Always refuses oath", "Is always an accused doctor", "Can never be cross-examined"], "The court may permit cross-examination of one's own hostile witness."),
        ("Perjury means", "Giving false evidence under oath", ["Refusing private practice", "Disclosing notifiable disease", "Failing to preserve viscera"], "Perjury is intentional false sworn testimony in judicial proceedings."),
        ("A doctor receives court summons for original wound certificate but sends only a photocopy without permission. The main legal problem is failure to", "Produce the required documentary evidence", ["Maintain sterility", "Perform dying deposition", "Claim professional secrecy"], "When summoned with records, the doctor must produce the documents required by court.", True),
        ("Conduct money is paid to a witness for", "Expenses of attending court", ["Punishment for contempt", "Compensation to accused", "Postmortem fee only"], "Conduct money covers travel and attendance expenses."),
        ("In court, a forensic expert says an injury is possible by the alleged weapon but cannot identify the assailant. This is appropriate because medical evidence mainly establishes", "Nature, age and possible causation of injuries", ["Identity of accused in every case", "Motive for crime", "Final verdict"], "Medical evidence supports facts such as injury characteristics; guilt is decided by court.", True),
    ]),
    ("medical-ethics", "Medical Ethics, Consent and Professional Negligence", [
        ("Valid consent for examination requires", "Voluntary agreement after understanding the nature of the act", ["Only a signature without explanation", "Police permission in every patient", "Consent from any adult bystander"], "Consent must be informed, voluntary and given by a competent person or lawful guardian."),
        ("In an emergency where delay threatens life and no guardian is available, a doctor may treat under", "Implied consent", ["Dying declaration", "Perjury", "Hostile witness rule"], "Emergency treatment is justified by implied consent to save life or prevent serious harm."),
        ("Professional negligence requires duty, breach and", "Resulting damage caused by the breach", ["Only an unhappy patient", "Only a criminal complaint", "Only absence of written prescription"], "Negligence is established when breach of duty causes legally recognized harm."),
        ("An unconscious road-traffic victim has expanding extradural hematoma and no relatives are reachable. Emergency surgery is performed. The best legal basis is", "Implied consent in life-saving emergency", ["Express written consent", "Dying deposition", "Privileged communication"], "Life-saving care need not wait for formal consent when delay is dangerous.", True),
        ("Res ipsa loquitur means", "The thing speaks for itself", ["Let the buyer beware", "No one can be judge in own cause", "Hear the other side"], "It applies when negligence is inferred from an event that ordinarily would not occur without negligence."),
        ("Therapeutic privilege allows limited withholding of information when disclosure would", "Seriously harm the patient", ["Reduce hospital income", "Avoid all documentation", "Prevent every police case"], "It is narrow and patient-centered, not a license for concealment."),
        ("A consent form for sterilization signed during active labor is ethically weak mainly because", "Voluntariness may be impaired by pain and stress", ["Sterilization never needs consent", "Only police can consent", "Consent is valid only after autopsy"], "Consent must be free from coercion and obtained in a suitable mental state.", True),
        ("Professional secrecy may be breached when", "Disclosure is required by law or public interest", ["A neighbor is curious", "The doctor wants publicity", "The patient misses follow-up"], "Confidentiality yields to statutory duties and serious public safety concerns."),
        ("The Bolam test relates to", "Whether conduct conforms to a responsible body of medical opinion", ["Identification by fingerprints", "Age of bruises", "Estimation of blood alcohol"], "Bolam is used in assessing professional negligence."),
        ("A surgeon leaves a sponge inside the abdomen, requiring reoperation. This is a classic example where negligence may be inferred under", "Res ipsa loquitur", ["Doli incapax", "Corpus delicti", "Subpoena duces tecum"], "Retained surgical material is an event that usually implies a breach of care.", True),
    ]),
    ("identification", "Identification: Age, Sex, Stature and Race", [
        ("The most reliable skeletal feature for sex determination in adults is the", "Pelvis", ["Clavicle", "Radius", "Patella"], "The adult pelvis shows the greatest sexual dimorphism due to obstetric adaptation."),
        ("Dental eruption is most useful for age estimation in", "Children and adolescents", ["Centenarians", "Burnt adult skeletons only", "Pregnant women only"], "Tooth eruption and calcification follow predictable developmental sequences in youth."),
        ("Fusion of epiphyses helps estimate", "Age in adolescents and young adults", ["Blood group", "Cause of poisoning", "Manner of death"], "Epiphyseal union occurs in a recognized age sequence."),
        ("An unknown skeleton has a wide sciatic notch, broad subpubic angle and oval obturator foramen. The sex is most likely", "Female", ["Male", "Indeterminate child", "Cannot be assessed from pelvis"], "A broad subpubic angle and wide sciatic notch favor a female pelvis.", True),
        ("Stature from long bones is estimated by using", "Regression formulae or multiplication factors", ["Diatom test", "Marsh test", "Hydrostatic test"], "Long-bone length correlates with living stature."),
        ("The dental formula of a permanent adult dentition is", "2123/2123", ["2102/2102", "2122/2122", "2012/2012"], "Adult quadrants contain two incisors, one canine, two premolars and three molars."),
        ("Gustafson method estimates adult age mainly from", "Age changes in teeth", ["Rigor mortis", "Gunshot residue", "Ligature mark"], "Attrition, secondary dentine and other dental changes are used."),
        ("A charred body has intact molars with restorations matching antemortem dental charts. The best identification evidence is", "Comparative dental identification", ["Stature alone", "Color of clothes", "Postmortem lividity"], "Dental restorations and charts can strongly identify burned or decomposed bodies.", True),
        ("The cephalic index is used in assessment of", "Head shape", ["Blood alcohol", "Weapon sharpness", "Time since death"], "Cephalic index classifies skull shape using head breadth and length."),
        ("A child has first permanent molars and lower central incisors erupted. The approximate developmental age is around", "6 to 7 years", ["2 years", "14 to 15 years", "25 years"], "First permanent molars and central incisors erupt around 6 to 7 years.", True),
    ]),
    ("fingerprints-dna", "Fingerprints, Footprints and DNA Profiling", [
        ("Fingerprints are valuable for identification because they are", "Unique and permanent", ["Always inherited unchanged", "Visible only after death", "Destroyed by washing"], "Friction ridge patterns are individualized and persist throughout life."),
        ("The common fingerprint pattern with one delta is", "Loop", ["Whorl", "Arch", "Composite always"], "Loops usually have one delta; whorls usually have two."),
        ("A plain arch fingerprint has", "No delta", ["One delta", "Two deltas", "Four deltas"], "Arches lack a true delta."),
        ("At a burglary scene, latent ridge marks on glass are developed and match the suspect's right index finger at multiple ridge characteristics. This evidence is based on", "Fingerprint individuality", ["ABO incompatibility", "Bertillon age formula", "Postmortem staining"], "Matching minutiae in friction ridges supports personal identification.", True),
        ("DNA profiling most commonly uses variation in", "Short tandem repeats", ["Serum albumin only", "Hair color genes only", "Mitochondrial ribosomes only"], "STR loci are highly polymorphic and useful in forensic identification."),
        ("Mitochondrial DNA is especially useful when testing", "Shafts of old hair or maternally related remains", ["Fresh liquid blood only", "Fingerprints on paper only", "Alcohol in breath only"], "Mitochondrial DNA is abundant and maternally inherited."),
        ("The chain of custody is meant to prove that a sample was", "Collected, sealed, transferred and tested without tampering", ["Always positive", "Taken only by police", "Never photographed"], "Documented custody maintains evidentiary integrity."),
        ("A sexual assault swab is left unsealed on a desk before dispatch. The major forensic defect is", "Break in chain of custody and contamination risk", ["Wrong cephalic index", "Failure of ossification", "Normal hypostasis"], "Unsealed evidence can be contaminated or challenged in court.", True),
        ("Locard exchange principle states that contact between two objects results in", "Transfer of trace material", ["Instant death", "No evidentiary change", "Only fingerprint destruction"], "Contact often leaves or removes trace evidence."),
        ("Skeletal remains of a disaster victim are compared with the mother's sample when nuclear DNA is degraded. The useful test is", "Mitochondrial DNA profiling", ["Breath alcohol analysis", "Diatom microscopy", "Precipitin ring only"], "mtDNA can identify maternal lineage when nuclear DNA is limited.", True),
    ]),
    ("death-signs", "Death, Brain Death and Early Postmortem Changes", [
        ("Somatic death means irreversible loss of", "Vital functions of the body as a whole", ["Only hair growth", "Only one limb reflex", "Only gastric emptying"], "Somatic death is failure of integrated life functions."),
        ("Brain death is diagnosed by irreversible loss of", "All brainstem functions with apnea in a suitable clinical setting", ["Only cortical EEG slowing", "Only coma from sedatives", "Only absent limb movement"], "Brainstem death requires strict prerequisites and tests."),
        ("Algor mortis refers to", "Cooling of the body after death", ["Muscle stiffening", "Blood settling", "Drying of exposed mucosa"], "Algor mortis is postmortem fall in body temperature."),
        ("A ventilated head-injury patient has fixed pupils, absent corneal and gag reflexes, and no respiratory effort on apnea test after exclusions. This supports", "Brain death", ["Suspended animation", "Catalepsy", "Instant putrefaction"], "Absent brainstem reflexes and apnea after prerequisites support brain death.", True),
        ("Rigor mortis is due to", "ATP depletion causing fixed actin-myosin bridges", ["Bacterial gas formation", "Hemoglobin diffusion only", "Immediate freezing of muscles"], "After death, ATP depletion prevents muscle relaxation."),
        ("Postmortem lividity is caused by", "Gravitational settling of blood in dependent vessels", ["Active arterial bleeding", "Muscle contraction", "DNA fragmentation"], "Hypostasis results from blood settling after circulation stops."),
        ("Cadaveric spasm differs from rigor mortis because it", "Occurs instantly in muscles active at the moment of death", ["Always involves the whole body", "Begins after putrefaction", "Is caused by maggots"], "Cadaveric spasm is instantaneous and localized."),
        ("A drowned victim is recovered with weeds tightly grasped in the hand immediately after death. This finding is classically explained by", "Cadaveric spasm", ["Secondary relaxation", "Mummification", "Adipocere"], "Instantaneous grip of material at death suggests cadaveric spasm.", True),
        ("Tache noire is drying discoloration of the", "Exposed sclera", ["Liver", "Spleen", "Gastric mucosa"], "Open eyelids permit drying of sclera, producing a dark band."),
        ("A body is found supine with fixed purple staining over the back and blanching at pressure points. The finding is", "Postmortem lividity", ["Antemortem bruising", "Petechial hemorrhage only", "Heat stiffening"], "Dependent hypostasis with pressure pallor is typical lividity.", True),
    ]),
    ("late-pmi", "Late Postmortem Changes and Time Since Death", [
        ("Putrefaction is mainly caused by", "Bacterial decomposition of tissues", ["Sterile drying alone", "ATP restoration", "Active circulation"], "Bacteria and enzymes break down tissues after death."),
        ("The earliest external sign of putrefaction is commonly", "Greenish discoloration of right iliac fossa", ["Adipocere of face", "Skeletonization of skull", "Instant mummification"], "Cecal bacteria commonly produce early right iliac fossa greening."),
        ("Marbling in putrefaction is due to", "Hemolysed blood outlining superficial veins", ["Tattooing by gunpowder", "Antemortem whip marks", "Fingerprint ridges"], "Bacterial hemolysis stains the venous pattern."),
        ("A body found in a warm room shows green right iliac fossa discoloration, abdominal distension and marbling. The best interpretation is", "Putrefactive change after death", ["Fresh antemortem bruising", "Instant rigor only", "Mummification in dry heat"], "Greening, gas distension and marbling are putrefaction signs.", True),
        ("Adipocere is formed by", "Hydrogenation and hydrolysis of body fat in moist conditions", ["Complete burning", "Freezing of blood", "Only insect feeding"], "Moist anaerobic conditions favor conversion of fat to waxy adipocere."),
        ("Mummification is favored by", "Dry heat and good ventilation", ["Wet stagnant water", "Septicemia only", "Deep burial in clay"], "Dry, warm, airy conditions desiccate tissues and inhibit putrefaction."),
        ("Forensic entomology estimates time since death by studying", "Insect colonization and developmental stages", ["Dental formula only", "Blood group alone", "Court summons"], "Insect succession and larval age help estimate postmortem interval."),
        ("A partially submerged body has waxy, greasy, gray-white tissue over cheeks and buttocks. This preservation change is", "Adipocere formation", ["Mummification", "Fresh hypostasis", "Cadaveric spasm"], "Moist environments can produce adipocere in fatty areas.", True),
        ("Casper dictum broadly states decomposition occurs fastest in", "Air", ["Water", "Earth", "Sealed coffin always"], "Classically, decomposition is fastest in air, slower in water, slowest in earth."),
        ("Maggot length and stage are submitted from a decomposed body to estimate postmortem interval. The discipline applied is", "Forensic entomology", ["Forensic odontology only", "Toxicology only", "Ballistics only"], "Larval development provides a biological clock after colonization.", True),
    ]),
    ("autopsy", "Medico-Legal Autopsy and Exhumation", [
        ("The main objective of medico-legal autopsy is to determine", "Cause, manner and circumstances of death", ["Hospital billing", "Blood group of relatives", "Eligibility for insurance only"], "A forensic autopsy answers legal questions around death."),
        ("In India, medico-legal autopsy is usually conducted on requisition from", "Police or magistrate", ["Any neighbor", "Media reporter", "Insurance agent"], "Legal authority requests the postmortem in unnatural or suspicious deaths."),
        ("In suspected poisoning, viscera should be preserved in", "Suitable clean containers with preservative as indicated", ["Open newspaper", "Formalin for all toxicology samples", "Unlabeled plastic bag"], "Proper containers, labeling and preservatives protect toxicology evidence."),
        ("A young woman dies suddenly after alleged pesticide ingestion. At autopsy, stomach and contents, liver, kidney and blood are preserved and sealed. The purpose is", "Toxicological analysis", ["Age estimation", "Fingerprint development", "Determination of stature"], "Viscera preservation permits chemical examination for poison.", True),
        ("Exhumation means", "Lawful disinterment of a buried body", ["Burning a corpse", "Instant autopsy", "Brain death testing"], "Exhumation is done under legal order for identification or cause of death questions."),
        ("A negative autopsy means", "No definite cause of death is found after complete examination", ["Autopsy was illegal", "Death did not occur", "All organs were absent"], "Some deaths remain unexplained despite adequate autopsy and ancillary tests."),
        ("A postmortem report should include", "External and internal findings with opinion and preserved samples", ["Only final punishment", "Only accused confession", "Only hospital address"], "The report documents observations and the medical opinion."),
        ("A buried body is dug up months later on magistrate order because poisoning is alleged. This procedure is", "Exhumation", ["Inquest only", "Dying deposition", "Disinterested testimony"], "Lawful disinterment for investigation is exhumation.", True),
        ("In decomposed bodies, identification is aided by", "Clothing, dental findings, bones and DNA", ["Rigor alone", "Fresh pulse", "Active bleeding"], "Multiple durable clues may assist identification when soft tissues decay."),
        ("A sealed viscera jar reaches the forensic laboratory without sample seal impression. The main evidentiary weakness is", "Inability to verify seal authenticity", ["Absence of rigor mortis", "Wrong sex from pelvis", "Low cephalic index"], "Seal comparison confirms that the received sample is the same sealed evidence.", True),
    ]),
    ("wounds-general", "Mechanical Injuries: General Principles", [
        ("An abrasion involves injury to", "Epidermis or superficial epithelium", ["Only bone marrow", "Full-thickness organ rupture", "Only hair shaft"], "Abrasion is superficial scraping of skin or mucosa."),
        ("A bruise is caused by", "Extravasation of blood into tissues from blunt force", ["Superficial epidermal loss only", "Clean incised division", "Thermal charring only"], "Contusion reflects ruptured vessels with blood infiltration."),
        ("A laceration is typically produced by", "Blunt force tearing or splitting tissue", ["A sharp clean blade only", "Poisoning", "Electrocution only"], "Lacerations have tissue bridging and irregular margins."),
        ("A child has patterned tramline bruises on the thigh matching a stick. This most directly indicates", "Impact by a cylindrical blunt object", ["Self-inflicted incised wound", "Postmortem lividity", "Adipocere"], "Patterned bruises can reproduce the shape of the impacting object.", True),
        ("A contusion changes color over time mainly due to", "Hemoglobin breakdown", ["New melanin synthesis only", "Gunpowder tattooing", "ATP depletion"], "Color changes reflect degradation of hemoglobin pigments."),
        ("Defense wounds are commonly found on", "Hands and forearms", ["Soles only", "Scalp only", "Back of trunk only"], "Victims often raise hands and forearms to ward off assault."),
        ("Hesitation cuts suggest", "Self-infliction", ["Lightning strike", "Drowning", "Postmortem animal activity"], "Multiple superficial tentative cuts near a deeper wound favor suicide."),
        ("A woman attacked with a knife has cuts across the palms and ulnar forearms while trying to hold the blade away. These are", "Defense wounds", ["Fabricated wounds", "Postmortem artifacts", "Thermal burns"], "Defense wounds occur while resisting or warding off assault.", True),
        ("A fabricated wound is usually", "Superficial, accessible and avoids vital areas", ["Always fatal", "Always on the back only", "Always associated with skull fracture"], "Self-made false wounds tend to be reachable and relatively safe."),
        ("A superficial parallel series of wrist cuts near one deeper fatal cut most strongly suggests", "Hesitation cuts in suicidal injury", ["Defense wounds from assault", "Lacerations from fall", "Postmortem splitting"], "Tentative parallel cuts are common in self-inflicted sharp-force deaths.", True),
    ]),
    ("regional-trauma", "Regional Injuries and Road-Traffic Trauma", [
        ("A coup injury occurs", "At the site of impact", ["Opposite the impact only", "Only in spinal cord", "Only after drowning"], "Coup lesions are beneath the impact site."),
        ("A contrecoup injury occurs", "Opposite the site of impact", ["Only at weapon edge", "Only in abdomen", "Only postmortem"], "Brain movement inside the skull can injure the opposite pole."),
        ("Lucid interval is classically associated with", "Extradural hemorrhage", ["Adipocere", "Drowning", "Mummification"], "Middle meningeal artery bleeding may cause transient recovery before deterioration."),
        ("A motorcyclist briefly talks after a temporal impact, then becomes unconscious with ipsilateral pupil dilation. The likely lesion is", "Extradural hemorrhage", ["Chronic arsenic poisoning", "Adipocere", "Simple abrasion only"], "Temporal fracture with middle meningeal artery bleed causes extradural hematoma and lucid interval.", True),
        ("Ring fracture of skull is commonly seen around the", "Foramen magnum", ["Nasal bridge", "Mandible angle", "Orbit roof only"], "Axial loading or falls can produce basal ring fractures around the foramen magnum."),
        ("Whiplash injury primarily affects the", "Cervical spine and soft tissues", ["Tarsal bones", "Dental enamel", "Spleen only"], "Sudden acceleration-deceleration strains the neck."),
        ("Bumper fracture in pedestrians classically involves the", "Leg bones at vehicle bumper height", ["Skull vault only", "Fingers only", "Sternum only"], "Impact height helps reconstruct vehicle-pedestrian collisions."),
        ("A pedestrian has tibia-fibula fractures at one level with primary impact abrasions at bumper height. This pattern helps infer", "Vehicle impact height and direction", ["Blood alcohol level", "Exact time since death", "Victim's fingerprint class"], "Bumper injuries are important in traffic accident reconstruction.", True),
        ("A steering wheel impact commonly injures the", "Chest and abdomen", ["Only fingertips", "Only ear lobule", "Only teeth"], "Blunt deceleration against the wheel can injure thoracoabdominal organs."),
        ("A driver without seat belt has patterned chest bruising and ruptured liver after frontal collision. The injury mechanism is", "Blunt deceleration impact", ["Sharp-force defense wound", "Drowning", "Electric joule burn"], "Rapid deceleration and impact against vehicle interiors cause internal trauma.", True),
    ]),
    ("sharp-firearm", "Sharp-Force and Firearm Injuries", [
        ("An incised wound typically has", "Clean-cut margins longer than deep", ["Tissue bridges", "Abraded collar only", "Burnt margins always"], "Sharp cutting produces clean margins and length exceeds depth."),
        ("A stab wound is usually", "Deeper than its surface length", ["Always superficial", "Always caused by blunt force", "Always postmortem"], "Stabs penetrate deeper than the skin wound length."),
        ("Chop wounds are produced by", "Heavy sharp-edged weapons", ["Ligature compression", "Heat alone", "Poisoning"], "Axes and heavy blades combine sharp cutting with blunt force."),
        ("A victim has an elliptical chest wound deeper than its skin length with one sharp angle and one blunt angle. The weapon is likely", "Single-edged knife", ["Round stick", "Rifled firearm at distance", "Acid splash"], "Single-edged blades often produce one acute and one blunt wound angle.", True),
        ("An abrasion collar around a bullet entry wound is due to", "Scraping of skin by the entering bullet", ["Exit gas expansion", "Postmortem drying only", "Knife guard impact"], "The bullet abrades the skin edge as it enters."),
        ("Tattooing around a firearm entry wound indicates", "Unburnt powder particles striking skin", ["Adipocere", "Old bruise", "Diatoms"], "Powder stippling suggests close-range firing."),
        ("A stellate entry wound over the skull may occur in", "Contact firearm discharge", ["Distant blunt punch", "Simple drowning", "Ligature hanging"], "Gas expansion under scalp can split skin in contact shots."),
        ("A forehead wound has soot, muzzle imprint and stellate tearing over bone. This supports", "Contact shot entry wound", ["Distant exit wound", "Fabricated abrasion", "Postmortem insect damage"], "Soot, muzzle imprint and gas tearing are contact-shot features.", True),
        ("Rifling marks on a bullet help identify", "The firearm barrel that fired it", ["Victim's age", "Time since death", "Poison type"], "Lands and grooves impart individual marks to bullets."),
        ("A recovered bullet is compared microscopically with a test bullet fired from a suspect pistol. Matching striations establish", "Ballistic linkage to the firearm", ["Brain death", "Mummification", "Dental age"], "Comparison microscopy can link bullets to a specific rifled barrel.", True),
    ]),
]


PM_TRAUMA_TOPICS = [
    ("asphyxia-general", "Asphyxial Deaths: General Features", [
        ("Asphyxia means deficient oxygenation due to", "Interference with respiration or oxygen utilization", ["Only starvation", "Only renal failure", "Only fever"], "Asphyxia results when oxygen delivery, exchange or use is critically impaired."),
        ("Petechial hemorrhages in asphyxia are due to", "Raised venous pressure and capillary rupture", ["Adipocere", "Bone marrow embolism only", "Dental caries"], "Venous congestion can rupture small vessels."),
        ("Cyanosis in asphyxia reflects increased", "Reduced hemoglobin", ["Carboxyhemoglobin only", "Bile pigment", "Melanin"], "Deoxygenated hemoglobin causes bluish discoloration."),
        ("A body has conjunctival petechiae, facial congestion and cyanosis after chest compression in a crowd crush. The mechanism is", "Mechanical asphyxia", ["Corrosive poisoning", "Incised injury", "Brain death testing"], "Chest compression prevents respiratory movements and venous return.", True),
        ("Tardieu spots are", "Petechial hemorrhages under serous membranes", ["Bullet entry marks", "Burn blisters", "Dental restorations"], "They are small hemorrhages seen in asphyxial and congestive deaths."),
        ("Asphyxial signs are best regarded as", "Supportive but not individually diagnostic", ["Always pathognomonic", "Never seen in any death", "Only postmortem artifacts"], "Many signs overlap with other causes and must be interpreted in context."),
        ("Traumatic asphyxia is caused by", "Severe compression of chest or abdomen", ["Knife penetration only", "Sea water immersion only", "Snakebite"], "External compression prevents ventilation and causes venous congestion."),
        ("A worker trapped under soil is recovered with intense facial congestion, petechiae and subconjunctival hemorrhage. The diagnosis is", "Traumatic asphyxia", ["Mummification", "Chronic starvation", "Contact firearm wound"], "Thoracoabdominal compression can cause traumatic asphyxia.", True),
        ("Suffocation can result from", "Smothering, choking or environmental oxygen deficiency", ["Only sharp weapons", "Only epiphyseal fusion", "Only dental decay"], "Suffocation includes obstruction of air entry or lack of breathable oxygen."),
        ("An infant is found dead with a plastic bag over the face and no major external injuries. The likely mechanism is", "Suffocation by smothering", ["Hanging", "Drowning", "Firearm injury"], "Covering mouth and nose can cause fatal smothering with few injuries.", True),
    ]),
    ("hanging-strangulation", "Hanging, Ligature Strangulation and Manual Strangulation", [
        ("Hanging is asphyxia caused by neck constriction where the constricting force is", "Body weight", ["Hand pressure only", "Water entry", "Chest crush"], "In hanging, suspension of the body tightens the ligature."),
        ("The ligature mark in typical hanging is usually", "Oblique, non-continuous and above thyroid cartilage", ["Horizontal and low", "Always absent", "Around the wrists"], "Hanging classically produces an oblique mark running upward to the suspension point."),
        ("Ligature strangulation usually produces a mark that is", "Horizontal and completely encircling the neck", ["Oblique upward", "Only on ankles", "Always postmortem"], "Strangulation marks are commonly transverse and low."),
        ("A body is found suspended from a fan with an oblique parchment-like ligature mark high on the neck, saliva dribbling from the mouth angle. The death is most consistent with", "Hanging", ["Ligature strangulation", "Drowning", "Smothering"], "High oblique ligature mark and suspension favor hanging.", True),
        ("Manual strangulation is also called", "Throttling", ["Bansdola", "Garroting", "Burking"], "Throttling is neck compression by hands."),
        ("Fracture of hyoid bone is more common in", "Manual strangulation in older adults", ["Newborn drowning", "Adipocere", "Mummification"], "Direct neck pressure and age-related ossification increase fracture likelihood."),
        ("Judicial hanging aims to cause death mainly by", "Fracture-dislocation of upper cervical spine", ["Slow drowning", "Corrosive burns", "Carbon monoxide poisoning"], "Long-drop hanging can fracture-dislocate the neck."),
        ("A woman is found dead with crescentic nail abrasions and bruises on the neck, facial petechiae and fractured hyoid. These findings favor", "Manual strangulation", ["Suicidal hanging", "Drowning", "Heat stroke"], "Grip marks, nail abrasions and hyoid fracture are typical of throttling.", True),
        ("Burking involves", "Smothering with chest compression", ["Suspension by neck", "Burning after death", "Gunshot at contact range"], "Burking combines airway obstruction with thoracic compression."),
        ("A victim is pinned down, mouth and nose are covered, and the chest is compressed until death. This is", "Burking", ["Typical hanging", "Cafe coronary", "Immersion syndrome"], "Burking is homicidal smothering with chest compression.", True),
    ]),
    ("drowning", "Drowning and Immersion Deaths", [
        ("Drowning is death due to", "Respiratory impairment from submersion or immersion in liquid", ["Only cold exposure", "Only neck compression", "Only electric current"], "Drowning occurs when liquid immersion/submersion impairs breathing."),
        ("Fine froth at mouth and nostrils in drowning is due to", "Air, water and mucus churned by respiratory efforts", ["Gunpowder soot", "Adipocere only", "Dental plaque"], "Persistent fine froth supports antemortem drowning when interpreted with other findings."),
        ("Washerwoman changes are seen in", "Hands and feet after immersion", ["Skull fracture", "Bullet track", "Hyoid fracture"], "Prolonged immersion causes sodden wrinkling of palms and soles."),
        ("A body recovered from a lake has copious fine white froth, overdistended lungs and water in stomach. These findings support", "Antemortem drowning", ["Postmortem immersion only", "Contact firearm death", "Mummification"], "Froth and emphysematous lungs are supportive features of drowning.", True),
        ("Diatom test is based on finding diatoms in", "Distant organs or bone marrow after aspiration into circulation", ["Hair shaft only", "Ligature knot", "Fingerprint ridge"], "Circulating diatoms can reach organs if water is inhaled during life."),
        ("Cadaveric spasm in drowning may show", "Weeds or mud grasped in the hand", ["Burnt soles", "Bullet wipe", "Dental calculus"], "Instantaneous grip may preserve material seized during death struggle."),
        ("Dry drowning involves", "Laryngeal spasm with little water entering lungs", ["Complete skeletonization", "Gunshot wound", "Only postmortem sinking"], "A small proportion die from reflex laryngeal closure."),
        ("A suspected drowning body has diatoms in femoral bone marrow matching pond water. The significance is", "Water was likely aspirated during life", ["Death must be from hanging", "Only postmortem contamination", "No forensic value"], "Diatoms in closed distant sites support antemortem aspiration.", True),
        ("Immersion syndrome is sudden death due to", "Vagal inhibition on sudden contact with cold water", ["Rigor mortis", "Carbonization", "Sharp-force trauma"], "Cold water can trigger fatal reflex cardiac inhibition."),
        ("A swimmer suddenly collapses immediately after jumping into cold water, with minimal water in lungs and no trauma. The mechanism may be", "Immersion syndrome", ["Ligature strangulation", "Poisoned wound", "Chop injury"], "Sudden cold immersion can provoke vagal cardiac arrest.", True),
    ]),
    ("thermal-burns", "Burns, Scalds and Heat-Related Deaths", [
        ("A burn is caused by", "Dry heat", ["Moist heat only", "Ligature pressure", "Water aspiration"], "Dry heat produces burns; moist heat produces scalds."),
        ("A scald is caused by", "Moist heat such as hot liquids or steam", ["Flame only", "Knife blade", "Bullet"], "Hot liquids and steam cause scalds."),
        ("Line of redness around a burn indicates", "Vital reaction", ["Postmortem artifact only", "Diatom entry", "Fingerprint pattern"], "Inflammatory redness suggests the person was alive when burned."),
        ("A person trapped in a house fire has soot in the airways and cherry-red hypostasis. The key antemortem fire indicator is", "Soot inhalation in respiratory passages", ["Skin splitting alone", "Heat rupture of skull", "Postmortem pugilistic attitude"], "Soot below the vocal cords indicates breathing during fire.", True),
        ("Pugilistic attitude in burns is due to", "Heat stiffening and muscle contraction", ["Defensive fighting posture", "Cadaveric spasm only", "Rigor from drowning"], "Heat causes flexor muscles to contract, producing a boxer-like posture."),
        ("Heat ruptures of skin may mimic", "Incised wounds", ["Drowning froth", "Diatom test", "Fingerprint loops"], "Postmortem heat splits can look like cuts but lack vital reaction."),
        ("Carboxyhemoglobin causes hypostasis to appear", "Cherry red", ["Green", "Black only", "Blue-gray always"], "Carbon monoxide forms carboxyhemoglobin, producing bright red lividity."),
        ("A charred body has splits over joints without bleeding or tissue reaction. These are best interpreted as", "Postmortem heat ruptures", ["Antemortem incised wounds", "Defense wounds", "Hesitation cuts"], "Heat splits lack vital hemorrhage and may occur after death.", True),
        ("Heat stroke is characterized by hyperthermia with", "Central nervous system dysfunction", ["Only frostbite", "Only drowning", "Only hyoid fracture"], "Heat stroke is a failure of thermoregulation with CNS disturbance."),
        ("A marathon runner collapses on a hot day with core temperature above 40 C, confusion and dry hot skin. The diagnosis is", "Heat stroke", ["Hypothermia", "Drowning", "Ligature strangulation"], "Severe hyperthermia with CNS dysfunction defines heat stroke.", True),
    ]),
    ("cold-electricity", "Cold Injury, Electrocution and Lightning", [
        ("Hypothermia is defined by core body temperature below", "35 C", ["40 C", "37.5 C", "30 C only"], "Clinically significant hypothermia begins below about 35 C."),
        ("Frostbite is injury due to", "Freezing of tissues", ["Moist heat", "Neck compression", "Poison ingestion"], "Cold exposure can freeze and damage peripheral tissues."),
        ("Joule burn is seen in", "Electrical contact injury", ["Drowning", "Hanging", "Mummification"], "Electrical resistance at contact converts energy to heat."),
        ("An electrician is found dead holding a live wire with a crater-like contact burn on the palm and exit mark on foot. Cause is", "Electrocution", ["Heat stroke", "Drowning", "Ligature strangulation"], "Entry and exit electrical marks with contact history support electrocution.", True),
        ("Electric current kills commonly by causing", "Ventricular fibrillation or respiratory arrest", ["Adipocere", "Diatom embolism", "Dental eruption"], "Current through the heart or respiratory centers can be fatal."),
        ("Alternating current is generally more dangerous because it can cause", "Tetanic grip and ventricular fibrillation", ["Immediate mummification", "Better release from source", "Only skin staining"], "AC can lock muscles onto the source and disturb cardiac rhythm."),
        ("Lightning marks on skin are called", "Lichtenberg figures", ["Tardieu spots", "Gustafson lines", "Casper marks"], "Arborescent fern-like marks may appear after lightning strike."),
        ("A farmer struck during a storm has fern-like branching erythematous skin marks and torn clothing. The marks are", "Lichtenberg figures", ["Ligature marks", "Tattooing", "Marbling from putrefaction"], "Lightning can produce transient arborescent skin patterns.", True),
        ("Metallization in electrical injury means", "Deposition of conductor metal on skin", ["Gold poisoning", "Dental filling decay", "Bone marrow diatoms"], "Metal from the conductor may vaporize and deposit at contact."),
        ("A copper wire contact leaves a greenish metallic deposit around an electrical mark. This is", "Metallization", ["Adipocere", "Frostbite", "Postmortem lividity"], "Conductor metal may be deposited on skin during electrical contact.", True),
    ]),
    ("starvation-neglect", "Starvation, Neglect and Torture-Related Injuries", [
        ("Starvation causes progressive loss first mainly of", "Fat stores", ["Skull sutures", "Fingerprints", "Dental enamel"], "Body fat is mobilized early, followed by muscle wasting."),
        ("A key autopsy feature in starvation is", "Emaciation with loss of subcutaneous fat", ["Cherry-red lividity", "Sooty airway", "Bullet wipe"], "Severe nutritional deprivation produces marked wasting."),
        ("Cafe coronary refers to choking due to", "Food bolus obstruction of airway", ["Coffee poisoning", "Thermal scald", "Judicial hanging"], "Sudden choking on food can mimic cardiac death."),
        ("An elderly neglected patient is found emaciated with pressure sores, poor hygiene and no fatal injury. The findings suggest", "Death related to neglect and starvation", ["Contact gunshot", "Fresh drowning", "Lightning strike"], "Neglect deaths show deprivation, ulcers, infections and wasting.", True),
        ("Torture injuries are often assessed by documenting", "Pattern, age, distribution and consistency with alleged mechanism", ["Only horoscope", "Only clothing brand", "Only court fee"], "Careful injury documentation helps evaluate allegations of torture."),
        ("Falanga causes injuries mainly to the", "Soles of feet", ["Scalp", "Earlobe", "Umbilicus"], "Falanga is repeated beating of soles."),
        ("Cigarette burns are typically", "Round burns of uniform size", ["Linear incised wounds", "Diatom deposits", "Rifling grooves"], "Inflicted cigarette burns may be multiple, round and similar in size."),
        ("A detainee alleges beating on soles; examination shows tender patterned bruising over plantar surfaces with difficulty walking. This is consistent with", "Falanga", ["Burking", "Drowning", "Mummification"], "Falanga targets the soles and may leave plantar bruises.", True),
        ("Pressure sores in a dependent neglected person indicate", "Prolonged immobility and inadequate care", ["High-velocity bullet", "Lightning entry", "Hanging suspension"], "Bedsores support prolonged pressure and care failure."),
        ("A child has multiple circular burns of same diameter on accessible and inaccessible areas, inconsistent with accidental splash. The likely injury is", "Inflicted cigarette burns", ["Scald splash only", "Postmortem drying", "Washerwoman change"], "Uniform circular burns in suspicious distribution suggest inflicted injury.", True),
    ]),
    ("sexual-offences", "Sexual Offences: Examination and Evidence", [
        ("Consent in sexual offence evaluation must be", "Voluntary, informed and legally competent", ["Assumed from silence always", "Given only by police", "Irrelevant to examination"], "Medical examination and evidence collection require appropriate consent."),
        ("The first priority in sexual assault care is", "Medical stabilization and treatment of injuries", ["Media briefing", "Immediate conviction", "Destroying clothing"], "Patient care comes before evidence collection."),
        ("Semen detection may use tests for", "Spermatozoa and seminal markers", ["Diatoms only", "Gunpowder only", "Bile salts only"], "Microscopy and biochemical markers can support seminal fluid identification."),
        ("A survivor presents within 6 hours of assault with genital pain and torn clothing. After consent, the doctor should prioritize", "Treatment, documentation and timely forensic evidence collection", ["Delay until trial", "Wash all samples first", "Refuse care without police"], "Early care includes medical needs, consented evidence collection and documentation.", True),
        ("Chain of custody for sexual assault samples requires", "Proper labeling, sealing and documented transfer", ["Open storage", "Anonymous unlabeled swabs", "Verbal report only"], "Evidence must be traceable from collection to laboratory."),
        ("Absence of genital injury in an alleged sexual assault", "Does not exclude assault", ["Always proves false allegation", "Always proves consent", "Means no examination is needed"], "Many assaults leave no visible injury, especially with delay or nonviolent acts."),
        ("Drug-facilitated sexual assault samples should include early", "Blood and urine collection", ["Bone marrow only", "Hair after 10 years only", "Dental cast only"], "Many drugs are rapidly cleared; timely specimens are important."),
        ("A patient reports assault after suspected drink spiking and delayed memory. The most appropriate toxicology specimens are", "Blood and urine as early as possible", ["Only nail clippings after a month", "Only diatom sample", "Only skull x-ray"], "Prompt blood and urine collection improves detection of sedatives or alcohol.", True),
        ("Medical opinion in sexual assault should avoid", "Commenting on truthfulness or consent beyond medical evidence", ["Documenting injuries", "Collecting samples with consent", "Treating injuries"], "The doctor records findings; legal conclusions are for the court."),
        ("A report states 'no injuries, therefore no rape occurred.' The major flaw is that", "Absence of injury does not rule out sexual assault", ["All swabs are useless", "Consent is never relevant", "Only police can examine"], "Medical findings can be normal despite assault; wording must be objective.", True),
    ]),
    ("toxicology-general", "General Toxicology and Poisoning Duties", [
        ("A poison is a substance that can cause harm by", "Chemical action when introduced into the body", ["Only mechanical tearing", "Only legal order", "Only x-ray exposure"], "Poisons injure through chemical or physicochemical effects."),
        ("The first step in management of poisoning is usually", "Stabilization of airway, breathing and circulation", ["Writing final death certificate", "Waiting for laboratory report", "Exhumation"], "Resuscitation and supportive care come before specific antidotes."),
        ("Gastric lavage is generally most useful when", "Performed early for selected serious ingestions", ["Done in every poisoning after 48 hours", "Used for corrosives routinely", "Used without airway protection in coma"], "Lavage has limited indications and must be risk-assessed."),
        ("A comatose pesticide-poisoned patient reaches emergency with secretions and respiratory distress. The immediate priority is", "Airway and breathing support", ["Age estimation", "Fingerprinting", "Court testimony"], "Life support is the first priority in acute poisoning.", True),
        ("Activated charcoal acts mainly by", "Adsorbing many toxins in the gut", ["Neutralizing all acids", "Increasing alcohol absorption", "Breaking bones"], "Charcoal reduces absorption of many, but not all, poisons."),
        ("An antidote is", "A substance that counteracts poison effects", ["A court order", "A postmortem stain", "A fingerprint class"], "Antidotes work by binding, blocking, converting or physiologically opposing toxins."),
        ("In medico-legal poisoning, the doctor should", "Treat first and preserve relevant samples with documentation", ["Refuse care until police arrive", "Discard gastric contents", "Avoid recording history"], "Clinical care and evidence preservation both matter."),
        ("After gastric lavage in suspected poisoning, the first wash and vomitus are saved, sealed and labeled. This is done for", "Chemical analysis of suspected poison", ["Dental age estimation", "Ballistic comparison", "Brain death testing"], "Gastric contents can contain unabsorbed poison.", True),
        ("A common route for occupational poisoning is", "Inhalation or dermal exposure", ["Only prayer", "Only bone fusion", "Only postmortem invasion"], "Workplace toxins often enter through lungs or skin."),
        ("A farm worker collapses after spraying pesticide without protection. History, contaminated clothing and cholinergic signs should prompt", "Treatment plus preservation of relevant samples", ["Immediate discharge", "Only civil consent form", "No medico-legal documentation"], "Occupational poisoning needs urgent care and documented evidence.", True),
    ]),
    ("corrosives-irritants", "Corrosive and Irritant Poisons", [
        ("Corrosive acids cause tissue injury mainly by", "Coagulative necrosis", ["Liquefactive necrosis only", "Ventricular fibrillation only", "Diatom embolism"], "Strong acids denature proteins and produce coagulative necrosis."),
        ("Corrosive alkalis cause tissue injury mainly by", "Liquefactive necrosis", ["Coagulative necrosis only", "Mummification", "Rigor mortis"], "Alkalis saponify fats and penetrate deeply."),
        ("Carbolic acid poisoning may produce", "White leathery burns with phenolic odor", ["Cherry-red lividity only", "Washerwoman hands", "Hyoid fracture"], "Phenol can cause pale leathery corrosive burns and systemic toxicity."),
        ("A patient drinks toilet-cleaning acid and presents with oral burns and dysphagia. Gastric lavage should generally be avoided because of", "Risk of perforation and further injury", ["Failure to identify fingerprints", "Need for epiphyseal fusion", "Absence of poison"], "Corrosive ingestion risks perforation; blind lavage can worsen injury.", True),
        ("Oxalic acid poisoning is notable for", "Hypocalcemia due to calcium oxalate formation", ["Hyperglycemia only", "Carbon monoxide formation", "Hyoid fracture"], "Oxalate binds calcium and may injure kidneys."),
        ("Sulfuric acid stains clothing and tissues", "Black or brown due to dehydration and charring", ["Bright green always", "Blue from cyanosis only", "No color change"], "Sulfuric acid is strongly dehydrating and chars organic matter."),
        ("Nitric acid commonly causes", "Yellow staining due to xanthoproteic reaction", ["Fern-like lightning marks", "Adipocere", "Marbling veins"], "Nitric acid reacts with proteins producing yellow discoloration."),
        ("A person has yellow stains around mouth after suspected acid ingestion. The corrosive suggested is", "Nitric acid", ["Oxalic acid", "Hydrochloric acid only", "Phenol only"], "Nitric acid causes yellow xanthoproteic staining.", True),
        ("Irritant poisons commonly cause", "Gastrointestinal pain, vomiting and diarrhea", ["Only silent hypothermia", "Only skeletal fusion", "Only fingerprint loss"], "Irritants inflame the GI tract."),
        ("Severe vomiting, abdominal pain and hypocalcemic tetany after ingestion of a bleaching compound suggests", "Oxalic acid poisoning", ["Drowning", "Manual strangulation", "Heat stroke"], "Oxalic acid causes GI corrosion and calcium binding.", True),
    ]),
    ("neurotoxic-asphyxiant-poisons", "Neurotoxic and Asphyxiant Poisons", [
        ("Organophosphorus poisoning inhibits", "Acetylcholinesterase", ["Monoamine oxidase only", "DNA polymerase", "Alcohol dehydrogenase"], "Organophosphates phosphorylate acetylcholinesterase, causing acetylcholine excess."),
        ("The muscarinic features of organophosphorus poisoning include", "Salivation, lacrimation, bronchorrhea and miosis", ["Dry mouth and mydriasis", "Cherry-red skin only", "Painless paralysis without secretions"], "Cholinergic excess produces secretions, bronchospasm, bradycardia and pinpoint pupils."),
        ("Atropine in organophosphorus poisoning mainly treats", "Muscarinic manifestations", ["Aging of enzyme directly", "Diatom embolism", "Skin corrosion"], "Atropine blocks muscarinic receptors but does not reactivate cholinesterase."),
        ("A farmer presents with miosis, sweating, salivation, wheeze, fasciculations and bradycardia after pesticide exposure. The best diagnosis is", "Organophosphorus poisoning", ["Carbon monoxide poisoning", "Oxalic acid poisoning", "Heat stroke"], "The cholinergic toxidrome after pesticide exposure is classic for organophosphates.", True),
        ("Pralidoxime is useful in organophosphorus poisoning because it", "Reactivates phosphorylated acetylcholinesterase before aging", ["Blocks opioid receptors", "Forms methemoglobin", "Neutralizes acid burns"], "Oximes can regenerate cholinesterase if given before aging of the enzyme complex."),
        ("Carbon monoxide causes hypoxia by", "Binding hemoglobin with high affinity to form carboxyhemoglobin", ["Destroying calcium only", "Blocking hyoid bone", "Producing diatoms"], "CO shifts oxygen carriage and delivery by forming carboxyhemoglobin."),
        ("A classic postmortem color in carbon monoxide poisoning is", "Cherry-red lividity", ["Green right iliac fossa", "Black sulfur tattooing", "Yellow nitric staining"], "Carboxyhemoglobin gives blood and lividity a bright red color."),
        ("A family sleeping near a faulty heater is found confused with headache; one member dies with cherry-red hypostasis. The likely poison is", "Carbon monoxide", ["Phenol", "Oxalic acid", "Snake venom"], "Faulty combustion in enclosed spaces produces carbon monoxide poisoning.", True),
        ("Cyanide poisoning inhibits", "Cytochrome oxidase and cellular respiration", ["Acetylcholine release only", "Blood clotting factor VIII", "Bone mineralization"], "Cyanide blocks oxidative phosphorylation, causing histotoxic hypoxia."),
        ("A laboratory worker collapses rapidly after exposure to cyanide salts, with bitter almond odor noted by responders. The key mechanism is", "Histotoxic hypoxia from cytochrome oxidase inhibition", ["Liquefactive corrosion", "Mechanical neck compression", "Immersion syndrome"], "Cyanide prevents tissues from using oxygen despite oxygenated blood.", True),
    ]),
]


def build_chapter(chapter_slug, chapter_title, chapter_order, topics):
    out = []
    for topic_order, (slug, topic, rows) in enumerate(topics, 1):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} rows")
        for index, row in enumerate(rows, 1):
            data = q(*row)
            answer = data["answer"]
            shift = (topic_order + index + chapter_order) % 4
            opts = data["options"][shift:] + data["options"][:shift]
            out.append({
                **data,
                "id": f"fmt-section1-{chapter_slug}-{slug}-{index:02d}",
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "subject": SUBJECT_TITLE,
                "chapterTitle": chapter_title,
                "chapterOrder": chapter_order,
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "source": "ai",
                "sourcePdf": SOURCE_PDF,
                "imageUrls": [],
                "options": opts,
                "answerIndex": opts.index(answer),
                "answer": answer,
            })
    return out


def build():
    return (
        build_chapter("legal-identification-death", "Section 1: Legal Medicine, Identification and Thanatology", 1, LEGAL_TOPICS)
        + build_chapter("postmortem-trauma-asphyxia-toxicology", "Section 1: Postmortem Changes, Injuries, Asphyxia and Toxicology", 2, PM_TRAUMA_TOPICS)
    )


def validate(questions):
    if len(questions) != 200:
        raise ValueError(f"Expected 200 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != len(questions):
        raise ValueError("Duplicate IDs in generated questions")
    for chapter in {item["chapterTitle"] for item in questions}:
        chapter_qs = [item for item in questions if item["chapterTitle"] == chapter]
        clinical = sum("clinical" in item.get("tags", []) for item in chapter_qs)
        if len(chapter_qs) != 100:
            raise ValueError(f"{chapter}: expected 100, got {len(chapter_qs)}")
        if clinical != 30:
            raise ValueError(f"{chapter}: expected 30 clinical, got {clinical}")
        for topic in {item["topic"] for item in chapter_qs}:
            topic_qs = [item for item in chapter_qs if item["topic"] == topic]
            topic_clinical = sum("clinical" in item.get("tags", []) for item in topic_qs)
            if len(topic_qs) != 10 or topic_clinical != 3:
                raise ValueError(f"{topic}: {len(topic_qs)} questions, {topic_clinical} clinical")
    for item in questions:
        if item["options"][item["answerIndex"]] != item["answer"]:
            raise ValueError(item["id"])


def update(path, questions):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ids = {item["id"] for item in questions}
    data["questions"] = [item for item in data.get("questions", []) if item.get("id") not in ids] + questions
    data["questions"].sort(key=lambda item: item.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    questions = build()
    validate(questions)
    for path in DATA_PATHS:
        update(path, questions)
        print(f"Added {len(questions)} FMT Section 1 questions to {path}.")
    for chapter in sorted({item["chapterTitle"] for item in questions}):
        print(f"- {chapter}: 100 questions, 30 clinical")


if __name__ == "__main__":
    main()
