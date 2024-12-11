import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import openai

# Configurar a chave da API
openai.api_key = "CHAVE_API"

# Definição dos ciclos
cycles = {
    "Hard Fun": ["Frustração", "Fiero", "Alívio"],
    "Easy Fun": ["Curiosidade", "Surpresa", "Maravilhamento", "Reverência"],
    "Serious Fun": ["Relaxamento", "Foco Zen", "Empolgação"],
    "People Fun": ["Admiração", "Amiero", "Diversão", "Amici"]
}

# Variável para armazenar o progresso do ciclo
last_feedback_stage = {ptype: 0 for ptype in cycles.keys()}  # Armazena o índice da etapa atual

# Perguntas do quiz
questions = [
    {
        "question": "Qual é a capital da França?",
        "options": ["Paris", "Londres", "Berlim", "Madrid"],
        "correct": "Paris"
    },
    {
        "question": "Quem pintou a Mona Lisa?",
        "options": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"],
        "correct": "Leonardo da Vinci"
    },

     {
        "question": "Qual é o maior planeta do Sistema Solar?",
        "options": ["Terra", "Júpiter", "Saturno", "Marte"],
        "correct": "Júpiter"
    },
    {
        "question": "Quem pintou a Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"],
        "correct": "Leonardo da Vinci"
    },
    {
        "question": "Qual é o elemento químico representado pelo símbolo 'O'?",
        "options": ["Oxigênio", "Ouro", "Ozônio", "Osmio"],
        "correct": "Oxigênio"
    },
    {
        "question": "Qual país é conhecido como a Terra do Sol Nascente?",
        "options": ["China", "Japão", "Coreia do Sul", "Tailândia"],
        "correct": "Japão"
    },
    {
        "question": "Quantos continentes existem no mundo?",
        "options": ["5", "6", "7", "8"],
        "correct": "7"
    },
    {
        "question": "Quem foi o primeiro homem a pisar na Lua?",
        "options": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"],
        "correct": "Neil Armstrong"
    },
    {
        "question": "Qual é o rio mais longo do mundo?",
        "options": ["Rio Nilo", "Rio Amazonas", "Rio Yangtze", "Rio Mississippi"],
        "correct": "Rio Amazonas"
    },
    {
        "question": "Qual é a moeda oficial do Reino Unido?",
        "options": ["Euro", "Libra Esterlina", "Dólar", "Franco"],
        "correct": "Libra Esterlina"
    },
    {
        "question": "Quem escreveu 'Dom Quixote'?",
        "options": ["Miguel de Cervantes", "William Shakespeare", "Dante Alighieri", "Victor Hugo"],
        "correct": "Miguel de Cervantes"
    },
    {
        "question": "Qual é o símbolo químico do ouro?",
        "options": ["Au", "Ag", "Fe", "Cu"],
        "correct": "Au"
    }
]

# Função para determinar a próxima etapa no ciclo
def get_next_stage(player_type):
    current_index = last_feedback_stage[player_type]
    cycle = cycles[player_type]
    next_stage = cycle[current_index]
    last_feedback_stage[player_type] = (current_index + 1) % len(cycle)  # Atualiza para o próximo estágio
    return next_stage

# Função que utiliza a API para gerar feedbacks
def get_feedback(player_type, question, user_answer, correct):
    next_stage = get_next_stage(player_type)  # Determina a próxima emoção no ciclo

    prefix = {
        "Frustração": "Droga!", "Fiero": "Yes!", "Alívio": "Ufa!",
        "Curiosidade": "Hmm…", "Surpresa": "Uau!", "Maravilhamento": "Incrível!", "Reverência": "Uau que impressionante!",
        "Relaxamento": "Ahhh…", "Foco Zen": "Ok, vamos lá.", "Empolgação": "Bora!",
        "Admiração": "Que show!", "Amiero": "Aí sim!", "Diversão": "Haha!", "Amici": "Tamo junto!"
    }[next_stage]

    feedback_type = "certa" if correct else "errada"
    prompt = f"O jogador do tipo {player_type} respondeu a pergunta: '{question}' e a resposta foi {feedback_type}. Dê um feedback apropriado baseado na emoção '{next_stage}' do ciclo: {cycles[player_type]}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um gerador de feedback para diferentes tipos de jogadores."},
            {"role": "user", "content": prompt}
        ]
    )
    feedback_message = response.choices[0].message['content']
    return f"{next_stage}: {prefix} {feedback_message}"  # Adiciona o nome da emoção antes do feedback

# Classe principal do aplicativo
class QuizApp(App):
    def build(self):
        Window.size = (400, 600)  # Ajustar tamanho da janela
        self.current_question = 0
        self.player_type = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.question_label = Label(text="Escolha seu tipo de jogador:", font_size=28, size_hint=(1, 0.2))
        self.layout.add_widget(self.question_label)
        self.add_player_type_buttons()

        return self.layout

    def add_player_type_buttons(self):
        player_types = cycles.keys()
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), spacing=20)
        for ptype in player_types:
            btn = Button(text=ptype, size_hint_y=None, height=70, font_size=24)
            btn.bind(on_release=self.select_player_type)
            button_layout.add_widget(btn)
        self.layout.add_widget(button_layout)

    def select_player_type(self, instance):
        self.player_type = instance.text
        self.layout.clear_widgets()
        self.show_question()

    def show_question(self):
        question = questions[self.current_question]
        self.question_label.text = question['question']
        self.layout.add_widget(self.question_label)

        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), spacing=20)
        for option in question['options']:
            btn = Button(text=option, size_hint_y=None, height=70, font_size=24)
            btn.bind(on_release=self.check_answer)
            button_layout.add_widget(btn)
        self.layout.add_widget(button_layout)

    def check_answer(self, instance):
        question = questions[self.current_question]
        user_answer = instance.text
        correct = user_answer == question['correct']
        feedback = get_feedback(self.player_type, question['question'], user_answer, correct)

        feedback_popup = Popup(title='Resultado', size_hint=(None, None), size=(400, 600))
        scroll = ScrollView(size_hint=(1, 1))
        feedback_label = Label(text=feedback, halign="center", valign="middle", text_size=(380, None), size_hint_y=None, font_size=20)
        feedback_label.bind(size=lambda *args: feedback_label.setter('text_size')(feedback_label, (380, None)))
        feedback_label.bind(texture_size=lambda *args: feedback_label.setter('height')(feedback_label, feedback_label.texture_size[1]))
        scroll.add_widget(feedback_label)
        feedback_popup.content = scroll
        feedback_popup.open()

        self.current_question += 1
        if self.current_question < len(questions):
            self.layout.clear_widgets()
            self.show_question()
        else:
            self.layout.clear_widgets()
            self.question_label.text = "Fim do Quiz! Obrigado por jogar!"
            self.layout.add_widget(self.question_label)

if __name__ == '__main__':
    QuizApp().run()
