from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is my new Django app!")

def quiz_view(request):
    # Define questions and answers as a dictionary
    questions = [
        {"text": "When does the University aim to be net zero?", "answer": "2030"},
        {"text": "What system does the University use to integrate sustainability (acronym)?", "answer": "EMS"},
        {"text": "What kind of emergency did the University declare in 2019?", "answer": "Climate"},
        {"text": "What is the name of Exeter's sustainability goal for the long-term?", "answer": "Strategy2030"},
        {"text": "Which Exeter campus leads sustainability?", "answer": "Penryn"},
        {"text": "How many UN Sustainability Development Goals are there?", "answer": "17"},
        {"text": "What is Exeter Univerisities biodiversity action plan called?", "answer": "Nature"},
        
    ]
    
    if request.method == 'POST':
        correct_answers = 0
        total_questions = len(questions)

        # Check the user's answers
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            if user_answer and user_answer.strip().lower() == question["answer"].lower():
                correct_answers += 1

        return render(request, 'game1/quiz_result.html', {
            'correct_answers': correct_answers,
            'total_questions': total_questions,
        })

    return render(request, 'game1/quiz.html', {'questions': questions})
