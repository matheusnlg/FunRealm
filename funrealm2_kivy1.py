import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
import openai

# Certifique-se de configurar a chave da API corretamente
openai.api_key = "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"

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

# Função que utiliza a API para gerar feedbacks
def get_feedback(player_type, question, user_answer, correct):
    if correct:
        prompt = f"Você é um instrutor, e irá dar o feedback para a resposta correta. Os tipos de jogadores possuem emoções diferentes, como um ciclo, e esse feedback deve seguir esse ciclo de emoções. Vou explicar pra você cada tipo de jogador, e seu ciclo de emoções: Hard Fun: Oferece um desafio, uma sensação de domínio e realização. Os jogadores precisam concentrar sua atenção e usar estratégias para superar obstáculos. Ciclo de emoções: Frustração > Fiero > Relief. Frustração: Surge quando alguém encontra um obstáculo ou dificuldade em uma tarefa, gerando uma sensação de impotência ou insatisfação. Fiero: É o sentimento de orgulho ou vitória que ocorre ao superar esse desafio ou obstáculo, trazendo satisfação pessoal. Alívio ou Relief: Após a conquista, vem uma sensação de relaxamento, como se a tensão emocional e física finalmente fosse liberada. Easy Fun: Proporciona uma sensação de exploração e dramatização. Os jogadores podem experimentar diferentes estados, fantasias ou simplesmente desfrutar dos controles. Trata-se de capturar o plástico bolha do design do jogo. Emoções: Curiosidade > Surpresa > Maravilhamento > Reverência. Curiosidade: O interesse inicial desperta a vontade de explorar ou entender algo desconhecido. Surpresa. A reação a algo inesperado ou diferente do que se imaginava, criando uma quebra de expectativa. Maravilhamento: Um sentimento de admiração e fascínio ao perceber a profundidade, beleza ou complexidade daquilo que foi descoberto. Reverência: A emoção intensa de estar diante de algo grandioso, que inspira respeito e espanto pela magnitude ou impacto dessa experiência. Serious Fun: Muda a forma como os jogadores pensam, sentem, se comportam ou fazem a diferença no mundo real. Adiciona emoção às tarefas chatas e oferece uma sensação de catarse. Emoções: Relaxation >  Zen focus > Excitement Relaxamento (Relaxation): Um estado de tranquilidade, onde o corpo e a mente estão em descanso, livres de tensão ou estresse. Foco Zen (Zen focus): Um estado de atenção profunda e calma, no qual há total concentração e clareza mental, sem distrações, muitas vezes associado a práticas meditativas. Empolgação (Excitement): A transição para uma energia mais ativa e vibrante, onde o entusiasmo e a antecipação de algo estimulante começam a emergir.]. People Fun: Oferece uma desculpa para sair com os amigos. É aditivo e ajuda a construir laços sociais e trabalho em equipe. Emoções: Admiration > Amiero > Amusement > Amici [Admiração (Admiration): Um sentimento de respeito ou reconhecimento por algo ou alguém que consideramos digno, pelas qualidades ou realizações que apreciamos. Amiero: Um termo menos comum, pode representar uma mistura de amizade e afeto, onde o respeito inicial se transforma em uma conexão mais emocional, baseada em uma apreciação afetuosa. Diversão (Amusement): Um estado de alegria e leveza, onde momentos compartilhados geram riso ou prazer, fortalecendo o vínculo. Amici: Vem do latim e significa amigos. Representa a evolução dessas emoções em uma amizade genuína, onde há confiança, carinho e afeição mútua. O caractere > representa uma seta, indicando o ciclo. Os feedbacks que você irá fornecer tem que seguir rigorosamente o ciclo de acordo com o tipo de jogador selecionado. Lembre-se: um feedback de cada vez; nada de colocar vários feedbacks ao mesmo tempo. Coloque um de cada vez seguindo a ordem do ciclo. Ao iniciar o feedback use as seguintes palavras no início: Frustração: Droga!, Fiero: Yes!, Alívio: Ufa!, Curiosidade: Hmm…, Surpresa: Uau!, Maravilhamento: Incrível!, Reverência: Uau que impressionante!, Relaxamento: Ahhh…, Foco Zen: Ok, vamos lá., Empolgação: Bora!, Admiração: Que show!, Amiero: Aí sim!, Diversão: Haha!, Amici: Tamo junto! Em seguida, o restante do feedback. Você deve guardar na memória os feedbacks que você deu, pois o feedback seguinte será em sequência, conforme o ciclo explicado anteriormente. Agora, o jogador do tipo {player_type} acertou a seguinte pergunta: {question}. Dê um feedback positivo com base em seu tipo de jogador. Ps: deve ser apenas 1 feedback por questão, e deve seguir o ciclo."
    else:
        prompt = f"Você é um instrutor, e irá dar o feedback para a resposta correta. Os tipos de jogadores possuem emoções diferentes, como um ciclo, e esse feedback deve seguir esse ciclo de emoções. Vou explicar pra você cada tipo de jogador, e seu ciclo de emoções: Hard Fun: Oferece um desafio, uma sensação de domínio e realização. Os jogadores precisam concentrar sua atenção e usar estratégias para superar obstáculos. Ciclo de emoções: Frustração > Fiero > Relief. Frustração: Surge quando alguém encontra um obstáculo ou dificuldade em uma tarefa, gerando uma sensação de impotência ou insatisfação. Fiero: É o sentimento de orgulho ou vitória que ocorre ao superar esse desafio ou obstáculo, trazendo satisfação pessoal. Alívio ou Relief: Após a conquista, vem uma sensação de relaxamento, como se a tensão emocional e física finalmente fosse liberada. Easy Fun: Proporciona uma sensação de exploração e dramatização. Os jogadores podem experimentar diferentes estados, fantasias ou simplesmente desfrutar dos controles. Trata-se de capturar o plástico bolha do design do jogo. Emoções: Curiosidade > Surpresa > Maravilhamento > Reverência. Curiosidade: O interesse inicial desperta a vontade de explorar ou entender algo desconhecido. Surpresa. A reação a algo inesperado ou diferente do que se imaginava, criando uma quebra de expectativa. Maravilhamento: Um sentimento de admiração e fascínio ao perceber a profundidade, beleza ou complexidade daquilo que foi descoberto. Reverência: A emoção intensa de estar diante de algo grandioso, que inspira respeito e espanto pela magnitude ou impacto dessa experiência. Serious Fun: Muda a forma como os jogadores pensam, sentem, se comportam ou fazem a diferença no mundo real. Adiciona emoção às tarefas chatas e oferece uma sensação de catarse. Emoções: Relaxation >  Zen focus > Excitement Relaxamento (Relaxation): Um estado de tranquilidade, onde o corpo e a mente estão em descanso, livres de tensão ou estresse. Foco Zen (Zen focus): Um estado de atenção profunda e calma, no qual há total concentração e clareza mental, sem distrações, muitas vezes associado a práticas meditativas. Empolgação (Excitement): A transição para uma energia mais ativa e vibrante, onde o entusiasmo e a antecipação de algo estimulante começam a emergir.]. People Fun: Oferece uma desculpa para sair com os amigos. É aditivo e ajuda a construir laços sociais e trabalho em equipe. Emoções: Admiration > Amiero > Amusement > Amici [Admiração (Admiration): Um sentimento de respeito ou reconhecimento por algo ou alguém que consideramos digno, pelas qualidades ou realizações que apreciamos. Amiero: Um termo menos comum, pode representar uma mistura de amizade e afeto, onde o respeito inicial se transforma em uma conexão mais emocional, baseada em uma apreciação afetuosa. Diversão (Amusement): Um estado de alegria e leveza, onde momentos compartilhados geram riso ou prazer, fortalecendo o vínculo. Amici: Vem do latim e significa amigos. Representa a evolução dessas emoções em uma amizade genuína, onde há confiança, carinho e afeição mútua. O caractere > representa uma seta, indicando o ciclo. Os feedbacks que você irá fornecer tem que seguir rigorosamente o ciclo de acordo com o tipo de jogador selecionado. Lembre-se: um feedback de cada vez; nada de colocar vários feedbacks ao mesmo tempo. Coloque um de cada vez seguindo a ordem do ciclo. Ao iniciar o feedback use as seguintes palavras no início: Frustração: Droga!, Fiero: Yes!, Alívio: Ufa!, Curiosidade: Hmm…, Surpresa: Uau!, Maravilhamento: Incrível!, Reverência: Uau que impressionante!, Relaxamento: Ahhh…, Foco Zen: Ok, vamos lá., Empolgação: Bora!, Admiração: Que show!, Amiero: Aí sim!, Diversão: Haha!, Amici: Tamo junto! Em seguida, o restante do feedback. Você deve guardar na memória os feedbacks que você deu, pois o feedback seguinte será em sequência, conforme o ciclo explicado anteriormente. Agora, o jogador do tipo {player_type} errou a seguinte pergunta: {question}. Dê um feedback positivo com base em seu tipo de jogador. Ps: deve ser apenas 1 feedback por questão, e deve seguir o ciclo."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um gerador de feedback para diferentes tipos de jogadores."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

class QuizApp(App):
    def build(self):
        # Definir o tamanho da janela para ser mais responsivo
        Window.size = (400, 600)  # Defina o tamanho inicial da janela
        
        self.current_question = 0
        self.player_type = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Título do quiz
        self.question_label = Label(text="Escolha seu tipo de jogador:", font_size=28, size_hint=(1, 0.2))
        self.layout.add_widget(self.question_label)

        # Botões para escolher o tipo de jogador
        self.add_player_type_buttons()

        return self.layout

    def add_player_type_buttons(self):
        player_types = ["Hard Fun", "Easy Fun", "Serious Fun", "People Fun"]
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
        self.question_label.font_size = 28  # Aumentando o tamanho da fonte da pergunta
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
        
        # Gerar feedback usando a função `get_feedback`
        feedback = get_feedback(self.player_type, question['question'], user_answer, correct)
        
        # Mostrar feedback em um Popup
        feedback_popup = Popup(title='Resultado',
                               size_hint=(None, None), size=(400, 600))  # Aumentar tamanho do Popup
        
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
