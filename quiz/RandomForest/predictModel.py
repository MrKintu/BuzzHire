import logging
import pickle

import pandas as pd
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger(__name__)


def PredictPersona(user_responses):
    # Create data set from User Responses and Preprocess Data
    questions = []
    answers = []
    for response in user_responses:
        question = response.question.text
        questions.append(question)

        answer = response.response
        answers.append(answer)

    label_encoder = LabelEncoder()
    data_set = pd.DataFrame()
    questions = label_encoder.fit_transform(questions)
    data_set["Question"] = questions
    data_set["Answer"] = answers

    # Make predictions
    random_forest_path = '/srv/www/BuzzHire/quiz/RandomForest/random_forest.pkl'
    with open(random_forest_path, 'rb') as file:
        rf_model = pickle.load(file)
    predictions = rf_model.predict(data_set)

    # Log Model Predictions
    logger.info("Random Forest Model Evaluation.")
    logger.info(f'{predictions}')

    flat_list = predictions.flatten().tolist()
    I_count = (flat_list.count("Introversion") / len(flat_list)) * 100
    E_count = (flat_list.count("Extroversion") / len(flat_list)) * 100
    S_count = (flat_list.count("Sensing") / len(flat_list)) * 100
    N_count = (flat_list.count("Intuition") / len(flat_list)) * 100
    T_count = (flat_list.count("Thinking") / len(flat_list)) * 100
    F_count = (flat_list.count("Feeling") / len(flat_list)) * 100
    J_count = (flat_list.count("Judging") / len(flat_list)) * 100
    P_count = (flat_list.count("Perceiving") / len(flat_list)) * 100

    persona_list = []
    if I_count > E_count:
        persona_list.append('I')
    else:
        persona_list.append('E')
    if S_count > N_count:
        persona_list.append('S')
    else:
        persona_list.append('N')
    if T_count > F_count:
        persona_list.append('T')
    else:
        persona_list.append('F')
    if J_count > P_count:
        persona_list.append('J')
    else:
        persona_list.append('P')

    persona = "".join(persona_list)

    send = {
        "introversion": I_count,
        "extroversion": E_count,
        "sensing": S_count,
        "intuition": N_count,
        "thinking": T_count,
        "feeling": F_count,
        "judging": J_count,
        "perceiving": P_count,
        "persona": persona
    }

    return send
