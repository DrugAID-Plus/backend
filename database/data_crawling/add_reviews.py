import json
import numpy as np
from numpy.random import choice
from glob import glob
import time


def random_verification():
    return bool(choice(np.arange(0, 2), p=[0.7, 0.3]) > 0)


# get extracted data
with open('./demo_classification.json') as f:
    extracted_data = json.load(f)


with open('./webmd_and_drugbank.json') as g:
    webmd_and_drugbank_data = json.load(g)

final_data = []
needed_webmd_data = []
drug_names = []
for review in extracted_data:
    for value in webmd_and_drugbank_data:
        if review['drug'].lower() == value['name'].lower() and value['name'] not in drug_names:
            drug_names.append(value['name'])
            needed_webmd_data.append(value)

print('A total of {0} drugs were found'.format(len(needed_webmd_data)))
time.sleep(5)
final_data = []
for value in needed_webmd_data:
    value['side_effects'] = {
        'common_side_effects': [],
        'count': {
            'total': 0
        },
        'reported_effects': {
            'hepatic': {'definition': "Hepatic is the term that shows relation to the liver and liver system. Typically ‘hepatic’ is used in terms of having trouble with the liver, specifically liver failure. Hepatic, or liver, failure is commonly caused by negative reactions of medicines, infections, and alcohol abuse. Common side effects include yellow skin, yellow eyes (jaundice), stomach ache/pain, swelling in the stomach, swelling in the legs and ankles (edema), dark urine, and chronic fatigue.", 'side_effects': []},
            'gastrointestinal': {'definition': "The gastrointestinal tract is an organ system within humans and other animals which takes in food, digests it to extract and absorb energy and nutrients, and expels the remaining waste as feces, including the organs such as the stomach, intestines, and kidneys. The mouth, esophagus, stomach, and intestines are part of the gastrointestinal tract. Common gastrointestinal side effects include constipation, diarrhea, flatulence, gas, burping, indigestion, nausea, vomiting, bowel and stomach aches, pains and cramps. This also includes heartburn and problems with the kidneys.", 'side_effects': []},
            'hypersensitivity': {'definition': "Hypersensitivity is a condition in which the immune system reacts abnormally to a foreign substance. Common examples of hypersensitivity include allergic reactions, anaphylaxis, asthma, and dermatitis.", 'side_effects': []},
            'hematologic': {'definition': "Hematologic side effects deal with diseases that affect the bloodstream. Common drug side effects that are hematologic include anemia(including side effects of cold hands and feet), neutropenia, hypoglycemia, hemolytic and aplastic anemia and other common effects like decreased hemoglobin levels or disseminated intravascular coagulation, bleeding, and or blood clotting.", 'side_effects': []},
            'dermatologic': {'definition': "Dermatology is the branch of medicine dealing with the skin, nails, hair and its diseases. Common dermatologic side effects include skin rashes, itchiness, necrosis, contact dermatitis, acne, moles and other inflammations related to the skin. Dry skin and skin breakdown are other potential drug side effects.", 'side_effects': []},
            'respiratory': {'definition': "Respiratory is relating to or affecting respiration or the organs of respiration, specifically the lungs. Symptoms relating to upper and overall respiratory functions include congestions, runny nose, sneezing, sore or scratchy throat, wheezing, cough, loud breathing, chest pain, chronic mucus, and coughing up blood. This can include respiratory infections, asthma, severe sweating, thirstiness, COPD, influenza, pneumonia, tuberculosis, and bronchitis.", 'side_effects': []},
            'cardiovascular': {'definition': "Cardiovascular relates to the circulatory system, which comprises the heart and blood vessels and carries nutrients and oxygen to the tissues of the body and removes carbon dioxide and other wastes from them. Common side effects include congestive heart failure, cardiac arrest, slow heartbeat, racing heartbeat, fainting, angina(chest pain), or dizziness, high blood pressure and or heart failure. Other examples include angina, atrial fibrillation and heartburn. Stroke is also prominent, congenital heart disease, arrhythmia, and peripheral artery disease.", 'side_effects': []},
            'ocular': {'definition': "Ocular diseases is related to any problems or effects on vision / eyesight and the eye. Common side effects include blurred vision, eye pain and soreness, eye redness, light sensitivity, eye twitching, eye floaters, seeing spots, eye infections, eye gunk, and eye freckles. Other examples include eye strain, eyesight changes, night blindness, keratoconus, lack of Vitamin A, conjunctivitis or pinkeye, nearsightedness, cataracts. Worse conditions include color blindness, crossed eyes, bulging eyes and glaucoma.", 'side_effects': []},
            'psychiatric': {'definition': "Psychiatric problems are relating to any conflicts of mental illnesses and its treatments. Common psychiatric and mental disorders include autism, attention deficit - hyperactivity disorder(ADHD), bipolar disorder, drowsiness, tired, exhaustion, paranoia, depressions, and schizophrenia. It can also include anxiety, dementia, obsessive compulsive disorder(OCD), and post - traumatic stress disorder, impaired concentration, confusion, insomnia, and abnormal thinkings. All of these have symptoms that include headaches and migraines, persistent feelings of sadness or lack of emotions, decrease in appetite, mood swings, dramatic and strong urges, nervousness and feeling panicked, feeling scared and frightened, inability to focus, lack of communication and social skills, inability to calm down, troubles sleeping, and significant tiredness and low energy.", 'side_effects': []},
            'nervous-system': {'definition': "The nervous system is the part of an animal that coordinates its actions by transmitting signals to and from different parts of its body. The nervous system detects environmental changes that impact the body, then works in tandem with the endocrine system to respond to such events. Common nervous system side effects include convulsions or seizures, cerebral hemorrhage and other hemorrhage types, irritability, restlessness, jitteriness, tremors and brain injury. Other nervous system - based results include metabolic diseases like hyperglycemia, acidosis, metallic taste, temporary weight gain or weight loss, and decreased thyroxine. Other common side effects include neurotoxicity, ataxia, sclerosis.", 'side_effects': []},
            'other': {'definition': 'All adverse drug events that cannot be classified into the 10 classes.', 'side_effects': []}
        }
    }

    value['search_name'] = '-'.join([word.lower()
                                     for word in value['name'].split()])
    for review in extracted_data:
        if review['drug'].lower() == value['name'].lower():
            review['doctor_verified'] = random_verification()
            review['official_verified'] = random_verification()
            if review['classification'][0].lower() == 'nervous system':
                value['side_effects']['reported_effects']['nervous-system']['side_effects'].append(
                    review)
            else:
                value['side_effects']['reported_effects'][review['classification']
                                                          [0].lower()]['side_effects'].append(review)
            value['side_effects']['count']['total'] += 1

    final_data.append(value)


with open('demo_drug_data-fixed.json', 'w') as f:
    json.dump(final_data, f, indent=4)
