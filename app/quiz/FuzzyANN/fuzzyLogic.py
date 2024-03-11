import numpy as np
import pandas as pd
import skfuzzy as fuzz


# Function to preprocess user responses using fuzzy logic
def preprocess_responses(user_answers):
    # Define the scale for user responses
    scale = np.arange(1, 8)

    # Define membership functions for each choice in the scale
    membership_functions = []
    for choice in scale:
        membership_functions.append(fuzz.trimf(scale, [choice - 1, choice, choice + 1]))

    # Fuzzify user responses
    fuzzy_responses = []
    for response in user_answers:
        membership_degrees = [fuzz.interp_membership(scale, mf, response) for mf in membership_functions]
        fuzzy_responses.append(membership_degrees)

    # Reshape Dataframe
    fuzzy_responses = np.array(fuzzy_responses).reshape(-1, 4)

    # Convert the results to a DataFrame for easier handling
    df = pd.DataFrame(fuzzy_responses, columns=['I/E', 'S/I', 'T/F', 'J/P'])

    return df


# Example usage
if __name__ == "__main__":
    user_responses = np.random.randint(1, 8, size=(100, 100))  # Example user responses
    preprocessed_data = preprocess_responses(user_responses)
    print(preprocessed_data.shape)  # Displaying preprocessed data
