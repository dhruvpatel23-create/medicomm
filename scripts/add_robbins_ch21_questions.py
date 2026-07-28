import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Lower Urinary Tract and Male Genital System"
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
    ("cystitis-obstruction", "Cystitis, Obstruction, and Bladder Injury Patterns", [
        q("easy", "Cystitis means inflammation of the:", "Urinary bladder", ["Prostate gland", "Renal glomerulus", "Seminal vesicle"], "Cystitis is inflammation of the bladder mucosa."),
        q("easy", "The most common bacterial cause of cystitis is:", "Escherichia coli", ["Hepatitis B virus", "Giardia lamblia", "Mycobacterium leprae"], "Uropathogenic E. coli causes most uncomplicated UTIs."),
        q("easy", "Hemorrhagic cystitis can be caused by:", "Cyclophosphamide", ["Omeprazole", "Aspirin only", "Metformin"], "Cyclophosphamide metabolite acrolein can injure bladder mucosa."),
        q("moderate", "Interstitial cystitis is also called:", "Painful bladder syndrome", ["Renal colic syndrome", "Fanconi syndrome", "Nephrotic syndrome"], "It causes chronic bladder pain and urinary frequency without infection."),
        q("moderate", "Malakoplakia contains macrophages with:", "Michaelis-Gutmann bodies", ["Auer rods", "Reed-Sternberg cells", "Mallory bodies"], "Michaelis-Gutmann bodies are mineralized bacterial remnants."),
        q("moderate", "Chronic bladder outlet obstruction can cause bladder:", "Trabeculation", ["Podocyte effacement", "Wire-loop lesions", "Crescent formation"], "Muscular hypertrophy produces trabeculated bladder wall."),
        q("moderate", "Urinary obstruction above the bladder may cause:", "Hydroureter and hydronephrosis", ["Membranous nephropathy", "Minimal change disease", "Amyloidosis only"], "Back pressure dilates ureter and renal collecting system."),
        q("high", "A woman has dysuria, urgency, suprapubic pain, and urine culture growing E. coli. Bladder biopsy would most likely show acute inflammation of the mucosa. Which diagnosis fits best?", "Acute bacterial cystitis", ["Interstitial cystitis", "Urothelial carcinoma", "Schistosomal carcinoma"], "Acute bacterial cystitis is usually caused by ascending E. coli."),
        q("high", "A patient receiving cyclophosphamide for chemotherapy develops gross hematuria and bladder mucosal ulceration from a toxic metabolite concentrated in urine. Which metabolite is responsible?", "Acrolein", ["Aflatoxin B1", "Ceruloplasmin", "Myoglobin"], "Acrolein mediates cyclophosphamide-associated hemorrhagic cystitis."),
        q("high", "An older man with chronic urinary retention has a thick-walled trabeculated bladder, diverticula, bilateral hydroureter, and hydronephrosis. Which process caused the upper tract dilation?", "Chronic bladder outlet obstruction", ["Anti-GBM nephritis", "Podocyte injury", "Immune complex nephritis"], "Long-standing outlet obstruction transmits pressure to ureters and kidneys."),
    ]),
    ("urothelial-neoplasia", "Urothelial Neoplasia and Bladder Carcinoma", [
        q("easy", "The most common bladder malignancy is:", "Urothelial carcinoma", ["Wilms tumor", "Renal oncocytoma", "Seminoma"], "Most bladder cancers arise from urothelium."),
        q("easy", "The classic presenting symptom of bladder cancer is:", "Painless hematuria", ["Steatorrhea", "Hemarthrosis", "Painless jaundice"], "Gross painless hematuria is a common presentation."),
        q("easy", "A major risk factor for urothelial carcinoma is:", "Cigarette smoking", ["Gluten intake", "Low salt diet", "Iron deficiency"], "Smoking exposes urothelium to carcinogens."),
        q("moderate", "A papillary urothelial neoplasm grows into the:", "Bladder lumen", ["Renal cortex only", "Prostatic stroma only", "Seminiferous tubules only"], "Papillary tumors project into the bladder cavity."),
        q("moderate", "Flat high-grade urothelial carcinoma in situ is often:", "Multifocal", ["Always encapsulated", "Always benign", "Only in children"], "Carcinoma in situ can involve broad urothelial fields."),
        q("moderate", "Muscle invasion in bladder carcinoma worsens prognosis because it indicates invasion of:", "Muscularis propria", ["Lamina propria only", "Surface umbrella cells", "Mucus layer only"], "Detrusor muscle invasion is a major staging threshold."),
        q("moderate", "Aromatic amine exposure increases risk of:", "Urothelial carcinoma", ["Seminoma only", "Wilms tumor", "Prostatic hyperplasia"], "Industrial aromatic amines are classic bladder carcinogens."),
        q("high", "An older smoker has painless hematuria and cystoscopy showing a papillary exophytic bladder mass. Biopsy shows atypical urothelial cells lining fibrovascular cores. Which cancer is most likely?", "Urothelial carcinoma", ["Squamous cell carcinoma", "Renal cell carcinoma", "Prostatic adenocarcinoma"], "Papillary urothelial carcinoma commonly presents with painless hematuria."),
        q("high", "A bladder biopsy shows flat high-grade cytologic atypia throughout the urothelium without invasion through the basement membrane. Which precursor or noninvasive lesion is present?", "Urothelial carcinoma in situ", ["Papilloma", "Cystitis cystica", "Nephrogenic adenoma"], "Carcinoma in situ is flat high-grade noninvasive urothelial carcinoma."),
        q("high", "A patient has a bladder tumor initially limited to lamina propria, but repeat resection shows extension into detrusor muscle. Which feature now most changes staging and management?", "Muscularis propria invasion", ["Papillary architecture alone", "Hematuria alone", "Tumor location at dome"], "Muscle invasion marks invasive bladder cancer with worse prognosis."),
    ]),
    ("squamous-adenocarcinoma", "Squamous, Glandular, and Variant Bladder Tumors", [
        q("easy", "Schistosoma haematobium is linked to bladder:", "Squamous cell carcinoma", ["Seminoma", "Wilms tumor", "Oncocytoma"], "Chronic schistosomal cystitis predisposes to squamous carcinoma."),
        q("easy", "Bladder adenocarcinoma may arise from remnants of the:", "Urachus", ["Vitelline duct", "Thyroglossal duct", "Ductus arteriosus"], "Urachal remnants can give rise to adenocarcinoma at the dome."),
        q("easy", "Chronic irritation can produce squamous metaplasia in:", "Bladder urothelium", ["Seminiferous tubules", "Adrenal cortex", "Renal glomeruli"], "Persistent irritation can convert urothelium to squamous epithelium."),
        q("moderate", "Bladder squamous carcinoma is associated with:", "Chronic infection and stones", ["Minimal change disease", "Alport syndrome", "Acute pancreatitis"], "Long-standing irritation predisposes to squamous carcinoma."),
        q("moderate", "Urachal adenocarcinoma usually occurs near the:", "Bladder dome", ["Bladder trigone only", "Prostatic apex", "Renal papilla"], "The urachus connects to the bladder dome."),
        q("moderate", "Small cell carcinoma of bladder shows:", "Neuroendocrine differentiation", ["Ovarian-type stroma", "Squamoid nests only", "Podocyte effacement"], "Small cell bladder carcinoma is a neuroendocrine malignancy."),
        q("moderate", "Keratin pearls in a bladder tumor suggest:", "Squamous differentiation", ["Pure urothelial carcinoma in situ", "Renal cell carcinoma", "Seminoma"], "Keratinization supports squamous carcinoma."),
        q("high", "A patient from an endemic region has chronic hematuria and bladder wall calcification from Schistosoma haematobium infection. Years later, a keratinizing invasive bladder tumor develops. Which carcinoma is favored?", "Squamous cell carcinoma", ["Urothelial papilloma", "Clear cell RCC", "Prostatic adenocarcinoma"], "Schistosomiasis predisposes to squamous carcinoma of bladder."),
        q("high", "A tumor at the bladder dome produces mucin and gland-forming malignant cells. The pathologist suspects origin from an embryologic midline remnant. Which diagnosis best fits?", "Urachal adenocarcinoma", ["Papillary urothelial carcinoma", "Seminoma", "Angiomyolipoma"], "Urachal adenocarcinoma arises near the bladder dome and forms glands."),
        q("high", "A patient with long-standing bladder stones develops a tumor composed of invasive nests of atypical squamous cells with keratin pearls. Which pathogenesis best explains this tumor?", "Chronic irritation causing squamous metaplasia and carcinoma", ["Anti-GBM antibody injury", "Podocyte cytokine injury", "Germ cell neoplasia"], "Chronic irritation promotes squamous metaplasia and carcinoma."),
    ]),
    ("prostatitis-bph", "Prostatitis and Benign Prostatic Hyperplasia", [
        q("easy", "Benign prostatic hyperplasia arises mainly in the:", "Transition zone", ["Peripheral zone", "Renal cortex", "Seminiferous tubules"], "BPH develops in the periurethral transition zone."),
        q("easy", "BPH commonly causes:", "Lower urinary tract obstruction", ["Nephrotic syndrome directly", "Hemoptysis", "Steatorrhea"], "Nodular hyperplasia compresses the urethra."),
        q("easy", "Acute bacterial prostatitis often presents with:", "Fever and dysuria", ["Painless jaundice", "Hemarthrosis", "Visual aura"], "Acute prostatitis causes systemic and urinary symptoms."),
        q("moderate", "BPH is driven largely by:", "Dihydrotestosterone", ["Cortisol only", "Calcitonin", "Erythropoietin"], "DHT stimulates stromal and glandular proliferation."),
        q("moderate", "Histology of BPH shows hyperplasia of:", "Glands and stroma", ["Only squamous epithelium", "Only Leydig cells", "Only podocytes"], "BPH is nodular glandular and stromal hyperplasia."),
        q("moderate", "Chronic prostatitis may present with:", "Pelvic discomfort and recurrent urinary symptoms", ["Massive proteinuria", "Biliary colic", "Hemolysis"], "Chronic prostatitis causes persistent pelvic and urinary complaints."),
        q("moderate", "Nodular BPH can produce bladder:", "Trabeculation and diverticula", ["Wire-loop lesions", "Fat necrosis", "Goblet cell metaplasia"], "Outlet obstruction causes bladder wall hypertrophy and diverticula."),
        q("high", "An older man has hesitancy, weak stream, nocturia, and incomplete bladder emptying. The enlarged prostate has periurethral nodules composed of proliferating glands and fibromuscular stroma. Which diagnosis is likely?", "Benign prostatic hyperplasia", ["Prostatic adenocarcinoma", "Chronic cystitis only", "Seminoma"], "BPH arises in the transition zone and obstructs urine flow."),
        q("high", "A man with fever, chills, dysuria, and a tender boggy prostate has prostatic secretions rich in neutrophils and bacteria. Which inflammatory condition is most likely?", "Acute bacterial prostatitis", ["Benign prostatic hyperplasia", "Prostatic adenocarcinoma", "Granulomatous orchitis"], "Acute bacterial prostatitis causes fever, dysuria, and neutrophilic inflammation."),
        q("high", "A patient with nodular prostatic enlargement develops chronic urinary retention, bladder trabeculation, hydroureter, bilateral hydronephrosis, and recurrent infections. Which hormone-dependent process initiated the obstruction?", "DHT-driven transition zone hyperplasia", ["Androgen-independent peripheral zone carcinoma", "Anti-GBM antibody injury", "Leydig cell tumor secretion"], "DHT promotes transition-zone BPH and urethral compression."),
    ]),
    ("prostate-cancer", "Prostatic Adenocarcinoma", [
        q("easy", "Prostatic adenocarcinoma usually arises in the:", "Peripheral zone", ["Transition zone", "Renal pelvis", "Epididymis"], "Most prostate cancers arise posteriorly in the peripheral zone."),
        q("easy", "A useful serum marker for prostate cancer is:", "PSA", ["AFP only", "CA-125", "Troponin"], "PSA is used in detection and monitoring."),
        q("easy", "Prostate cancer commonly metastasizes to:", "Bone", ["Spleen only", "Appendix only", "Gallbladder"], "Osteoblastic bone metastases are classic."),
        q("moderate", "Prostatic adenocarcinoma often produces bone lesions that are:", "Osteoblastic", ["Purely lytic always", "Cystic only", "Cartilaginous"], "Prostate cancer commonly causes sclerotic bone metastases."),
        q("moderate", "Gleason grading is based on:", "Glandular architectural pattern", ["Tumor color", "Urine protein amount", "Serum calcium only"], "Gleason score evaluates prostate cancer gland architecture."),
        q("moderate", "Loss of basal cell layer supports diagnosis of:", "Prostatic adenocarcinoma", ["Benign prostatic hyperplasia", "Acute prostatitis", "Cystitis cystica"], "Cancerous glands lack the basal cell layer."),
        q("moderate", "Perineural invasion is a common feature of:", "Prostatic adenocarcinoma", ["Minimal change disease", "Seminoma only", "BPH only"], "Prostate cancer often tracks along nerves."),
        q("high", "A man has a hard irregular nodule on digital rectal exam. Biopsy from the posterior peripheral zone shows small crowded glands lacking basal cells. Which diagnosis is most likely?", "Prostatic adenocarcinoma", ["Benign prostatic hyperplasia", "Acute bacterial prostatitis", "Urothelial papilloma"], "Peripheral-zone malignant glands without basal cells indicate prostate cancer."),
        q("high", "A patient with prostate cancer develops persistent back pain, elevated alkaline phosphatase, and imaging shows dense sclerotic vertebral lesions. Which metastatic pattern is characteristic of this tumor?", "Osteoblastic bone metastases", ["Mucinous peritoneal deposits", "Pure lung cavitation", "Splenic infarction only"], "Prostatic adenocarcinoma commonly causes osteoblastic bone metastases."),
        q("high", "A prostate biopsy contains separate tumor patterns scored by architecture, and the sum predicts prognosis better than tumor size alone. Which grading system is being used?", "Gleason grading system", ["Nottingham grading", "Fuhrman grading", "Ann Arbor staging"], "Gleason grading sums dominant architectural patterns."),
    ]),
    ("testis-congenital-inflammatory", "Testicular Developmental, Vascular, and Inflammatory Disorders", [
        q("easy", "Cryptorchidism means undescended:", "Testis", ["Bladder", "Kidney", "Prostate"], "Cryptorchidism is failure of testicular descent."),
        q("easy", "Testicular torsion compromises blood flow through the:", "Spermatic cord", ["Ureter", "Renal vein only", "Ductus arteriosus"], "Torsion twists the spermatic cord."),
        q("easy", "Mumps can cause inflammation of the:", "Testis", ["Gallbladder", "Pancreatic islets only", "Renal pelvis only"], "Mumps orchitis can occur after puberty."),
        q("moderate", "Cryptorchidism increases risk of:", "Germ cell tumor", ["Bladder stones only", "BPH", "Renal cysts"], "Undescended testes have increased malignancy risk."),
        q("moderate", "Testicular torsion causes sudden severe pain because of:", "Venous outflow obstruction and ischemia", ["Immune complex deposition", "Podocyte effacement", "DHT excess"], "Twisting initially obstructs venous drainage then arterial flow."),
        q("moderate", "Varicocele most commonly occurs on the:", "Left side", ["Right side always", "Midline bladder", "Prostatic urethra"], "Left testicular vein drainage predisposes to left varicocele."),
        q("moderate", "Chronic orchitis with granulomas may be due to:", "Tuberculosis", ["Minimal change disease", "Aflatoxin", "Wilson disease"], "Tuberculous infection can cause granulomatous epididymo-orchitis."),
        q("high", "A newborn boy has one testis absent from the scrotum and located in the inguinal canal on examination. If untreated, which long-term complication is increased?", "Testicular germ cell tumor", ["Urothelial carcinoma", "Benign prostatic hyperplasia", "Renal cell carcinoma"], "Cryptorchidism increases infertility and germ cell tumor risk."),
        q("high", "An adolescent has abrupt severe testicular pain, a high-riding testis, and absent cremasteric reflex. Surgical exploration shows twisting of the spermatic cord. Which diagnosis is most likely?", "Testicular torsion", ["Acute prostatitis", "Varicocele only", "Hydrocele"], "Torsion is a surgical emergency causing ischemia."),
        q("high", "A postpubertal patient develops painful swollen testes after parotitis, and biopsy shows interstitial mononuclear inflammation with seminiferous tubule damage. Which viral complication is present?", "Mumps orchitis", ["Schistosomal cystitis", "HPV condyloma", "Bacterial prostatitis"], "Mumps can cause orchitis and infertility after puberty."),
    ]),
    ("germ-cell-tumors", "Testicular Germ Cell Tumors: Seminoma and Nonseminoma", [
        q("easy", "The most common testicular tumors are:", "Germ cell tumors", ["Smooth muscle tumors", "Lymphomas in children", "Urothelial tumors"], "Most testicular neoplasms arise from germ cells."),
        q("easy", "Seminoma tumor cells classically have clear cytoplasm and central:", "Nuclei", ["Auer rods", "Keratin pearls", "Michaelis-Gutmann bodies"], "Seminoma has large cells with clear cytoplasm and central nuclei."),
        q("easy", "Yolk sac tumor often elevates:", "Alpha-fetoprotein", ["PSA", "Calcitonin", "Troponin"], "AFP is produced by yolk sac tumor."),
        q("moderate", "Most postpubertal germ cell tumors arise from:", "Germ cell neoplasia in situ", ["BPH nodules", "Bladder CIS", "Leydig cell hyperplasia"], "GCNIS is the precursor for many adult germ cell tumors."),
        q("moderate", "Seminoma is typically radiosensitive and has:", "Good prognosis", ["Uniformly fatal course", "No treatment response", "Only childhood onset"], "Pure seminoma responds well to therapy."),
        q("moderate", "Embryonal carcinoma is usually:", "More aggressive than seminoma", ["Always benign", "Only cystic", "A stromal tumor"], "Embryonal carcinoma is an aggressive nonseminomatous tumor."),
        q("moderate", "Choriocarcinoma may produce high levels of:", "hCG", ["PSA", "CEA only", "Renin"], "Syncytiotrophoblasts secrete hCG."),
        q("high", "A man has a painless testicular mass composed of sheets of uniform large cells with clear cytoplasm, fibrous septa, and lymphocytes. Which germ cell tumor is most likely?", "Seminoma", ["Yolk sac tumor", "Embryonal carcinoma", "Leydig cell tumor"], "Seminoma has clear cells in lobules with lymphocytic septa."),
        q("high", "A young child has a testicular tumor with reticular architecture, Schiller-Duval bodies, hyaline globules, and elevated serum alpha-fetoprotein. Which germ cell tumor is most likely?", "Yolk sac tumor", ["Seminoma", "Choriocarcinoma", "Teratoma"], "Yolk sac tumor has Schiller-Duval bodies and AFP elevation."),
        q("high", "A testicular tumor contains malignant cytotrophoblasts and syncytiotrophoblasts, causes very high hCG, and spreads hematogenously early despite a small primary lesion. Which tumor is this?", "Choriocarcinoma", ["Seminoma", "Yolk sac tumor", "Spermatocytic tumor"], "Choriocarcinoma is aggressive and hCG-producing."),
    ]),
    ("sex-cord-stromal", "Sex Cord-Stromal Tumors and Testicular Lymphoma", [
        q("easy", "Leydig cells normally produce:", "Testosterone", ["PSA", "Bile", "Erythropoietin"], "Leydig cells are androgen-producing interstitial cells."),
        q("easy", "Sertoli cells support:", "Spermatogenesis", ["Bile secretion", "Urine concentration", "Gastric acid secretion"], "Sertoli cells support developing germ cells."),
        q("easy", "The most common testicular tumor in older men may be:", "Lymphoma", ["Yolk sac tumor", "Seminoma only", "Wilms tumor"], "Testicular lymphoma is important in older men."),
        q("moderate", "Leydig cell tumors may contain:", "Reinke crystals", ["Auer rods", "Psammoma bodies", "Schiller-Duval bodies"], "Reinke crystals are characteristic of Leydig cell tumors."),
        q("moderate", "Leydig cell tumors in children may cause:", "Precocious puberty", ["Nephrotic syndrome", "Painless jaundice", "Hemarthrosis"], "Androgen secretion can produce early puberty."),
        q("moderate", "Sertoli cell tumors are usually:", "Benign", ["Always metastatic", "Infectious", "Purely urothelial"], "Most Sertoli cell tumors behave benignly."),
        q("moderate", "Testicular lymphoma in older men is commonly:", "Diffuse large B-cell lymphoma", ["Burkitt lymphoma only", "Hodgkin lymphoma always", "Follicular lymphoma only"], "DLBCL is a common testicular lymphoma subtype."),
        q("high", "A boy develops precocious puberty and a testicular mass. Microscopy shows polygonal cells with eosinophilic cytoplasm and rod-shaped Reinke crystals. Which tumor is most likely?", "Leydig cell tumor", ["Seminoma", "Yolk sac tumor", "Sertoli cell tumor"], "Leydig cell tumors may secrete androgens and contain Reinke crystals."),
        q("high", "An older man has painless testicular enlargement due to sheets of malignant lymphoid cells rather than a germ cell tumor. Which diagnosis is most likely in this age group?", "Diffuse large B-cell lymphoma", ["Embryonal carcinoma", "Yolk sac tumor", "Leydig cell tumor"], "Testicular lymphoma, often DLBCL, occurs in older men."),
        q("high", "A testicular mass is composed of tubules formed by cells resembling normal Sertoli cells and lacks germ cell tumor markers. Which sex cord-stromal tumor is suggested?", "Sertoli cell tumor", ["Choriocarcinoma", "Seminoma", "Teratoma"], "Sertoli cell tumors show tubules resembling sex cord differentiation."),
    ]),
    ("penis-scrotum", "Penis, Scrotum, and Sexually Transmitted Lesions", [
        q("easy", "Condyloma acuminatum is caused by:", "Human papillomavirus", ["Hepatitis C virus", "E. coli", "Schistosoma"], "Low-risk HPV types cause genital warts."),
        q("easy", "Penile squamous cell carcinoma is associated with:", "HPV infection", ["Minimal change disease", "BPH alone", "Mumps only"], "HPV infection is an important risk factor."),
        q("easy", "Peyronie disease involves fibrous plaques of the:", "Tunica albuginea", ["Bladder mucosa", "Renal cortex", "Prostate transition zone"], "Fibrosis of tunica albuginea causes penile curvature."),
        q("moderate", "High-risk HPV types linked to penile carcinoma include:", "HPV 16 and 18", ["HPV 6 and 11 only", "EBV only", "CMV only"], "HPV 16 and 18 are oncogenic types."),
        q("moderate", "Bowen disease of penis is:", "Squamous carcinoma in situ", ["Benign cystitis", "Leydig cell tumor", "BPH"], "Bowen disease is in situ squamous carcinoma."),
        q("moderate", "Erythroplasia of Queyrat occurs on the:", "Glans penis", ["Renal pelvis", "Epididymis", "Seminal vesicle"], "It is carcinoma in situ of glans or prepuce."),
        q("moderate", "Scrotal squamous carcinoma was historically linked to:", "Soot exposure", ["Gluten exposure", "Aflatoxin only", "Wilson disease"], "Chimney sweeps developed soot-related scrotal carcinoma."),
        q("high", "A sexually active man has soft exophytic papillary genital warts. Histology shows koilocytosis in squamous epithelium, and HPV testing detects low-risk types. Which lesion is present?", "Condyloma acuminatum", ["Bowen disease", "Penile squamous carcinoma", "Peyronie disease"], "Condyloma acuminatum is an HPV-related genital wart."),
        q("high", "An uncircumcised man has an ulcerated penile mass with invasive nests of atypical squamous cells and keratin pearls. Which malignant tumor is most likely?", "Penile squamous cell carcinoma", ["Seminoma", "Leydig cell tumor", "Urothelial carcinoma"], "Penile carcinoma is usually squamous cell carcinoma."),
        q("high", "A man develops painful curvature of the penis during erection, and pathology shows dense fibrous plaques involving the tunica albuginea. Which condition is most likely?", "Peyronie disease", ["Condyloma acuminatum", "Bowen disease", "Hydrocele"], "Peyronie disease is fibrous thickening of tunica albuginea."),
    ]),
    ("epididymis-prostate-misc", "Epididymis, Seminal Vesicles, Infertility, and Miscellaneous Lesions", [
        q("easy", "Epididymitis is inflammation of the:", "Epididymis", ["Bladder dome", "Renal glomerulus", "Prostate transition zone only"], "Epididymitis affects the epididymal duct."),
        q("easy", "Hydrocele is fluid accumulation in the:", "Tunica vaginalis", ["Seminiferous tubules", "Prostatic glands", "Bladder wall"], "Hydrocele is serous fluid around the testis."),
        q("easy", "Spermatocele is a cystic dilation containing:", "Sperm", ["Bile", "Keratin pearls", "Amyloid"], "Spermatoceles contain spermatozoa."),
        q("moderate", "In younger men, epididymitis is commonly caused by:", "Chlamydia trachomatis or Neisseria gonorrhoeae", ["Schistosoma only", "Hepatitis A", "Giardia"], "Sexually transmitted organisms are common causes in younger men."),
        q("moderate", "In older men, epididymitis is often related to:", "Urinary tract pathogens", ["HPV only", "Aflatoxin", "Mumps only"], "Older men often have ascending infection by enteric urinary organisms."),
        q("moderate", "Sperm granuloma can follow:", "Vasectomy", ["Cholecystectomy", "Appendectomy only", "Colectomy"], "Leakage of sperm can trigger granulomatous inflammation."),
        q("moderate", "A varicocele is dilation of veins in the:", "Pampiniform plexus", ["Prostatic urethra", "Renal papilla", "Bladder trigone"], "Varicocele is varicose dilation of pampiniform plexus veins."),
        q("high", "A young man has scrotal pain, fever, dysuria, swelling, and epididymal tenderness after urethritis. Testing detects Chlamydia trachomatis. Which diagnosis best explains the pain?", "Acute epididymitis", ["Testicular torsion", "Seminoma", "Hydrocele"], "Sexually transmitted infection can ascend to cause epididymitis."),
        q("high", "After vasectomy, a man develops a small painful nodule along the vas deferens. Histology shows foreign-body giant cell reaction around extravasated sperm. Which lesion is this?", "Sperm granuloma", ["Leydig cell tumor", "Condyloma acuminatum", "Urothelial carcinoma"], "Sperm leakage after vasectomy can cause sperm granuloma."),
        q("high", "A man has a painless scrotal swelling that transilluminates, and ultrasound shows clear fluid surrounding the testis within tunica vaginalis. Which lesion is most likely?", "Hydrocele", ["Varicocele", "Sperm granuloma", "Testicular torsion"], "Hydrocele is fluid within the tunica vaginalis."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch21-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 21 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch21-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 21 questions")
    print(f"Removed {total_removed} existing Chapter 21 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 21 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
