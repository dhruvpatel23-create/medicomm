import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Female Genital Tract"
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
    ("vulva-vagina", "Vulva and Vagina: Inflammation, Cysts, and Neoplasia", [
        q("easy", "Condyloma acuminatum is caused by:", "Human papillomavirus", ["Candida albicans", "Treponema pallidum", "Trichomonas vaginalis"], "Low-risk HPV types 6 and 11 commonly cause genital warts."),
        q("easy", "Bartholin cyst occurs from obstruction of the:", "Bartholin duct", ["Fallopian tube", "Endocervical canal", "Ureter"], "Duct obstruction causes cystic dilation of the Bartholin gland."),
        q("easy", "Vaginal candidiasis is commonly associated with:", "Thick white discharge", ["Green frothy discharge only", "Painless ulcer", "Watery ascites"], "Candida often causes pruritus and curd-like discharge."),
        q("moderate", "Lichen sclerosus of vulva increases risk of:", "Squamous cell carcinoma", ["Ovarian serous cystadenoma", "Endometrial stromal sarcoma", "Choriocarcinoma"], "Chronic vulvar dermatoses can predispose to squamous carcinoma."),
        q("moderate", "Paget disease of vulva is characterized by malignant cells in:", "Epidermis", ["Ovarian stroma", "Myometrium", "Fallopian tube fimbria"], "Extramammary Paget disease has intraepidermal malignant glandular cells."),
        q("moderate", "Clear cell adenocarcinoma of vagina is linked to in utero exposure to:", "Diethylstilbestrol", ["Tamoxifen", "Cyclophosphamide", "Aflatoxin"], "DES exposure increases vaginal clear cell adenocarcinoma risk."),
        q("moderate", "Trichomonas vaginalis classically produces:", "Frothy green-yellow discharge", ["Thick curd-like discharge", "Fishy clue cells only", "Painless chancre"], "Trichomoniasis causes frothy discharge and strawberry cervix."),
        q("high", "A young woman has exophytic vulvar warts. Biopsy shows papillary squamous proliferation with koilocytotic atypia, and HPV testing detects low-risk viral types. Which lesion is most likely?", "Condyloma acuminatum", ["Lichen sclerosus", "Extramammary Paget disease", "Bartholin cyst"], "Condyloma acuminatum is a low-risk HPV-related wart."),
        q("high", "An older woman has vulvar pruritus and thin white parchment-like plaques. Biopsy shows epidermal atrophy, dermal fibrosis, and chronic inflammation. Which disorder is most likely?", "Lichen sclerosus", ["Condyloma acuminatum", "Bartholin abscess", "Clear cell adenocarcinoma"], "Lichen sclerosus produces white atrophic plaques and raises SCC risk."),
        q("high", "A woman whose mother received diethylstilbestrol during pregnancy develops a vaginal mass composed of malignant clear cells with glandular architecture. Which tumor is most classically associated?", "Clear cell adenocarcinoma of vagina", ["Embryonal rhabdomyosarcoma", "Squamous papilloma", "Bartholin gland cyst"], "In utero DES exposure is linked to vaginal clear cell adenocarcinoma."),
    ]),
    ("cervicitis-hpv", "Cervicitis, HPV Infection, and Cervical Intraepithelial Neoplasia", [
        q("easy", "The most important cause of cervical cancer is:", "High-risk HPV infection", ["Candida infection", "Endometriosis", "Leiomyoma"], "Oncogenic HPV drives most cervical carcinomas."),
        q("easy", "HPV types 16 and 18 are considered:", "High-risk types", ["Low-risk wart-only types", "Bacterial pathogens", "Protozoa"], "HPV 16 and 18 are strongly oncogenic."),
        q("easy", "Koilocytosis suggests infection by:", "HPV", ["CMV", "HSV only", "Candida"], "Koilocytes are HPV-infected squamous cells."),
        q("moderate", "The cervical transformation zone is important because it is the usual site of:", "Squamous intraepithelial lesion", ["Leiomyoma", "Endometrioma", "Teratoma"], "Cervical precancers arise near the squamocolumnar junction."),
        q("moderate", "HPV E6 promotes degradation of:", "p53", ["RB only", "BRCA1 only", "PTEN only"], "E6 inactivates p53 tumor suppressor function."),
        q("moderate", "HPV E7 inactivates:", "RB", ["APC", "VHL", "HFE"], "E7 releases E2F by disrupting RB control."),
        q("moderate", "LSIL corresponds broadly to:", "CIN 1", ["CIN 3 only", "Invasive carcinoma", "Endometrial hyperplasia"], "LSIL is usually productive HPV infection with mild dysplasia."),
        q("high", "A Pap smear shows koilocytes and mild squamous atypia limited to the lower third of the cervical epithelium. Which cervical lesion is most likely?", "Low-grade squamous intraepithelial lesion", ["High-grade squamous intraepithelial lesion", "Invasive adenocarcinoma", "Endometrial polyp"], "LSIL/CIN 1 has mild dysplasia and HPV cytopathic change."),
        q("high", "A cervical biopsy shows atypical squamous cells involving nearly the full epithelial thickness, high mitotic activity, and no basement membrane invasion. Which lesion is present?", "High-grade squamous intraepithelial lesion", ["Condyloma acuminatum only", "Chronic cervicitis", "Invasive squamous carcinoma"], "HSIL includes CIN 2 and CIN 3 without stromal invasion."),
        q("high", "A high-risk HPV protein promotes cervical carcinogenesis by targeting p53, while another viral protein disables RB and promotes cell-cycle progression. Which pair is correct?", "E6 targets p53 and E7 targets RB", ["E6 targets APC and E7 targets VHL", "E6 targets PTEN and E7 targets BRCA1", "E6 targets HFE and E7 targets CFTR"], "High-risk HPV E6 and E7 disable p53 and RB pathways."),
    ]),
    ("cervical-cancer", "Invasive Cervical Carcinoma and Screening", [
        q("easy", "The most common invasive cervical cancer type is:", "Squamous cell carcinoma", ["Leiomyosarcoma", "Serous carcinoma", "Granulosa cell tumor"], "Most cervical cancers are squamous carcinomas."),
        q("easy", "Pap smear screening is used mainly to detect:", "Cervical precancer", ["Ovarian torsion", "Leiomyoma", "Ectopic pregnancy"], "Cytology detects cervical intraepithelial lesions."),
        q("easy", "Cervical adenocarcinoma arises from:", "Endocervical glandular epithelium", ["Myometrial smooth muscle", "Ovarian germ cells", "Vulvar epidermis only"], "Adenocarcinoma is gland-forming cervical malignancy."),
        q("moderate", "Invasive cervical carcinoma is diagnosed when tumor:", "Invades cervical stroma", ["Shows koilocytes only", "Is limited to epithelium", "Forms a benign polyp"], "Stromal invasion separates carcinoma from intraepithelial lesion."),
        q("moderate", "Cervical cancer commonly spreads locally to:", "Parametrium", ["Adrenal cortex", "Renal glomeruli", "Pancreatic ducts"], "Local extension can involve parametrium and pelvic structures."),
        q("moderate", "Adenocarcinoma in situ of cervix is associated with:", "High-risk HPV", ["Low estrogen only", "Bacterial vaginosis only", "Endometriosis"], "High-risk HPV also drives glandular cervical precursors."),
        q("moderate", "HPV vaccination primarily prevents disease caused by:", "Oncogenic HPV types", ["Candida species", "Chlamydia only", "Treponema pallidum"], "Vaccination reduces infection by high-risk HPV types."),
        q("high", "A woman with poor screening history has postcoital bleeding and an ulcerated cervical mass. Biopsy shows invasive nests of malignant squamous cells extending into stroma. Which diagnosis is most likely?", "Invasive squamous cell carcinoma of cervix", ["HSIL only", "Endometrial carcinoma", "Leiomyoma"], "Stromal invasion by malignant squamous cells defines invasive cervical SCC."),
        q("high", "A cervical glandular lesion has atypical mucin-producing cells replacing endocervical glands but remaining above the basement membrane without stromal invasion. Which diagnosis fits best?", "Adenocarcinoma in situ", ["Invasive adenocarcinoma", "Nabothian cyst", "Endometrial polyp"], "AIS is a high-risk HPV-related glandular precursor."),
        q("high", "A patient with invasive cervical carcinoma develops hydronephrosis because the tumor extends through the cervix into lateral pelvic tissues. Which local structure is commonly involved?", "Parametrium", ["Ovarian cortex", "Uterine fundal endometrium only", "Vaginal Bartholin gland"], "Parametrial invasion can obstruct ureters and worsen stage."),
    ]),
    ("endometrium-hyperplasia", "Endometrium: Abnormal Bleeding, Hyperplasia, and Polyps", [
        q("easy", "Endometrial hyperplasia is driven mainly by excess:", "Estrogen", ["Progesterone only", "Androgen absence", "Prolactin only"], "Unopposed estrogen stimulates endometrial proliferation."),
        q("easy", "Endometrial polyps commonly cause:", "Abnormal uterine bleeding", ["Hemoptysis", "Painless jaundice", "Renal colic"], "Polyps often present with irregular bleeding."),
        q("easy", "Anovulatory cycles can lead to unopposed:", "Estrogen stimulation", ["Bile obstruction", "Trypsin activation", "Iron overload"], "Lack of progesterone permits persistent estrogen effect."),
        q("moderate", "Atypical endometrial hyperplasia is now often termed:", "Endometrial intraepithelial neoplasia", ["CIN 1", "Serous tubal intraepithelial carcinoma", "Vulvar Paget disease"], "EIN indicates precancerous atypical gland proliferation."),
        q("moderate", "Endometrial hyperplasia risk is increased by:", "Polycystic ovary syndrome", ["Low estrogen state", "Mumps infection", "HPV 6 only"], "PCOS can cause chronic anovulation and estrogen exposure."),
        q("moderate", "Endometrial polyps are localized overgrowths of:", "Endometrial glands and stroma", ["Myometrial smooth muscle only", "Cervical squamous epithelium", "Ovarian germ cells"], "Polyps contain glands, stroma, and thick-walled vessels."),
        q("moderate", "Tamoxifen use can increase risk of:", "Endometrial hyperplasia and carcinoma", ["Cervical LSIL only", "Vaginal candidiasis", "Ovarian torsion"], "Tamoxifen has partial estrogen agonist effects in endometrium."),
        q("high", "A woman with obesity and chronic anovulation has abnormal uterine bleeding. Biopsy shows crowded proliferative glands with cytologic atypia and increased gland-to-stroma ratio. Which lesion is present?", "Endometrial intraepithelial neoplasia", ["Endometrial polyp only", "Atrophic endometrium", "Leiomyoma"], "Atypical hyperplasia/EIN is estrogen-driven precancer."),
        q("high", "A postmenopausal woman taking tamoxifen develops irregular bleeding, and hysteroscopy reveals a focal endometrial mass with cystically dilated glands and thick-walled vessels. Which lesion is likely?", "Endometrial polyp", ["Endocervical carcinoma", "Ovarian fibroma", "Hydatidiform mole"], "Tamoxifen is associated with endometrial polyps and hyperplasia."),
        q("high", "A patient with persistent unopposed estrogen exposure develops abnormal bleeding, endometrial gland crowding, and atypia. Which clinical condition most strongly explains this hormonal environment?", "Chronic anovulation from PCOS", ["Ovulatory cycles with high progesterone", "HPV infection", "Tubal torsion"], "PCOS causes chronic anovulation and unopposed estrogen stimulation."),
    ]),
    ("endometrial-cancer", "Endometrial Carcinoma and Precursors", [
        q("easy", "The most common gynecologic malignancy in many developed countries is:", "Endometrial carcinoma", ["Vaginal sarcoma", "Cervical sarcoma", "Ovarian lymphoma"], "Endometrial carcinoma is common in postmenopausal women."),
        q("easy", "Endometrioid carcinoma is associated with excess:", "Estrogen", ["Calcitonin", "Insulin absence only", "Bile salts"], "Type I endometrial carcinoma is estrogen-related."),
        q("easy", "Serous endometrial carcinoma often has mutation in:", "TP53", ["HBB", "CFTR", "HFE"], "Serous carcinoma is a type II tumor with p53 abnormalities."),
        q("moderate", "Endometrioid carcinoma commonly has mutation in:", "PTEN", ["VHL", "RET only", "BCR-ABL"], "PTEN mutations are common in endometrioid carcinoma."),
        q("moderate", "Serous carcinoma may arise in:", "Atrophic endometrium", ["Only hyperplastic endometrium", "Bartholin gland", "Ovarian germ cells only"], "Type II tumors often arise in atrophic endometrium."),
        q("moderate", "Postmenopausal bleeding should raise concern for:", "Endometrial carcinoma", ["Functional ovarian cyst only", "Candidiasis only", "Hydrocele"], "Bleeding after menopause requires evaluation for malignancy."),
        q("moderate", "Lynch syndrome increases risk of:", "Endometrial carcinoma", ["Condyloma acuminatum only", "Leiomyoma only", "Mature teratoma"], "Mismatch repair defects increase endometrial cancer risk."),
        q("high", "An obese postmenopausal woman with diabetes has vaginal bleeding. Biopsy shows malignant glands resembling endometrium and arising in a background of atypical hyperplasia. Which carcinoma type fits?", "Endometrioid endometrial carcinoma", ["Serous carcinoma", "Clear cell carcinoma of vagina", "Cervical squamous carcinoma"], "Endometrioid carcinoma is estrogen-related and often follows EIN."),
        q("high", "An elderly woman with atrophic endometrium develops an aggressive tumor with papillary architecture, marked atypia, and p53 mutation. Which endometrial carcinoma type is most likely?", "Serous carcinoma", ["Endometrioid carcinoma", "Leiomyosarcoma", "Endometrial polyp"], "Serous carcinoma is high grade and p53-driven."),
        q("high", "A woman with family history of colon and endometrial cancers develops an endometrial tumor showing microsatellite instability and mismatch repair protein loss. Which inherited syndrome is likely?", "Lynch syndrome", ["BRCA2-only syndrome", "Turner syndrome", "Peutz-Jeghers syndrome only"], "Lynch syndrome increases endometrial and colorectal carcinoma risk."),
    ]),
    ("myometrium", "Myometrium: Leiomyoma, Leiomyosarcoma, and Adenomyosis", [
        q("easy", "The most common benign tumor of the uterus is:", "Leiomyoma", ["Leiomyosarcoma", "Endometrial carcinoma", "Yolk sac tumor"], "Leiomyomas are common benign smooth muscle tumors."),
        q("easy", "Leiomyomas are composed of benign:", "Smooth muscle", ["Squamous epithelium", "Germ cells", "Trophoblasts"], "Fibroids are benign myometrial smooth muscle tumors."),
        q("easy", "Adenomyosis means endometrial glands and stroma within:", "Myometrium", ["Ovary", "Cervix only", "Fallopian tube lumen"], "Adenomyosis is endometrium located in myometrium."),
        q("moderate", "Leiomyomas often enlarge in response to:", "Estrogen", ["Low oxygen only", "HPV", "Bile acids"], "Fibroids are hormone responsive."),
        q("moderate", "Leiomyosarcoma usually arises:", "De novo from myometrium", ["By malignant transformation of most leiomyomas", "From cervical HPV infection", "From Bartholin duct"], "Most leiomyosarcomas arise independently rather than from fibroids."),
        q("moderate", "Adenomyosis commonly causes:", "Menorrhagia and dysmenorrhea", ["Painless hematuria", "Steatorrhea", "Jaundice"], "Ectopic endometrium in myometrium causes painful heavy bleeding."),
        q("moderate", "Leiomyosarcoma diagnosis depends on atypia, necrosis, and:", "Mitotic activity", ["Koilocytosis", "Schiller-Duval bodies", "Michaelis-Gutmann bodies"], "Mitotic rate helps separate sarcoma from benign smooth muscle tumor."),
        q("high", "A reproductive-age woman has heavy menstrual bleeding and a well-circumscribed whorled white uterine mass composed of bland smooth muscle bundles. Which tumor is most likely?", "Leiomyoma", ["Leiomyosarcoma", "Endometrial stromal sarcoma", "Adenomyosis"], "Leiomyoma is a benign whorled smooth muscle tumor."),
        q("high", "A postmenopausal woman has a rapidly enlarging uterine mass with hemorrhage, necrosis, marked cytologic atypia, and numerous mitoses. Which malignant myometrial tumor is most likely?", "Leiomyosarcoma", ["Leiomyoma", "Endometrial polyp", "Adenomyosis"], "Leiomyosarcoma is malignant smooth muscle tumor with atypia, mitoses, and necrosis."),
        q("high", "A woman has a diffusely enlarged boggy uterus with severe dysmenorrhea. Histology shows benign endometrial glands and stroma embedded deep within hypertrophic myometrium. Which diagnosis fits?", "Adenomyosis", ["Endometriosis", "Leiomyosarcoma", "Cervical carcinoma"], "Adenomyosis places endometrium within the myometrial wall."),
    ]),
    ("endometriosis", "Endometriosis and Extrauterine Endometrial Lesions", [
        q("easy", "Endometriosis is endometrial tissue located:", "Outside the uterus", ["Only within myometrium", "Only in cervix", "Only in placenta"], "Endometriosis is ectopic endometrial glands and stroma outside uterus."),
        q("easy", "Endometriosis commonly causes:", "Pelvic pain", ["Hemoptysis only", "Painless jaundice", "Renal casts"], "Cyclic pelvic pain is common."),
        q("easy", "An ovarian endometriotic cyst is called a:", "Chocolate cyst", ["Dermoid cyst", "Hydatidiform mole", "Bartholin cyst"], "Old blood gives endometriomas a chocolate appearance."),
        q("moderate", "Endometriosis requires histologic identification of:", "Endometrial glands and stroma", ["Only hemosiderin", "Only smooth muscle", "Only koilocytes"], "Both glands and stroma support diagnosis."),
        q("moderate", "Endometriosis can cause infertility by:", "Pelvic adhesions and tubal distortion", ["DHT excess", "HPV E6 effect", "Acrolein toxicity"], "Inflammation and adhesions impair fertility."),
        q("moderate", "Common sites of endometriosis include:", "Ovary and uterosacral ligaments", ["Kidney glomeruli", "Pancreatic ducts", "Thymus"], "Endometriosis often involves ovaries and pelvic peritoneum."),
        q("moderate", "Endometriosis lesions often contain hemosiderin from:", "Repeated cyclic bleeding", ["Iron overload diet", "Hemoglobinopathy only", "Bacterial pigment"], "Ectopic endometrium bleeds cyclically."),
        q("high", "A woman has cyclic pelvic pain, dyspareunia, infertility, and ovarian cysts filled with thick brown fluid. Histology shows endometrial glands, stroma, and hemosiderin-laden macrophages. Which diagnosis is most likely?", "Endometriosis", ["Adenomyosis", "Mature cystic teratoma", "Serous cystadenoma"], "Endometriosis causes ectopic cyclic bleeding and chocolate cysts."),
        q("high", "A patient with pelvic endometriosis develops infertility because dense adhesions distort the tubes and ovaries after repeated hemorrhage and inflammation. Which mechanism best explains infertility?", "Pelvic scarring with tubal distortion", ["High-risk HPV infection", "DHT-mediated obstruction", "Anti-GBM antibody injury"], "Endometriosis can impair fertility through adhesions and anatomic distortion."),
        q("high", "A biopsy from a pelvic peritoneal implant shows hemosiderin-laden macrophages, endometrial-type glands, and cellular stroma in a patient with cyclic pain. What lesion is present?", "Endometriotic implant", ["Leiomyoma", "Cervical LSIL", "Hydatidiform mole"], "Ectopic glands and stroma establish endometriosis."),
    ]),
    ("ovary-surface", "Ovarian Surface Epithelial Tumors", [
        q("easy", "The most common category of ovarian tumors is:", "Surface epithelial tumors", ["Germ cell tumors only", "Sex cord-stromal tumors only", "Lymphomas"], "Most ovarian neoplasms are surface epithelial."),
        q("easy", "Serous ovarian tumors resemble epithelium of the:", "Fallopian tube", ["Endocervix", "Endometrium only", "Vulvar epidermis"], "Serous tumors show tubal-type epithelium."),
        q("easy", "Mucinous ovarian tumors contain:", "Mucin-producing epithelium", ["Smooth muscle only", "Trophoblasts", "Leydig cells"], "Mucinous tumors are lined by mucinous epithelium."),
        q("moderate", "High-grade serous carcinoma is commonly associated with mutation in:", "TP53", ["HFE", "CFTR", "RET only"], "Nearly all high-grade serous carcinomas have p53 abnormalities."),
        q("moderate", "BRCA1 or BRCA2 mutation increases risk of:", "High-grade serous carcinoma", ["Leiomyoma only", "Cervical LSIL only", "Bartholin cyst"], "BRCA mutations raise ovarian and tubal high-grade serous carcinoma risk."),
        q("moderate", "Psammoma bodies are classically seen in:", "Serous tumors", ["Mucinous tumors only", "Fibromas only", "Dysgerminomas only"], "Serous neoplasms may contain psammoma bodies."),
        q("moderate", "Pseudomyxoma peritonei is often associated with mucinous tumor from:", "Appendix", ["Thyroid", "Cervix only", "Myometrium"], "Many cases arise from appendiceal mucinous neoplasms."),
        q("high", "A woman with BRCA1 mutation develops bilateral ovarian masses with solid and papillary areas. Histology shows marked atypia, slit-like spaces, and p53 mutation. Which tumor is most likely?", "High-grade serous carcinoma", ["Mucinous cystadenoma", "Fibroma", "Mature teratoma"], "High-grade serous carcinoma is linked to BRCA mutations and TP53."),
        q("high", "A large multiloculated ovarian cyst is lined by tall mucin-producing epithelium and lacks stromal invasion or solid malignant nodules. Which benign epithelial ovarian tumor is most likely?", "Mucinous cystadenoma", ["Serous carcinoma", "Granulosa cell tumor", "Dysgerminoma"], "Mucinous cystadenoma is a benign multilocular mucinous epithelial tumor."),
        q("high", "A serous tubal intraepithelial carcinoma is found in the fimbria of a risk-reducing salpingo-oophorectomy specimen from a BRCA carrier. Which ovarian cancer pathway is implicated?", "High-grade serous carcinoma pathway", ["Endometrioid hyperplasia pathway", "Germ cell neoplasia pathway", "Leiomyosarcoma pathway"], "Many high-grade serous carcinomas originate in fimbrial tubal epithelium."),
    ]),
    ("ovary-germ-stromal", "Ovarian Germ Cell and Sex Cord-Stromal Tumors", [
        q("easy", "A mature cystic teratoma is also called:", "Dermoid cyst", ["Chocolate cyst", "Hydatidiform mole", "Bartholin cyst"], "Mature teratoma is a dermoid cyst."),
        q("easy", "Dysgerminoma is the ovarian counterpart of:", "Seminoma", ["Leiomyoma", "Wilms tumor", "Choriocarcinoma only"], "Dysgerminoma resembles testicular seminoma."),
        q("easy", "Granulosa cell tumors may secrete:", "Estrogen", ["Bile", "PSA", "Erythropoietin"], "Granulosa cell tumors can be estrogenic."),
        q("moderate", "Call-Exner bodies are seen in:", "Granulosa cell tumor", ["Mature teratoma", "Mucinous cystadenoma", "Leiomyoma"], "Granulosa tumors may have Call-Exner bodies."),
        q("moderate", "Sertoli-Leydig cell tumors may cause:", "Virilization", ["Painless hematuria", "Cervical koilocytosis", "Hydronephrosis"], "Androgen secretion can cause virilization."),
        q("moderate", "Fibroma of ovary can be associated with ascites and hydrothorax called:", "Meigs syndrome", ["Zollinger-Ellison syndrome", "Trousseau syndrome", "Cushing syndrome"], "Meigs syndrome is fibroma with ascites and pleural effusion."),
        q("moderate", "Immature teratoma is malignant and contains immature:", "Neuroectodermal tissue", ["Endometrial glands only", "Smooth muscle only", "Mucin only"], "Immature neural tissue is important in grading."),
        q("high", "A young woman has an ovarian cyst containing hair, sebaceous material, cartilage, and squamous epithelium from multiple germ layers. Which tumor is most likely?", "Mature cystic teratoma", ["Dysgerminoma", "Granulosa cell tumor", "Serous cystadenoma"], "Mature teratoma contains mature tissues from different germ layers."),
        q("high", "A woman has an ovarian tumor producing estrogen and endometrial hyperplasia. Microscopy shows grooved coffee-bean nuclei and Call-Exner bodies. Which tumor is most likely?", "Granulosa cell tumor", ["Dysgerminoma", "Fibroma", "Mucinous cystadenoma"], "Granulosa cell tumors are estrogenic and show Call-Exner bodies."),
        q("high", "A young woman has a solid ovarian tumor composed of sheets of large clear cells separated by fibrous septa with lymphocytes. Which germ cell tumor is most likely?", "Dysgerminoma", ["Mature teratoma", "Yolk sac tumor", "Sertoli-Leydig cell tumor"], "Dysgerminoma resembles seminoma and has clear cells with lymphocytes."),
    ]),
    ("fallopian-gestational", "Fallopian Tube Disease, Ectopic Pregnancy, and Gestational Trophoblastic Disease", [
        q("easy", "The most common site of ectopic pregnancy is the:", "Fallopian tube", ["Ovary", "Cervix", "Vulva"], "Most ectopic pregnancies implant in the tube."),
        q("easy", "Hydatidiform mole is an abnormal proliferation of:", "Trophoblast", ["Smooth muscle", "Squamous epithelium", "Endometrial stroma only"], "Moles are gestational trophoblastic proliferations."),
        q("easy", "Choriocarcinoma produces high levels of:", "hCG", ["PSA", "AFP only", "Calcitonin"], "Trophoblastic tumors secrete hCG."),
        q("moderate", "Complete hydatidiform mole usually has karyotype:", "46,XX of paternal origin", ["45,X maternal only", "47,XXY always", "46,XY with fetal tissue always"], "Complete moles are androgenetic and usually diploid."),
        q("moderate", "Partial mole is commonly:", "Triploid with fetal tissue", ["Purely androgenetic without embryo", "A benign leiomyoma", "A cervical HPV lesion"], "Partial mole often has triploidy and some fetal parts."),
        q("moderate", "Ruptured ectopic pregnancy can cause:", "Hemoperitoneum", ["Nephrotic syndrome", "Hydatid cyst", "Bowel metaplasia"], "Tubal rupture can produce life-threatening bleeding."),
        q("moderate", "Acute salpingitis is often caused by:", "Chlamydia or gonorrhea", ["HPV 6 only", "Candida only", "Aflatoxin"], "PID commonly involves Chlamydia trachomatis or Neisseria gonorrhoeae."),
        q("high", "A pregnant patient has pelvic pain, amenorrhea, and vaginal bleeding. Surgery shows tubal rupture with products of conception in the fallopian tube. Which diagnosis is most likely?", "Tubal ectopic pregnancy", ["Complete mole", "Endometriosis", "Leiomyoma"], "The fallopian tube is the commonest ectopic implantation site."),
        q("high", "A uterus contains swollen avascular chorionic villi with diffuse circumferential trophoblastic proliferation and no fetal parts. Genetic testing shows diploid paternal DNA. Which lesion is present?", "Complete hydatidiform mole", ["Partial mole", "Placental site nodule", "Choriocarcinoma"], "Complete moles are androgenetic with diffuse trophoblastic proliferation."),
        q("high", "After evacuation of a molar pregnancy, a patient develops very high hCG and hemorrhagic metastatic lung nodules composed of malignant cytotrophoblast and syncytiotrophoblast without villi. Which tumor is likely?", "Choriocarcinoma", ["Placental site trophoblastic tumor", "Partial mole", "Endometrial polyp"], "Choriocarcinoma is malignant trophoblast without chorionic villi."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch22-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 22 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch22-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 22 questions")
    print(f"Removed {total_removed} existing Chapter 22 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 22 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
