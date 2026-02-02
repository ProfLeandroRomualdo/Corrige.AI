**Corrige AI**


Software para correção de provas e trabalhos acadêmicos. O Backend possui funcionalidades de ler diversos tipos de arquivos, como.ipynb, PDF e .SQL. Possui função recursiva bastando apontar o diretorio onde se encontram os arquivos das provas. 

Será gerado um arquivo de saida para cada prova com pontos positivos, negativos, feedback e nota de acordo com o range passado no prompt.

Esta sendo utilizado uma LLM 4 Llama Maverick, mas as primeiras versões foram feitas usando llama 3 rodando local com Anaconda AI Navigator disponibilizando como API.

Para rodar local mas alterar a chamado do modelo para o endpoint disponibilizado pelo AI Navigator ou baixar o llama e alterar a chamada para o modelo local.

Para executar o front-end execute o arquivo gui_lancher.py, aponte para o diretorio e escreva o prompt.

A aplicação foi pensada para rodar como asplicativo local, caso deseje pode clonar o respositório e fazer melhorias, pull request com as melhorias são super bem vindos! ;) 

O tempo de correção varia de acordo com a quantidade de provas a serem corrigidas e a capacidade da sua LLM (local ou nuvem e tamanho do modelo).

Em casos de analise de arquitetura, kanban e outras imagens, estou usando modelo multimodal Llama 4 Maverick.  


<img width="297" height="313" alt="image" src="https://github.com/user-attachments/assets/3cab4d60-2ddc-41a2-898a-ee581e9cbc45" />
