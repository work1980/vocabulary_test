import streamlit as st
import random
import json
import os

# Load vocabulary from JSON file
with open('1-初中-顺序.json', 'r') as file:
    vocabulary = json.load(file)

# Temp files to store score and incorrect answers
score_file = 'score.txt'
wrong_answers_file = 'wrong_answers.txt'

# Initialize or load the score
if 'score' not in st.session_state:
    st.session_state['score'] = 0

# Initialize or load the total number of questions
if 'total_questions' not in st.session_state:
    st.session_state['total_questions'] = 0

# Initialize or load the current question and options
if 'current_question' not in st.session_state:
    st.session_state['current_question'], st.session_state['correct_answer'], st.session_state['options'] = None, None, None

# Function to get a random word and options
def get_question():
    word_entry = random.choice(vocabulary)
    word = word_entry['word']
    correct_translation = word_entry['translations'][0]['translation']
    
    # Generate wrong choices
    wrong_choices = random.sample([entry['translations'][0]['translation'] for entry in vocabulary if entry['word'] != word], 3)
    options = wrong_choices + [correct_translation]
    random.shuffle(options)
    
    return word, correct_translation, options

# Function to save the score
def save_score():
    with open(score_file, 'w') as f:
        f.write(str(st.session_state['score']))

# Function to save wrong answers
def save_wrong_answer(word, correct_translation):
    with open(wrong_answers_file, 'a') as f:
        f.write(f"{word} - Correct: {correct_translation}\n")

# Load a new question if not already loaded
if st.session_state['current_question'] is None:
    st.session_state['current_question'], st.session_state['correct_answer'], st.session_state['options'] = get_question()

# Streamlit app
st.title('初中英语单词测验3200词汇版')

# Show the current word and options
st.write(f"选择正确的中文翻译: **{st.session_state['current_question']}**?")

# Checkbox list for options
selected_option = None
checkboxes = []
for option in st.session_state['options']:
    checkboxes.append(st.checkbox(option, key=option))

# Ensure only one checkbox is selected
if sum([1 for cb in checkboxes if cb]) > 1:
    st.error("Please select only one option.")
else:
    for i, option in enumerate(st.session_state['options']):
        if checkboxes[i]:
            selected_option = option

# Submit button
if st.button('Submit'):
    if not selected_option:
        st.error("Please select an option before submitting.")
    else:
        st.session_state['total_questions'] += 1
        if selected_option == st.session_state['correct_answer']:
            st.success("Correct!")
            st.session_state['score'] += 1
        else:
            st.error(f"Wrong! The correct translation was: {st.session_state['correct_answer']}")
            save_wrong_answer(st.session_state['current_question'], st.session_state['correct_answer'])
        
        # Save score
        save_score()

        # Load the next question
        st.session_state['current_question'], st.session_state['correct_answer'], st.session_state['options'] = get_question()

        # Rerun the app to refresh the question and options
        #st.experimental_rerun()
        st.rerun()

# Calculate the score percentage
if st.session_state['total_questions'] > 0:
    score_percentage = (st.session_state['score'] / st.session_state['total_questions']) * 100
    score_display = f"Your score: {score_percentage:.2f}%"
else:
    score_display = "Your score: 0.00%"

# Display the score with larger, red font
st.markdown(f"<h1 style='color: red;'>{score_display}</h1>", unsafe_allow_html=True)

# Display current score and total questions
st.write(f"Correct answers: {st.session_state['score']} out of {st.session_state['total_questions']}")

# Allow user to review wrong answers
if os.path.exists(wrong_answers_file):
    st.write("Review your incorrect answers:")
    with open(wrong_answers_file, 'r') as f:
        wrong_answers = f.read()
    st.text(wrong_answers)

# Clear wrong answers
if st.button('Clear wrong answers'):
    open(wrong_answers_file, 'w').close()
    st.write("Wrong answers cleared.")

# Reset score and total questions
if st.button('Reset Score'):
    st.session_state['score'] = 0
    st.session_state['total_questions'] = 0
    save_score()
    st.write("Score reset.")
