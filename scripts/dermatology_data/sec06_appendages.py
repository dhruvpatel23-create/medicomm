from .common import q

CHAPTERS = [
    (22, "Acne Vulgaris and Rosacea", "hard", [
        q(
            "What four fundamental, interlocking pathophysiological factors drive the development of inflammatory Acne Vulgaris within the pilosebaceous unit?",
            "Hyperkeratinization, sebum overproduction, Cutibacterium acnes proliferation, and inflammation",
            ["Demodex colonization, mast cell degranulation, and eccrine plugging", "Staphylococcus aureus superinfection, follicular rupture, and eccrine fibrosis", "Apocrine gland metaplasia, keratin obstruction, and autoimmune destruction"],
            "Acne vulgaris is a chronic multifactorial inflammatory disease of the pilosebaceous unit involving 4 key interrelated mechanisms: 1. Follicular infundibular hyperkeratinization leading to microcomedone formation; 2. Androgen-stimulated sebaceous gland hyperactivity (excess sebum); 3. Proliferation and follicular colonization of Cutibacterium acnes (formerly Propionibacterium acnes); 4. Host inflammatory response via activation of Toll-like receptor 2 (TLR-2) on monocytes, releasing IL-1, TNF-alpha, and IL-8.",
            clinical=False
        ),
        q(
            "What is the primary initial microscopic precursor lesion from which all clinical comedones and inflammatory acne lesions subsequently evolve?",
            "Microcomedo",
            ["Open comedo (blackhead)", "Closed comedo (whitehead)", "Inflammatory papule"],
            "The microcomedo is the microscopic, subclinical primary precursor lesion of all acne: abnormal retention hyperkeratosis of the follicular infundibulum causes desquamated corneocytes and cohesive sebum to accumulate, obstructing the pilosebaceous canal. Accumulation expands the follicle into a closed comedo (whitehead, non-inflamed dome-shaped papule) or open comedo (blackhead, whose dark color is due to oxidized melanin and lipid oxidation, NOT trapped dirt).",
            clinical=False
        ),
        q(
            "A 17-year-old male with severe nodulocystic acne was started on high-dose oral Isotretinoin (1.0 mg/kg/day). Three weeks later, he develops high spiking fever, leukocytosis, arthralgias of the knees and hips, painful osteolytic clavicular lesions, and rapid hemorrhagic ulceration of all facial acne nodules with copious purulent slough. What severe acute complication has occurred, and what is the immediate treatment?",
            "Acne fulminans; systemic oral corticosteroids followed by reintroduction of low-dose isotretinoin",
            ["Acne conglobata; increase the dose of isotretinoin immediately", "Stevens-Johnson syndrome; intravenous immunoglobulins", "Pyoderma gangrenosum; surgical debridement"],
            "Acne fulminans (acne febrile ulcerativa conglobata) is an acute, severe, highly inflammatory reaction classically precipitated by initiating high-dose oral isotretinoin in patients with extensive comedonal/nodular acne without corticosteroid pre-treatment. Massive lysis of C. acnes releases large antigenic loads, triggering an explosive hypersensitivity cascade. Immediate treatment requires oral Prednisolone (0.5 to 1.0 mg/kg/day) to control systemic inflammation before cautiously restarting low-dose isotretinoin.",
            clinical=True
        ),
        q(
            "What is the only systemic pharmacological agent for acne that simultaneously targets ALL four primary pathogenic mechanisms, and what mandatory clinical laboratory parameter must be screened prior to initiation in female patients?",
            "Oral isotretinoin; mandatory serial serum pregnancy tests",
            ["Oral doxycycline; routine monitoring of renal function", "Oral spironolactone; serial serum potassium monitoring", "Oral dapsone; baseline G6PD enzyme level screening"],
            "Oral Isotretinoin (13-cis-retinoic acid) is the single most effective acne drug: it induces apoptosis of sebocytes (reducing sebum production by >90%), normalizes follicular hyperkeratinization, indirectly suppresses C. acnes growth by depriving it of sebum substrate, and exerts direct anti-inflammatory effects. It is notoriously teratogenic (causing craniofacial, thymic, cardiac, and CNS malformations in >30% of exposed fetuses), necessitating strict pre-treatment and monthly negative pregnancy tests.",
            clinical=False
        ),
        q(
            "A 24-year-old female presents with persistent, recalcitrant inflammatory papulonodular acne concentrated predominantly along the jawline, chin, and anterior neck, accompanied by irregular oligomenorrhea, hirsutism on the upper lip, and female pattern hair thinning on the crown. What endocrine evaluation is indicated, and what is the targeted anti-androgenic therapy?",
            "PCOS; antiandrogenic oral contraceptives and spironolactone",
            ["Cushing syndrome; high-dose dexamethasone suppression therapy", "Congenital adrenal hyperplasia; oral fludrocortisone replacement", "Prolactinoma; dopamine agonist cabergoline therapy"],
            "Adult female acne with a 'U-shaped' mandibular/jawline distribution, associated with hirsutism, alopecia, and menstrual irregularities, strongly indicates hyperandrogenism, most commonly secondary to Polycystic Ovary Syndrome (PCOS). Hormonal evaluation (total/free testosterone, DHEAS, LH/FSH ratio, 17-OHP) is indicated. Treatment targets androgen excess using combined oral contraceptives (containing anti-androgenic progestins like drospirenone or cyproterone) and the androgen-receptor antagonist Spironolactone.",
            clinical=True
        ),
        q(
            "Which cardinal clinical feature definitively distinguishes Papulopustular Rosacea from inflammatory Acne Vulgaris?",
            "Total absence of comedones in rosacea",
            ["Absence of facial erythema in rosacea", "Presence of widespread open blackheads on the nose in rosacea", "Presence of severe trunk involvement in rosacea"],
            "Although papulopustular rosacea shares inflammatory papules and pustules on the central face with acne vulgaris, Rosacea is distinguished by the absolute, total absence of comedones (blackheads and whiteheads). Furthermore, rosacea is characterized by background fixed centrofacial erythema, telangiectasias, flushing, ocular symptoms, and strict confinement to the central convexities of the face (cheeks, nose, forehead, chin), sparing the trunk.",
            clinical=False
        ),
        q(
            "A 48-year-old male presents with persistent facial erythema, flushing provoked by spicy foods and hot coffee, telangiectasias across both cheeks, and recurrent crops of inflammatory papulopustules. Microscopic examination of sebum scraped from the follicles reveals high densities of which commensal saprophytic follicular mite?",
            "Demodex folliculorum (and Demodex brevis)",
            ["Sarcoptes scabiei", "Trombicula alfreddugesi", "Pediculus humanus"],
            "Demodex mites (Demodex folliculorum in the follicular infundibulum and Demodex brevis in the sebaceous ducts) are part of the normal facial cutaneous microbiome. In patients with rosacea, Demodex densities are significantly increased (often >5 mites per square centimeter), triggering innate immune activation via Toll-like receptor 2 (TLR-2) and upregulating kallikrein 5, which cleaves cathelicidin into the proinflammatory, angiogenic peptide LL-37.",
            clinical=True
        ),
        q(
            "A 66-year-old male presents with massive, lobulated, bulbous enlargement of his nose with dilated, gaping follicular pores and purplish telangiectasias ('whiskey nose'). Biopsy reveals exuberant sebaceous gland hyperplasia, thick collagenous dermal fibrosis, and chronic inflammation. What is this end-stage manifestation of rosacea termed?",
            "Rhinophyma (Phymatous rosacea)",
            ["Otophyma", "Gnathophyma", "Lupus pernio"],
            "Rhinophyma is the advanced, severe phymatous subtype of rosacea occurring almost exclusively in men over 50 years of age. It represents chronic, irreversible soft-tissue hypertrophy characterized by massive sebaceous gland hyperplasia, connective tissue fibrosis, and persistent lymphatic and vascular ectasia, transforming the nose into a bulbous, irregular, nodular mass. Surgical debulking (CO2 laser, electrosurgery, or surgical excision) is required.",
            clinical=True
        ),
        q(
            "What topical anti-inflammatory and anti-parasitic agent is approved as a first-line therapy for the inflammatory papulopustules of Rosacea, acting by targeting both Demodex mites and suppressing cellular inflammatory cytokine release?",
            "Topical Ivermectin 1% cream",
            ["Topical Mupirocin 2% ointment", "Topical Ketoconazole 2% cream", "Topical Clotrimazole 1% solution"],
            "Topical Ivermectin 1% cream applied once daily is a first-line treatment for moderate-to-severe papulopustular rosacea. It possesses a dual mechanism of action: 1. Anti-parasitic: it causes paralysis and death of Demodex mites by binding to glutamate-gated chloride ion channels; 2. Anti-inflammatory: it directly inhibits lipopolysaccharide-induced production of inflammatory cytokines (TNF-alpha, IL-1beta) and decreases cathelicidin/kallikrein expression.",
            clinical=False
        ),
        q(
            "A chemical plant worker accidentally exposed to high levels of 2,3,7,8-tetrachlorodibenzo-p-dioxin (TCDD) presents with an explosive outbreak of hundreds of discrete, pale yellow cysts and non-inflammatory open comedones densely covering the malar crescents beneath his eyes, retroauricular skin, and genitalia. What is this occupational toxic dermatosis termed?",
            "Chloracne",
            ["Acne cosmetica", "Acne venenata", "Pomade acne"],
            "Chloracne is one of the most sensitive and specific cutaneous biomarkers of systemic poisoning by halogenated aromatic hydrocarbons (dioxins, polychlorinated biphenyls [PCBs], dibenzofurans). Exposure leads to aryl hydrocarbon receptor (AhR) activation, transforming sebaceous glands into hyperkeratotic squamous cysts. Hallmarks: striking abundance of pale straw-colored cysts and comedones concentrated on the malar crescents, behind the ears, and in the groin/axillae.",
            clinical=True
        ),
    ]),
    (23, "Eccrine and Apocrine Gland Disorders", "easy", [
        q(
            "What precise anatomical level of eccrine sweat duct obstruction and histological micro-vesicle location differentiates Miliaria Crystallina, Miliaria Rubra, and Miliaria Profunda?",
            "Crystallina: subcorneal; Rubra: intraepidermal; Profunda: dermo-epidermal junction",
            ["Crystallina: reticular dermis; Rubra: subcutaneous fat; Profunda: stratum corneum", "Crystallina: spinous layer; Rubra: dermo-epidermal junction; Profunda: granulosum", "Crystallina: papillary dermis; Rubra: stratum basale; Profunda: spinosum"],
            "Miliaria results from retention of sweat due to occlusion of the eccrine sweat duct at varying depths: 1. Miliaria crystallina (sudamina): Obstruction in the superficial stratum corneum, producing tiny, crystal-clear, non-inflammatory vesicles without erythema; 2. Miliaria rubra (prickly heat): Obstruction in the mid-epidermis (stratum spinosum), causing intensely pruritic, erythematous papules; 3. Miliaria profunda: Obstruction at or below the dermo-epidermal junction, producing asymptomatic, flesh-colored dermal nodules.",
            clinical=False
        ),
        q(
            "A 26-year-old female presents with recurrent, painful, deep-seated, suppurative nodules, double-ended interconnected open comedones, foul-smelling discharging abscesses, and dense bridged hypertrophic keloidal scars in both axillae and inguinal folds. According to the Hurley staging system, what defines 'Hurley Stage II' severity?",
            "Recurrent abscesses with sinus tracts separated by normal skin",
            ["Isolated single or multiple abscesses without sinus tract formation", "Diffuse coalescent abscesses with interconnected sinus tracts across zone", "Superficial follicular pustules without deep dermal inflammatory involvement"],
            "Hidradenitis Suppurativa (acne inversa) is staged by the classic Hurley classification: Stage I: Solitary or multiple isolated abscess formation without sinus tracts and without cicatrization/scarring; Stage II: Recurrent abscesses with sinus tract formation and hypertrophic scarring, separated by normal intervening skin; Stage III: Diffuse, confluent involvement with multiple interconnected sinus tracts, extensive abscesses, and continuous scarring across the entire anatomical area.",
            clinical=True
        ),
        q(
            "What biological tumor necrosis factor-alpha (TNF-alpha) inhibitor is officially approved for the systemic treatment of moderate-to-severe, treatment-refractory Hidradenitis Suppurativa (Hurley Stage II and III)?",
            "Adalimumab",
            ["Rituximab", "Eculizumab", "Omalizumab"],
            "Adalimumab (a fully human monoclonal anti-TNF-alpha IgG1 antibody) was the first biologic approved for moderate-to-severe Hidradenitis Suppurativa. Massive overexpression of TNF-alpha, IL-1beta, and IL-17 in HS lesions drives chronic follicular occlusion, suppurative inflammation, and tissue destruction. Weekly maintenance dosing of Adalimumab significantly reduces inflammatory nodule and abscess counts (HiSCR response).",
            clinical=False
        ),
        q(
            "A 24-year-old female presents with intensely pruritic, monomorphic, flesh-colored to yellowish, dome-shaped follicular papules confined strictly to both axillae, areolae of the breasts, and pubic area, which become much more pruritic during emotional stress and hot weather. What is the diagnosis?",
            "Fox-Fordyce disease (Apocrine miliaria)",
            ["Hidradenitis suppurativa", "Darier disease", "Hailey-Hailey disease"],
            "Fox-Fordyce disease (apocrine miliaria) is a chronic inflammatory disorder occurring almost exclusively in post-pubertal females (aged 13-35 years). It is caused by keratinous plugging of the apocrine duct infundibulum, causing sweat retention, rupture of the intraepidermal duct, and intense spongiotic microvesiculation. Hallmarks: intensely pruritic, monomorphic, dome-shaped follicular papules localized strictly to apocrine-bearing areas (axillae, areolae, umbilicus, pubic region).",
            clinical=True
        ),
        q(
            "What neurochemical mechanism explains why intradermal injections of Botulinum Toxin Type A provide prolonged, profound relief (6 to 9 months) in severe Primary Focal Palmar and Axillary Hyperhidrosis?",
            "Cleaves SNAP-25, blocking presynaptic acetylcholine release at eccrine glands",
            ["Competitive antagonist at postjunctional muscarinic M3 receptors", "Destroys sympathetic chain ganglia through coagulative necrosis", "Blocks apical membrane voltage-gated chloride channels in coils"],
            "Eccrine sweat glands are anatomically innervated by postganglionic sympathetic fibers that are uniquely CHOLINERGIC (releasing acetylcholine, not norepinephrine). Botulinum toxin Type A enters presynaptic nerve endings and enzymatically cleaves SNAP-25 (a core SNARE protein), preventing the docking and fusion of acetylcholine vesicles with the presynaptic membrane, thereby abolishing neuroglandular stimulation and sweat secretion for 6 to 9 months.",
            clinical=False
        ),
    ]),
    (24, "Disorders of Hair", "hard", [
        q(
            "In the normal human hair growth cycle, what are the three sequential physiological phases of a follicular unit, their average durations, and the percentage of scalp hairs normally residing in each phase?",
            "Anagen: 2-6 years (85-90%); Catagen: 2-3 weeks (1-2%); Telogen: 3 months (10-15%)",
            ["Anagen: 1 year (50%); Catagen: 5 years (40%); Telogen: 1 week (10%)", "Anagen: 3 months (90%); Catagen: 6 months (5%); Telogen: 1 year (5%)", "Anagen: 2 weeks (80%); Catagen: 10 years (15%); Telogen: 2 years (5%)"],
            "The hair cycle consists of: 1. Anagen (active growth phase): lasts 2 to 6 years, determines hair length, accounts for 85-90% of scalp hairs; 2. Catagen (transition/regression phase): apoptosis-driven involution of the lower two-thirds of the follicle, lasts 2 to 3 weeks, accounts for 1-2% of hairs; 3. Telogen (resting phase): club hair forms, lasts ~3 months (100 days), accounts for 10-15% of hairs, culminating in exogen (shedding).",
            clinical=False
        ),
        q(
            "A 24-year-old male presents with the sudden appearance of a completely smooth, round, well-circumscribed, non-scarring patch of hair loss on his beard and scalp. Trichoscopic examination at the active advancing border demonstrates short, fractured hairs whose proximal shaft near the scalp is thin and hypopigmented while the distal end is dark and expanded ('exclamation-mark hairs'). What is the diagnosis?",
            "Alopecia areata",
            ["Trichotillomania", "Tinea capitis", "Telogen effluvium"],
            "Alopecia areata is an autoimmune condition caused by collapse of hair follicle immune privilege in the anagen bulb driven by CD8+ NKG2D+ cytotoxic T-lymphocytes. Hallmark: round, smooth, non-scarring bald patches. Pathognomonic dermoscopic/trichoscopic feature at the active perimeter: 'exclamation-mark hairs' (micro-attenuation of the hair shaft near the scalp due to transient inflammation of the matrix, snapping as it emerges).",
            clinical=True
        ),
        q(
            "What clinical pattern of Alopecia Areata is characterized by a wave of band-like hair loss running along the lower posterior occipital and temporal margins of the scalp, and is notoriously refractory to conventional therapy?",
            "Ophiasis pattern alopecia areata",
            ["Alopecia totalis", "Alopecia universalis", "Sisapho pattern"],
            "Ophiasis (derived from the Greek 'ophis' = snake, describing its serpentine distribution) is a distinct clinical variant of alopecia areata where hair loss follows a winding, band-like track along the temporal and lower occipital scalp margins. It is strongly associated with atopic diathesis, carries a poor prognosis for spontaneous regrowth, and is notoriously resistant to standard intralesional corticosteroids and systemic therapy.",
            clinical=False
        ),
        q(
            "What class of targeted small-molecule oral therapeutics (such as Baricitinib and Ritlecitinib) has been approved for severe Alopecia Areata, acting by disrupting the interferon-gamma (IFN-gamma) and interleukin-15 (IL-15) signaling cascades to restore follicular immune privilege?",
            "Janus Kinase (JAK) inhibitors",
            ["Calcineurin inhibitors", "Phosphodiesterase-4 (PDE-4) inhibitors", "IL-17 receptor antagonists"],
            "In alopecia areata, CD8+ T cells secrete IFN-gamma, which signals through the JAK1/JAK2 pathway to induce follicular epithelial cells to secrete IL-15. IL-15 then binds IL-15R on CD8+ T cells (signaling through JAK1/JAK3) to promote cytotoxic granzyme and perforin release. Oral JAK inhibitors (such as Baricitinib, a JAK1/2 inhibitor, and Ritlecitinib, a JAK3/TEC inhibitor) interrupt this feed-forward loop, suppressing follicular inflammation and restoring anagen hair regrowth.",
            clinical=False
        ),
        q(
            "Which validated clinical classification scales are used to grade the progressive severity of Male-Pattern Hair Loss versus Female-Pattern Hair Loss, respectively?",
            "Hamilton-Norwood scale for males; Ludwig scale (or Sinclair scale) for females",
            ["Hunt-Hess scale for males; Glasgow scale for females", "Enneking scale for males; Mankin scale for females", "Risser scale for males; Tanner scale for females"],
            "Androgenetic alopecia severity is graded using standardized morphological scales: 1. Hamilton-Norwood classification for males: grades frontotemporal recession (Types I-III) progressing to vertex thinning (Type IV-V) and confluence leaving only an occipitotemporal rim (Types VI-VII); 2. Ludwig scale for females: evaluates progressive, diffuse centrifugal thinning over the crown and vertex with strict preservation of the frontal hairline (Grades I, II, and III).",
            clinical=False
        ),
        q(
            "What is the precise enzymatic mechanism and hormonal metabolite responsible for driving follicular miniaturization in Androgenetic Alopecia (pattern hair loss)?",
            "Type II 5-alpha reductase converts testosterone to DHT, miniaturizing hairs",
            ["Aromatase converts androstenedione to estradiol, inducing premature teloptosis", "17-beta hydroxysteroid dehydrogenase converts DHEA to cortisol, destroying bulges", "Steroid sulfatase hydrolyzes DHEA-S, triggering lymphocytic follicular scarring"],
            "In androgenetic alopecia, genetically susceptible dermal papillae hair follicles express high levels of the intracellular enzyme Type II 5-alpha reductase. This enzyme converts circulating Testosterone into Dihydrotestosterone (DHT), which has a 5-fold higher binding affinity for the androgen receptor. DHT-receptor complexes alter gene expression, shortening the anagen growth phase from years to months and progressively transforming large, pigmented terminal hairs into microscopic, non-pigmented vellus hairs.",
            clinical=False
        ),
        q(
            "What is the pharmacological mechanism of action of oral Finasteride in the treatment of Male Androgenetic Alopecia, and why is its handling strictly prohibited by women who are pregnant or may become pregnant?",
            "Type II 5-alpha reductase inhibitor; causes male fetal feminization",
            ["Androgen receptor antagonist; induces maternal ventricular arrhythmias", "Lanosterol demethylase inhibitor; induces fatal fetal aplasia cutis", "Dihydrofolate reductase inhibitor; triggers severe maternal megaloblastic anemia"],
            "Finasteride is a synthetic 4-azasteroid that acts as a potent, competitive, selective inhibitor of the Type II 5-alpha reductase isoenzyme, suppressing serum and scalp DHT concentrations by >70%. Because DHT is absolutely essential for the normal differentiation of external male genitalia during fetal organogenesis, pregnant women must never ingest or even handle crushed/broken finasteride tablets due to transdermal absorption risking severe pseudohermaphroditism and hypospadias in a male fetus.",
            clinical=False
        ),
        q(
            "A 28-year-old female presents with acute, diffuse shedding of hair across her entire scalp that began abruptly 10 weeks after a severe bout of high-grade dengue fever and hospitalization. A gentle hair pull test extracts over 15 hairs, all of which exhibit uniform, non-dystrophic, club-shaped bulbs without root sheaths under light microscopy. What is the diagnosis?",
            "Acute telogen effluvium",
            ["Anagen effluvium", "Alopecia areata incognita", "Androgenetic alopecia"],
            "Acute Telogen Effluvium is a non-scarring, diffuse alopecia occurring characteristically 2 to 3 months (the duration of the normal telogen phase) after a major systemic physiological or metabolic insult (high fever, severe infection, major surgery, hemorrhage, childbirth [telogen gravidarum], or crash dieting). The stress prematurely precipitates up to 30-50% of growing anagen hairs into catagen and telogen, resulting in massive, synchronous club hair shedding 100 days later.",
            clinical=True
        ),
        q(
            "A 42-year-old woman undergoing systemic intravenous chemotherapy with Doxorubicin and Cyclophosphamide for breast cancer presents with dramatic, near-complete hair loss that began just 10 days after her first chemotherapy infusion. Microscopic examination of shed hairs reveals fractured, tapered, pencil-point proximal hair shafts. What is the mechanism of this hair loss?",
            "Anagen effluvium; acute mitotic arrest of matrix keratinocytes",
            ["Telogen effluvium; synchronized premature entry into resting telogen", "Alopecia areata; autoimmune CD8+ attack against hair bulb", "Trichotillomania; mechanical fracture of shafts with trichomalacia"],
            "Anagen effluvium is caused by an acute, catastrophic insult to the rapidly dividing keratinocytes in the anagen hair bulb (matrix cells, which have the highest mitotic rate in the human body). Cytotoxic chemotherapy or ionizing radiation abruptly halts DNA synthesis and mitosis: the hair shaft thins acutely, narrows, and fractures inside the follicular canal or at the skin surface within 1 to 2 weeks of exposure. The hair roots show characteristic tapered, pencil-point, dysplastic proximal ends.",
            clinical=True
        ),
        q(
            "An 11-year-old girl is brought by her parents with an irregular, bizarre-shaped, asymmetrical patch of hair loss on her right frontoparietal scalp. Trichoscopy demonstrates hairs fractured at varying, uneven lengths from the scalp surface, coiled/corkscrew hairs, broom hairs, and black dots, with completely healthy, non-inflamed underlying scalp skin. What is the diagnosis?",
            "Trichotillomania",
            ["Alopecia areata", "Tinea capitis", "Traction alopecia"],
            "Trichotillomania is an obsessive-compulsive related disorder characterized by repetitive, compulsive manual pulling of one's own hair. Clinical hallmarks: irregular, geometric, bizarrely contoured patches of incomplete baldness (usually on the side of the dominant hand); hairs are broken at varying lengths; exclamation-mark hairs are absent; the scalp skin is normal and non-scarred. Trichoscopy shows fractured shafts, trichoptilosis (split ends), flame hairs, and coiled hair remnants.",
            clinical=True
        ),
    ]),
    (25, "Disorders of Nail", "easy", [
        q(
            "Which clinical presentation of onychomycosis is recognized as a specific, highly sensitive clinical cutaneous marker of severe immunosuppression and advanced HIV infection?",
            "Proximal Subungual Onychomycosis (PSO)",
            ["Distal and Lateral Subungual Onychomycosis (DLSO)", "Superficial White Onychomycosis (SWO)", "Total Dystrophic Onychomycosis (TDO)"],
            "While Distal and Lateral Subungual Onychomycosis (DLSO) is by far the most common pattern in immunocompetent hosts, Proximal Subungual Onychomycosis (PSO)—where the fungus penetrates directly into the proximal nail fold and invades the newly formed nail plate from the matrix—is exceedingly rare in healthy individuals. It is considered an important clinical cutaneous hallmark of advanced HIV/AIDS (CD4 count <200 cells/mcL) and profound immunosuppression.",
            clinical=False
        ),
        q(
            "A 35-year-old male presents with transverse, horizontal, band-like depressions running across all twenty nail plates at exactly the same distance from the proximal nail fold. History reveals he suffered a life-threatening episode of septic shock requiring intensive care 3 months ago. What are these diagnostic grooves termed?",
            "Beau lines",
            ["Muehrcke lines", "Mees lines", "Lindsay nails"],
            "Beau's lines are transverse, horizontal linear depressions traversing the entire width of the nail plate. They reflect a temporary, acute, reversible arrest of mitotic division in the proximal nail matrix caused by severe systemic physiological stress (high fever, sepsis, myocardial infarction, chemotherapy). Because normal fingernails grow at ~3 mm/month (0.1 mm/day), the exact distance of the groove from the cuticle allows dating of the antecedent illness.",
            clinical=True
        ),
        q(
            "A 28-year-old female presents with severe fatigue, pallor, and spoon-shaped fingernails characterized by central concavity and everted, upturned lateral and distal edges capable of holding a drop of water without spilling ('koilonychia'). What is the most common underlying hematological etiology?",
            "Severe chronic iron deficiency anemia (with or without Plummer-Vinson syndrome)",
            ["Beta-thalassemia minor", "Aplastic anemia", "Vitamin B12 deficiency"],
            "Koilonychia (spoon nails) is an abnormal nail plate dystrophy where the normal convex curvature is inverted, forming a saucer-like or spoon-like central depression. The classic physical examination test is the 'water-drop test' (a drop of water placed on the nail plate remains pooled without rolling off). Severe, chronic iron deficiency anemia is by far the most frequent systemic cause (also seen in hemochromatosis and Plummer-Vinson syndrome).",
            clinical=True
        ),
        q(
            "An 8-year-old boy presents with uniform, severe dystrophic changes affecting all twenty fingernails and toenails. Every nail plate appears dull, opaque, lusterless, fragile, and marked by excessive fine longitudinal striations and superficial scaling, giving a rough 'sandpaper' texture. What is this entity termed, and with which three dermatoses is it classically associated?",
            "Trachyonychia (Twenty-Nail Dystrophy); Alopecia areata, Lichen planus, and Psoriasis",
            ["Onychogryphosis; Syphilis, Scabies, and Leprosy", "Pachyonychia congenita; Epidermolysis bullosa, Darier disease, and Hailey-Hailey disease", "Koilonychia; Scurvy, Rickets, and Beriberi"],
            "Trachyonychia (Twenty-Nail Dystrophy / sandpaper nails) is a benign inflammatory matrix dystrophy affecting children and young adults. All 20 nails (or a subset) become uniformly rough, dull, grayish, brittle, and covered by prominent longitudinal ridging likened to rough sandpaper. Nail matrix biopsy reveals that trachyonychia is not a distinct disease, but an idiopathic phenotypic expression of Lichen Planus (spongiotic or lichenoid matrix inflammation), Alopecia Areata, or Psoriasis.",
            clinical=True
        ),
        q(
            "What classic clinical triad defines Yellow Nail Syndrome, a rare systemic disorder characterized by complete cessation of nail plate growth?",
            "Yellow nails, primary lymphedema, and chronic respiratory disease",
            ["Yellow nails, chronic renal failure, and hepatosplenomegaly", "Yellow nails, sensory peripheral neuropathy, and corneal opacities", "Yellow nails, multiple endocrine neoplasia, and cutaneous neurofibromas"],
            "Yellow Nail Syndrome is a rare clinical entity defined by the classic triad of: 1. Characteristic nail changes: nail growth slows to <0.1 mm/week, nails become thickened, pale yellow-to-green, excessively curved transversely, with loss of the lunula and cuticle; 2. Chronic lymphedema (present in 80%, typically bilateral lower limbs); 3. Chronic respiratory tract manifestations (exudative pleural effusions, bronchiectasis, chronic sinusitis). The underlying defect is congenital or acquired lymphatic microangiopathy.",
            clinical=False
        ),
    ]),
]
