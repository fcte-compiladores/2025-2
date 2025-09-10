# Um mapa do território

> Você precisa ter um mapa, por mais rudimentar que seja. Caso contrário, você
> vagueia por todo o lugar. Em _O Senhor dos Anéis_, eu nunca fiz ninguém ir
> mais longe do que podia em um determinado dia.
>
> <cite>J. R. R. Tolkien</cite>

Não queremos vaguear por todo o lugar, então, antes de começarmos, vamos
examinar o território mapeado por implementadores anteriores da linguagem. Isso
nos ajudará a entender para onde estamos indo e as rotas alternativas que outros
tomaram.

Primeiro, deixe-me estabelecer um resumo. Grande parte deste livro trata da
_implementação_ de uma linguagem, que é distinta da _própria linguagem_ em algum
tipo de forma ideal platônica. Coisas como "pilha", "bytecode" e "descendência
recursiva" são detalhes práticos que uma implementação específica pode usar. Da
perspectiva do usuário, desde que o dispositivo resultante siga fielmente a
especificação da linguagem, tudo são detalhes de implementação.

Vamos dedicar muito tempo a esses detalhes, então, se eu tiver que escrever
"linguagem _implementação_" toda vez que mencioná-los, vou me cansar. Em vez
disso, usarei "linguagem" para me referir a uma linguagem ou a uma implementação
dela, ou a ambas, a menos que a distinção importe.

## As Partes de uma Linguagem

Engenheiros desenvolvem linguagens de programação desde a Idade das Trevas da
computação. Assim que conseguimos nos comunicar com computadores, descobrimos
que fazer isso era muito difícil e pedimos a ajuda deles. Acho fascinante que,
embora as máquinas de hoje sejam literalmente um milhão de vezes mais rápidas e
tenham ordens de magnitude a mais de armazenamento, a maneira como construímos
linguagens de programação permanece praticamente inalterada.

Embora a área explorada pelos designers de linguagens seja vasta, as trilhas que
eles abriram são <span name="dead">poucas</span>. Nem todas as linguagens seguem
exatamente o mesmo caminho — algumas pegam um atalho ou dois — mas, fora isso,
são tranquilamente semelhantes, desde o primeiro compilador COBOL da
Contra-Almirante Grace Hopper até alguma linguagem nova e interessante,
transpilada para JavaScript, cuja "documentação" consiste inteiramente em um
único README mal editado em um repositório Git em algum lugar.

<aside name="dead">

Certamente existem becos sem saída, pequenos e tristes becos sem saída de
artigos de Ciência da Computação com zero citações e otimizações agora
esquecidas que só faziam sentido quando a memória era medida em bytes
individuais.

</aside>

Eu visualizo a rede de caminhos que uma implementação pode escolher como escalar
uma montanha. Você começa de baixo com o programa como texto-fonte bruto,
literalmente apenas uma sequência de caracteres. Cada fase analisa o programa e
o transforma em uma representação de nível superior, onde a semântica — o que o
autor deseja que o computador faça — se torna mais aparente.

Finalmente, chegamos ao pico. Temos uma visão panorâmica do programa do usuário
e podemos ver o que seu código _significa_. Começamos nossa descida pelo outro
lado da montanha. Transformamos essa representação de nível superior em formas
sucessivamente de nível inferior para nos aproximarmos cada vez mais de algo que
sabemos como fazer a CPU realmente executar.

<img src="image/a-map-of-the-territory/mountain.png" alt="Os caminhos de ramificação que uma linguagem pode percorrer na montanha." class="wide" />

Vamos traçar cada uma dessas trilhas e pontos de interesse. Nossa jornada começa
à esquerda, com o texto básico do código-fonte do usuário:

<img src="image/a-map-of-the-territory/string.png" alt="var average = (min + max) / 2;" />

### Escaneamento

O primeiro passo é o **escaneamento**, também conhecido como **lexing**, ou (se
você estiver tentando impressionar alguém) **análise lexical**. Todos significam
praticamente a mesma coisa. Eu gosto de "lexing" porque soa como algo que um
supervilão maligno faria, mas usarei "scanning" porque parece ser um pouco mais
comum.

Um **scanner** (ou **lexer**) capta o fluxo linear de caracteres e os agrupa em
em uma série de algo mais parecido com <span name="word">"palavras"</span>. Em
linguagens de programação, cada uma dessas palavras é chamada de **token**.
Alguns tokens são caracteres únicos, como `(` e `,`. Outros podem ter vários
caracteres, como números (`123`), literais de string (`"hi!"`) e identificadores
(`min`).

<aside name="word">

"Lexical" vem da raiz grega "lex", que significa "palavra".

</aside>

Alguns caracteres em um arquivo de origem não significam nada. Espaços em branco
são frequentemente insignificantes e comentários, por definição, são ignorados
pela linguagem. O scanner geralmente os descarta, deixando uma sequência limpa
de tokens significativos.

<img src="image/a-map-of-the-territory/tokens.png" alt="[var] [average] [=] [(] [min] [+] [max] [)] [/] [2] [;]" />

### Análise Sintática

O próximo passo é a análise sintática. É aqui que nossa sintaxe ganha uma
gramática — a capacidade de compor expressões e instruções maiores a partir de
partes menores. Você já diagramava frases na aula de inglês? Se sim, você fez o
que um analisador sintático faz, exceto que o inglês tem milhares e milhares de
"palavras-chave" e uma cornucópia transbordante de ambiguidade. Linguagens de
programação são muito mais simples.

Um analisador sintático pega a sequência plana de tokens e constrói uma
estrutura de árvore que espelha a natureza aninhada da gramática. Essas árvores
têm alguns nomes diferentes — **árvore de análise sintática** ou **árvore de
sintaxe abstrata** — dependendo de quão próximas da estrutura sintática básica
da linguagem de origem elas estão. Na prática, os hackers da linguagem
geralmente as chamam de **árvores de sintaxe**, **ASTs** ou frequentemente
apenas **árvores**.

<img src="image/a-map-of-the-territory/ast.png" alt="Uma árvore sintática abstrata." />

A análise sintática tem uma longa e rica história na ciência da computação,
intimamente ligada à comunidade de inteligência artificial. Muitas das técnicas
usadas hoje para analisar linguagens de programação foram originalmente
concebidas para analisar linguagens _humanas_ por pesquisadores de IA que
tentavam fazer com que os computadores se comunicassem conosco.

Acontece que as linguagens humanas eram muito confusas para as gramáticas
rígidas que esses analisadores conseguiam lidar, mas eram perfeitas para as
gramáticas artificiais mais simples das linguagens de programação. Infelizmente,
nós, humanos falhos, ainda conseguimos usar essas gramáticas simples
incorretamente, então o trabalho do analisador também inclui nos avisar quando o
fazemos, relatando **erros de sintaxe**.

### Análise estática

Os dois primeiros estágios são bastante semelhantes em todas as implementações.
Agora, as características individuais de cada linguagem começam a entrar em
jogo. Neste ponto, conhecemos a estrutura sintática do código — coisas como
quais expressões estão aninhadas em quais — mas não sabemos muito mais do que
isso.

Em uma expressão como `a + b`, sabemos que estamos adicionando `a` e `b`, mas
não sabemos a que esses nomes se referem. São variáveis ​​locais? Globais? Onde
são definidas?

A primeira parte da análise que a maioria das linguagens faz é chamada de
**vinculação** ou **resolução**. Para cada **identificador**, descobrimos onde
esse nome está definido e conectamos os dois. É aqui que o **escopo** entra em
ação — a região do código-fonte onde um determinado nome pode ser usado para se
referir a uma determinada declaração.

Se a linguagem for <span name="type">estaticamente tipada</span>, é quando
fazemos a verificação de tipo. Depois de saber onde `a` e `b` são declarados,
também podemos descobrir seus tipos. Então, se esses tipos não suportarem a
adição uns aos outros, relatamos um **erro de tipo**.

<aside name="type">

A linguagem que construiremos neste livro é tipada dinamicamente, portanto, ela
fará a verificação de tipo posteriormente, em tempo de execução.

</aside>

Respire fundo. Chegamos ao topo da montanha e a uma visão abrangente do programa
do usuário. Todo esse insight semântico que nos é visível a partir da análise
precisa ser armazenado em algum lugar. Existem alguns lugares onde podemos
escondê-lo:

- Muitas vezes, ele é armazenado de volta como **atributos** na própria árvore
  sintática -- campos extras nos nós que não são inicializados durante a análise
  mas são preenchidos posteriormente.

- Outras vezes, podemos armazenar dados em uma tabela de consulta ao lado.
  Normalmente, as chaves para essa tabela são identificadores -- nomes de
  variáveis ​​e declarações. Nesse caso, chamamos de **tabela de símbolos** e os
  valores que ela associa a cada chave nos dizem a que esse identificador se
  refere.

- A ferramenta de contabilidade mais poderosa é transformar a árvore em uma
  estrutura de dados inteiramente nova que expresse mais diretamente a semântica
  do código. Essa é a próxima seção.

Tudo até este ponto é considerado o **front-end** da implementação. Você pode
imaginar que tudo depois disso seja o **back-end**, mas não. Antigamente, quando
"front-end" e "back-end" foram cunhados, os compiladores eram muito mais
simples. Pesquisadores posteriores inventaram novas fases para colocar entre as
duas metades. Em vez de descartar os termos antigos, William Wulf e companhia
agregaram essas novas fases ao nome charmoso, mas espacialmente paradoxal, de
**intermediário**.

### Representações Intermediárias

Você pode pensar no compilador como um pipeline onde a função de cada estágio é
organizar os dados que representam o código do usuário de uma forma que torne o
próximo estágio mais simples de implementar. O front-end do pipeline é
específico para a linguagem-fonte em que o programa foi escrito. O back-end se
preocupa com a arquitetura final onde o programa será executado.

No meio, o código pode ser armazenado em alguma <span name="ir">**representação
intermediária**</span> (**IR**) que não está intimamente ligada à forma de
origem ou de destino (daí o termo "intermediário"). Em vez disso, a IR atua como
uma interface entre essas duas linguagens.

<aside name="ir">

Existem alguns estilos bem estabelecidos de IRs por aí. Acesse o mecanismo de
busca de sua escolha e procure por "gráfico de fluxo de controle", "atribuição
única estática", "estilo de passagem de continuação" e "código de três
endereços".

</aside>

Isso permite que você suporte múltiplas linguagens de origem e plataformas de
destino com menos esforço. Digamos que você queira implementar compiladores
Pascal, C e Fortran, e queira ter como alvo x86, ARM e, sei lá, SPARC.
Normalmente, isso significa que você está se inscrevendo para escrever _nove_
compiladores completos: Pascal &rarr;x86, C&rarr;ARM e todas as outras
combinações.

Uma representação intermediária <span name="gcc">compartilhada</span> reduz isso
drasticamente. Você escreve _um_ front-end para cada linguagem de origem que
produz a IR. Depois, _um_ back-end para cada arquitetura de destino. Agora você
pode misturá-los e combiná-los para obter todas as combinações.

<aside name="gcc">

Se você já se perguntou como o [GCC][] suporta tantas linguagens e arquiteturas
malucas, como o Modula-3 no Motorola 68k, agora você sabe. Front-ends de
linguagens visam um dos poucos IRs, principalmente [GIMPLE][] e [RTL][].
Back-ends visam como o do 68k e, em seguida, pegam esses IRs e produzem código
nativo.

[gcc]: https://en.wikipedia.org/wiki/GNU_Compiler_Collection
[gimple]: https://gcc.gnu.org/onlinedocs/gccint/GIMPLE.html
[rtl]: https://gcc.gnu.org/onlinedocs/gccint/RTL.html

</aside>

Há outro grande motivo pelo qual podemos querer transformar o código em um
formato que torne a semântica mais aparente...

### Otimização

Depois de entendermos o que o programa do usuário significa, estamos livres para
trocá-lo por um programa diferente que tenha a _mesma semântica_, mas a
implemente de forma mais eficiente -- podemos **otimizá-lo**.

Um exemplo simples é o **dobramento constante**: se alguma expressão sempre
resulta no mesmo valor exato, podemos fazer a avaliação em tempo de compilação e
substituir o código da expressão pelo seu resultado. Se o usuário digitasse
isto:

```python
penny_area = 3,14159 * (0,75 / 2) * (0,75 / 2)
```

poderíamos fazer toda essa aritmética no compilador e alterar o código para:

```python
penny_area = 0,4417860938
```

A otimização é uma parte importante do negócio das linguagens de programação.
Muitos hackers de linguagem passam a carreira inteira aqui, extraindo cada gota
de desempenho possível de seus compiladores para obter seus benchmarks uma
fração de um por cento mais rápido. Isso pode se tornar uma espécie de obsessão.

Vamos, principalmente, <span name="rathole">pular esse buraco de rato</span>
neste livro. Muitas linguagens de sucesso têm surpreendentemente poucas
otimizações em tempo de compilação. Por exemplo, Lua e CPython geram código
relativamente não otimizado e concentram a maior parte de seus esforços de
desempenho no tempo de execução.

<aside name="rathole">

Se você não consegue resistir a tentar, algumas palavras-chave para começar são
"propagação constante", "eliminação de subexpressões comuns", "movimento de
código invariante em loop", "numeração de valor global", "redução de força",
"substituição escalar de agregados", "eliminação de código morto" e
"desenrolamento de loop".

</aside>

### Geração de código

Aplicamos todas as otimizações que conseguimos imaginar ao programa do usuário.
A última etapa é convertê-lo para um formato que a máquina possa realmente
executar. Em outras palavras, **gerar código** (ou **gerar código**), onde
"código" aqui geralmente se refere ao tipo de instruções primitivas em assembly
que uma CPU executa e não ao tipo de "código-fonte" que um humano gostaria de
ler.

Finalmente, estamos no **backend**, descendo o outro lado da montanha. Daqui em
diante, nossa representação do código se torna cada vez mais primitiva, como uma
evolução ao contrário, à medida que nos aproximamos de algo que nossa máquina
simplista pode entender.

Temos uma decisão a tomar. Geramos instruções para uma CPU real ou uma virtual?
Se gerarmos código de máquina real, obtemos um executável que o sistema
operacional pode carregar diretamente no chip. Código nativo é extremamente
rápido, mas gerá-lo dá muito trabalho. As arquiteturas atuais têm pilhas de
instruções, pipelines complexos e <span name="aad">bagagem histórica</span>
suficiente para encher o compartimento de bagagem de um 747.

Falar a linguagem do chip também significa que seu compilador está vinculado a
uma arquitetura específica. Se o seu compilador tiver como alvo código de
máquina [x86][], ele não rodará em um dispositivo [ARM][]. Lá nos anos 60,
durante a explosão cambriana das arquiteturas de computadores, essa falta de
portabilidade era um verdadeiro obstáculo.

<aside name="aad">

Por exemplo, a instrução [AAD][] ("ASCII Adjust AX Before Division") permite
realizar divisões, o que parece útil. Exceto que essa instrução usa, como
operandos, dois dígitos decimais codificados em binário compactados em um único
registrador de 16 bits. Quando foi a última vez que _você_ precisou de BCD em
uma máquina de 16 bits?

[aad]: http://www.felixcloutier.com/x86/AAD.html

</aside>

[x86]: https://en.wikipedia.org/wiki/X86
[arm]: https://en.wikipedia.org/wiki/ARM_architecture

Para contornar isso, hackers como Martin Richards e Niklaus Wirth, famosos por
BCPL e Pascal, respectivamente, fizeram seus compiladores produzirem código de
máquina _virtual_. Em vez de instruções para um chip real, eles produziram
código para uma máquina hipotética e idealizada. Wirth chamou isso de **p-code**
para _portable_, mas hoje, geralmente o chamamos de **bytecode** porque cada
instrução geralmente tem um único byte de comprimento.

Essas instruções sintéticas são projetadas para mapear um pouco mais de perto a
semântica da linguagem e não ficarem tão presas às peculiaridades de qualquer
arquitetura de computador e seu histórico acumulado. Você pode pensar nisso como
uma codificação binária densa das operações de baixo nível da linguagem.

### Máquina virtual

Se o seu compilador produz bytecode, seu trabalho não termina quando ele é
concluído. Como não há um chip que fale esse bytecode, é seu trabalho traduzir.
Novamente, você tem duas opções. Você pode escrever um pequeno minicompilador
para cada arquitetura de destino que converte o bytecode em código nativo para
aquela máquina. Você ainda precisa trabalhar para
<span name="shared">cada</span> chip que você suporta, mas esta última etapa é
bem simples e você pode reutilizar o restante do pipeline do compilador em todas
as máquinas que você suporta. Você está basicamente usando seu bytecode como uma
representação intermediária.

<aside name="shared" class="bottom">

O princípio básico aqui é que quanto mais adiante no pipeline você empurra o
trabalho específico da arquitetura, mais das fases anteriores você pode
compartilhar entre as arquiteturas.

Há uma tensão, no entanto. Muitas otimizações, como alocação de registradores e
seleção de instruções, funcionam melhor quando conhecem os pontos fortes e as
capacidades de um chip específico. Descobrir quais partes do seu compilador
podem ser compartilhadas e quais devem ser específicas para o destino é uma
arte.

</aside>

Ou você pode escrever uma <span name="vm">**máquina virtual**</span> (**VM**),
um programa que emula um chip hipotético que suporta sua arquitetura virtual em
tempo de execução. Executar bytecode em uma VM é mais lento do que traduzi-lo
para código nativo antecipadamente, porque cada instrução deve ser simulada em
tempo de execução cada vez que é executada. Em troca, você obtém simplicidade e
portabilidade. Implemente sua VM em, digamos, C, e você poderá executar sua
linguagem em qualquer plataforma que tenha um compilador C. É assim que funciona
o segundo interpretador que construímos neste livro. #TODO

<aside name="vm">

O termo "máquina virtual" também se refere a um tipo diferente de abstração. Uma
**máquina virtual de sistema** emula uma plataforma de hardware e um sistema
operacional inteiros em software. É assim que você pode jogar jogos do Windows
em sua máquina Linux e como os provedores de nuvem oferecem aos clientes a
experiência de controlar seu próprio "servidor" sem precisar alocar fisicamente
computadores separados para cada usuário.

O tipo de VM sobre o qual falaremos neste livro são **máquinas virtuais de
linguagem** ou **máquinas virtuais de processo**, se você quiser ser claro.

</aside>
### Tempo de Execução

Finalmente, transformamos o programa do usuário em um formato executável. O
último passo é executá-lo. Se o compilamos em código de máquina, simplesmente
informamos ao sistema operacional para carregar o executável e pronto. Se o
compilamos em bytecode, precisamos iniciar a VM e carregar o programa nela.

Em ambos os casos, para todas as linguagens de baixo nível, exceto as mais
básicas, geralmente precisamos de alguns serviços que nossa linguagem fornece
enquanto o programa está em execução. Por exemplo, se a linguagem gerencia a
memória automaticamente, precisamos de um coletor de lixo para recuperar bits
não utilizados. Se nossa linguagem suporta testes de "instância de" para que
você possa ver que tipo de objeto possui, então precisamos de alguma
representação para rastrear o tipo de cada objeto durante a execução.

Tudo isso acontece em tempo de execução, então é chamado, apropriadamente, de
**tempo de execução**. Em uma linguagem totalmente compilada, o código que
implementa o tempo de execução é inserido diretamente no executável resultante.
Em, digamos, [Go][], cada aplicativo compilado tem sua própria cópia do tempo de
execução de Go diretamente incorporada. Se a linguagem for executada dentro de
um interpretador ou VM, o tempo de execução reside lá. É assim que a maioria das
implementações de linguagens como Java, Python e JavaScript funciona.

[go]: https://golang.org/

## Atalhos e Rotas Alternativas

Esse é o caminho longo que abrange todas as fases possíveis que você pode
implementar. Muitas linguagens percorrem todo o caminho, mas existem alguns
atalhos e caminhos alternativos.

### Compiladores de passagem única

Alguns compiladores simples intercalam análise sintática, análise e geração de
código para que produzam código de saída diretamente no analisador, sem nunca
alocar nenhuma árvore sintática ou outras IRs. Esses
<span name="sdt">**compiladores de passagem única**</span> restringem o design
da linguagem. Você não tem estruturas de dados intermediárias para armazenar
informações globais sobre o programa e não revisa nenhuma parte do código
previamente analisada. Isso significa que, assim que você vir alguma expressão,
precisará saber o suficiente para compilá-la corretamente.

<aside name="sdt">

[**Tradução direcionada por sintaxe**][pass] é uma técnica estruturada para
construir esses compiladores tudo de uma vez. Você associa uma _ação_ a cada
parte da gramática, geralmente uma que gera código de saída. Então, sempre que o
analisador corresponde a esse pedaço de sintaxe, ele executa a ação, construindo
o código alvo, uma regra de cada vez.

[pass]: https://en.wikipedia.org/wiki/Syntax-directed_translation

</aside>

Pascal e C foram projetados em torno dessa limitação. Na época, a memória era
tão preciosa que um compilador talvez nem conseguisse armazenar um
_arquivo-fonte_ inteiro na memória, muito menos o programa inteiro. É por isso
que a gramática de Pascal exige que declarações de tipo apareçam primeiro em um
bloco. É por isso que em C você não pode chamar uma função acima do código que a
define, a menos que tenha uma declaração de avanço explícita que diga ao
compilador o que ele precisa saber para gerar código para uma chamada para a
função posterior.

### Interpretadores Tree-walk

Algumas linguagens de programação começam a executar o código logo após
analisá-lo para uma AST (talvez com um pouco de análise estática aplicada). Para
executar o programa, o interpretador percorre a árvore sintática, um ramo e uma
folha de cada vez, avaliando cada nó à medida que avança.

Este estilo de implementação é comum para projetos de estudantes e pequenas
linguagens, mas não é amplamente utilizado para linguagens de
<span name="ruby">propósito geral</span> já que tende a ser lento. Algumas
pessoas usam "interpretador" para se referir apenas a esses tipos de
implementação, mas outras definem essa palavra de forma mais geral, então usarei
o indiscutivelmente explícito **interpretador tree-walk** para me referir a
elas. Nosso primeiro interpretador funciona assim.

<aside name="ruby">

Uma exceção notável são as primeiras versões do Ruby, que eram tree walkers. Na
versão 1.9, a implementação canônica do Ruby mudou do MRI original (Matz's Ruby
Interpreter) para o YARV (Yet Another Ruby VM) de Koichi Sasada. O YARV é uma
máquina virtual de bytecode.

</aside>
### Transpiladores

<span name="gary">Escrever</span> um backend completo para uma linguagem pode
dar muito trabalho. Se você já tiver alguma IR genérica para direcionar, pode
parafusar seu frontend nela. Caso contrário, parece que você está preso. Mas e
se você tratasse alguma outra _linguagem de origem_ como se fosse uma
representação intermediária?

Você escreve um frontend para sua linguagem. Então, no backend, em vez de fazer
todo o trabalho de _reduzir_ a semântica para alguma linguagem de destino
primitiva, você produz uma sequência de código-fonte válido para alguma outra
linguagem que seja tão alto quanto a sua. Então, você usa as ferramentas de
compilação existentes para _aquela_ linguagem como sua rota de fuga da montanha
para algo que você possa executar.

Costumavam chamar isso de **compilador de origem para origem** ou
**transcompilador**. Após o surgimento de linguagens que compilam para
JavaScript para rodar no navegador, elas afetaram o apelido hipster de
**transpilador**.

<aside name="gary">

O primeiro transcompilador, o XLT86, traduziu o assembly 8080 para o
assembly 8086. Isso pode parecer simples, mas lembre-se de que o 8080 era um
chip de 8 bits e o 8086, um chip de 16 bits que podia usar cada registrador como
um par de registradores de 8 bits. O XLT86 fazia análise de fluxo de dados para
rastrear o uso de registradores no programa de origem e em seguida, mapeá-lo
eficientemente para o conjunto de registradores do 8086.

Foi escrito por Gary Kildall, um herói trágico da ciência da computação, se é
que algum dia existiu um. Uma das primeiras pessoas a reconhecer a promessa dos
microcomputadores, ele criou PL/M e CP/M, a primeira linguagem de alto nível e
sistema operacional para eles.

Ele era capitão de navio, empresário, piloto licenciado e motociclista. Um
apresentador de TV com o visual estilo Kris Kristofferson, usado por caras
barbudos e elegantes nos anos 80. Ele enfrentou Bill Gates e, como muitos,
perdeu, antes de encontrar seu fim em um bar de motoqueiros em circunstâncias
misteriosas. Ele morreu muito jovem, mas com certeza viveu antes disso.

</aside>

Enquanto o primeiro transcompilador traduzia uma linguagem assembly para outra,
hoje, a maioria dos transcompiladores trabalha com linguagens de alto nível.
Após a disseminação viral do UNIX para diversas máquinas, iniciou-se uma longa
tradição de compiladores que produziam C como linguagem de saída. Compiladores C
estavam disponíveis em todos os lugares onde o UNIX estava e produziam código
eficiente, então focar em C era uma boa maneira de fazer sua linguagem rodar em
diversas arquiteturas.

Os navegadores web são as "máquinas" de hoje, e seu "código de máquina" é
JavaScript, então, hoje em dia, parece que [quase todas as linguagens por
aí][js] têm um compilador voltado para JS, já que essa é a
<span name="js">principal</span> maneira de fazer seu código rodar em um
navegador.

[js]:
  https://github.com/jashkenas/coffeescript/wiki/list-of-languages-that-compile-to-js

<aside name="js">

JS costumava ser a _única_ maneira de executar código em um navegador. Graças ao
[WebAssembly][], os compiladores agora têm uma segunda linguagem de baixo nível
que podem ter como alvo e que roda na web.

[webassembly]: https://github.com/webassembly/

</aside>

O front-end — scanner e parser — de um transpilador se parece com outros
compiladores. Então, se a linguagem de origem for apenas uma simples camada
sintática sobre a linguagem de destino, ela pode pular a análise completamente e
ir direto para a saída da sintaxe análoga na linguagem de destino.

Se as duas linguagens forem semanticamente mais diferentes, você verá mais das
fases típicas de um compilador completo, incluindo análise e possivelmente até
otimização. Então, quando se trata de geração de código, em vez de gerar alguma
linguagem binária como código de máquina, você produz uma sequência de código
fonte (bem, destino) gramaticalmente correto na linguagem de destino.

De qualquer forma, você executa o código resultante através do pipeline de
compilação existente na linguagem de saída e está pronto para começar.

### Compilação just-in-time

Esta última é menos um atalho e mais uma perigosa corrida alpina, melhor
reservada para especialistas. A maneira mais rápida de executar código é
compilá-lo para código de máquina, mas você pode não saber qual arquitetura a
máquina do seu usuário final suporta. O que fazer?

Você pode fazer o mesmo que a Máquina Virtual Java (JVM) HotSpot, o Common
Language Runtime (CLR) da Microsoft e a maioria dos interpretadores JavaScript
fazem. Na máquina do usuário final, quando o programa é carregado — seja do
código-fonte, no caso de JavaScript, ou do bytecode independente de plataforma
para a JVM e o CLR — você o compila em código nativo para a arquitetura
suportada pelo computador. Naturalmente, isso é chamado de **compilação
just-in-time**. A maioria dos hackers apenas diz "JIT", pronunciado como se
rimasse com "fit".

Os JITs mais sofisticados inserem ganchos de criação de perfil no código gerado
para ver quais regiões são mais críticas para o desempenho e que tipo de dados
está fluindo por elas. Então, com o tempo, eles recompilarão automaticamente
esses <span
name="hot">pontos críticos</span> com otimizações mais avançadas.

<aside name="hot">

É exatamente daí, claro, que vem o nome da JVM HotSpot.

</aside>

## Compiladores e Interpretadores

Agora que enchi sua cabeça com um dicionário de jargões de linguagens de
programação, podemos finalmente abordar uma questão que atormenta os
programadores desde tempos imemoriais: Qual é a diferença entre um compilador e
um interpretador?

Acontece que isso é como perguntar a diferença entre uma fruta e um vegetal.
Parece uma escolha binária, mas na verdade "fruta" é um termo _botânico_ e
"vegetal" é _culinário_. Um não implica estritamente a negação do outro. Existem
frutas que não são vegetais (maçãs) e vegetais que não são frutas (cenouras),
mas também plantas comestíveis que são frutas _e_ vegetais, como tomates.

<span name="veg"></span>

<img src="image/a-map-of-the-territory/plants.png" alt="Um diagrama de Venn de plantas comestíveis" />

<aside name="veg">

Amendoins (que nem são nozes) e cereais como o trigo são, na verdade, frutas,
mas eu entendi errado este desenho. O que posso dizer? Sou engenheiro de
software, não botânico. Eu provavelmente deveria apagar o amendoim, mas ele é
tão fofo que eu não consigo!

Já os _pinhões_, por outro lado, são alimentos vegetais que não são frutas nem
vegetais. Pelo menos até onde eu sei.

</aside>

Então, voltando às linguagens:

- **Compilação** é uma _técnica de implementação_ que envolve traduzir uma
  linguagem fonte para alguma outra forma — geralmente de nível inferior. Quando
  você gera bytecode ou código de máquina, você está compilando. Ao transpilar
  para outra linguagem de alto nível, você também está compilando.

- Quando dizemos que uma implementação de linguagem "é um **compilador**",
  queremos dizer que ela traduz o código-fonte para alguma outra forma, mas não
  o executa. O usuário precisa pegar a saída resultante e executá-la ele mesmo.

- Por outro lado, quando dizemos que uma implementação "é um **interpretador**",
  queremos dizer que ela recebe o código-fonte e o executa imediatamente. Ela
  executa programas "a partir do código-fonte".

Como maçãs e laranjas, algumas implementações são claramente compiladores e
_não_ interpretadores. GCC e Clang pegam seu código C e o compilam para código
de máquina. Um usuário final executa esse executável diretamente e pode nunca
saber qual ferramenta foi usada para compilá-lo. Portanto, esses são
_compiladores_ para C.

Em versões mais antigas da implementação canônica de Ruby de Matz, o usuário
executava Ruby a partir do código-fonte. A implementação o analisava e o
executava diretamente, percorrendo a árvore sintática. Nenhuma outra tradução
ocorreu, seja internamente ou em qualquer formato visível ao usuário. Portanto,
este era definitivamente um _interpretador_ para Ruby.

Mas e o CPython? Quando você executa seu programa em Python usando-o, o código é
analisado e convertido para um formato de bytecode interno, que é então
executado dentro da VM. Da perspectiva do usuário, este é claramente um
interpretador — ele executa seu programa a partir do código-fonte. Mas se você
olhar sob a estrutura escamosa do CPython, verá que definitivamente há alguma
compilação em andamento.

A resposta é que ele é <span name="go">ambos</span>. O CPython _é_ um
interpretador e _tem_ um compilador. Na prática, a maioria das linguagens de
script funciona desta maneira, como você pode ver:

<aside name="go">

A [ferramenta Go][go] é ainda mais uma curiosidade hortícola. Se você executar
`go build`, ele compila seu código-fonte Go para código de máquina e para. Se
você digitar `go run`, ele faz isso e executa imediatamente o executável gerado.

Portanto, `go` _é_ um compilador (você pode usá-lo como uma ferramenta para
compilar código sem executá-lo), _é_ um interpretador (você pode invocá-lo para
executar um programa imediatamente a partir do código-fonte) e também _tem_ um
compilador (quando você o usa como interpretador, ele ainda está compilando
internamente).

[ferramenta go]: https://golang.org/cmd/go/

</aside>

<img src="image/a-map-of-the-territory/venn.png" alt="Um diagrama de Venn de compiladores e interpretadores" />

Essa região sobreposta no centro é onde nosso segundo interpretador também está,
já que ele compila internamente para bytecode. Então, embora este livro seja
nominalmente sobre intérpretes, também abordaremos algumas compilações.

## Nossa Jornada

É muita coisa para absorver de uma vez. Não se preocupe. Este não é o capítulo
em que você precisa entender todas essas peças e partes. Eu só quero que você
saiba que elas estão lá fora e, mais ou menos, como se encaixam.

Este mapa deve ser útil para você explorar o território além do caminho guiado
que seguimos neste livro. Quero deixá-lo ansioso para sair por conta própria e
vagar por toda aquela montanha.

Mas, por enquanto, é hora de começar a nossa própria jornada. Aperte os
cadarços, prenda a mochila e venha. Daqui <span name="here">em</span> em diante,
tudo o que você precisa focar é no caminho à sua frente.

<aside name="here">

De agora em diante, prometo suavizar toda a metáfora da montanha.

</aside>

<div class="challenges">

## Desafios

1. Escolha uma implementação de código aberto de uma linguagem que você goste.
   Baixe o código-fonte e explore-o. Tente encontrar o código que implementa o
   scanner e o parser. Eles são escritos à mão ou gerados usando ferramentas
   como Lex e Yacc? (Arquivos `.l` ou `.y` geralmente implicam o último.)

1. A compilação just-in-time tende a ser a maneira mais rápida de implementar
   linguagens tipadas dinamicamente, mas nem todas a utilizam. Quais são os
   motivos para _não_ usar JIT?

1. A maioria das implementações Lisp que compilam para C também contém um
   interpretador que permite executar código Lisp dinamicamente. Por quê?

</div>
