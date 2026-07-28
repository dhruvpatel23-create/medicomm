import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]

CLINICAL_PROMPTS = {
    "physiology-nerve-muscle-nerve-04": "After a peripheral nerve is cut during trauma, the neuron shows chromatolysis of Nissl bodies. Which event is most directly responsible for this change?",
    "physiology-nerve-muscle-nerve-07": "A child with a contaminated wound develops tetanus after toxin travels from the wound toward the spinal cord. Which neuronal transport mechanism explains this spread?",
    "physiology-nerve-muscle-nerve-10": "A nerve fibre receives a weak stimulus that causes small local depolarization but no propagated impulse. Propagation begins only when the membrane reaches about:",
    "physiology-nerve-muscle-neuromuscular-junction-07": "A patient has fluctuating skeletal muscle weakness due to impaired postsynaptic transmission at the motor end plate. Which site is primarily affected?",
    "physiology-nerve-muscle-neuromuscular-junction-08": "A toxin blocks acetylcholine release from motor nerve terminals. What immediate functional effect is expected in skeletal muscle?",
    "physiology-nerve-muscle-neuromuscular-junction-10": "A patient receives a drug that inhibits acetylcholinesterase at the neuromuscular junction. Which effect is expected at the end plate?",
    "physiology-nerve-muscle-skeletal-muscle-07": "A man holds a heavy suitcase steady without visible shortening of the biceps. Which type of muscle contraction is occurring?",
    "physiology-nerve-muscle-skeletal-muscle-08": "During lifting of a dumbbell, the biceps shortens while moving the load. Which type of contraction is this?",
    "physiology-nerve-muscle-skeletal-muscle-09": "A patient with suspected myopathy is evaluated by recording electrical activity from skeletal muscle. Which investigation is being used?",
    "physiology-nerve-muscle-smooth-muscle-07": "A strip of intestinal smooth muscle shows rhythmic slow waves that trigger periodic contractions. These slow waves are produced by:",
    "physiology-nerve-muscle-smooth-muscle-09": "Autonomic fibres supplying visceral smooth muscle do not end as motor end plates; instead transmitter is released from bead-like swellings. These swellings are:",
    "physiology-nerve-muscle-smooth-muscle-10": "A bright light stimulates constriction of the pupil through smooth muscle that behaves as separate motor units. This is an example of smooth muscle responding mainly to:",
    "physiology-nerve-muscle-cardiac-muscle-05": "Sustained fused contraction would prevent ventricular filling. Which property of cardiac muscle prevents tetanus?",
    "physiology-nerve-muscle-cardiac-muscle-07": "A fall in extracellular calcium reduces myocardial contractile force. This reflects that cardiac excitation-contraction coupling is partly dependent on:",
    "physiology-nerve-muscle-cardiac-muscle-10": "A physiology teacher explains why the heart relaxes between beats instead of remaining in sustained contraction. Which principle best explains this?",
    "physiology-blood-immune-plasma-proteins-04": "A patient with nephrotic-range protein loss develops pedal edema. Loss of which plasma protein function best explains the edema?",
    "physiology-blood-immune-plasma-proteins-08": "A patient with unconjugated hyperbilirubinemia needs plasma transport of bilirubin to the liver. Which plasma protein performs this carrier function?",
    "physiology-blood-immune-plasma-proteins-09": "A patient with advanced liver failure develops edema and prolonged bleeding. Which combined plasma protein defect best explains these findings?",
    "physiology-blood-immune-red-cells-anaemias-04": "A patient with chronic inflammatory disease has a high ESR on testing. What does this finding most commonly indicate?",
    "physiology-blood-immune-red-cells-anaemias-06": "A strict vegetarian develops macrocytic anaemia with defective nuclear maturation. Deficiency of which maturation factors commonly causes this pattern?",
    "physiology-blood-immune-red-cells-anaemias-07": "A woman with chronic blood loss has microcytic hypochromic red cells on smear. Which anaemia does this suggest?",
    "physiology-blood-immune-white-blood-cells-02": "A patient with acute bacterial pneumonia shows marked neutrophilia. Which leukocyte is most important for acute bacterial phagocytosis?",
    "physiology-blood-immune-white-blood-cells-03": "A child with helminthic infestation has eosinophilia on differential count. Which leukocyte commonly rises in parasitic and allergic conditions?",
    "physiology-blood-immune-white-blood-cells-09": "A patient receiving chemotherapy develops recurrent infections with a very low neutrophil count. What is this abnormality called?",
    "physiology-blood-immune-immune-mechanisms-04": "A child receives a vaccine and later produces his own antibodies and memory cells. What type of immunity has developed?",
    "physiology-blood-immune-immune-mechanisms-05": "A newborn is protected for the first months of life by antibodies received from the mother. Which type of immunity is this?",
    "physiology-blood-immune-immune-mechanisms-10": "Before renal transplantation, donor and recipient tissues are matched to reduce graft rejection. Which test/concept is most relevant?",
    "physiology-blood-immune-platelets-haemostasis-06": "A patient with obstructive jaundice develops bleeding due to impaired absorption of a fat-soluble vitamin required for clotting factor synthesis. Which vitamin is involved?",
    "physiology-blood-immune-platelets-haemostasis-07": "A boy has recurrent hemarthroses and factor VIII deficiency. Which bleeding disorder is this?",
    "physiology-blood-immune-platelets-haemostasis-10": "A patient has petechiae, mucosal bleeding and a low platelet count with prolonged bleeding time. Which category of disorder best explains this?",
    "physiology-blood-immune-blood-groups-transfusion-07": "An Rh-negative mother carrying an Rh-positive fetus is at risk of erythroblastosis fetalis in a later pregnancy. What is the usual incompatibility setting?",
    "physiology-blood-immune-blood-groups-transfusion-08": "An Rh-negative mother delivers an Rh-positive baby. Which prophylaxis prevents sensitization and future haemolytic disease of the newborn?",
    "physiology-blood-immune-blood-groups-transfusion-10": "Soon after an incompatible transfusion, a patient develops fever, chills, haemolysis and shock. This is best classified as:",
}


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    changed = 0
    for question in data.get("questions", []):
        prompt = CLINICAL_PROMPTS.get(question.get("id"))
        if not prompt:
            continue
        question["prompt"] = prompt
        tags = set(question.get("tags", []))
        tags.add("clinical")
        question["tags"] = sorted(tags)
        changed += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Clinicalized {changed} questions in {path}.")


def main():
    for path in DATA_PATHS:
        update(path)


if __name__ == "__main__":
    main()
