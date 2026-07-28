import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "General Anatomy"
COVER_IMAGE = "/uploads/anatomy-general-page1-img1.jpg"
BASE = {"subjectId": "anatomy", "subjectTitle": "Anatomy", "chapterTitle": CHAPTER, "source": "ai"}


def q(prompt, answer, wrong, explanation, image=False):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation, "imageUrls": [COVER_IMAGE] if image else []}


TOPICS = [
    ("introduction", "Introduction", [
        q("The source-book cover image shows gross anatomical structures of the upper limb and head-neck region. The branch of anatomy that studies structures visible to the naked eye is:", "Gross anatomy", ["Histology", "Cytogenetics", "Biochemistry"], "Gross anatomy deals with macroscopic structures, usually studied by dissection, inspection, palpation, and imaging.", True),
        q("A student studying the upper limb by dissecting all structures in that limb is using which approach?", "Regional anatomy", ["Systemic anatomy", "Comparative anatomy", "Experimental anatomy"], "Regional anatomy studies all structures in one body region together."),
        q("Studying all arteries of the body as one continuous system is an example of:", "Systemic anatomy", ["Regional anatomy", "Surface anatomy", "Physical anthropology"], "Systemic anatomy studies organ systems such as vascular, nervous, skeletal, and muscular systems."),
        q("The anatomical term 'medial' means:", "Nearer to the median plane", ["Away from the median plane", "Nearer to the head", "Nearer to the surface"], "Medial denotes position closer to the median plane of the body."),
        q("In anatomical position, the palms face:", "Anteriorly", ["Posteriorly", "Medially", "Inferiorly"], "In anatomical position the body stands erect, upper limbs by the side, palms facing forwards."),
        q("A plane dividing the body into right and left halves is called:", "Sagittal plane", ["Coronal plane", "Transverse plane", "Oblique plane"], "Sagittal planes divide the body into right and left parts; the median sagittal plane divides it into equal halves."),
        q("The term 'proximal' is most useful for describing:", "A structure nearer the root of a limb", ["A structure nearer the skin", "A structure nearer the midline", "A structure nearer the tail"], "Proximal and distal are commonly used along limbs relative to their attachment."),
        q("The movement that brings a limb toward the median plane is:", "Adduction", ["Abduction", "Extension", "Circumduction"], "Adduction means movement toward the midline; abduction is away from it."),
        q("Pronation of the forearm places the palm:", "Posteriorly or downward", ["Anteriorly or upward", "Laterally always", "Medially always"], "Pronation rotates the forearm so the palm faces posteriorly in anatomical position or downward when flexed."),
        q("The study of deeper structures in relation to the skin surface is:", "Surface anatomy", ["Embryology", "Histology", "Comparative anatomy"], "Surface anatomy correlates internal structures with palpable or visible surface landmarks."),
    ]),
    ("skeleton", "Skeleton", [
        q("A bone that develops in a tendon is called a:", "Sesamoid bone", ["Pneumatic bone", "Irregular bone", "Flat bone"], "Sesamoid bones develop within tendons; the patella is the largest example."),
        q("The epiphyseal plate is responsible mainly for:", "Longitudinal growth of a long bone", ["Increase in medullary cavity only", "Bone marrow destruction", "Articular cartilage nutrition only"], "Endochondral ossification at the epiphyseal plate increases bone length."),
        q("The shaft of a typical long bone is the:", "Diaphysis", ["Epiphysis", "Metaphysis", "Apophysis"], "The diaphysis is the shaft; epiphyses are the ends and metaphyses are transition zones."),
        q("The Haversian system is a structural unit of:", "Compact bone", ["Hyaline cartilage", "Elastic cartilage", "Synovial membrane"], "Compact bone is organized into osteons or Haversian systems around central canals."),
        q("A nutrient artery of a long bone usually enters through the:", "Nutrient foramen", ["Epiphyseal plate", "Articular cartilage", "Periosteal collar only"], "Nutrient arteries enter through nutrient foramina and supply marrow and inner cortex."),
        q("Articular surfaces of a synovial joint are usually covered by:", "Hyaline cartilage", ["Fibrocartilage always", "Elastic cartilage", "Dense regular tendon"], "Most synovial joint surfaces are covered by hyaline articular cartilage."),
        q("Red bone marrow is primarily concerned with:", "Hematopoiesis", ["Calcium excretion", "Synovial fluid secretion", "Nerve conduction"], "Red marrow produces blood cells; yellow marrow is fat-rich."),
        q("A bone with air-filled cavities, such as frontal bone, is:", "Pneumatic bone", ["Sesamoid bone", "Accessory bone", "Sutural bone only"], "Pneumatic bones contain air sinuses that reduce weight and affect resonance."),
        q("The periosteum is absent over:", "Articular cartilage-covered surfaces", ["Shaft of long bones", "Outer skull vault", "Tendon attachment zones"], "Periosteum covers bone except at articular cartilage and a few attachment sites."),
        q("In fracture healing, the soft callus is later replaced by:", "Bony hard callus", ["Synovial membrane", "Elastic cartilage permanently", "Necrotic muscle"], "Fracture repair progresses from hematoma to soft callus, hard callus, and remodeling."),
    ]),
    ("joints", "Joints", [
        q("A joint with a cavity, capsule, synovial membrane, and articular cartilage is:", "Synovial joint", ["Fibrous joint", "Primary cartilaginous joint", "Suture"], "Synovial joints are characterized by a joint cavity and synovial lining."),
        q("The source-book cover image shows a mobile upper limb region. The joint type permitting the greatest range of movement is:", "Ball-and-socket joint", ["Plane joint", "Suture", "Gomphosis"], "Ball-and-socket joints like shoulder and hip allow multiaxial movements.", True),
        q("A primary cartilaginous joint is united by:", "Hyaline cartilage", ["Fibrocartilage", "Dense irregular capsule only", "Synovial fluid"], "Primary cartilaginous joints are synchondroses united by hyaline cartilage."),
        q("The intervertebral disc between vertebral bodies is an example of:", "Secondary cartilaginous joint", ["Primary cartilaginous joint", "Plane synovial joint", "Fibrous suture"], "Symphyses are secondary cartilaginous joints united by fibrocartilage."),
        q("A hinge joint primarily permits:", "Flexion and extension", ["Rotation only", "Circumduction only", "Gliding only"], "Hinge joints are uniaxial and allow flexion-extension, e.g., elbow."),
        q("A pivot joint primarily permits:", "Rotation around a vertical axis", ["Abduction only", "Flexion only", "Inversion only"], "Pivot joints, such as proximal radioulnar and median atlanto-axial joints, permit rotation."),
        q("A bursa reduces friction between:", "Moving tendons/skin and bone", ["Neuron and myelin", "Artery and vein only", "Red and yellow marrow"], "Bursae are synovial sacs that reduce friction around joints and tendons."),
        q("A joint stabilized mainly by its muscles rather than bony congruity is the:", "Shoulder joint", ["Hip joint", "Suture", "Pubic symphysis"], "The shoulder sacrifices stability for mobility and depends heavily on rotator cuff muscles."),
        q("Hilton's law states that a joint is supplied by nerves that also supply:", "Muscles moving the joint and skin over their insertions", ["Only overlying arteries", "Only periosteum of unrelated bones", "Only lymph nodes"], "Hilton's law links articular innervation with muscles acting on the joint and overlying skin."),
        q("Osteoarthritis primarily involves degeneration of:", "Articular cartilage", ["Motor end plate", "Red marrow", "Epidermis"], "Osteoarthritis is a degenerative joint disease mainly affecting articular cartilage and subchondral bone."),
    ]),
    ("muscles", "Muscles", [
        q("The anatomical structure in the cover image prominently includes muscle masses. Skeletal muscle is best described as:", "Voluntary striated muscle", ["Involuntary non-striated muscle", "Involuntary cardiac muscle", "Avascular connective tissue"], "Skeletal muscle is striated and under voluntary control.", True),
        q("A muscle producing the main desired movement is called the:", "Prime mover", ["Antagonist", "Fixator", "Neutralizer only"], "The prime mover or agonist is chiefly responsible for a movement."),
        q("A muscle that opposes the action of the prime mover is the:", "Antagonist", ["Synergist", "Fixator", "Origin"], "Antagonists control and oppose movement produced by agonists."),
        q("A pennate muscle arrangement usually favors:", "Greater force production", ["Maximum range of shortening only", "No tendon attachment", "Absence of fascicles"], "Pennation packs more fibers into a given volume, increasing force."),
        q("The functional contractile unit of skeletal muscle is the:", "Sarcomere", ["Osteon", "Nephron", "Haversian canal"], "Sarcomeres extend from Z line to Z line and contain actin-myosin filaments."),
        q("A motor unit consists of:", "One motor neuron and all muscle fibers it supplies", ["One muscle fiber and all sensory nerves", "One tendon and its bone", "One fascial compartment"], "Motor unit size determines precision and power of muscle activity."),
        q("The connective tissue surrounding an entire muscle is:", "Epimysium", ["Perimysium", "Endomysium", "Periosteum"], "Epimysium surrounds the whole muscle; perimysium surrounds fascicles; endomysium surrounds fibers."),
        q("A tendon attaches muscle to:", "Bone", ["Skin only", "Synovial fluid", "Lymph node"], "Tendons are dense connective tissue structures transmitting muscle force to bone."),
        q("Isometric contraction means muscle tension increases while:", "Muscle length remains nearly constant", ["Muscle length always increases", "The joint must move rapidly", "Nerve supply is absent"], "In isometric contraction force is generated without appreciable shortening."),
        q("Paralysis of a muscle most commonly follows injury to its:", "Motor nerve supply", ["Venous drainage only", "Overlying skin", "Nearby lymph node"], "Skeletal muscle contraction depends on intact lower motor neuron innervation."),
    ]),
    ("cardiovascular-system", "Cardiovascular System", [
        q("An artery is defined as a vessel that carries blood:", "Away from the heart", ["Toward the heart", "Only oxygenated blood", "Only deoxygenated blood"], "Arteries carry blood away from the heart; pulmonary arteries carry deoxygenated blood but remain arteries."),
        q("The vessel wall layer containing smooth muscle and elastic tissue is the:", "Tunica media", ["Tunica intima", "Tunica adventitia", "Endocardium"], "Tunica media is the muscular middle layer, especially developed in arteries."),
        q("The pulse felt in an artery is mainly due to:", "Pressure wave from ventricular systole", ["Venous valve closure", "Lymphatic contraction", "Skeletal muscle tone only"], "Arterial pulse is the palpable pressure wave produced by cardiac systole."),
        q("Veins differ from arteries by having:", "Valves commonly in limbs", ["Thicker muscular walls always", "No lumen", "No adventitia"], "Many limb veins contain valves that help prevent backflow."),
        q("Capillaries are specialized mainly for:", "Exchange between blood and tissues", ["Pulse generation", "Valve formation", "Storage of bile"], "Thin capillary walls permit gas, nutrient, and waste exchange."),
        q("An end artery is clinically important because occlusion causes:", "Ischemia/infarction of supplied territory", ["Immediate collateral compensation always", "Only venous congestion", "No tissue effect"], "True end arteries have little effective collateral supply."),
        q("Anastomosis between arteries is beneficial because it:", "Provides collateral circulation", ["Prevents all emboli", "Stops lymph flow", "Eliminates need for veins"], "Arterial anastomoses can maintain perfusion if one route narrows or is blocked."),
        q("The vasa vasorum supply:", "Walls of large blood vessels", ["Synovial fluid", "Cartilage matrix", "Epidermis"], "Large vessel walls are too thick to be nourished entirely by luminal diffusion."),
        q("The great saphenous vein is clinically used because it is:", "A long superficial vein suitable for grafting", ["An end artery", "A lymphatic trunk", "A nerve"], "The great saphenous vein is commonly harvested for bypass grafts."),
        q("A portal venous system connects:", "Two capillary beds before returning to heart", ["Two arteries directly", "A nerve to a lymph node", "Bone marrow to synovial cavity"], "Portal systems, such as hepatic portal circulation, interpose two capillary networks."),
    ]),
    ("lymphatic-system", "Lymphatic System", [
        q("The lymphatic system primarily returns excess tissue fluid to the:", "Venous circulation", ["Arterial circulation directly", "Synovial cavity", "Urinary bladder"], "Lymphatics collect interstitial fluid and return it to the venous system."),
        q("Lymph capillaries differ from blood capillaries because they:", "Begin blindly in tissues", ["Have thick muscular walls", "Carry red cells normally", "Have no endothelial lining"], "Lymph capillaries are blind-ended channels that absorb tissue fluid."),
        q("The right lymphatic duct drains lymph from:", "Right upper quadrant of the body", ["Both lower limbs", "Left thorax only", "Entire gastrointestinal tract"], "It drains right head-neck, right upper limb, and right thorax."),
        q("The thoracic duct usually opens into the:", "Left venous angle", ["Right atrium", "Inferior vena cava", "Portal vein"], "The thoracic duct drains into the junction of left internal jugular and subclavian veins."),
        q("Lymph nodes function mainly as:", "Filters and immune response sites", ["Synovial fluid producers", "Arterial pulse generators", "Bone-forming centers"], "Lymph nodes filter lymph and house lymphocytes and antigen-presenting cells."),
        q("Cancer cells spread through lymphatics most commonly to:", "Regional lymph nodes", ["Articular cartilage", "Tendons only", "Epidermis only"], "Lymphatic metastasis often first appears in draining regional nodes."),
        q("Lymphedema after lymph node removal results from:", "Obstructed lymph drainage", ["Excess arterial oxygen", "Increased bone marrow activity", "Reduced synovial fluid"], "Surgical/radiation injury to lymphatics can impair fluid return and cause swelling."),
        q("Lacteals are lymphatic vessels specialized for absorption of:", "Dietary fats", ["Oxygen", "Urea", "Bile pigments only"], "Intestinal lacteals absorb chylomicrons and carry chyle."),
        q("A sentinel lymph node is:", "First draining lymph node from a tumor area", ["Largest lymph node in body", "Node without immune cells", "A venous valve"], "Sentinel node biopsy assesses early lymphatic spread."),
        q("The spleen differs from lymph nodes because it filters:", "Blood", ["Synovial fluid", "CSF", "Bile"], "The spleen is a lymphoid organ that filters blood and removes aged RBCs."),
    ]),
    ("nervous-system", "Nervous System", [
        q("The cover image shows superficial nerves among vessels and muscles. The structural unit of the nervous system is the:", "Neuron", ["Sarcomere", "Osteon", "Lobule"], "Neurons are specialized excitable cells that receive and transmit nerve impulses.", True),
        q("A collection of neuron cell bodies outside the CNS is called a:", "Ganglion", ["Nucleus", "Tract", "Commissure"], "Ganglia are peripheral collections of neuronal cell bodies; nuclei are within the CNS."),
        q("A bundle of nerve fibers within the CNS is called a:", "Tract", ["Peripheral nerve", "Ganglion", "Motor unit"], "Tracts are bundles of axons in the CNS; nerves are bundles in the PNS."),
        q("Myelin in the peripheral nervous system is formed by:", "Schwann cells", ["Oligodendrocytes", "Astrocytes", "Microglia"], "Schwann cells myelinate peripheral axons; oligodendrocytes myelinate CNS axons."),
        q("Loss of pain and temperature on one side suggests involvement of:", "Spinothalamic pathway", ["Posterior column only", "Corticospinal tract only", "Optic radiation"], "The spinothalamic tract carries pain and temperature sensations."),
        q("The posterior column pathway carries:", "Fine touch, vibration, and conscious proprioception", ["Pain and temperature only", "Motor impulses only", "Taste"], "Posterior columns transmit discriminative touch, vibration, and proprioception."),
        q("A lower motor neuron lesion typically causes:", "Flaccid paralysis with reduced reflexes", ["Spasticity with hyperreflexia", "No muscle wasting ever", "Only sensory loss"], "LMN damage causes weakness, hypotonia, hyporeflexia, fasciculations, and wasting."),
        q("An upper motor neuron lesion typically causes:", "Spasticity and exaggerated reflexes", ["Flaccidity with absent reflexes only", "No Babinski sign", "Immediate denervation atrophy"], "UMN lesions remove inhibitory control, causing spasticity and hyperreflexia."),
        q("The autonomic nervous system supplies:", "Smooth muscle, cardiac muscle, and glands", ["Skeletal muscle only", "Articular cartilage only", "Bone marrow only"], "Autonomic fibers regulate involuntary effectors."),
        q("A dermatome is an area of skin supplied by:", "A single spinal nerve segment", ["One artery", "One lymph node", "One muscle tendon"], "Dermatomes are clinically useful for localizing radicular lesions."),
    ]),
    ("skin-and-fasciae", "Skin and Fasciae", [
        q("The epidermis is derived mainly from:", "Ectoderm", ["Mesoderm", "Endoderm", "Neural crest only"], "Epidermis is ectodermal, while dermis is largely mesodermal."),
        q("The thickest epidermal layer in thick skin is usually:", "Stratum corneum", ["Stratum basale", "Stratum spinosum only", "Stratum lucidum only"], "Thick skin of palms/soles has a very thick keratinized stratum corneum."),
        q("Superficial fascia contains:", "Loose connective tissue and fat", ["Only compact bone", "Only hyaline cartilage", "Only synovial membrane"], "Superficial fascia is subcutaneous connective tissue containing fat, vessels, nerves, and lymphatics."),
        q("Deep fascia is clinically important because it:", "Forms compartments and retinacula", ["Secretes sweat", "Produces red blood cells", "Forms epidermis"], "Deep fascia invests muscles, forms intermuscular septa, retinacula, and fascial compartments."),
        q("Compartment syndrome is dangerous mainly because raised pressure causes:", "Neurovascular ischemia", ["Excess sweating only", "Improved venous drainage", "Cartilage hypertrophy"], "High pressure in closed fascial compartments can compromise nerves and vessels."),
        q("Lines of cleavage of skin are important in surgery because incisions parallel to them:", "Heal with less gaping and scarring", ["Always avoid bleeding", "Prevent all infection", "Do not require sutures"], "Incisions along Langer lines tend to gape less and heal better cosmetically."),
        q("Sebaceous glands usually open into:", "Hair follicles", ["Synovial cavities", "Lymph nodes", "Arteries"], "Sebaceous glands secrete sebum into hair follicles except in modified locations."),
        q("Sweat glands are primarily involved in:", "Thermoregulation", ["Bone growth", "Myelination", "Joint lubrication"], "Eccrine sweat glands help regulate body temperature."),
        q("A retinaculum is a thickening of:", "Deep fascia", ["Epidermis", "Compact bone", "Synovial cartilage"], "Retinacula hold tendons in place near joints, especially wrist and ankle."),
        q("Skin over the anterior neck moves easily because of:", "Loose superficial fascia", ["Absence of dermis", "No blood supply", "Replacement by cartilage"], "Loose subcutaneous tissue permits mobility of skin over deeper structures."),
    ]),
    ("connective-tissue-ligaments-raphe", "Connective Tissue, Ligaments and Raphe", [
        q("Dense regular connective tissue is best suited for:", "Tensile force in one direction", ["Gas exchange", "Rapid nerve conduction", "Blood filtration"], "Parallel collagen bundles in tendons/ligaments resist unidirectional pull."),
        q("A ligament usually connects:", "Bone to bone", ["Muscle to bone", "Nerve to skin", "Artery to vein"], "Ligaments stabilize joints by connecting bones to bones."),
        q("The most abundant fiber in dense connective tissue is:", "Collagen", ["Elastin only", "Reticulin only", "Keratin"], "Collagen provides tensile strength and is abundant in tendons, ligaments, and fascia."),
        q("Elastic ligaments are prominent where repeated stretch and recoil are needed, such as:", "Ligamenta flava", ["Patellar ligament only", "Interosseous membrane only", "Palmar aponeurosis"], "Ligamenta flava contain abundant elastic tissue and aid vertebral column recoil."),
        q("An aponeurosis is:", "A flat expanded tendon", ["A lymphatic valve", "A bone marrow cavity", "A nerve plexus"], "Aponeuroses are sheet-like tendons that provide broad muscle attachment."),
        q("A raphe is best described as:", "A seam-like fibrous interdigitation", ["A synovial cavity", "A sesamoid bone", "A nerve root"], "A raphe is a line of union where fibers interlace, e.g., pterygomandibular raphe."),
        q("Loose areolar tissue is important because it:", "Allows movement between adjacent structures", ["Prevents all edema", "Has no vessels", "Forms compact bone"], "Areolar tissue permits sliding and contains vessels, nerves, and immune cells."),
        q("Reticular fibers are abundant in:", "Lymphoid organs", ["Articular cartilage only", "Enamel", "Epidermal keratin"], "Reticular fibers form supportive stroma in lymphoid organs and marrow."),
        q("A tendon sheath reduces friction by containing:", "Synovial fluid", ["Air", "Bone marrow", "CSF"], "Synovial tendon sheaths facilitate tendon gliding in confined spaces."),
        q("Sprain refers to injury of a:", "Ligament", ["Peripheral nerve only", "Artery only", "Bone marrow"], "A sprain is stretching or tearing of ligament fibers, commonly around joints."),
    ]),
    ("principles-of-radiography", "Principles of Radiography", [
        q("On a plain X-ray, cortical bone appears white mainly because it:", "Absorbs/attenuates X-rays strongly", ["Allows all X-rays through", "Emits visible light", "Contains air"], "Dense calcium-rich bone is radiopaque and appears white on radiographs."),
        q("Air in the lung appears black on X-ray because it is:", "Radiolucent", ["Radiopaque", "Calcified", "Metallic"], "Air attenuates very little radiation, so it appears dark."),
        q("The standard initial imaging for suspected simple fracture is usually:", "Plain radiography", ["PET scan", "Endoscopy", "EEG"], "Plain X-ray is fast, accessible, and good for most bone injuries."),
        q("A contrast medium is used to:", "Increase visibility of structures with similar natural density", ["Remove radiation exposure", "Replace anatomy knowledge", "Stop all motion artifacts"], "Contrast agents outline lumens or spaces not well seen on plain films."),
        q("CT imaging is especially useful because it provides:", "Cross-sectional anatomical detail", ["Only surface temperature", "Only electrical activity", "No radiation ever"], "CT reconstructs cross-sectional images and shows bone, air, fluid, and soft tissue relationships."),
        q("MRI is particularly superior for evaluating:", "Soft tissues and nervous system structures", ["Only cortical bone fracture lines", "Only lung air", "Only swallowed barium"], "MRI gives excellent soft tissue contrast without ionizing radiation."),
        q("Ultrasound image formation depends mainly on:", "Reflection of high-frequency sound waves", ["X-ray absorption", "Magnetic resonance", "Radioactive decay only"], "Ultrasound uses sound waves reflected at tissue interfaces."),
        q("A radiograph taken with the X-ray beam passing from posterior to anterior is a:", "PA view", ["AP view", "Lateral view", "Oblique view"], "PA means posterior-to-anterior beam direction; AP is anterior-to-posterior."),
        q("A radiopaque foreign body is most likely made of:", "Metal", ["Air", "Fat", "Simple fluid only"], "Metal strongly attenuates X-rays and appears very white."),
        q("A good radiological anatomy question first requires identifying:", "View, side, and anatomical landmarks", ["Only patient age", "Only machine brand", "Only film color"], "Correct interpretation begins with orientation: projection/view, laterality, and recognizable landmarks."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({
                **BASE,
                "id": f"anatomy-general-{slug}-{question_index:02d}",
                "topic": topic,
                "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high",
                "prompt": row["prompt"],
                "options": options,
                "answerIndex": answer_index,
                "answer": row["answer"],
                "explanation": row["explanation"],
                "imageUrls": row["imageUrls"],
            })

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "anatomy" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 10 or len(questions) != 100:
        raise AssertionError(f"Expected 10 topics and 100 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 100:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")
    if not Path("runtime-data/uploads/anatomy-general-page1-img1.jpg").exists():
        raise AssertionError("Expected source-book cover image is missing")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
