import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Reproductive System"
CHAPTER_ORDER = 12
BASE = {"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":641,"sourcePdfPageEnd":720,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt":prompt,"options":[answer,*wrong],"answerIndex":0,"answer":answer,"explanation":explanation,"difficulty":"moderate","tags":["clinical"] if clinical else []}

TOPICS=[
("sexual-growth-development","Sexual Growth and Development",1,[
q("Which hormone from hypothalamus initiates the reproductive endocrine axis at puberty?", "GnRH", ["TRH","ADH","Oxytocin"], "Pulsatile GnRH stimulates pituitary gonadotropin release."),
q("FSH and LH are secreted from which gland?", "Anterior pituitary", ["Posterior pituitary","Adrenal medulla","Pineal gland"], "Gonadotrophs of anterior pituitary secrete FSH and LH."),
q("Primary sex characteristics refer mainly to development of which organs?", "Gonads and genital organs", ["Voice alone","Body hair alone","Breast fat only"], "Primary sex characteristics involve reproductive organs."),
q("A boy with delayed puberty has low LH and FSH with low testosterone. Which level is likely affected?", "Hypothalamic-pituitary axis", ["Renal tubules","Adrenal medulla only","Thyroid C cells"], "Low gonadotropins with low sex steroids suggests central hypogonadism.", True),
q("Secondary sex characteristics in males are produced mainly by which hormone?", "Testosterone", ["Progesterone","Prolactin","Calcitonin"], "Androgens produce male secondary sexual characters."),
q("Secondary sex characteristics in females depend mainly on which hormones?", "Oestrogens", ["Aldosterone","Glucagon","ADH"], "Oestrogens produce female secondary sexual development."),
q("Inhibin primarily suppresses secretion of which pituitary hormone?", "FSH", ["ACTH","TSH","Prolactin"], "Inhibin from gonads selectively inhibits FSH."),
q("A girl with early breast development and pubic hair before expected age is being evaluated for which condition?", "Precocious puberty", ["Menopause","Sheehan syndrome","Diabetes insipidus"], "Early development of secondary sexual characters suggests precocious puberty.", True),
q("Sex differentiation of internal male ducts requires which fetal hormone?", "Testosterone", ["Cortisol","Insulin","PTH"], "Testosterone supports Wolffian duct development."),
q("Failure of androgen action in an XY fetus can cause undervirilization because target tissues cannot respond to which hormone?", "Testosterone/dihydrotestosterone", ["Thyroxine","Calcitonin","Secretin"], "Androgen receptor/action defects impair male genital differentiation.", True),
]),
("male-reproductive","Male Reproductive Physiology",2,[
q("Spermatogenesis occurs in which structure?", "Seminiferous tubules", ["Epididymal duct only","Prostate gland","Vas deferens only"], "Sperm are produced in seminiferous tubules."),
q("Leydig cells primarily secrete which hormone?", "Testosterone", ["Inhibin","Oxytocin","Oestrogen only"], "LH stimulates Leydig cells to produce testosterone."),
q("Sertoli cells support spermatogenesis and secrete which hormone?", "Inhibin", ["Aldosterone","Gastrin","ADH"], "Sertoli cells secrete inhibin and support germ cells."),
q("A man with pituitary failure has infertility and low testosterone. Which hormone deficiency directly reduces Leydig cell stimulation?", "LH", ["TSH","ADH","Prolactin only"], "LH stimulates testosterone secretion from Leydig cells.", True),
q("FSH in males primarily acts on which cells?", "Sertoli cells", ["Leydig cells only","Prostate smooth muscle","Epididymal epithelium only"], "FSH stimulates Sertoli cell function and spermatogenesis."),
q("Testosterone is converted to the more potent androgen DHT by which enzyme?", "5-alpha reductase", ["Aromatase","Tyrosinase","Carbonic anhydrase"], "5-alpha reductase converts testosterone to DHT in target tissues."),
q("The epididymis is important mainly for which sperm function?", "Maturation and storage", ["Production of testosterone","Formation of seminal fructose","Urine concentration"], "Sperm gain motility and maturity in epididymis."),
q("A patient with bilateral obstruction of vas deferens has azoospermia despite normal testicular size. Which process is blocked?", "Transport of sperm", ["Testosterone synthesis","LH secretion","Sertoli cell formation"], "Duct obstruction prevents sperm from entering ejaculate.", True),
q("Seminal vesicles contribute a secretion rich in which nutrient?", "Fructose", ["Bile salts","Creatinine","Urea"], "Fructose supports sperm metabolism."),
q("Varicocele can impair fertility mainly by increasing testicular temperature and reducing which process?", "Spermatogenesis", ["Prolactin release","Bile secretion","ADH action"], "Spermatogenesis requires a cooler scrotal environment.", True),
]),
("female-reproductive","Female Reproductive Physiology",3,[
q("Ovarian follicles produce which major steroid during the follicular phase?", "Oestrogen", ["Aldosterone","Cortisol only","Calcitonin"], "Growing follicles secrete oestrogen."),
q("Ovulation is triggered mainly by a surge of which hormone?", "LH", ["TSH","ACTH","ADH"], "The midcycle LH surge triggers ovulation."),
q("Corpus luteum secretes mainly which hormone?", "Progesterone", ["Renin","Calcitonin","Secretin"], "Corpus luteum secretes progesterone and oestrogen."),
q("A woman with regular cycles has peak basal body temperature after ovulation. Which hormone explains this rise?", "Progesterone", ["FSH","Oxytocin","Prolactin"], "Progesterone has thermogenic action after ovulation.", True),
q("The proliferative phase of endometrium is driven mainly by which hormone?", "Oestrogen", ["Progesterone","ADH","Glucagon"], "Oestrogen rebuilds endometrium after menstruation."),
q("The secretory phase of endometrium is driven mainly by which hormone?", "Progesterone", ["Calcitonin","Aldosterone","Insulin only"], "Progesterone converts endometrium to secretory state."),
q("Menstruation occurs primarily due to withdrawal of which hormones?", "Oestrogen and progesterone", ["Insulin and glucagon","PTH and calcitonin","ADH and oxytocin"], "Regression of corpus luteum causes steroid withdrawal and shedding."),
q("A woman with anovulatory cycles has infertility because which event fails?", "Release of oocyte from follicle", ["Formation of bile","Gastric emptying","Renal filtration"], "Anovulation prevents oocyte release.", True),
q("FSH promotes follicular growth mainly by acting on which ovarian cells?", "Granulosa cells", ["Leydig cells","Chief cells","Kupffer cells"], "FSH stimulates granulosa cell proliferation and aromatase."),
q("Polycystic ovarian syndrome commonly causes anovulation with increased androgen effect. Which clinical feature may appear?", "Hirsutism", ["Tetany","Jaundice only","Polyuria from ADH loss"], "Androgen excess can cause hirsutism in PCOS.", True),
]),
("coitus-pregnancy-parturition","Physiology of Coitus, Pregnancy and Parturition",4,[
q("Fertilization most commonly occurs in which part of the uterine tube?", "Ampulla", ["Isthmus near uterus only","Cervix","Uterine fundus"], "The ampulla is the usual site of fertilization."),
q("Human chorionic gonadotropin maintains which structure in early pregnancy?", "Corpus luteum", ["Graafian follicle only","Adrenal medulla","Posterior pituitary"], "hCG maintains corpus luteum progesterone secretion."),
q("Progesterone during pregnancy helps maintain what?", "Uterine quiescence and endometrium", ["Menstrual shedding","Milk ejection","Spermatogenesis"], "Progesterone supports pregnancy and reduces uterine contractility."),
q("A woman with ectopic tubal pregnancy has implantation outside the uterus. Fertilization likely occurred normally in which site?", "Fallopian tube", ["Ovary cortex only","Vagina","Cervical canal only"], "Most fertilization occurs in the tube; abnormal transport can lead to ectopic implantation.", True),
q("Placenta functions as an endocrine organ by secreting hCG and which steroid hormones?", "Oestrogen and progesterone", ["Insulin and glucagon","PTH and calcitonin","ADH and oxytocin"], "Placenta produces steroid hormones during pregnancy."),
q("Relaxin in pregnancy mainly helps by affecting which tissues?", "Pelvic ligaments and cervix", ["Retina","Renal glomeruli only","Liver sinusoids"], "Relaxin softens cervix and pelvic ligaments."),
q("Parturition is promoted by oxytocin and which local mediators?", "Prostaglandins", ["Bile salts","Pepsin","Erythropoietin"], "Oxytocin and prostaglandins increase uterine contractions."),
q("A woman in labour receives oxytocin infusion. Which uterine response is expected?", "Stronger rhythmic contractions", ["Permanent relaxation","Absent cervical dilation always","Suppressed prostaglandins only"], "Oxytocin stimulates uterine smooth muscle contraction.", True),
q("Positive feedback in labour involves cervical stretch increasing release of which hormone?", "Oxytocin", ["Insulin","Calcitonin","Gastrin"], "Ferguson reflex increases oxytocin during labour."),
q("Failure of cervical dilation despite weak uterine contractions may be treated by augmenting which physiological pathway?", "Oxytocin-mediated uterine contraction", ["ADH-mediated water retention","PTH-mediated calcium absorption","TSH-mediated thyroid release"], "Oxytocin can augment uterine contractions during labour when appropriate.", True),
]),
("lactation","Physiology of Lactation",5,[
q("Milk production is stimulated mainly by which anterior pituitary hormone?", "Prolactin", ["Oxytocin","TSH","ACTH"], "Prolactin promotes milk synthesis in mammary alveoli."),
q("Milk ejection is caused mainly by which hormone?", "Oxytocin", ["Prolactin","Aldosterone","Gastrin"], "Oxytocin contracts myoepithelial cells and ejects milk."),
q("Suckling increases prolactin by reducing hypothalamic release of which inhibitor?", "Dopamine", ["GnRH","CRH","GHRH"], "Suckling reduces dopamine inhibition of prolactin."),
q("A mother can produce milk but cannot eject it after postpartum haemorrhage-related pituitary injury. Which hormone pathway is most relevant?", "Oxytocin reflex", ["Calcitonin pathway","Renin pathway","Gastrin pathway"], "Milk ejection depends on neurohypophyseal oxytocin release.", True),
q("Colostrum is especially rich in which protective component?", "Immunoglobulins", ["Bile salts","Gastric acid","Creatinine"], "Colostrum contains high immunoglobulin content."),
q("High prolactin during lactation suppresses fertility mainly by inhibiting which hypothalamic hormone?", "GnRH", ["TRH","ADH","Oxytocin"], "Prolactin suppresses GnRH pulsatility and ovulation."),
q("The let-down reflex is initiated by stimulation of which receptors?", "Nipple mechanoreceptors", ["Baroreceptors","Osmoreceptors only","Chemoreceptors in carotid body"], "Suckling activates nipple sensory afferents."),
q("A lactating woman has amenorrhoea in the early postpartum period because prolactin suppresses which process?", "Ovulatory cycle", ["Milk ejection","Calcium absorption","Thyroid hormone synthesis"], "Lactational amenorrhoea occurs from suppressed GnRH/LH pulsatility.", True),
q("Mammary gland growth during pregnancy is supported by oestrogen, progesterone and which hormone?", "Prolactin", ["PTH","Calcitonin","Secretin"], "Multiple hormones prepare breast tissue for lactation."),
q("Stress can inhibit milk let-down primarily by reducing release/action of which hormone?", "Oxytocin", ["Insulin","Gastrin","Aldosterone"], "Stress can impair the oxytocin-mediated ejection reflex.", True),
]),
("contraception","Physiology of Contraception",6,[
q("Combined oral contraceptive pills mainly prevent ovulation by suppressing which hormones?", "FSH and LH", ["TSH and ACTH","ADH and oxytocin","PTH and calcitonin"], "Oestrogen-progestin feedback suppresses gonadotropins."),
q("Progesterone-only contraception thickens which secretion to reduce sperm entry?", "Cervical mucus", ["Bile","Saliva","Pancreatic juice"], "Progestins thicken cervical mucus and inhibit sperm penetration."),
q("Copper intrauterine devices mainly act by producing which local effect?", "Spermicidal inflammatory reaction", ["Increased ovulation","Raised prolactin","Complete pituitary failure"], "Copper IUDs create a local environment toxic to sperm."),
q("A woman misses multiple combined pills and ovulates. Which feedback suppression was lost?", "Gonadotropin suppression", ["ADH suppression","PTH suppression","Calcitonin suppression"], "Missed pills can permit FSH/LH rise and ovulation.", True),
q("Emergency contraception with levonorgestrel works mainly before fertilization by delaying what?", "Ovulation", ["Implantation always after pregnancy established","Milk ejection","Parturition"], "Levonorgestrel emergency contraception mainly delays or inhibits ovulation."),
q("Barrier methods prevent pregnancy mainly by blocking what?", "Sperm entry into female reproductive tract", ["LH synthesis","Progesterone receptors","Milk production"], "Condoms and diaphragms mechanically reduce sperm entry."),
q("Vasectomy prevents fertility by interrupting which structure?", "Vas deferens", ["Seminiferous tubule only","Prostate gland","Ureter"], "Vasectomy blocks sperm transport through the vas deferens."),
q("After vasectomy, testosterone levels usually remain normal because which cells are preserved?", "Leydig cells", ["Thyroid C cells","Adrenal chromaffin cells","Pancreatic beta cells"], "Vasectomy blocks ducts but does not remove Leydig cells.", True),
q("Tubal ligation prevents pregnancy mainly by blocking which event?", "Meeting of sperm and ovum", ["Menstruation","Oestrogen synthesis always","Lactation"], "Blocking uterine tubes prevents fertilization."),
q("A copper IUD user has contraception without systemic hormonal suppression. Which pituitary pattern is expected?", "FSH and LH cycles may continue", ["Permanent zero LH","Absent ACTH","Suppressed TSH always"], "Copper IUD acts locally and does not primarily suppress the hypothalamic-pituitary-ovarian axis.", True),
]),
]

def build():
    out=[]
    for slug,topic,order,rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4
            opts=row["options"][shift:]+row["options"][:shift]
            ans=row["answer"]
            out.append({**BASE,**row,"id":f"physiology-reproductive-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
    return out

def validate(qs):
    if len(qs)!=60: raise ValueError(f"Expected 60, got {len(qs)}")
    if len({q["id"] for q in qs})!=60: raise ValueError("Duplicate IDs")
    for _,topic,_,_ in TOPICS:
        t=[q for q in qs if q["topic"]==topic]
        if len(t)!=10 or sum("clinical" in q.get("tags",[]) for q in t)<3: raise ValueError(topic)
    for qn in qs:
        if qn["answer"]!=qn["options"][qn["answerIndex"]]: raise ValueError(qn["id"])

def update(path,qs):
    data=json.loads(path.read_text(encoding="utf-8-sig"))
    ids={q["id"] for q in qs}
    data["questions"]=[q for q in data.get("questions",[]) if q.get("id") not in ids]+qs
    data["questions"].sort(key=lambda q:q.get("id",""))
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def main():
    qs=build(); validate(qs)
    for p in DATA_PATHS:
        update(p,qs); print(f"Added {len(qs)} physiology questions to {p}.")
    for _,topic,_,_ in TOPICS: print(f"- {topic}: 10 questions")

if __name__=="__main__":
    main()
