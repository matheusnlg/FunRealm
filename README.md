O FunRealm Quiz App é um aplicativo de perguntas e respostas (quiz) desenvolvido com o framework Kivy. Ele permite que os usuários testem seus conhecimentos com diversas perguntas de múltipla escolha, abordando tópicos variados, enquanto recebem feedbacks personalizados baseados em ciclos emocionais.

O aplicativo possui funcionalidades como um quiz de múltipla escolha, que apresenta perguntas com quatro opções, onde apenas uma é a resposta correta, uma interface amigável organizada com layouts e widgets do Kivy, e um sistema de feedback gamificado. O sistema de feedback segue ciclos emocionais específicos para cada tipo de jogador, com base em categorias previamente definidas. Os ciclos emocionais são: 
Hard Fun (Frustração > Fiero > Alívio);
Easy Fun (Curiosidade > Surpresa > Maravilhamento > Reverência);
Serious Fun (Relaxamento > Foco Zen > Empolgação);
People Fun (Admiração > Amiero > Diversão > Amici).
Esses ciclos garantem que cada feedback seja apresentado em sequência, respeitando as emoções específicas de cada tipo de jogador.

Para executar o aplicativo, é necessário ter 
- Python 3.x;
- Kivy e a biblioteca `openai` instalados. 

Antes de rodar o aplicativo, é imprescindível configurar a chave da API da OpenAI no campo `openai.api_key` (linha 12) do código. Para maior segurança, recomenda-se armazenar a chave da API em uma variável de ambiente. Com as dependências instaladas, o aplicativo pode ser executado com o comando `python FunRealm.py`.

O arquivo `FunRealm.py` também permite a adição de novas perguntas ao quiz. Para isso, basta localizar a seção `# Perguntas do quiz` no código e adicionar novas perguntas no formato padrão, com a estrutura:
{"question": "Sua pergunta aqui", "options": ["Opção 1", "Opção 2", "Opção 3", "Opção 4"], "correct": "Resposta Correta"}`. 

O FunRealm Quiz App utiliza os ciclos emocionais para oferecer feedbacks detalhados e personalizados. Cada tipo de jogador segue um ciclo específico: 
o ciclo Hard Fun é composto por Frustração, Fiero e Alívio; 
o ciclo Easy Fun inclui Curiosidade, Surpresa, Maravilhamento e Reverência; 
o ciclo Serious Fun apresenta Relaxamento, Foco Zen e Empolgação; 
O ciclo People Fun abrange Admiração, Amiero, Diversão e Amici. 
Esses ciclos garantem uma experiência gamificada e educativa, mantendo a continuidade e o engajamento dos usuários durante o quiz.

O FunRealm Quiz App é fácil de configurar, permite personalizações e oferece uma experiência única ao unir aprendizado e gamificação em uma interface intuitiva e moderna.
