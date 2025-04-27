import streamlit as st

# OOP Classes
class Question:
    def __init__(self, question_text: str, options: list[str], correct_answer: str):
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
    
    def is_correct(self, user_answer: str) -> bool:
        return user_answer == self.correct_answer

class Quiz:
    def __init__(self):
        self.questions: list[Question] = []
        
    def add_question(self, question: Question):
        self.questions.append(question)
    
    def display_questions(self):
        answers = []
        for idx, question in enumerate(self.questions, 1):
            st.subheader(f"Question {idx}")
            user_answer = st.radio(question.question_text, question.options, key=f"quiz_{idx}")
            answers.append(user_answer)
        return answers
    
    def calculate_score(self, answers):
        score = 0
        for question, answer in zip(self.questions, answers):
            if question.is_correct(answer):
                score += 1
        return score, len(self.questions)

# Streamlit App
def main():
    st.title("📝 Customizable Quiz Creator")
    
    # Initialize session state variables if they don't exist
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'quiz' not in st.session_state:
        st.session_state.quiz = Quiz()
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    
    # Create quiz in sidebar
    st.sidebar.title("Create Your Quiz")
    quiz = st.session_state.quiz
    
    if not st.session_state.quiz_started:
        num_questions = st.sidebar.number_input("How many questions?", min_value=1, max_value=10, value=3)
        
        # Clear existing questions when changing number of questions
        if len(quiz.questions) != num_questions:
            quiz.questions = []
        
        for i in range(1, num_questions + 1):
            st.sidebar.markdown(f"### Question {i}")
            q_text = st.sidebar.text_input(f"Enter question {i}", key=f"q_text_{i}")
            options = []
            for j in range(1, 5):
                option = st.sidebar.text_input(f"Option {j} for question {i}", key=f"q_{i}_opt_{j}")
                options.append(option)
            
            if all(options):  # Only show correct answer selector if all options have text
                correct = st.sidebar.selectbox(f"Correct answer for question {i}", options, key=f"q_{i}_correct")
                
                # Update existing question or add new one
                if i <= len(quiz.questions):
                    quiz.questions[i-1] = Question(q_text, options, correct)
                elif q_text:
                    quiz.add_question(Question(q_text, options, correct))
        
        if st.button("Start Quiz"):
            if len(quiz.questions) > 0 and all(q.question_text for q in quiz.questions):
                st.session_state.quiz_started = True
            else:
                st.warning("Please create at least one full question first!")
    
    # Display the quiz
    if st.session_state.quiz_started and not st.session_state.quiz_submitted:
        st.session_state.user_answers = quiz.display_questions()
        
        if st.button("Submit Quiz"):
            st.session_state.quiz_submitted = True
    
    # Show results after submission
    if st.session_state.quiz_submitted:
        score, total = quiz.calculate_score(st.session_state.user_answers)
        st.success(f"You scored {score} out of {total}!")
        
        if st.button("Create New Quiz"):
            st.session_state.quiz_started = False
            st.session_state.quiz_submitted = False
            st.session_state.quiz = Quiz()
            st.session_state.user_answers = []
            st.rerun()

if __name__ == "__main__":
    main()