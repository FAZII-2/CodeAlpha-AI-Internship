import numpy as np


def sample_with_temperature(predictions, temperature=1.0):

    temperature = max(temperature, 1e-8)

    predictions = np.asarray(predictions).astype("float64")
    log_preds = np.log(predictions + 1e-8)
    scaled = log_preds / temperature
    exp_preds = np.exp(scaled)
    final_preds = exp_preds / np.sum(exp_preds)


    choices = range(len(predictions))
    chosen_index = np.random.choice(choices, p=final_preds)

    return chosen_index


def generate_notes(music_model, seed_sequence, num_notes=200, temperature=1.0):
   
    sequence_length = music_model.sequence_length
    vocab_size = music_model.vocab_size

    
    pattern = list(seed_sequence)
    generated = []

    for _ in range(num_notes):
        
        input_seq = pattern[-sequence_length:]
        input_array = np.reshape(input_seq, (1, sequence_length, 1))
        input_array = input_array / float(vocab_size)

        prediction = music_model.model.predict(input_array, verbose=0)[0]

        next_index = sample_with_temperature(prediction, temperature)

        pattern.append(next_index)
        generated.append(next_index)

    
    generated_tokens = [music_model.int_to_note[idx] for idx in generated]

    return generated_tokens